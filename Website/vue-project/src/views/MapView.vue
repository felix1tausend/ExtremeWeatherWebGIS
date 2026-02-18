<template>
  <div class="map-view">
    <NavBar></NavBar>
    <BasicSearchInterface></BasicSearchInterface>
    <Map v-if="store.marker" :stations="store.marker" />
  </div>
</template>

<script setup>
import { useStore1 } from '@/stores/store1'
const store = useStore1()
import NavBar from '../components/NavBar.vue'
import Map from '../components/Map.vue'
import BasicSearchInterface from '@/components/BasicSearchInterface.vue'



</script>

<style scoped>
.map-view {
  height: 100%;
  width: 100%;
  position: relative;
}
</style>