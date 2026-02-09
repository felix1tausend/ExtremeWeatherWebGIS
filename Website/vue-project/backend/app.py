from flask import Flask, request, jsonify
import psycopg2
from configparser import ConfigParser
from flask_cors import CORS
from psycopg2 import sql
import json
import matplotlib.pyplot as plt
import numpy as np

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

def gemeinsameAbfrage(parameter):
    conditions = []
    values = []
    #räumliche Auswahl
    bundesland = request.args.get("bundesland") #optional
    stationsnamen_raw = request.args.get("stationsnamen") #optional
    höheüber = request.args.get("höheüber") #optional
    höheunter = request.args.get("höheunter") #optional
    
    stationsnamen =  None

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
    return conditions, values


@app.route("/api/fundamentalsearch/", methods=['GET'])
def fundamentalsearch():
    #Darstellung eines Parameters und festgelegten Tages für die einfache Suchabfrage
    #Ergebnis ist Kartenausschnitt mit Stationen und ihren Werten an einem bestimmten festgelegten Tag
    #Basisparameter
    parameter = request.args.get("parameter")
    messdatum = request.args.get("messdatum")
    #Werteingrenzung
    untereschwelle = request.args.get("untereschwelle")#optional #Messwert soll größergleich einem angegebenen Schwellwert sein
    obereschwelle = request.args.get("obereschwelle")#optional #Messwert soll kleinergleich einem angegebenen Schwellwert sein
    
    conditions, values = gemeinsameAbfrage(parameter)
    if untereschwelle:
        conditions.append(sql.SQL("messwerte.{col} >= %s").format(col=sql.Identifier(parameter)))
        values.append(float(untereschwelle))
    if obereschwelle:
        conditions.append(sql.SQL("messwerte.{col} <= %s").format(col=sql.Identifier(parameter)))
        values.append(float(obereschwelle))
    values = [messdatum, messdatum] + values
    conn = db_connection()
    cur = conn.cursor()

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
        conditions=sql.SQL(" AND ").join(conditions) if conditions else sql.SQL("TRUE"))
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
        conditions=sql.SQL(" AND ").join(conditions) if conditions else sql.SQL("TRUE"))
    cur.execute(query, values)
    rows2 = cur.fetchall()
    cur.close()
    conn.close()

    data = []
    extremwerte = []
    for row in rows:
        data.append({
            "von_datum": row[0],
            "bis_datum": row[1],
            "stationshoehe": row[2],
            "stationsname": row[3],
            "bundesland": row[4],
            "geom": json.loads(row[5]),
            "mess_datum": row[6],
            "wert": row[7]
        })
    for row in rows2:
        extremwerte.append({
            "von_datum": row[0],
            "bis_datum": row[1],
            "stationsname": row[3],
            "geom": json.loads(row[5]),
            "wert": row[7]
        })
    return jsonify({
        "daten": data,
        "extremwerte": extremwerte
    })




