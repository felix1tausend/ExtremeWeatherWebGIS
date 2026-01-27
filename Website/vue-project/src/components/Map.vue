<script setup>
import { onMounted, watch } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import 'leaflet-groupedlayercontrol/dist/leaflet.groupedlayercontrol.min.css'
import 'leaflet-groupedlayercontrol'
import { useStore1 } from '@/stores/store1'
const store = useStore1()
let map
let markerLayer
let osm, google, otp, esris, esrit
let groupedLayerControl

const props = defineProps({
  stations: {
    type: Array,
    required: true
  }
})


onMounted(async() => {


  map = L.map('map',{
  center: [51, 10],
  zoom: 7,
  zoomControl: false, 
  });

  osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap contributors'
  });

  otp = L.tileLayer('https://tile.opentopomap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: 'OpenTopoMap'});

  google = L.tileLayer('http://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}', {
    maxZoom: 19,
    attribution: 'google'
  });

  esris = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',{ 
  maxZoom: 19,
  attribution: 'Tiles &copy; Esri &mdash; Street Map' });


  esrit = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}', {
  attribution: 'Tiles &copy; Esri &mdash; Topographic'
}).addTo(map);

markerLayer = L.layerGroup().addTo(map)


const baseMaps = { "OpenStreetMap": osm, "OpenTopoMap": otp, "Satellit": google, 'ESRI Street Map': esris, 'ESRI Topographic': esrit};
const overlayMaps = { "Stationsmesswerte": { "Tagesmaximaltemperatur": markerLayer } }

groupedLayerControl = L.control.groupedLayers(baseMaps, overlayMaps,{ 
  position: 'topright'}).addTo(map);

L.control.zoom({position: 'bottomright'}).addTo(map);
})


watch(
  () => props.stations,
  (newStations) => {
    markerLayer.clearLayers()

    newStations.forEach(station => {
      const coords = station.geom

      L.marker([
        coords.coordinates[1],
        coords.coordinates[0]
      ])
        .bindPopup(`
          <b>${station.stationsname}</b><br>
          ${store.parameterbezeichnung}: ${station.parameter} ${store.einheit}
        `)
        .addTo(markerLayer)
    })
  },
  { deep: true }
)
</script>


<template>
<div class ="mapwrapper">
  <div id="map"></div>
</div>
</template>

<style scoped>
</style>
