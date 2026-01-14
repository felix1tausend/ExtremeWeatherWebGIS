from flask import Flask, jsonify
import psycopg2
from configparser import ConfigParser
from flask_cors import CORS
from psycopg2 import sql



app = Flask(__name__)
CORS(app) 

def db_connection():
    parser = ConfigParser()
    parser.read('database.ini')
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
        stationlist.stationsname,
        stationlist.geobreite,
        stationlist.geolaenge,
        stationdata.{column}
    FROM stationdata
    JOIN stationlist
      ON stationdata.stations_id = stationlist.stations_id
    WHERE stationdata.mess_datum = %s;
    """).format(
    column=sql.Identifier(parameter)
    )
    messdatum = '2022-01-01'
    cur.execute(query, (messdatum,))
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


@app.route("/api/testmesswert", methods=['GET'])
def auslesen():
    conn = db_connection()
    cur = conn.cursor()
    parameter = 'txk'
    query = sql.SQL("""
    SELECT
        stationlist.stationsname,
        stationlist.geobreite,
        stationlist.geolaenge,
        stationdata.{column}
    FROM stationdata
    JOIN stationlist
      ON stationdata.stations_id = stationlist.stations_id
    WHERE stationdata.mess_datum = %s;
    """).format(
    column=sql.Identifier(parameter)
    )
    messdatum = '2022-01-01'
    cur.execute(query, (messdatum,))
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



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

