<template>
  <div class="operadoras-search">
    <div class="header">
      <h1>Consulta de Operadoras Médicas</h1>
      <p class="subtitle">Encontre informações sobre operadoras de saúde no Brasil</p>
    </div>

    <div class="search-container">
      <div class="search-box">
        <div class="search-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#0077cc" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
        </div>
        <input
          v-model="searchTerm"
          @input="handleSearch"
          placeholder="Busque por nome, CNPJ ou razão social..."
          class="search-input"
        />
        <button @click="handleSearch" class="search-button">
          <span>Buscar</span>
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="5" y1="12" x2="19" y2="12"></line>
            <polyline points="12 5 19 12 12 19"></polyline>
          </svg>
        </button>
      </div>
    </div>

    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Carregando informações...</p>
    </div>
    
    <div v-else-if="error" class="error-state">
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#d32f2f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"></circle>
        <line x1="12" y1="8" x2="12" y2="12"></line>
        <line x1="12" y1="16" x2="12.01" y2="16"></line>
      </svg>
      <p>{{ error }}</p>
    </div>

    <div v-if="operadoras.length" class="results-container">
      <div class="results-header">
        <h2>{{ operadoras.length }} operadoras encontradas</h2>
      </div>

      <div class="table-container">
        <table class="results-table">
          <thead>
            <tr>
              <th v-for="header in headers" :key="header.key" @click="sortBy(header.key)" :class="{ active: sortKey === header.key }">
                {{ header.label }}
                <span v-if="sortKey === header.key" class="sort-icon">
                  {{ sortOrder === 'asc' ? '↑' : '↓' }}
                </span>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="op in sortedOperadoras" :key="op.Registro_ANS" @click="selectOperadora(op)" :class="{ selected: selectedOperadora === op }">
              <td>{{ op.Registro_ANS }}</td>
              <td>{{ op.Razao_Social }}</td>
              <td>{{ op.Nome_Fantasia }}</td>
              <td>{{ formatCNPJ(op.CNPJ) }}</td>
              <td>
                <span class="uf-badge">{{ op.UF }}</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <div v-if="selectedOperadora" class="details-panel">
        <h3>Detalhes da Operadora</h3>
        <div class="details-grid">
          <div v-for="(value, key) in selectedOperadora" :key="key" class="detail-item">
            <span class="detail-label">{{ formatLabel(key) }}:</span>
            <span class="detail-value">{{ value || 'N/A' }}</span>
          </div>
        </div>
      </div>
    </div>
    
    <div v-else-if="searchTerm && !loading" class="empty-state">
      <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#0077cc" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"></circle>
        <line x1="12" y1="8" x2="12" y2="12"></line>
        <line x1="12" y1="16" x2="12.01" y2="16"></line>
      </svg>
      <h3>Nenhuma operadora encontrada para "{{ searchTerm }}"</h3>
      <p>Tente ajustar sua busca ou verificar a ortografia</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useOperadoras } from '../composables/useOperadoras'

const searchTerm = ref('')
const { operadoras, loading, error, searchOperadoras } = useOperadoras()
const selectedOperadora = ref(null)
const sortKey = ref('Razao_Social')
const sortOrder = ref('asc')

const headers = [
  { key: 'Registro_ANS', label: 'Registro ANS' },
  { key: 'Razao_Social', label: 'Razão Social' },
  { key: 'Nome_Fantasia', label: 'Nome Fantasia' },
  { key: 'CNPJ', label: 'CNPJ' },
  { key: 'UF', label: 'UF' }
]

const sortedOperadoras = computed(() => {
  return [...operadoras.value].sort((a, b) => {
    let modifier = 1
    if (sortOrder.value === 'desc') modifier = -1
    
    if (a[sortKey.value] < b[sortKey.value]) return -1 * modifier
    if (a[sortKey.value] > b[sortKey.value]) return 1 * modifier
    return 0
  })
})

const handleSearch = () => {
  if(searchTerm.value.length > 1 || searchTerm.value.length === 0) {
    selectedOperadora.value = null
    searchOperadoras(searchTerm.value)
  }
}

const selectOperadora = (op) => {
  selectedOperadora.value = op
}

