import { ref } from 'vue'
import axios from 'axios'

export function useOperadoras(){
    const operadoras = ref([])
    const loading = ref(false)
    const error = ref(null)

    const searchOperadoras = async (term) => {
        loading.value = true
        error.value = null

        try {
            const response = await axios.get(`http://localhost:8080/api/operadoras?q=${term}`)
            operadoras.value = response.data.results
        } catch(err){
            error.value = err.response?.data?.detail || err.message
        } finally {
            loading.value = false
        }
    }

    return {operadoras, loading, error, searchOperadoras }
}