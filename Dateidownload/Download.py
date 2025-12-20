import requests as rq
from bs4 import BeautifulSoup as bs
import zipfile as zf
import pandas as pd

#Alle Links der DWD-Seite in eine Liste extrahieren
url = 'https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/kl/historical/'
page = rq.get(url)
soup = bs(page.content, 'html.parser')
linklist = []
for link in soup.find_all('a'):
    text = str(link.get('href'))
    linklist.append(text)
    
linklist = [l for l in linklist if l and l.endswith('.zip')]


i = 1 
filelist = []

#Für jeden Link auf der DWD-Seite die dazugehörige Zip-Datei herunterladen, entpacken, und anschließend die relevanten Datensätze auswählen
for i, lin in enumerate(linklist, start=1):
    
    #Downloadlink und lokalen Abspeicherlink erstellen
    distincturl = url + lin
    response = rq.get(distincturl)
    outputdir = r'C:\Users\felix\OneDrive\Felixdaten\Studium\7. Semester und Bachelorarbeit\Bachelorarbeit\Programmierung\Dateidownload\data'
    output =  outputdir + '\\' + lin
    
    #ZIP lokal abspeichern
    with open(output, 'wb') as f:
        f.write(response.content)
        
    #ZIP entpacken
    with zf.ZipFile(output, 'r') as zip_ref:
        zip_ref.extractall(outputdir)
    
    #Zugriffslink für TXT-Datei mit den relevanten Daten erstellen
    filename = 'produkt_klima_tag_' +  lin[20:37] + lin[13:19]
    filepath = outputdir + '\\' + filename + '.txt'
    
    #Datenmebge auf notwendige Zeilen und Spalten beschränken
    csvoutputdir = r'C:\Users\felix\OneDrive\Felixdaten\Studium\7. Semester und Bachelorarbeit\Bachelorarbeit\Programmierung\Dateidownload\csv\\' + filename + '.csv'
    csvfile = pd.read_csv(filepath, sep=' *; *', usecols=['STATIONS_ID','MESS_DATUM','FX','RSK','TXK', 'TNK'], index_col=False, engine = 'python', dtype={'STATIONS_ID': 'int32', 'MESS_DATUM': 'int32', 'FX': 'float32', 'RSK': 'float32', 'TXK': 'float32', 'TNK': 'float32'})
    csvfile = csvfile[csvfile['MESS_DATUM']>= 19500000]
    if csvfile.empty:
        continue
    
    #Für erste CSV einen Header erstellen, für alle darauf folgenden nicht
    #if i == 1:
        #csvfile.to_csv(csvoutputdir, sep = ',', header = ['STATIONS_ID','MESS_DATUM','FX','RSK','TXK', 'TNK'])
    #else: 
        #csvfile.to_csv(csvoutputdir, sep = ',', header = None)
    csvfile.columns = ['STATIONS_ID','MESS_DATUM','FX','RSK','TXK', 'TNK']
    csvfile.to_csv(csvoutputdir, sep=',', index=False)
    #CSV-Dateien Liste zusammenstellen
    filelist.append(csvoutputdir)
    
    
    
    
#Alle einzelnen CSV-Dateien zu einer großen CSV-Datei zusammenfügen
#dataframe = pd.concat(map(pd.read_csv,filelist))

final_file = r'C:\Users\felix\OneDrive\Felixdaten\Studium\7. Semester und Bachelorarbeit\Bachelorarbeit\Programmierung\Dateidownload\\weatherdata.csv'
cols_fill = ['STATIONS_ID','FX','RSK','TXK', 'TNK']
first_file = True

for f in filelist:
    for chunk in pd.read_csv(f, chunksize=100_000, engine = 'python'):
        #Leere Werte auffüllen
        chunk[cols_fill] = chunk[cols_fill].fillna(0)
        
        #Messdatum bereinigen
        chunk['MESS_DATUM'] = chunk['MESS_DATUM'].astype(str).str.replace('.0', '', regex=False)
        chunk['MESS_DATUM'] = pd.to_datetime(chunk['MESS_DATUM'], format='%Y%m%d')
        
        #Direkt in finale CSV schreiben
        chunk.to_csv(final_file, sep=';', mode='a', header=first_file, index=False)
        first_file = False

#Leere Werte auffüllen und das Messdatum bereinigen
#dataframe = pd.read_csv(final_file, sep=';')
#cols_fill = ['stations_id', 'fx', 'rsk', 'txk', 'tnk']
#dataframe[cols_fill] = dataframe[cols_fill].fillna(0)
#dataframe['mess_datum'] = dataframe['mess_datum'].astype(str)
#dataframe['mess_datum'] = dataframe['mess_datum'].str.replace('.0', '')
#dataframe.to_csv(final_file, sep = ',',
 #                columns = ['stations_id','mess_datum','fx','rsk','txk', 'tnk'], index = False)

#Datentyp für alle Spalten festlegen
#dataframe2 = pd.read_csv(final_file, sep = ',', index_col = False,
#                         engine = 'python', dtype={'stations_id': 'int32', 'mess_datum': 'str', 'fx': 'float32', 'rsk': 'float32', 'txk': 'float32', 'tnk': 'float32'})
#dataframe2['mess_datum'] = pd.to_datetime(
#    dataframe2['mess_datum'],
#    format='%Y%m%d'
#)
#dataframe2.to_csv(final_file, sep = ';', index = False)
    
     

    