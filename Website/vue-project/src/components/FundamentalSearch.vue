<template>
  <div class="fundamental-search">
    <h2>Einfache Suche</h2>
    <div id="Basisparameter">
        <h3>Basisfilter</h3>
        <p>Wetterparameter:
            <select id="wetterparameter">
            <option>Tagesmaximaltemperatur</option>
            <option>Tagesminimaltemperatur</option>
            <option>Tagesmaximalgeschwindigkeit</option>
            <option>Tagesniederschlag</option>
        </select>
        </p>
        <p>Datum:</p>
        

    </div>
    <div id="Raumauswahl">
        <h3>Räumliche Auswahl (optional) </h3>
        <p>Bundesland:</p>
        <p>Bestimmte Stationen:</p>
        <p>Stationshöhe:</p>
    </div>
    <div id = "Werteingrenzung">
        <h3>Werteingrenzung (optional)</h3>
        <p>Messwertebereich:</p>
    </div>
    <div id ="Listenbereich"></div>

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

#wetterparameter{
    float: right;
    padding: 2px;
    margin-right: 5%;
    background-color: #142d4cd1;
    border: 2px solid #142d4c;
    border-radius: 2px;
    color: white;
}
</style>