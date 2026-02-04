from flask import Flask, request, jsonify
import psycopg2
from configparser import ConfigParser
from flask_cors import CORS
from psycopg2 import sql
import json

app = Flask(__name__)
CORS(app)

def db_connection():
    parser = ConfigParser()
    parser.read('database.ini', encoding="utf-8")
    db = parser['postgresql']  
    
    
    conn = psycopg2.connect(
        host=db['host'],
        database=db['database'],
        user=db['user'],
        password=db['password'],
        port=db.get('port', 5432)  
    )
    return conn


@app.route("/api/fundamentalsearch/", methods=['GET'])
def fundamentalsearch():
    #Darstellung eines Parameters und festgelegten Tages für die einfache Suchabfrage
    #Ergebnis ist Kartenausschnitt mit Stationen und ihren Werten an einem bestimmten festgelegten Tag
    #Basisparameter
    parameter = request.args.get("parameter")
    messdatum = request.args.get("messdatum")
    #räumliche Auswahl
    bundesland = request.args.get("bundesland") #optional
    stationsnamen_raw = request.args.get("stationsnamen") #optional
    höheüber = request.args.get("höheüber") #optional
    höheunter = request.args.get("höheunter") #optional
    #Werteingrenzung
    untereschwelle = request.args.get("untereschwelle")#optional #Messwert soll größergleich einem angegebenen Schwellwert sein
    obereschwelle = request.args.get("obereschwelle")#optional #Messwert soll kleinergleich einem angegebenen Schwellwert sein
    #Liste mit top 10 höchsten und niedrigsten Werten

    conn = db_connection()
    cur = conn.cursor()
    conditions = []
    values = [messdatum, messdatum]

    stationsnamen = None
    if stationsnamen_raw:
        stationsnamen = stationsnamen_raw.split(",")  
    if bundesland and not stationsnamen:
        conditions.append(sql.SQL("stationen.bundesland = %s"))
        values.append(bundesland)
    if stationsnamen and not bundesland:
        conditions.append(sql.SQL("stationen.stationsname = ANY(%s)"))
        values.append(stationsnamen)
    if bundesland and stationsnamen:
        conditions.append(sql.SQL("(stationen.bundesland = %s OR stationen.stationsname = ANY(%s))"))
        values.extend([bundesland, stationsnamen])
    if höheüber:
        conditions.append(sql.SQL("stationen.stationshoehe > %s"))
        values.append(int(höheüber))
    if höheunter:
        conditions.append(sql.SQL("stationen.stationshoehe < %s"))
        values.append(int(höheunter))
    if untereschwelle:
        conditions.append(sql.SQL("messwerte.{column} > %s").format(column=sql.Identifier(parameter)))
        values.append(float(untereschwelle))
    if obereschwelle:
        conditions.append(sql.SQL("messwerte.{column} < %s").format(column=sql.Identifier(parameter)))
        values.append(float(obereschwelle))

    query = sql.SQL("""
        SELECT
            stationen.von_datum,
            stationen.bis_datum,
            stationen.stationshoehe,
            stationen.stationsname,
            stationen.bundesland,
            ST_AsGeoJSON(stationen.geom) AS geom,
            COALESCE(messwerte.mess_datum, %s) AS mess_datum,
            COALESCE(messwerte.{column}, -999) AS wert
        FROM stationen
        LEFT JOIN messwerte
        ON stationen.stations_id = messwerte.stations_id
        AND messwerte.mess_datum = %s
        WHERE {conditions}
    """).format(
        column=sql.Identifier(parameter),
        conditions=sql.SQL(" AND ").join(conditions) if conditions else sql.SQL("TRUE")
    )
    cur.execute(query, values)
    rows = cur.fetchall()

    if parameter == "tnk":
        conditions.append(sql.SQL("messwerte.{column} != -999 ORDER BY messwerte.{column} ASC LIMIT 10 ").format(column=sql.Identifier(parameter)))
    else:
        conditions.append(sql.SQL("messwerte.{column} != -999 ORDER BY messwerte.{column} DESC LIMIT 10 ").format(column=sql.Identifier(parameter)))
        
    query = sql.SQL("""
        SELECT
            stationen.von_datum,
            stationen.bis_datum,
            stationen.stationshoehe,
            stationen.stationsname,
            stationen.bundesland,
            ST_AsGeoJSON(stationen.geom) AS geom,
            COALESCE(messwerte.mess_datum, %s) AS mess_datum,
            COALESCE(messwerte.{column}, -999) AS wert
        FROM stationen
        LEFT JOIN messwerte
        ON stationen.stations_id = messwerte.stations_id
        AND messwerte.mess_datum = %s
        WHERE {conditions}
    """).format(
        column=sql.Identifier(parameter),
        conditions=sql.SQL(" AND ").join(conditions) if conditions else sql.SQL("TRUE")
    )
    cur.execute(query, values)
    rows2 = cur.fetchall()
    cur.close()
    conn.close()

    data = []
    extremwerte = []
    for row in rows:
        data.append({
            "stationshoehe": row[2],
            "stationsname": row[3],
            "bundesland": row[4],
            "geom": json.loads(row[5]),
            "mess_datum": row[6],
            "wert": row[7]
        })
    for row in rows2:
        extremwerte.append({
            "stationsname": row[3],
            "geom": json.loads(row[5]),
            "wert": row[7]
        })

    return jsonify({
        "daten": data,
        "extremwerte": extremwerte
    })


@app.route("/api/expandedsearch", methods=['GET'])
def expandedsearch():
    #Darstellung eines Parameters und festgelegten Zeitraumes für die erweiterte Suchabfrage, 
    #Ergebnis ist 
    #1) Kartenausschnitt mit einzelnen Stationen und ihren extremsten Werten/ Durchschnittlichen Messwerten in dem Zeitraum mit Angabe des Datums
    #2) Liste am Rand der Karte mit den extremsten Werten
    #Basisparameter
    parameter = request.args.get("parameter")
    von_datum = request.args.get("von_datum")
    bis_datum = request.args.get("bis_datum")
    #räumliche Auswahl
    bundesland = request.args.get("bundesland") #optional
    stationsname = request.args.get("stationsname") #optional
    höheüber = request.args.get("höheüber") #optional
    höheunter = request.args.get("höheunter") #optional
    #Aggregatfunktionen
    aggregation = request.args.get("aggregation") # erlaubt: max | min | avg | sum
     #maximale Werte in einem Zeitraum, mit angabe des Messdatums, pro Station, evtl mit liste pro Station
     #minimale Werte in einem Zeitraum, mit angabe des Messdatums, pro Station, evtl mit liste pro Station
     #durchschnittliche Werte in einem Zeitraum, pro Station, evtl mit liste am Rand mit top 10 höchsten und niedrigsten durschschnittliche Werte
     #Summe NUR bei Niederschlag sinnvoll
#evtl kleiner Film

@app.route("/api/statisticalanalysis", methods=['GET'])
def statisticalanalysis():
    #Darstellung von komplexeren Trends und Mustern der Wetterdaten mithilfe von Diagrammen
  
    analysetyp = request.args.get("analysetyp") #z.b. Hitzetage, Kältetage, zukünftiger trend; in Abhängigkeit davon weitere Auswahlmöglichkeiten
    von_datum = request.args.get("von_datum")
    bis_datum = request.args.get("bis_datum")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

