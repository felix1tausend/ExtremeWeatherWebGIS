<template>
  <div id="navbar1">
   <ul>
      <li class="title">Extremwetter WebGIS</li>
      <li class="spacer"></li>
      <li><button class="info-btn" @click="showInfo = true">i</button></li>
    </ul>



    <div v-if="showInfo" class="modal-overlay" @click.self="showInfo = false">
        <div class="modal-content">
            <h2>Info</h2>
            <p>Test</p>
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
  position: absolute;
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



.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10000;
}


.modal-content {
  background-color: #142d4c;
  color: #fff;
  padding: 2em;
  border-radius: 8px;
  width: 400px;
  max-width: 80%;
  text-align: center;
  font-family: 'Ubuntu', sans-serif;
}


.close-btn {
  margin-top: 1em;
  padding: 0.5em 1em;
  border: none;
  border-radius: 4px;
  background-color: #385170;
  color: #fff;
  cursor: pointer;
}

.close-btn:hover {
  background-color: #4b6990;
}
</style>
