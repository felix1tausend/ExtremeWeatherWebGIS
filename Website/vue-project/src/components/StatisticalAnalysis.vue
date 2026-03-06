<template>
  <div class="searchinterface">
    <ul id="ul1">
        <li><h2>Statistische Analyse </h2></li>
        <li><button v-if = "showInfo === false" class="info-btn2" @click="showInfo = true"> ?</button>
            <button v-else class="info-btn2" @click="showInfo = false">?</button></li>
    </ul>
     <div v-if="showInfo" class="modal" @click.self="showInfo = false">
        <div class="modal-content">
            <h3>Was macht die statistische Suche?</h3>
            <p> Der Bereich der statistischen Analyse untersucht jährliche über Deutschland gemittelte klimatologische Kenngrößen. <br>
                Zu den Kenngrößen gehören: <br><br>
                <strong>1)	Die jährliche Anzahl der Hitze-, Kälte-, Sturm-, Starkregen- und Trockentage gemittelt über alle Stationen. <br><br>
                2)	Die jährliche Minimal- und Maximaltemperatur, Maximalwindgeschwindigkeit, <br>
                    maximale tägliche Niederschlagssumme sowie die Jahresniederschlagssumme gemittelt über alle Stationen.</strong><br><br>

                Diese Kenngrößen geben Aufschluss über die Entwicklung des Extremwetters in Deutschland. <br>
                Dabei werden die jährlichen Mittelwerte von 1950 bis 2024 in Diagrammen präsentiert. <br>
                 Aus diesen Daten berechnet sich auch eine Trendlinie berechnet, die bis ins Jahr 2050 extrapoliert wird.


            </p>
            <button class="close-btn" @click="showInfo = false">Schließen</button>
        </div>
     </div>
    
    <div class="bereich">
        <h3>Auswertungsmethode: </h3>
            <label class="label1">
                <input type="radio" value="hitze" name="analyse" v-model="store.analysetyp">
                Hitzetage und höchste Temperatur
            </label><br>
            <label class="label1">
                <input type="radio" value="kaelte" name="analyse" v-model="store.analysetyp">
                Kältetage und niedrigste Temperatur
            </label><br>
            <label class="label1">
                <input type="radio" value="wind" name="analyse" v-model="store.analysetyp">
                Sturmtage und maximale Windgeschwindigkeit
            </label><br>
            <label class="label1">
                <input type="radio" value="regen" name="analyse" v-model="store.analysetyp">
                Starkregentage und maximaler Niederschlag
            </label><br>
            <label class="label1">
                <input type="radio" value="trockenheit" name="analyse" v-model="store.analysetyp">
                Trockentage und jährliche Niederschlagssumme
            </label>
    </div>
    <div id ="unterenavbar">
        <ul>
            <li> 
                <button class="ergebnisbutton" @click="store.fetchResults()">
                    <svg viewBox="0 0 24 24" class="icon">
                        <circle cx="11" cy="11" r="7"/>
                        <line x1="16.65" y1="16.65" x2="22" y2="22"/>
                    </svg>
                </button>
            </li>
        </ul>   
    </div>
  </div>
  <div v-if="store.suche" class="modal" @click.self="store.suche = false">
        <div class="modal-content">
            <h2>Stationsmesswerte in Deutschland von 1950 bis 2024</h2>
            <img  id = "diagramm" v-if="store.diagramm" :src="store.diagramm" alt="Diagramm" /> <br>
            <button class="close-btn" @click="store.suche = false">Schließen</button>
        </div>
    </div>
</template>


<script setup>
import { ref, onMounted } from 'vue'
import { useStore1 } from '@/stores/store1'
const showInfo = ref(false)
const store = useStore1()
onMounted(() => {
    store.suchmodus = 'statistical'
})

</script>

<style scoped>
.searchinterface {
    height: 100%;
    width: 100%;
    margin: 0px;
    padding: 0.5em;
    font-family: 'Ubuntu', system-ui, sans-serif;
}

.label1{
    display: flex;
    width: 93%;
    margin-left: 1%;
    padding-top: 9px;
    padding-bottom: 9px;
    background-color: #142d4cd1;
    border: 1px groove #142d4c;
    border-radius: 4px;
    color: rgb(255, 255, 255);
    box-shadow: 0 0 5px rgba(0,0,0,0.3); 
}

h2{
    text-align: center; 
    margin: 5px;
    padding: 0px;
}
h3{
    text-align: left; 
    width: 100%;
    margin-top: 10px;
    margin-bottom: 10px;
}
p{
    margin-top: 0;
    padding-top: 2px;
}
#ul1{
    height: fit-content;
    width: fit-content;
    margin: 0 auto;
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


.modal {
  inset: 0; 
  z-index: 10000;
  position: fixed;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(0,0,0,0.5);
}

.modal-content {
  height: max-content;
  width: max-content;
  margin-top: 2%;
  border-radius: 8px;
  padding-left: 1em;
  padding-right: 1em;
  border: 3px solid #4b6380;
  background-color: #142d4cdc;
  font-family: 'Ubuntu', sans-serif;
  text-align: justify;
  color: #ffffff;
  overflow: auto;
}

.info-btn2 {
  height: 1.1rem;
  width: 1.1rem;
  position: flex;
  border-radius: 100%;
  font-weight: 600;
  border: 1px solid #4b6380;
  background-color: #142d4cdc;
  font-family: 'Times New Roman', Times, serif;
  color: #d9dbdd;
  cursor: pointer;
}

.info-btn2:hover {
  background-color: rgb(56, 81, 112);
}

#diagramm{
    height: auto;
    width: auto;
    background-color: white;
    border-radius: 4px;
}

</style>