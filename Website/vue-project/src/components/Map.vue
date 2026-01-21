<script setup>
import { onMounted } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import 'leaflet-groupedlayercontrol/dist/leaflet.groupedlayercontrol.min.css'
import 'leaflet-groupedlayercontrol'
let map
let osm
let google
let otp
let esris
let esrit
let baseMaps
let groupedLayerControl


onMounted(async() => {

  map = L.map('map',{
  center: [51.0557, 13.7274],
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




  
      // Daten vom Backend abrufen
      const response = await fetch('http://127.0.0.1:5000/api/testmesswert');
      const data = await response.json();
      console.log(data)
      const markerGroup = L.layerGroup();
    for (const item of data) {
      L.marker([item.lat, item.lng])
        .bindPopup(`<b>${item.name}</b><br>Tagesmaximaltemperatur: ${item.txk}`)
        .addTo(markerGroup);
    }
  markerGroup.addTo(map);


baseMaps = { "OpenStreetMap": osm, "OpenTopoMap": otp, "Satellit": google, 'ESRI Street Map': esris, 'ESRI Topographic': esrit};
const overlayMaps = { "Stationsmesswerte": { "Tagesmaximaltemperatur": markerGroup } }

groupedLayerControl = L.control.groupedLayers(baseMaps, overlayMaps,{ 
  position: 'topright'}).addTo(map);

L.control.zoom({position: 'bottomright'}).addTo(map);
})
</script>


<template>
<div class ="mapwrapper">
  <div id="map"></div>
</div>
</template>

<style scoped>
</style>
