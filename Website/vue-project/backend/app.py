from flask import Flask, request, jsonify
import psycopg2
from configparser import ConfigParser
from flask_cors import CORS
from psycopg2 import sql




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



@app.route("/api/testmesswert", methods=['GET'])
def testmesswert():
    conn = db_connection()
    cur = conn.cursor()
    parameter = 'txk'
    query = sql.SQL("""
    SELECT
        stationen.stationsname,
        stationen.geobreite,
        stationen.geolaenge,
        messwerte.{column}
    FROM messwerte
    JOIN stationen
      ON messwerte.stations_id = stationen.stations_id
    WHERE messwerte.mess_datum = %s
    AND (stationen.bundesland like %s 
    OR stationen.bundesland like %s);
    """).format(
    column=sql.Identifier(parameter)
    )
    messdatum = '2022-01-01'
    bundesland = 'Brandenburg'
    bundesland2 = 'Sachsen'
    cur.execute(query, (messdatum,bundesland,bundesland2))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    data = []
    for row in rows:
        data.append({
            "name": row[0],
            "lat": row[1],
            "lng": row[2],
            "txk": row[3]
        })
    return jsonify(data)


@app.route("/api/fundamentalsearch", methods=['GET'])
def fundamentalsearch():
    #Darstellung eines Parameters und festgelegten Tages für die einfache Suchabfrage
    #Ergebnis ist Kartenausschnitt mit Stationen und ihren Werten an einem bestimmten festgelegten Tag
    #Basisparameter
    parameter = request.args.get("parameter")
    messdatum = request.args.get("messdatum")
    #räumliche Auswahl
    bundesland = request.args.get("bundesland") #optional
    stationsname = request.args.get("stationsname") #optional
    höheüber = request.args.get("höheüber") #optional
    höheunter = request.args.get("höheunter") #optional
    #Werteingrenzung
    untereschwelle = request.args.get("untereschwelle")#optional #Messwert soll größergleich einem angegebenen Schwellwert sein
    obereschwelle = request.args.get("höheunter")#optional #Messwert soll kleinergleich einem angegebenen Schwellwert sein
    #Liste mit top 10 höchsten und niedrigsten Werten

    conn = db_connection()
    cur = conn.cursor()
    query = sql.SQL("""SELECT  
                        stationen.von_datum, 
                        stationen.bis_datum,
                        stationen.stationshoehe,
                        stationen.stationsname,
                        stationen.bundesland,
                        stationen.geom,
                        messwerte.mess_datum,
                        messwerte.{column}
                    FROM messwerte
                    JOIN stationen
                    ON messwerte.stations_id = stationen.stations_id
                    WHERE stationen.{column} like %s
                    AND messwerte.mess_datum like %s;
                    """).format(column=sql.Identifier(parameter))
    
    cur.execute(query, (parameter,messdatum))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    data = []
    for row in rows:
        data.append({
            "stationshoehe": row[2],
            "stationsname": row[3],
            "geom": row[5],
            "mess_datum": row[6],
            "parameter": row[7]
        })
    return jsonify(data)





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




@app.route("/api/statisticalanalysis", methods=['GET'])
def statisticalanalysis():
    #Darstellung von komplexeren Trends und Mustern der Wetterdaten mithilfe von Diagrammen
  
    analysetyp = request.args.get("analysetyp") #z.b. Hitzetage, Kältetage, zukünftiger trend; in Abhängigkeit davon weitere Auswahlmöglichkeiten
    von_datum = request.args.get("von_datum")
    bis_datum = request.args.get("bis_datum")







if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

