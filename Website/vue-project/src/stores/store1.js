import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'
import { API_BASE_URL } from '@/config'

export const useStore1 = defineStore('store1', function() {
  const parameter = ref('txk') //Wetterparameter
  const methode = ref('txk_max') //Aggregationsmethode der erweiterten Suche
  const messdatum = ref('2024-12-31') //Messdatum
  const von_datum = ref('2023-12-31') //Messzeitraum der erweiterten Suche
  const bis_datum = ref('2024-12-31') //Messzeitraum der erweiterten Suche
  const listensortierung = ref('desc') //Sortierung im Extremwert-Panel
  const bundesland = ref('') //Bundesland
  const stationsname = ref('') // Eingabe im Suchfeld
  const stationsliste = ref([]) // Alle Stationen aus Datei
  const ausgewählteStationen = ref([]) // Ausgewählte Stationen, für welche ein Ergebnis geliefert werden soll
  const höheüber = ref('') //Höhenbegrenzung
  const höheunter = ref('') //Höhenbegrenzung
  const untereschwelle = ref('') //Messwertbegrenzung
  const obereschwelle = ref('') //Messwertbegrenzung
  const marker = ref([]) //Stationsmarker
  const extremwerte = ref([]) //Extremwertliste
  const suchmodus = ref('fundamental') //Filterbereich
  const showExtremes = ref(true) //Extremwertpanelsteuerung
  const suche = ref(false) // Aktivität des Diagramm-Dialogfensters der statistischen Suche
  const analysetyp = ref('hitze') // Analysemethode der statistischen Analayse
  const diagramm = ref('') //Inhalt des Diagramms der statistischen Suche


// Zurücksetzen der default-Werte
  watch(suchmodus, function(neu){
    if (neu) {
      methode.value = 'txk_max'
      messdatum.value = '2024-12-31'
      von_datum.value = '2023-12-31'
      bis_datum.value = '2024-12-31'
      listensortierung.value = 'desc'
      bundesland.value = ''
      höheüber.value = ''
      höheunter.value = ''
      untereschwelle.value = ''
      obereschwelle.value = ''
    }
  })
// Ermittlung der Einheit des Wetterparameters
  const einheit = computed(function(){
      let param
      if (suchmodus.value === 'expanded') {
        param = methode.value.split('_')[0]
      } else {
        param = parameter.value
      }
      switch (param) {
        case 'txk':
        case 'tnk': return '°C'
        case 'fx': return 'm/s'
        case 'rsk': return 'mm'
        default: return ''
      }
    })
// Ermittlung der Bezeichnung des Wetterparameters
  const parameterbezeichnung = computed(function(){
      let param
      if (suchmodus.value === 'expanded') {
        param = methode.value.split('_')[0]
      } else {
        param = parameter.value
      }
      switch (param) {
        case 'txk': return 'Tagesmaximaltemperatur'
        case 'tnk': return 'Tagesminimaltemperatur'
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
  //Stationen filtern und ausgewählte Stationen anzeigen
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
//Gemeinsame Grundwerte
const gemeinsameParameter = function(url){
  if (bundesland.value && bundesland.value != '-')
    url.searchParams.set('bundesland', bundesland.value)
  if (ausgewählteStationen.value.length > 0)
    url.searchParams.set('stationsnamen', ausgewählteStationen.value.join(','))
  if (höheüber.value)
    url.searchParams.set('höheüber', höheüber.value)
  if (höheunter.value)
    url.searchParams.set('höheunter', höheunter.value)
  if (untereschwelle.value != null)
    url.searchParams.set('untereschwelle', untereschwelle.value)
  if (obereschwelle.value != null)
    url.searchParams.set('obereschwelle', obereschwelle.value)
  }
// Einfache Suche
const fundamentalurl = computed( function() {
  if (suchmodus.value !== 'fundamental') return '';
  const url = new URL(`${API_BASE_URL}/api/fundamentalsearch/`)
  url.searchParams.set('parameter', parameter.value)
  url.searchParams.set('messdatum', messdatum.value)
  gemeinsameParameter(url)
  return url.toString()
})
// Erweiterte Suche
const expandedurl = computed( function(){
  if (suchmodus.value !== 'expanded') return '';
  const url = new URL(`${API_BASE_URL}/api/expandedsearch/`)
  const [param, aggregation] = methode.value.split('_')
  url.searchParams.set('parameter', param)
  url.searchParams.set('aggregation', aggregation)
  url.searchParams.set('von_datum', von_datum.value)
  url.searchParams.set('bis_datum', bis_datum.value)
  if (aggregation === 'sum')
     url.searchParams.set('listensortierung', listensortierung.value)
  gemeinsameParameter(url)
  return url.toString()
})
//Statistische Analyse
const statisticalurl = computed(function() {
  if (suchmodus.value !== 'statistical') return '';
  const url = new URL(`${API_BASE_URL}/api/statisticalanalysis/`)
  url.searchParams.set('analysetyp', analysetyp.value)
  return url.toString()
})
  // Ergebnis-JSON von Flask holen
async function fetchResults() {
  if (suchmodus.value === "fundamental"){
    const response = await fetch(fundamentalurl.value)
    const json = await response.json()
    marker.value = json.daten
    extremwerte.value = json.extremwerte
  }if (suchmodus.value === "expanded"){
    const response = await fetch(expandedurl.value)
    const json = await response.json()
    marker.value = json.daten
    extremwerte.value = json.extremwerte
  }if (suchmodus.value === "statistical"){
      suche.value = true
      const response = await fetch(statisticalurl.value)
      const json = await response.json()
      diagramm.value = "data:image/png;base64," + json.image
  }}


  return { 
    parameter, 
    parameterbezeichnung, 
    einheit, 
    messdatum, 
    von_datum, bis_datum, 
    methode, 
    listensortierung, 
    bundesland, 
    stationsname, 
    stationsliste, 
    ausgewählteStationen, 
    fetchStationnames, 
    filteredStations, 
    toggleStation, 
    höheüber, höheunter, 
    untereschwelle, obereschwelle, 
    fundamentalurl, 
    expandedurl, 
    marker, 
    extremwerte, 
    fetchResults,
    suchmodus, 
    showExtremes, 
    suche, 
    analysetyp, 
    diagramm}
})
