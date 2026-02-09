**1 Anzahl Hitzetage pro Jahr**



**with hitzetage\_pro\_station as (select stations\_id, extract(year from mess\_datum) as jahr, count(\*) as hitzetage**

**from messwerte where txk >= 30**

**group by stations\_id, extract(year from mess\_datum))**



**select jahr, round(avg(hitzetage),2) as durchschnittliche\_hitzetage**

**from hitzetage\_pro\_station**

**group by jahr**

**order by jahr**



**1.1 Höchste mittlere Temperatur**

**with tmax as (**

**select stations\_id, extract(year from mess\_datum) as jahr, max(txk) as extremwert**

**from messwerte where txk > -100**

**group by stations\_id, extract(year from mess\_datum))**

**select jahr, round(avg(extremwert)::numeric, 2) as durchschnittlicher\_extremwert**

**from tmax**

**group by jahr**

**order by jahr;**





**2 Anzahl Kältetage pro Jahr**



**with kaeltetage\_pro\_station as (**

**select stations\_id, extract(year from mess\_datum) as jahr, count(\*) as kaeltetage**

**from messwerte**

**where tnk <= -10 and tnk > -100**

**group by stations\_id, extract(year from mess\_datum)**

**)**

**select jahr, round(avg(kaeltetage),2) as durchschnittliche\_kaeltetage**

**from kaeltetage\_pro\_station**

**group by jahr**

**order by jahr;**

**2.1 Niedrigste mittlere Temperatur**

**with tmin as (**

**select stations\_id, extract(year from mess\_datum) as jahr, min(tnk) as extremwert**

**from messwerte where tnk > -100**

**group by stations\_id, extract(year from mess\_datum))**

**select jahr, round(avg(extremwert)::numeric, 2) as durchschnittlicher\_extremwert**

**from tmin**

**group by jahr**

**order by jahr;**





**3 Anzahl Sturmtage pro Jahr**

**with sturmtage\_pro\_station as (**

**select stations\_id, extract(year from mess\_datum) as jahr, count(\*) as sturmtage**

**from messwerte**

**where fx >= 17.2**

**group by stations\_id, extract(year from mess\_datum)**

**)**

**select jahr, round(avg(sturmtage),2) as durchschnittliche\_sturmtage**

**from sturmtage\_pro\_station**

**group by jahr**

**order by jahr;**

**3.1 Höchste mittlere Windgeschwindigkeit**

**with fx as (**

**select stations\_id, extract(year from mess\_datum) as jahr, max(fx) as extremwert**

**from messwerte where fx > -100**

**group by stations\_id, extract(year from mess\_datum))**

**select jahr, round(avg(extremwert)::numeric, 2) as durchschnittlicher\_extremwert**

**from fx**

**group by jahr**

**order by jahr;**



**4 Anzahl Starkregentage pro Jahr**

**with starkregentage\_pro\_station as (**

**select stations\_id, extract(year from mess\_datum) as jahr, count(\*) as starkregentage**

**from messwerte**

**where rsk >= 20**

**group by stations\_id, extract(year from mess\_datum)**

**)**

**select jahr, round(avg(starkregentage),2) as durchschnittliche\_starkregentage**

**from starkregentage\_pro\_station**

**group by jahr**

**order by jahr;**

**4.1 Höchster mittlerer Niederschlag**

**with rsk as (**

**select stations\_id, extract(year from mess\_datum) as jahr, max(rsk) as extremwert**

**from messwerte where rsk > -100**

**group by stations\_id, extract(year from mess\_datum))**

**select jahr, round(avg(extremwert)::numeric, 2) as durchschnittlicher\_extremwert**

**from rsk**

**group by jahr**

**order by jahr;**

**4.2 Jährliche mittlere Niederschlagsmenge**

**with rsk as (**

**select stations\_id, extract(year from mess\_datum) as jahr, sum(rsk) as summe, count(\*) as messungen\_im\_jahr**

**from messwerte where rsk > -100**

**group by stations\_id, extract(year from mess\_datum))**

**select jahr, round(avg(summe)::numeric, 2) as durchschnittliche\_summe**

**from rsk where messungen\_im\_jahr > 364**

**group by jahr**

**order by jahr;**



**5 Anzahl Trockentage pro Jahr**



**with trockentage\_pro\_station as (**

**select stations\_id, extract(year from mess\_datum) as jahr, count(\*) as trockentage**

**from messwerte**

**where rsk <= 0.1 and rsk > -100**

**group by stations\_id, extract(year from mess\_datum)**

**)**

**select jahr, round(avg(trockentage),2) as durchschnittliche\_trockentage**

**from trockentage\_pro\_station**

**group by jahr**

**order by jahr;**













