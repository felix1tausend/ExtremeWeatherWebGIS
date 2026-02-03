// stores/store1.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useStore1 = defineStore('store1', function() {
  const parameter = ref('txk')
  const messdatum = ref('2024-12-31')
  const bundesland = ref('')
  const stationsname = ref('')         // Eingabe im Suchfeld
  const stationsliste = ref([])        // Alle Stationen aus Datei
  const ausgewählteStationen = ref([]) // Ausgewählte Stationen, für welche ein Ergebnis geliefert werden soll
  const höheüber = ref('')
  const höheunter = ref('')
  const untereschwelle = ref('')
  const obereschwelle = ref('')
  const marker = ref([]) //Stationsmarker
  const extremwerte = ref([]) //Extremwertliste


  const einheit = computed(function() {
    switch (parameter.value) {
      case 'txk':
      case 'tnk': return '°C'
      case 'fx': return 'm/s'
      case 'rsk': return 'mm'
      default: return ''
    }
  })

  const parameterbezeichnung = computed(function(){
    switch (parameter.value) {
      case 'txk': return 'Tagesmaximaltemperatur'
      case 'tnk': return 'Tagenminimaltemperatur'
      case 'fx': return 'Tagesmaximalwindgeschwindigkeit'
      case 'rsk': return 'Tagesniederschlagssumme'
      default: return ''
    }
  })


  // Stationen aus Datei laden und in Liste packen
  async function fetchStationnames() {
    const response = await fetch('/stationsliste.txt')
    const text = await response.text()
    stationsliste.value = text.split('\n')
  }

  //Stationen filternund ausgewählte Stationen anzeigen
  const filteredStations = computed(function () {
  const q = stationsname.value.toLowerCase().trim()
  let filtered = []

  if (q.length >= 2) {
    const words = q.split(/\s+/)

    filtered = stationsliste.value.filter(function (s) {
      const name = s.toLowerCase()
      return words.every(function (word) {
        return name.includes(word)
      })
    })
  }

  ausgewählteStationen.value.forEach(function (s) {
    if (!filtered.includes(s)) filtered.push(s)
  })

  return filtered.slice(0, 10)
})

  // Station auswählen/deselektieren
  function toggleStation(station) {
    const index = ausgewählteStationen.value.indexOf(station)
    if (index === -1) {
      ausgewählteStationen.value.push(station)
    } else {
      ausgewählteStationen.value.splice(index, 1)
    }
  }

  //URL aus eingegebenen Daten zusammensetzen
  const fundamentalurl = computed (function(){
    const url = new URL('http://localhost:5000/api/fundamentalsearch/')
    url.searchParams.set('parameter', parameter.value)
    url.searchParams.set('messdatum', messdatum.value)
    if (bundesland.value && bundesland.value != '-')
      url.searchParams.set('bundesland', bundesland.value)
    if (ausgewählteStationen.value.length > 0)
      url.searchParams.set('stationsnamen', ausgewählteStationen.value.join(','))
    if (höheüber.value)
      url.searchParams.set('höheüber', höheüber.value)
    if (höheunter.value)
      url.searchParams.set('höheunter', höheunter.value)
    if (untereschwelle.value)
      url.searchParams.set('untereschwelle', untereschwelle.value)
    if (obereschwelle.value)
      url.searchParams.set('obereschwelle', obereschwelle.value)
    return url.toString() 
  })


  // Ergebnis-JSON von Flask holen
async function fetchResults() {
  const response = await fetch(fundamentalurl.value)
  const json = await response.json()
  marker.value = json.daten
  extremwerte.value = json.extremwerte
}

  return { parameter, parameterbezeichnung, einheit, messdatum, bundesland, stationsname, stationsliste, ausgewählteStationen, fetchStationnames, filteredStations, toggleStation, höheüber, höheunter, untereschwelle, obereschwelle, fundamentalurl, marker, extremwerte, fetchResults}
})
