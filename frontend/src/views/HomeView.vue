<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

// Creiamo una variabile reattiva per contenere la nostra lista di candidati.
// 'ref' la rende "osservabile" da Vue, che aggiornerà il template quando cambia.
const candidates = ref([])
const isLoading = ref(true)
const error = ref(null)

// onMounted è un "lifecycle hook" di Vue. Il codice al suo interno
// viene eseguito non appena il componente è stato montato nel DOM.
// È il posto perfetto per caricare dati iniziali.
onMounted(async () => {
  try {
    // Usiamo axios per fare una richiesta GET al nostro endpoint Django.
    // NOTA: Usiamo l'URL completo del server Django.
    const response = await axios.get('http://127.0.0.1:8000/api/candidates/')
    
    // Se la richiesta ha successo, aggiorniamo la nostra variabile reattiva.
    candidates.value = response.data
  } catch (err) {
    // Se c'è un errore, lo salviamo per poterlo mostrare all'utente.
    console.error('Errore nel caricamento dei dati:', err)
    error.value = 'Impossibile caricare i dati dei candidati.'
  } finally {
    // In ogni caso (successo o errore), smettiamo di mostrare il "loading".
    isLoading.value = false
  }
})
</script>

<template>
  <main>
    <h1>Talent Tracker</h1>
    
    <div v-if="isLoading">
      <p>Caricamento in corso...</p>
    </div>
    
    <div v-else-if="error">
      <p style="color: red;">{{ error }}</p>
    </div>
    
    <ul v-else>
      <li v-for="candidate in candidates" :key="candidate.id">
        <strong>{{ candidate.name }}</strong> - {{ candidate.title }}
      </li>
    </ul>
  </main>
</template>

<style scoped>
ul {
  list-style: none;
  padding: 0;
}
li {
  background-color: #0c2daf;
  padding: 10px;
  margin-bottom: 5px;
  border-radius: 5px;
}
</style>