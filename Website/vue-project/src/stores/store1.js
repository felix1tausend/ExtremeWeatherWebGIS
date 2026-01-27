// stores/store1.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useStore1 = defineStore('store1', () => {
  const parameter = ref('txk')
  const messdatum = ref('2024-12-31')
  const bundesland = ref('')


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


  //URL aus eingegebenen Daten zusammensetzen
  const fundamentalurl = computed (()  => {
    const url = new URL('http://localhost:5000/api/fundamentalsearch/')
    url.searchParams.set('parameter', parameter.value)
    url.searchParams.set('messdatum', messdatum.value)
    if (bundesland.value) {
    url.searchParams.set('bundesland', bundesland.value)
    }
    return url.toString()
  })

  const results = ref([])
  // Ergebnis-JSON von Flask holen
  async function fetchResults() {
    const response = await fetch(fundamentalurl.value)
    results.value = await response.json()

}


  return { parameter,parameterbezeichnung, einheit, messdatum, bundesland, fundamentalurl, results, fetchResults}
})
