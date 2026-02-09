<template>
  <div class="fundamental-search">
    <h2>Erweiterte Suche</h2>
    <div class="bereich">
        <h3>Basisfilter</h3>
        <p>Auswertungsmethode:
            <select v-model="store.methode" class="eingabe">
            <option value="txk_max">Höchste Temperatur</option>
            <option value="tnk_min">Niedrigste Temperatur</option>
            <option value="fx_max">Höchste Windgeschwindigkeit</option>
            <option value="rsk_max">Höchster Tagesniederschlag</option>
            <option value="rsk_sum">Niederschlagssumme</option>
            </select>
        </p>
        <div>Zeitraum:
            <div class="bereich2">
            <p ><input class="eingabe2" type="date" min="1950-01-01" max="2024-12-31" v-model="store.von_datum"> bis
            <input class="eingabe2" type="date" min="1950-01-01" max="2024-12-31" v-model="store.bis_datum"></p>
            </div>
        </div>
        <div v-if="store.methode === 'rsk_sum'" class="extrem-toggle">
            <p>In Extremwertliste anzeigen:</p>
            <label class="label1">
                <input type="radio" value="desc" name="listensortierung" v-model="store.listensortierung">
                Nasseste Stationen
            </label>
            <br>
            <label class="label1">
                <input type="radio" value="asc" name="listensortierung" v-model="store.listensortierung">
                Trockenste Stationen
            </label>
        </div>
    </div>
    <div class="bereich">
        <h3>Räumliche Auswahl (optional) </h3>
        <p>Bundesland:
            <select class ="eingabe" v-model="store.bundesland" >
                <option>-</option>
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
            <input class ="eingabe" type="search" placeholder="Nach Station suchen..." v-model="store.stationsname">
            <ul class = "ul1" v-if="store.filteredStations.length">
                <li v-for="station in store.filteredStations" :key="station" >
                <label>
                    <input type="checkbox" 
                        :value="station"
                        :checked="store.ausgewählteStationen.includes(station)"
                        @change="store.toggleStation(station)">
                    {{ station }}
                </label>
                </li>
            </ul>
        </p>
        <div><p>Stationshöhe:</p>
            <div class="werteingrenzung">
                <p class="eingrenzungstext"> über &nbsp; <input class ="eingabe2" v-model="store.höheüber"> m</p>
                <p class="eingrenzungstext">unter <input class ="eingabe2" v-model="store.höheunter"> m</p>
            </div>
        </div>
    </div>
    <div id = "Werteingrenzung" class="bereich">
        <h3>Werteingrenzung (optional)</h3>
        <div><p>Messwertebereich:</p>
            <div class="werteingrenzung">
                <p class="eingrenzungstext"> über &nbsp; <input class="eingabe2" v-model="store.untereschwelle"> {{ store.einheit }}</p>
                <p class="eingrenzungstext">unter <input class="eingabe2" v-model="store.obereschwelle"> {{ store.einheit }}</p>
            </div>
        </div>
    </div>
    <div id ="unterenavbar">
        <ul>
            <li> 
                <button v-if = "store.showExtremes === false" class="ergebnisbutton" @click="store.showExtremes = true"> 
                    <svg viewBox="0 0 24 24" class="icon" id="icon1">
                        <path d="M13 2L3 14h7l-1 8 10-12h-7l1-8z"/>
                    </svg>
                </button> 
                <button v-else  class="ergebnisbutton" @click="store.showExtremes = false">
                    <svg viewBox="0 0 24 24" class="icon" id="icon1">
                        <path d="M13 2L3 14h7l-1 8 10-12h-7l1-8z"/>
                    </svg>
                </button>
            </li>
            <li> 
                <button class="ergebnisbutton" @click="store.fetchResults">
                    <svg viewBox="0 0 24 24" class="icon">
                        <circle cx="11" cy="11" r="7"/>
                        <line x1="16.65" y1="16.65" x2="22" y2="22"/>
                    </svg>
                </button>
            </li>
        </ul>   
    </div>
  </div>
  <div v-if="store.showExtremes" class="extrem-panel">
    <h3 id="h3-1" > Extremwerte
    </h3>
    <table id="extremwerteliste">
        <thead>
            <tr>
                <th>Station </th>
                <th>Wert</th>
                <th v-if = "store.methode !== 'rsk_sum' ">Messdatum</th>
            </tr>
        </thead>
        <tr v-for="item in store.extremwerte" :key="item.id">
           <td> {{ item.stationsname }} </td> <td>{{ item.wert }} {{ store.einheit }} &nbsp;</td><td v-if = "store.methode !== 'rsk_sum' ">{{ new Date(item.mess_datum).toLocaleDateString('de-DE') }}</td>
        </tr>
    </table>
  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue'