@app.route("/api/expandedsearch/", methods=['GET'])
def expandedsearch():
    rows = []
    rows2 = []
    #Darstellung eines Parameters und festgelegten Zeitraumes für die erweiterte Suchabfrage, 
    #Ergebnis ist 
    #1) Kartenausschnitt mit einzelnen Stationen und ihren extremsten Werten/ Durchschnittlichen Messwerten in dem Zeitraum mit Angabe des Datums
    #2) Liste am Rand der Karte mit den extremsten Werten
    #Basisparameter
    parameter = request.args.get("parameter")
    von_datum = request.args.get("von_datum")
    bis_datum = request.args.get("bis_datum")
    #Aggregatfunktionen
    aggregation = request.args.get("aggregation") # erlaubt: max | min | sum
     #maximale Werte in einem Zeitraum, mit angabe des Messdatums, pro Station
     #minimale Werte in einem Zeitraum, mit angabe des Messdatums, pro Station
     #Summe NUR bei Niederschlag sinnvoll
    untereschwelle = request.args.get("untereschwelle")#optional #Messwert soll größergleich einem angegebenen Schwellwert sein
    obereschwelle = request.args.get("obereschwelle")#optional #Messwert soll kleinergleich einem angegebenen Schwellwert sein
    listensortierung = request.args.get("listensortierung") #falls sum für Niederschlag gesetzt, kann zwischen den trockensten und nassesten Stationenen in der Extremwertliste unterschieden werden
    #Werteingrenzung
    untereschwelle = request.args.get("untereschwelle")#optional #Messwert soll größergleich einem angegebenen Schwellwert sein
    obereschwelle = request.args.get("obereschwelle")#optional #Messwert soll kleinergleich einem angegebenen Schwellwert sein
    
    conditions, values = gemeinsameAbfrage(parameter)
    conn = db_connection()
    cur = conn.cursor()

    if aggregation != "sum":
        values_inner = [von_datum, bis_datum] + values
        if parameter == "tnk":
            sortierung = sql.SQL("ASC")
        else:
            sortierung = sql.SQL("DESC")

        # Abfrage für Minimal- oder Maximalwerte
        inner_query = sql.SQL("""
            SELECT DISTINCT ON (stationen.stations_id)
                stationen.von_datum,
                stationen.bis_datum,
                stationen.stationshoehe,
                stationen.stationsname,
                stationen.bundesland,
                ST_AsGeoJSON(stationen.geom) AS geom,
                messwerte.mess_datum AS mess_datum,
                messwerte.{column} AS wert
            FROM stationen
            LEFT JOIN messwerte
                ON stationen.stations_id = messwerte.stations_id
                AND messwerte.mess_datum BETWEEN %s AND %s
            WHERE {conditions}
            AND messwerte.{column} IS NOT NULL
            ORDER BY stationen.stations_id, messwerte.{column} {sortierung}
        """).format(
            column=sql.Identifier(parameter),
            conditions=sql.SQL(" AND ").join(conditions) if conditions else sql.SQL("TRUE"),
            sortierung=sortierung
        )
        outer_conditions = [sql.SQL("wert != -999")]
        outer_values = []

        if untereschwelle:
            outer_conditions.append(sql.SQL("wert >= %s"))
            outer_values.append(float(untereschwelle))

        if obereschwelle:
            outer_conditions.append(sql.SQL("wert <= %s"))
            outer_values.append(float(obereschwelle))
        query_all = sql.SQL("""
            SELECT *
            FROM ({inner}) AS sub
            WHERE {outer_conditions}
        """).format(
            inner=inner_query,
            outer_conditions=sql.SQL(" AND ").join(outer_conditions)
        )
        cur.execute(query_all, values_inner + outer_values)
        rows = cur.fetchall()

        query_top10 = sql.SQL("""
            SELECT *
            FROM ({inner}) AS sub
            WHERE {outer_conditions}
            ORDER BY wert {sortierung}
            LIMIT 10
        """).format(
            inner=inner_query,
            outer_conditions=sql.SQL(" AND ").join(outer_conditions),
            sortierung=sortierung
        )
        cur.execute(query_top10, values_inner + outer_values)
        rows2 = cur.fetchall()

    else:
        # Abfrage für Summe des Niederschlages
        values = [von_datum, bis_datum] + values + [bis_datum, von_datum]
        if untereschwelle and obereschwelle:
            werteingrenzung = sql.SQL("BETWEEN %s AND %s")
            values = values + [untereschwelle, obereschwelle]
        elif untereschwelle:
            werteingrenzung = sql.SQL(">= %s")
            values = values + [untereschwelle]
        elif obereschwelle:
            werteingrenzung = sql.SQL("<= %s")
            values = values + [obereschwelle]
        else:
            werteingrenzung = sql.SQL(">0")
        query = sql.SQL("""
            SELECT
                stationen.von_datum,
                stationen.bis_datum,
                stationen.stationshoehe,
                stationen.stationsname,
                stationen.bundesland,
                ST_AsGeoJSON(stationen.geom) AS geom,
                MAX(messwerte.mess_datum) AS mess_datum,
                ROUND (SUM(messwerte.{column})::numeric,2) AS wert
            FROM stationen
            JOIN messwerte
            ON stationen.stations_id = messwerte.stations_id
            AND messwerte.mess_datum BETWEEN %s AND %s
            WHERE {conditions}
            AND messwerte.{column} != -999
            GROUP BY stationen.stations_id,
                stationen.von_datum,
                stationen.bis_datum,
                stationen.stationshoehe,
                stationen.stationsname,
                stationen.bundesland,
                stationen.geom
            HAVING COUNT(messwerte.mess_datum) = (DATE %s - DATE %s + 1) AND SUM(messwerte.{column}) {werteingrenzung};
        """).format(
            column=sql.Identifier(parameter),
            conditions=sql.SQL(" AND ").join(conditions) if conditions else sql.SQL("TRUE"),
            werteingrenzung = werteingrenzung)
        cur.execute(query, values)
        rows = cur.fetchall()

        if listensortierung == "desc":
            listsort = sql.SQL("DESC")
        if listensortierung == "asc":
             listsort = sql.SQL("ASC")
        query = sql.SQL("""
            SELECT
                stationen.von_datum,
                stationen.bis_datum,
                stationen.stationshoehe,
                stationen.stationsname,
                stationen.bundesland,
                ST_AsGeoJSON(stationen.geom) AS geom,
                MAX(messwerte.mess_datum) AS mess_datum,
                ROUND (SUM(messwerte.{column})::numeric,2) AS wert
            FROM stationen
            JOIN messwerte
            ON stationen.stations_id = messwerte.stations_id
            AND messwerte.mess_datum BETWEEN %s AND %s
            WHERE {conditions}
            AND messwerte.{column} != -999
            GROUP BY stationen.stations_id,
                stationen.von_datum,
                stationen.bis_datum,
                stationen.stationshoehe,
                stationen.stationsname,
                stationen.bundesland,
                stationen.geom
            HAVING COUNT(messwerte.mess_datum) = (DATE %s - DATE %s + 1) AND SUM(messwerte.{column}) {werteingrenzung}
            ORDER BY wert {listensortierung} LIMIT 10;
        """).format(
            column=sql.Identifier(parameter),
            conditions=sql.SQL(" AND ").join(conditions) if conditions else sql.SQL("TRUE"),
            werteingrenzung = werteingrenzung,
            listensortierung = listsort)
        cur.execute(query, values)
        rows2 = cur.fetchall()
    cur.close()
    conn.close()

    data = []
    extremwerte = []
    for row in rows:
        data.append({
            "von_datum": row[0],
            "bis_datum": row[1],
            "stationshoehe": row[2],
            "stationsname": row[3],
            "bundesland": row[4],
            "geom": json.loads(row[5]),
            "mess_datum": row[6],
            "wert": row[7]
        })
    for row in rows2:
        extremwerte.append({
            "von_datum": row[0],
            "bis_datum": row[1],
            "stationsname": row[3],
            "geom": json.loads(row[5]),
            "mess_datum": row[6],
            "wert": row[7]
        })
    return jsonify({
        "daten": data,
        "extremwerte": extremwerte
    })


@app.route("/api/statisticalanalysis", methods=['GET'])
def statisticalanalysis():
    #Darstellung von komplexeren Trends und Mustern der Wetterdaten mithilfe von Diagrammen
    analysetyp = request.args.get("analysetyp") #z.b. Hitzetage, Kältetage, zukünftiger Trend; in Abhängigkeit davon weitere Auswahlmöglichkeiten

    


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

