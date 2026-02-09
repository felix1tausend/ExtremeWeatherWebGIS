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
let legendControl

const props = defineProps({
  stations: {
    type: Array,
    required: true
  }
})


onMounted(async function() {


  map = L.map('map',{
  center: [51, 10],
  zoom: 7,
  zoomControl: false, 
  });

  addLegend(store.einheit, store.suchmodus, store.methode)

  osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '&copy; OpenStreetMap contributors'
  });
  otp = L.tileLayer('https://tile.opentopomap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: 'OpenTopoMap'
  });
  google = L.tileLayer('http://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}', {
  maxZoom: 19,
  attribution: 'google'
  });
  esris = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',{ 
  maxZoom: 19,
  attribution: 'Tiles &copy; Esri &mdash; Street Map' 
  });
  esrit = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}', {
  attribution: 'Tiles &copy; Esri &mdash; Topographic'
  }).addTo(map);

markerLayer = L.layerGroup().addTo(map)

const baseMaps = { "OpenStreetMap": osm, "OpenTopoMap": otp, "Satellit": google, 'ESRI Street Map': esris, 'ESRI Topographic': esrit};
const overlayMaps = { "Stationsmesswerte": { 'Wetterstationen' :  markerLayer } }

groupedLayerControl = L.control.groupedLayers(baseMaps, overlayMaps,{ 
  position: 'topright'}).addTo(map);

})



function addLegend(einheit, suchmodus, methode) {
  if (legendControl) {
    map.removeControl(legendControl)
  }
  legendControl = L.control({ position: 'bottomright' })
  legendControl.onAdd = function () {
    const div = L.DomUtil.create('div', 'legend')
    const items = getLegendItems(einheit, suchmodus, methode)
    div.innerHTML = `<strong>Legende</strong><br>`
    items.forEach( function (item) {
      div.innerHTML +=
        `<div class="legend-item">
          <span class="legend-color" style="background:${item.color}"></span>
          ${item.label}
        </div>`
    })
    return div
  }
  legendControl.addTo(map)
}

function getLegendItems(einheit, suchmodus, methode) {
  if (einheit === '°C') {
    return [
      { color: 'lightgray', label: 'keine Daten' },
      { color: '#360259', label: '< -30 °C' },
      { color: '#00305A', label: '-30 bis -20 °C' },
      { color: '#0288D1', label: '-20 bis -10 °C' },
      { color: '#0EEAFF', label: '-10 bis 0 °C' },
      { color: '#45BF55', label: '0 bis 10 °C' },
      { color: '#FFE11A', label: '10 bis 20 °C' },
      { color: '#F2B705', label: '20 bis 30 °C' },
      { color: '#D23600', label: '30 bis 40 °C' },
      { color: '#440505', label: '> 40 °C' }
    ]
  }

  if (einheit === 'm/s') {
    return [
      { color: 'lightgray', label: 'keine Daten' },
      { color: '#FFFFFF', label: '< 0.3 (Bft 0)' },
      { color: '#B0E1F7', label: '0.3 bis 1.6 (Bft 1)' },
      { color: '#81D4FA', label: '1.6 bis 3.4 (Bft 2)' },
      { color: '#4FC3F7', label: '3.4 bis 5.5 (Bft 3)' },
      { color: '#4CAF50', label: '5.5 bis 8.0 (Bft 4)' },
      { color: '#CDDC39', label: '8.0 bis 10.8 (Bft 5)' },
      { color: '#FFEB3B', label: '10.8 bis 13.9 (Bft 6)' },
      { color: '#FFC107', label: '13.9 bis 17.2 (Bft 7)' },
      { color: '#FF9800', label: '17.2 bis 20.8 (Bft 8)' },
      { color: '#F44336', label: '20.8 bis 24.5 (Bft 9)' },
      { color: '#D32F2F', label: '24.5 bis 28.5 (Bft 10)' },
      { color: '#7B1FA2', label: '28.5 bis 32.7 (Bft 11)' },
      { color: '#4A148C', label: '> 32.7 (Bft 12)' }
    ]
  }

  if (einheit === 'mm' && suchmodus ==='fundamental' ||   (suchmodus === 'expanded' && methode === 'rsk_max')) {
    return [
      { color: 'lightgray', label: 'keine Daten' },
      { color: '#FFFFFF', label: '< 0.1 mm' },
      { color: '#E3F2FD', label: '0.1 bis 1 mm' },
      { color: '#90CAF9', label: '1 bis 5 mm' },
      { color: '#42A5F5', label: '5 bis 10 mm' },
      { color: '#1E88E5', label: '10 bis 20 mm' },
      { color: '#1565C0', label: '20 bis 30 mm' },
      { color: '#6A1B9A', label: '30 bis 50 mm' },
      { color: '#AD1457', label: '50 bis 100 mm' },
      { color: '#B71C1C', label: '> 100 mm' }
    ]
  }
  if (einheit === 'mm' && suchmodus === 'expanded' && methode === 'rsk_sum') {
    const breaks = getBreaks(props.stations)
    return[
      { color: '#B71C1C', label: ' < '+ breaks[0]+ ' mm' },
      { color: '#D32F2F', label: breaks[0]+' bis '+ breaks[1] + ' mm' },
      { color: '#F44336', label: breaks[1]+' bis '+ breaks[2] + ' mm' },
      { color: '#FB8C00', label: breaks[2]+' bis '+ breaks[3] + ' mm' },
      { color: '#FDD835', label: breaks[3]+' bis '+ breaks[4] + ' mm' },
      { color: '#90CAF9', label: breaks[4]+' bis '+ breaks[5] + ' mm' },
      { color: '#42A5F5', label: breaks[5]+' bis '+ breaks[6] + ' mm' },
      { color: '#1E88E5', label: breaks[6]+' bis '+ breaks[7] + ' mm' },
      { color: '#0D47A1', label: '> '+ breaks[7] + ' mm' }
    ]
}return []}




