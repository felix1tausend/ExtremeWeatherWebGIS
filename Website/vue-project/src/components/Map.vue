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

function getColorByValue(wert, einheit) {
  if (einheit === '°C') {
    if (wert === -999) return 'lightgray' //keine Daten
    if (wert < -30) return '#360259'
    if (wert < -20) return '#00305A'
    if (wert < -10) return '#0288D1'
    if (wert < 0)   return '#0EEAFF'
    if (wert < 10)  return '#45BF55'
    if (wert < 20)  return '#FFE11A'
    if (wert < 30)  return '#F2B705'
    if (wert < 40)  return '#D23600'
    return '#440505'
  }
  if (einheit === 'm/s') {
    if (wert === -999) return 'lightgray' //keine Daten
    if (wert < 0.3)  return '#FFFFFF'  // Bft 0 
    if (wert < 3.4)  return '#81D4FA'  // Bft 2
    if (wert < 5.5)  return '#4FC3F7'  // Bft 3
    if (wert < 8.0)  return '#4CAF50'  // Bft 4
    if (wert < 10.8) return '#CDDC39'  // Bft 5
    if (wert < 13.9) return '#FFEB3B'  // Bft 6
    if (wert < 17.2) return '#FFC107'  // Bft 7
    if (wert < 20.8) return '#FF9800'  // Bft 8
    if (wert < 24.5) return '#F44336'  // Bft 9
    if (wert < 28.5) return '#D32F2F'  // Bft 10
    if (wert < 32.7) return '#7B1FA2'  // Bft 11
    return '#4A148C'                   // Bft 12
  }
  if (einheit === 'mm') {
    if (wert === -999) return 'lightgray' // keine Daten
    if (wert < 0.1)  return '#FFFFFF'
    if (wert < 1)    return '#E3F2FD'
    if (wert < 5)    return '#90CAF9'
    if (wert < 10)   return '#42A5F5'
    if (wert < 20)   return '#1E88E5'
    if (wert < 30)   return '#1565C0'
    if (wert < 50)   return '#6A1B9A'
    if (wert < 100)  return '#AD1457'
    return '#B71C1C'                 
  }}
 


watch(
  () => props.stations,
  (newStations) => {
    markerLayer.clearLayers()

       newStations
      .filter(station => station.wert === -999)
      .forEach(station => {
        const coords = station.geom
        const circleMarker = L.circleMarker([coords.coordinates[1], coords.coordinates[0]], {
          radius: 7,
          fillColor: getColorByValue(station.wert, store.einheit),
          color: 'black',
          weight: 0.5,
          opacity: 0.4,
          fillOpacity: 0.2
        }).bindPopup(`
          <b>${station.stationsname}</b><br>
          ${store.parameterbezeichnung}: keine Messung
        `)
        circleMarker.addTo(markerLayer)
      })


        newStations
      .filter(station => station.wert !== -999)
      .forEach(station => {
        const coords = station.geom
        const circleMarker = L.circleMarker([coords.coordinates[1], coords.coordinates[0]], {
          radius: 7,
          fillColor: getColorByValue(station.wert, store.einheit),
          color: 'black',
          weight: 0.5,
          fillOpacity: 0.8
        }).bindPopup(`
          <b>${station.stationsname}</b><br>
          ${store.parameterbezeichnung}: ${station.wert} ${store.einheit}
        `)
        circleMarker.addTo(markerLayer)
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
