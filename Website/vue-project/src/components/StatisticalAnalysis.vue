<template>
  <div class="fundamental-search">
    <h2>Statistische Analyse</h2>
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
    </div>
    <div id ="unterenavbar">
        <ul>
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

</style>