watch(
  function () {
    return props.stations
  },
  function (newStations) {
    markerLayer.clearLayers()
    for (let i = 0; i < newStations.length; i++) {
      const station = newStations[i]
      if (station.wert === -999) {
        ladeStationenohneWert(station)
      }
    }
    for (let i = 0; i < newStations.length; i++) {
      const station = newStations[i]
      if (station.wert !== -999) {
        ladeStationenmitWert(station, store.methode)
      }
    }
    addLegend(store.einheit, store.suchmodus, store.methode)
  }
)


  function ladeStationenohneWert(station){
    const coords = station.geom
    if (station.wert === -999) {
      let popupText = "<b>" + station.stationsname + "</b><br>"
                + store.parameterbezeichnung + ": keine Messung"
      const circleMarker = L.circleMarker(
      [coords.coordinates[1], coords.coordinates[0]],
      {
        radius: 7,
        fillColor: getColorByValue(station.wert, store.einheit, store.suchmodus, store.methode, props.stations),
        color: 'black',
        weight: 0.5,
        opacity: 0.4,
        fillOpacity: 0.2,
      }
    ).bindPopup(popupText)
    circleMarker.addTo(markerLayer)
    }}


  function ladeStationenmitWert(station){
    if (!markerLayer) return;
    const coords = station.geom;
    if (!coords || !coords.coordinates) return;

    const datum = new Date(station.mess_datum);
    const formattedDatum = new Intl.DateTimeFormat('de-DE', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    }).format(datum);

    if (station.wert === -999) return;
    let popupText = ''
    if (store.methode === 'rsk_sum'){
        popupText = `<b>${station.stationsname}</b><br>
                        Niederschlagssumme: <b>${station.wert} ${store.einheit}</b><br>
                        Stationshöhe: ${station.stationshoehe} m<br>
                        Standort: ${coords.coordinates[1]} N ${coords.coordinates[0]} O`;
    } else{
        popupText = `<b>${station.stationsname}</b><br>
                        ${store.parameterbezeichnung}: <b>${station.wert} ${store.einheit}</b><br>
                        Messdatum: ${formattedDatum}<br>
                        Stationshöhe: ${station.stationshoehe} m<br>
                        Standort: ${coords.coordinates[1]} N ${coords.coordinates[0]} O`;

    }

  const circleMarker = L.circleMarker(
    [coords.coordinates[1], coords.coordinates[0]],
    { 
      radius: 7,
      fillColor: getColorByValue(station.wert, store.einheit, store.suchmodus, store.methode, props.stations),
      color: 'black',
      weight: 0.5,
      opacity: 0.4,
      fillOpacity: 0.8
    }
  ).bindPopup(popupText);

  circleMarker.addTo(markerLayer);
}

function getBreaks(stations, n = 9) {
  const werte = stations.map(s => s.wert)
  const min = Math.min(...werte)
  const max = Math.max(...werte)
  const range = max - min
  const breaks = []
  for (let k = 1; k < n; k++) {
    const value =(min + Math.pow(k / n, 2) * range) // quadratische Klassifizierung
    breaks.push(Math.round(value * 100) / 100)
  }
  return breaks
}


  function getColorByValue(wert, einheit, suchmodus, methode, stations) {
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
      if (wert < 1.6)  return '#B0E1F7'  // Bft 1
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
    if (einheit === 'mm' && suchmodus ==='fundamental' ||   (suchmodus === 'expanded' && methode === 'rsk_max') ) {
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
    }                 
    if (einheit === 'mm' && suchmodus === 'expanded' && methode === 'rsk_sum') {
    if (wert === -999) return 'lightgray'
    const breaks = getBreaks(stations)
    const colors = [
      '#B71C1C',
      '#D32F2F',
      '#F44336',
      '#FB8C00',
      '#FDD835',
      '#90CAF9',
      '#42A5F5',
      '#1E88E5',
      '#0D47A1'
    ]
    for (let i = 0; i < breaks.length; i++) {
      if (wert < breaks[i]) return colors[i]
    }
    return colors[colors.length - 1]
  }
}




</script>


<template>
<div class ="mapwrapper">
  <div id="map"></div>
</div>
</template>

<style scoped>

</style>
