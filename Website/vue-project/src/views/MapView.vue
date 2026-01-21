<template>
  <div class="map-view">
    <NavBar></NavBar>
    <LayerControl></LayerControl>
    <FundamentalSearch @updateStations="stations = $event"/>
    <Map :stations="stations"/>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import NavBar from '../components/NavBar.vue'
import LayerControl from '@/components/LayerControl.vue'
import Map from '../components/Map.vue'
import FundamentalSearch from '../components/FundamentalSearch.vue'

const stations = ref([])
</script>

<style scoped>
.map-view {
  height: 100%;
  width: 100%;
  position: relative;
}
</style>