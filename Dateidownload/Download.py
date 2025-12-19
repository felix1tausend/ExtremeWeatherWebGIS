import requests as rq
from bs4 import BeautifulSoup as bs
import zipfile as zf
import pandas as pd
import csv


url = 'https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/kl/historical/'
page = rq.get(url)
soup = bs(page.content, 'html.parser')


linklist = []
for link in soup.find_all('a'):
    text = str(link.get('href'))
    linklist.append(text)
    

#print (linklist)

linklisttest = ['tageswerte_KL_00001_19370101_19860630_hist.zip','tageswerte_KL_00003_18910101_20110331_hist.zip']
i = 0

    
filelist = []

for lin in linklisttest:
    lin = linklisttest[i]
    distincturl = url + lin
    i= i +1
    response = rq.get(distincturl)
    outputdir = r'C:\Users\felix\OneDrive\Felixdaten\Studium\7. Semester und Bachelorarbeit\Bachelorarbeit\Programmierung\Dateidownload\data'
    output =  outputdir + '\\' + lin
    with open(output, 'wb') as f:
        f.write(response.content)
    with zf.ZipFile(output, 'r') as zip_ref:
        zip_ref.extractall(outputdir)
        
    filename = 'produkt_klima_tag_' +  lin[20:37] + lin[13:19]
    filepath = outputdir + '\\' + filename + '.txt'
    csvoutputdir = r'C:\Users\felix\OneDrive\Felixdaten\Studium\7. Semester und Bachelorarbeit\Bachelorarbeit\Programmierung\Dateidownload\csv\\' + filename + '.csv'
    
    
    csvfile = pd.read_csv(filepath, sep=' *; *', usecols=['STATIONS_ID','MESS_DATUM','FX','RSK','TXK', 'TNK'], index_col=0, engine = 'python')
    csvfile = csvfile[csvfile['MESS_DATUM']>= 19500000] #Alle Datensätze Filtern, deren Aufnahme ab dem 01.01.1950 geschehen ist
    csvfile.to_csv(csvoutputdir, sep = ',', header = None)
    
    filelist.append(csvoutputdir)
    
print (filelist)   
dataframe = pd.concat(map(pd.read_csv,filelist)) 
dataframe.to_csv(r'C:\Users\felix\OneDrive\Felixdaten\Studium\7. Semester und Bachelorarbeit\Bachelorarbeit\Programmierung\Dateidownload\\weatherdata.csv', sep = ';', header = None)
    
    
     

    