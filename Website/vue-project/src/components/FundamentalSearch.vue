<template>
  <div class="fundamental-search">
    <h2>Einfache Suche</h2>
    <div id="Basisparameter" class="bereich">
        <h3>Basisfilter</h3>
        <p>Wetterparameter:
            <select v-model="store.parameter" class="eingabe">
            <option value="txk">Tagesmaximaltemperatur</option>
            <option value="tnk">Tagesminimaltemperatur</option>
            <option value="fx">Tagesmaximalwindgeschwindigkeit</option>
            <option value="rsk">Tagesniederschlag</option>
            </select>
        </p>
        <p>Datum:
            <input id="datumseingabe" class ="eingabe" type="date"  min="1950-01-01" max="2024-12-31" v-model="store.messdatum">
        </p>
        

    </div>
    <div id="Raumauswahl" class="bereich">
        <h3>Räumliche Auswahl (optional) </h3>
        <p>Bundesland:
            <select id="Bundeslandeingabe" class ="eingabe" v-model="store.bundesland" >
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
            <ul v-if="store.stationsname">
                <li v-for="station in filteredStations" :key="station">
                {{ station }}
                </li>
            </ul>
        </p>
        <div><p>Stationshöhe:</p>
            <div id="höhenblock">
                <p class="höhentext"> über &nbsp; <input class ="eingabe2"> m</p>
                <p class="höhentext">unter <input class ="eingabe2"> m</p>
            </div>
        </div>
    </div>
    <div id = "Werteingrenzung" class="bereich">
        <h3>Werteingrenzung (optional)</h3>
        <div><p>Messwertebereich:</p>
            <div id="höhenblock">
                <p class="höhentext"> über &nbsp; <input class ="eingabe2"> {{ store.einheit }}</p>
                <p class="höhentext">unter <input class ="eingabe2"> {{ store.einheit }}</p>
            </div>
        </div>
    </div>
    <div id ="Listenbereich" class="bereich">
    <button @click="store.fetchResults">Suchen
    </button>
        
    </div>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useStore1 } from '@/stores/store1'
const store = useStore1()
const stations = ref([])

//Suche nach Stationen
fetch('/stationsname.txt')
  .then(r => r.text())
  .then(t => {
    stations.value = t.split('\n').filter(Boolean)
  })

const filteredStations = computed(() => {
  const q = store.stationsname.toLowerCase()
  if (q.length < 2) return []

  return stations.value
    .filter(s => s.toLowerCase().includes(q))
    .slice(0, 10)
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

.eingabe2{
    float: center;
    padding: 2px;
    background-color: #142d4cd1;
    border: 2px solid #142d4c;
    border-radius: 2px;
    color: white;
}

#höhenblock{
    display: grid;
    justify-content: right;
    margin-right: 5%;

}

.höhentext{
    margin-bottom: 10px;
    margin-top: 0px;
    width: max-content;
    text-align: left;
    
}

.bereich{
    overflow: hidden;
}

::placeholder {
  color: rgb(192, 190, 190);
  opacity: 1;
}

</style>