import { useStore1 } from '@/stores/store1'
const store = useStore1()
onMounted(() => {
  store.fetchStationnames()
})

</script>

<style scoped>
.fundamental-search {
    height: 100%;
    width: 100%;
    margin: 0px;
    padding: 0.5em;
    font-family: 'Ubuntu', system-ui, sans-serif;
}
.bereich{
    overflow: auto;
}
.bereich2{
    float: right;
    margin-right: 5%;
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
.label1{
    margin-left: 30%;
}
::placeholder {
    color: rgb(192, 190, 190);
    opacity: 1;
}
.eingabe2{
    float: center;
    padding: 2px;
    margin: 0px;
    background-color: #142d4cd1;
    border: 2px solid #142d4c;
    border-radius: 2px;
    color: white;
}
.eingrenzungstext{
    margin-bottom: 10px;
    margin-top: 0px;
    width: max-content;
    text-align: left; 
}
.werteingrenzung{
    display: grid;
    justify-content: right;
    margin-right: 5%;
}



h2{
    text-align: center; 
    margin: 5px;
    padding: 0px;
}
h3{
    text-align: left; 
    width: 100%;
    margin-top: 3px;
    margin-bottom: 5px;
}
#h3-1{
    text-align: center;
}
p{
    margin-top: 0;
    padding-top: 2px;
}


.ul1 {
     margin: 5px;
     margin-left: 20%;
     display: grid;
     flex-direction: column;
     justify-content: left;
}
li:nth-of-type(1n+11) {
    display: none;
} 


#unterenavbar{
    display: grid;
    justify-content: right; 
    margin-right: 5%;
}
.ergebnisbutton{
    height: 40px;
    width: 40px;
    margin-right: 10px;
    margin-top: 20px;
    border-radius: 2px;
    border: 1px groove #7990b173;
    background-color: rgba(222, 222, 222, 0.515);
    font-size: large;
    text-align: center;
    color: #d9dbdd;
    box-shadow: 0 0 5px rgba(0,0,0,0.3); 
}
.ergebnisbutton:hover {
  background-color: rgba(189, 189, 189, 0.666);
  cursor: pointer;
}
.icon-btn {
  display: flex;
  align-items: center;
  justify-content: center;
}
.icon {
  width: 22px;
  height: 22px;
  fill: lightblue;
  stroke: #757575;
  stroke-width: 2;
}
#icon1{
    fill: rgb(255, 179, 0);
    stroke: orange;
}


.extrem-panel {
  position: fixed;
  bottom: 43vh;
  right: 0;
  width: fit-content;
  height: fit-content;
  margin-right: 8px;
  padding: 5px;
  border: 2px groove #4b6380;
  border-radius: 4px;
  box-shadow: 0 0 5px rgba(0,0,0,0.3);
  font-family: 'Ubuntu', system-ui, sans-serif;
  line-height: 14pt;
  background: rgb(255, 255, 255);
  z-index: 9000;
}
#extremwerteliste{

  border-collapse: collapse;
  font-size: 9pt;
  letter-spacing: 1px;
  white-space: nowrap;
}
td, th{
    border: 1px solid rgb(160 160 160);
    width: fit-content;
    height: 100%;
}

</style>