const sortBy = (key) => {
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortKey.value = key
    sortOrder.value = 'asc'
  }
}

const formatCNPJ = (cnpj) => {
  if (!cnpj) return 'N/A'
  return cnpj.toString().replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, '$1.$2.$3/$4-$5')
}

const formatLabel = (key) => {
  return key
    .replace(/_/g, ' ')
    .replace(/\b\w/g, l => l.toUpperCase())
}
</script>

<style scoped>
.operadoras-search {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
  font-family: 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', sans-serif;
  color: #333;
}

.header {
  text-align: center;
  margin-bottom: 2rem;
}

.header h1 {
  color: #0077cc;
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #666;
  font-size: 1.1rem;
}

.search-container {
  background-color: #f8fafc;
  border-radius: 10px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 8px rgba(0, 119, 204, 0.1);
}

.search-box {
  display: flex;
  align-items: center;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.search-icon {
  padding: 0 1rem;
  display: flex;
  align-items: center;
}

.search-input {
  flex: 1;
  padding: 0.9rem 0;
  font-size: 1rem;
  border: none;
  outline: none;
}

.search-input::placeholder {
  color: #9ca3af;
}

.search-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.9rem 1.5rem;
  background-color: #0077cc;
  color: white;
  border: none;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.search-button:hover {
  background-color: #006bb3;
}

.loading-state, .error-state, .empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 1rem;
  text-align: center;
}

.loading-state {
  color: #0077cc;
}

.error-state {
  color: #d32f2f;
}

.spinner {
  border: 3px solid rgba(0, 119, 204, 0.2);
  border-radius: 50%;
  border-top: 3px solid #0077cc;
  width: 30px;
  height: 30px;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.results-container {
  background: white;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.2rem 1.5rem;
  background-color: #f8fafc;
  border-bottom: 1px solid #e5e7eb;
}

.results-header h2 {
  font-size: 1.2rem;
  color: #0077cc;
  margin: 0;
}

.export-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  color: #0077cc;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.export-button:hover {
  background-color: #f0f7ff;
}

.table-container {
  overflow-x: auto;
}

.results-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.95rem;
}

.results-table th {
  background-color: #f8fafc;
  color: #0077cc;
  font-weight: 600;
  text-align: left;
  padding: 1rem 1.5rem;
  position: sticky;
  top: 0;
  cursor: pointer;
  user-select: none;
}

.results-table th.active {
  background-color: #e6f2ff;
}

.results-table th:hover {
  background-color: #f0f7ff;
}

.sort-icon {
  margin-left: 0.3rem;
}

.results-table td {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.results-table tr:last-child td {
  border-bottom: none;
}

.results-table tr:hover {
  background-color: #f8fafc;
}

.results-table tr.selected {
  background-color: #e6f2ff;
}

.uf-badge {
  display: inline-block;
  padding: 0.2rem 0.5rem;
  background-color: #e6f2ff;
  color: #0077cc;
  border-radius: 4px;
  font-weight: 500;
  font-size: 0.85rem;
}

.details-panel {
  background-color: #f8fafc;
  padding: 1.5rem;
  border-top: 1px solid #e5e7eb;
}

.details-panel h3 {
  color: #0077cc;
  margin-top: 0;
  margin-bottom: 1rem;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
}

.detail-item {
  display: flex;
  flex-direction: column;
}

.detail-label {
  font-weight: 500;
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 0.2rem;
}

.detail-value {
  color: #333;
  font-size: 0.95rem;
}

.empty-state svg {
  margin-bottom: 1rem;
}

.empty-state h3 {
  color: #0077cc;
  margin-bottom: 0.5rem;
}

.empty-state p {
  color: #666;
  margin: 0;
}

@media (max-width: 768px) {
  .operadoras-search {
    padding: 1.5rem 1rem;
  }
  
  .search-box {
    flex-direction: column;
  }
  
  .search-input {
    width: 100%;
    padding: 0.9rem 1rem;
  }
  
  .search-button {
    width: 100%;
    justify-content: center;
  }
  
  .details-grid {
    grid-template-columns: 1fr;
  }
}
</style>