<template>
  <div class="fundamental-search">
    <h2>Einfache Suche</h2>
    <div id="Basisparameter" class="bereich">
        <h3>Basisfilter</h3>
        <p>Wetterparameter:
            <select id="wetterparametereingabe" class ="eingabe">
            <option>Tagesmaximaltemperatur</option>
            <option>Tagesminimaltemperatur</option>
            <option>Tagesmaximalgeschwindigkeit</option>
            <option>Tagesniederschlag</option>
        </select>
        </p>
        <p>Datum:
            <input id="datumseingabe" class ="eingabe" type="date" value="2024-12-31" min="1950-01-01" max="2024-12-31"> </input>

        </p>
        

    </div>
    <div id="Raumauswahl" class="bereich">
        <h3>Räumliche Auswahl (optional) </h3>
        <p>Bundesland:
            <select id="Bundeslandeingabe" class ="eingabe">
                <option></option>
                <option>Baden-Württemberg</option>
                <option>Bayern</option>
                <option>Berlin</option>
                <option>Brandenburg</option>
                <option>Bremen</option>
                <option>Hamburg</option>
                <option>Hessen</option>
                <option>Mecklenburg-Vorpommern</option>
                <option>Niedersachsen</option>
                <option>Nordrhein-Westfalen</option>
                <option>Rheinland-Pfalz</option>
                <option>Saarland</option>
                <option>Sachsen</option>
                <option>Sachsen-Anhalt</option>
                <option>Schleswig-Holstein</option>
                <option>Thüringen</option>
            </select>
        </p>
        <p>Stationen:
            <input class ="eingabe" type="search" placeholder="Nach Station suchen..."> </input>
        </p>
        <p>Stationshöhe:
            <p class="höhentext"> über &nbsp; <input class ="eingabe"> </input></p> 
            <p class="höhentext">unter &nbsp; <input class ="eingabe"></p>
        </p>
    </div>
    <div id = "Werteingrenzung" class="bereich">
        <h3>Werteingrenzung (optional)</h3>
        <p>Messwertebereich:</p>
    </div>
    <div id ="Listenbereich" class="bereich"></div>

  </div>
</template>

<style scoped>
.fundamental-search {
  height: 100%;
  width: 100%;
  margin: 0px;
  padding: 0.5em;
  font-family: 'Ubuntu', system-ui, sans-serif;
}

h2{
   text-align: center; 
   margin: 5px;
   padding: 0px;
}

.eingabe{
    float: right;
    padding: 2px;
    margin-right: 5%;
    background-color: #142d4cd1;
    border: 2px solid #142d4c;
    border-radius: 2px;
    color: white;
}

.höhentext{
    text-align: right;
    
}

.bereich{
    overflow: hidden;
}

</style>