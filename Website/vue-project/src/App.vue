<script setup>
import { onMounted } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

let map
let osm
let google
let baseMaps
let overlayMaps
let layerControl


onMounted(async() => {


  map = L.map('map',{
  center: [51.0557, 13.7274],
  zoom: 7,
  zoomControl: false, 
  });

  osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);


  google = L.tileLayer('http://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}', {
    maxZoom: 19,
    attribution: 'google'
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


baseMaps = { "OSM": osm,
  "Satellit": google
};

overlayMaps ={"Tagesmaximaltemperatur aller Stationen": markerGroup};

layerControl = L.control.layers(baseMaps, overlayMaps).addTo(map);
L.control.zoom({position: 'bottomright'}).addTo(map);
map.fitBounds(markerGroup.getBounds())


})


</script>

<template>
<div class ="mapwrapper">
  <div id="map"></div>
</div>
</template>

<style scoped></style>
