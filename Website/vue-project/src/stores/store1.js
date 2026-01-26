// stores/store1.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useStore1 = defineStore('store1', () => {
  const parameter = ref('txk')
  const messdatum = ref('2024-12-31')

  const einheit = computed(() => {
    switch (parameter.value) {
      case 'txk':
      case 'tnk': return '°C'
      case 'fx': return 'm/s'
      case 'rsk': return 'mm'
      default: return ''
    }
  })


  return { parameter, einheit}
})
