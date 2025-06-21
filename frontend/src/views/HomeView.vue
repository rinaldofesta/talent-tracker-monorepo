<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

// --- STATO ESISTENTE ---
const candidates = ref([])
const isLoading = ref(true)
const error = ref(null)

// --- NUOVO STATO PER IL FORM ---
// Usiamo un oggetto reattivo per tenere traccia dei dati del nuovo candidato.
// I valori iniziali saranno quelli di default del form.
const newCandidate = ref({
  name: '',
  surname: '',
  title: '',
  status: 'Applied' // Valore di default per il menu a tendina
})

// Definiamo la costante API una volta sola
const API_URL = 'http://127.0.0.1:8000/api/candidates/'

// Funzione per caricare i dati iniziali
const fetchCandidates = async () => {
  isLoading.value = true
  try {
    const response = await axios.get(API_URL)
    candidates.value = response.data
  } catch (err) {
    console.error('Errore nel caricamento dei dati:', err)
    error.value = 'Impossibile caricare i dati dei candidati.'
  } finally {
    isLoading.value = false
  }
}

// onMounted ora chiama la nostra funzione per caricare i dati
onMounted(fetchCandidates)

// Funzione per gestire invio dei form
const handleSubmit = async () => {
  try {
    // Usiamo axios.post per inviare i dati del form al nostro backend.
    // newCandidate.value contiene i dati inseriti dall'utente grazie a v-model.
    const response = await axios.post(API_URL, newCandidate.value)
    
    // Per una UI reattiva, aggiungiamo il nuovo candidato (restituito dal backend)
    // in cima alla nostra lista locale, senza dover ricaricare tutto.
    candidates.value.unshift(response.data)
    
    // Svuotiamo il form per prepararlo a un nuovo inserimento.
    newCandidate.value = { name: '', surname: '', title: '', status: 'Applied' }
  } catch (err) {
    console.error('Errore nella creazione del candidato:', err)
    // Qui potremmo mostrare un errore all'utente
  }
}

// Funzione per gestire la cancellazione dei candidati
const handleDelete = async (candidateId) => {
  // Chiediamo conferma per la cancellazione
  if (!window.confirm('Sei sicuro di voler cancellare il candidato?')){
    return // Se l'utente clicca "Annulla", non fare nulla
  }
  try {
    // Invia una richiesta DELETE all'URL specifico del candidato.
    // Usiamo i template literal (`) per costruire l'URL dinamicamente.
    await axios.delete(`${API_URL}${candidateId}/`)
    
    // Se la cancellazione ha successo, aggiorniamo la nostra lista locale
    // filtrando e rimuovendo il candidato con l'ID corrispondente.
    // Questo aggiorna la UI istantaneamente senza ricaricare la pagina.
    candidates.value = candidates.value.filter(c => c.id !== candidateId)
  } catch (err) {
    console.error('Errore nella cancellazione del candidato:', err)
  }
}
</script>

<template>
  <main>
    <h1>Talent Tracker</h1>

    <form @submit.prevent="handleSubmit" class="new-candidate-form">
      <h3>Add New Candidate</h3>
      <div class="form-row">
        <input
          v-model="newCandidate.name"
          type="text"
          placeholder="Candidate Name"
          required
        />
        <input
          v-model="newCandidate.surname"
          type="text"
          placeholder="Candidate Surname"
          required
        />
        <input
          v-model="newCandidate.title"
          type="text"
          placeholder="Job Title"
          required
        />
        <select v-model="newCandidate.status">
          <option>Applied</option>
          <option>Interview</option>
          <option>Hired</option>
          <option>Rejected</option>
        </select>
        <button type="submit">Add Candidate</button>
      </div>
    </form>

    <div v-if="isLoading">
      <p>Caricamento in corso...</p>
    </div>
    <div v-else-if="error">
      <p style="color: red;">{{ error }}</p>
    </div>
    <ul v-else>
      <li v-for="candidate in candidates" :key="candidate.id">
        <div>
        <strong>{{ candidate.name }} {{ candidate.surname }} </strong> - {{ candidate.title }}
        <span>Status: {{ candidate.status }}</span>
        </div>
        <button @click="handleDelete(candidate.id)" class="delete-btn">
          Delete
        </button>
      </li>
    </ul>
  </main>
</template>

<style scoped>

.new-candidate-form {
  background-color: #180497;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}
.form-row {
  display: flex;
  gap: 10px;
  align-items: center;
}
.form-row input, .form-row select {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.form-row button {
  padding: 8px 15px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.form-row button:hover {
  background-color: #218838;
}

ul {
  list-style: none;
  padding: 0;
}
li {
  background-color: #180497;
  padding: 10px 15px;
  margin-bottom: 8px;
  border-radius: 5px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
li span {
  background-color: #0d7756;
  padding: 3px 8px;
  border-radius: 12px;
  font-size: 0.9em;
}

.delete-btn {
  padding: 5px 10px;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9em;
}
.delete-btn:hover {
  background-color: #c82333;
}
li {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

</style>