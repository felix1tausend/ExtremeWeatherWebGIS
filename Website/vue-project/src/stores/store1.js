// stores/store1.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useStore1 = defineStore('store1', () => {
  const parameter = ref('txk')
  const messdatum = ref('2024-12-31')
  const bundesland = ref('')
  const stationsname = ref('')         // Eingabe im Suchfeld
  const stationsliste = ref([])        // Alle Stationen aus Datei
  const ausgewählteStationen = ref([]) // Ausgewählte Stationen, für welche ein Ergebnis geliefert werden soll
  const höheüber = ref('')
  const höheunter = ref('')


  const einheit = computed(() => {
    switch (parameter.value) {
      case 'txk':
      case 'tnk': return '°C'
      case 'fx': return 'm/s'
      case 'rsk': return 'mm'
      default: return ''
    }
  })

  const parameterbezeichnung= computed(() => {
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
const filteredStations = computed(() => {
  const q = stationsname.value.toLowerCase()
  let filtered = []
  if (q.length >= 2) {
    filtered = stationsliste.value.filter(s => s.toLowerCase().includes(q))
  }
  ausgewählteStationen.value.forEach(s => {
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
  const fundamentalurl = computed (()  => {
    const url = new URL('http://localhost:5000/api/fundamentalsearch/')
    url.searchParams.set('parameter', parameter.value)
    url.searchParams.set('messdatum', messdatum.value)
    if (bundesland.value && bundesland.value != '-')
      url.searchParams.set('bundesland', bundesland.value)
    if (ausgewählteStationen.value.length > 0)
      url.searchParams.set('stationsnamen', ausgewählteStationen.value.join(','))
    if (höheüber)
      url.searchParams.set('höheüber', höheüber.value)
    if (höheunter)
      url.searchParams.set('höheunter', höheunter.value)
    return url.toString() 
  })

  const results = ref([])

  // Ergebnis-JSON von Flask holen
  async function fetchResults() {
    const response = await fetch(fundamentalurl.value)
    results.value = await response.json()

}

  return { parameter, parameterbezeichnung, einheit, messdatum, bundesland, stationsname, stationsliste, ausgewählteStationen, fetchStationnames, filteredStations, toggleStation, höheüber, höheunter, fundamentalurl, results, fetchResults}
})
