<template>
  <div id="navbar1">
   <ul>
      <li class="spacer"></li>
      <li class="title">Extremwetter WebGIS</li>
      <li class="spacer"></li>
      <li><button v-if = "showInfo === false" class="info-btn" @click="showInfo = true">i</button>
          <button v-else class="info-btn" @click="showInfo = false">i</button></li>
    </ul>



    <div v-if="showInfo" class="modal" @click.self="showInfo = false">
        <div class="modal-content">
            <h3>Willkommen im Extremwetter WebGIS!</h3>
            <p> Dieses GIS visualisiert vergangene Extremwetterereignisse ab 1950 in Deutschland. <br>
                Dabei haben Sie die Möglichkeit, durch weitgehende Analysefunktionen an über 1300 Wetterstationen des Deutschen Wetterdienstes mehr über die Ausmaße von Extremwetter im gesamten Bundesgebiet zu erfahren. <br>
                <br>
                Im Zuge Dessen können Sie nach den 4 ausschlaggebenden Parametern <strong>Tagesmaximaltemperatur</strong>, <strong>Tagesminaimaltemperatur</strong>, <strong>Tageshöchstwindgeschwindigkeit</strong> und analysieren. <br>
                Die 3 im WebGIS vorkommenden Analysebereiche <i>Einfache Suche</i>, <i>Erweiterte Suche</i> und <i>Statistische Analyse</i> bieten hierbei eine logische Strukturierung, um den Einsatz des GIS effizient zu organisieren. <br>
                <br>
                Die <i>Einfache Suche</i> eignet sich für die Filterung nach bestimmten Wertebereichen der Messwerte an einem festgelegten Tag. <br>
                Der Bereich <i>Erweiterte Suche</i> ist hingegen besonders geeignet, um innerhalb eines individuell festgelegten Zeitabschnittes Durchschnitts- Maximal- oder Minimalmesswerte zu identifizieren. <br>
                Die <i>Statistische Analyse</i> ist schlussendlich für längerfristige Auswertung von Trends aus den Messdaten nützlich. <br>
                Dabei soll die historische sowie mögliche zukünftige Entwicklung der 4 Parameter durch vorgefertigte Analysen näher beleuchtet werden.

                </p>
            <button class="close-btn" @click="showInfo = false">Schließen</button>
        </div>
    </div>
  </div>

</template>
<script setup>

import { ref } from 'vue'
const showInfo = ref(false)

</script>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Ubuntu:wght@400;500;700&display=swap');
#navbar1 {
  width: 100%;
  height: 4vh;
  font-family: 'Ubuntu', system-ui, sans-serif;
  font-size: 2.9vh;
  color: #d9dbdd;
  background-color: #142d4c;
  box-shadow: 0 1px 10px rgb(51, 51, 51);
  z-index: 1000;
  position: fixed;
}

ul {
  display: flex;
  align-items: center;
  height: 100%;
  list-style: none;
  margin: 0;
  padding: 0 0.5vw;
}

.spacer {
  flex: 1;
}

.info-btn {
  display: flex;
  align-items: center; 
  justify-content: center;
  width: 2vh;
  height: 2vh;
  border-radius: 10%;
  font-family: 'Times New Roman', Times, serif;
  border: 2px solid #4b6380;
  background: transparent;
  color: #d9dbdd;
  font-weight: 600;
  font-size: 1.2vh;
  line-height: 1;
  cursor: pointer;
}

.info-btn:hover {
  background-color: rgba(56, 81, 112, 0.15);
}



.modal {
  position: fixed;
  width: 100%;
  height: 100%;
  background-color: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10000;
}


.modal-content {
  background-color: #142d4cdc;
  color: #fff;
  border-radius: 8px;
  padding-left: 1em;
  padding-right: 1em;
  border: 3px solid #4b6380;
  width: 55vw;
  height: 55vh;
  font-family: 'Ubuntu', sans-serif;
  text-align: justify;
}


.close-btn {
  margin-top: 1em;
  padding: 0.5em 1em;
  border: 2px solid #4b6380;
  border-radius: 1px;
  float: right;
  background-color: #385170;
  color: #fff;
  cursor: pointer;
  font-family: 'Ubuntu', system-ui, sans-serif;
  font-size: large;
}

.close-btn:hover {
  background-color: #4b6990;
}

p {
  font-size: x-large;
}
</style>
