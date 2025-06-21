<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

// --- STATO ---
const candidates = ref([])
const isLoading = ref(true)
const error = ref(null)
const newCandidate = ref({ name: '', surname: '', title: '', status: 'Applied' })

// Stato per la modifica
const editingCandidateId = ref(null) 
const editingCandidateData = ref({})

// --- COSTANTE API ---
// Definiamo l'URL base dell'API una sola volta per pulizia e manutenibilità
const API_URL = 'http://127.0.0.1:8000/api/candidates/'

// --- FUNZIONI API ---

// Carica la lista iniziale di candidati
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

// Invia il form per creare un nuovo candidato
const handleSubmit = async () => {
  try {
    const response = await axios.post(API_URL, newCandidate.value)
    candidates.value.unshift(response.data)
    newCandidate.value = { name: '', surname: '', title: '', status: 'Applied' }
  } catch (err) {
    console.error('Errore nella creazione del candidato:', err)
  }
}

// Attiva la modalità di modifica per un candidato
const startEditing = (candidate) => {
  // CORREZIONE: Usiamo la 'I' maiuscola per 'Id'
  editingCandidateId.value = candidate.id
  editingCandidateData.value = { ...candidate }
}

// Annulla la modalità di modifica
const cancelEditing = () => {
  editingCandidateId.value = null
  editingCandidateData.value = {}
}

// Invia le modifiche al backend
const handleUpdate = async () => {
  if (!editingCandidateId.value) return
  try {
    const response = await axios.patch(`${API_URL}${editingCandidateId.value}/`, editingCandidateData.value)
    const index = candidates.value.findIndex(c => c.id === editingCandidateId.value)
    if (index !== -1) {
      candidates.value[index] = response.data
    }
    cancelEditing()
  } catch (err) {
    console.error('Errore nell\'aggiornamento del candidato:', err)
  }
}

// Cancella un candidato
const handleDelete = async (candidateId) => {
  if (!window.confirm('Sei sicuro di voler cancellare il candidato?')) {
    return
  }
  try {
    await axios.delete(`${API_URL}${candidateId}/`)
    candidates.value = candidates.value.filter(c => c.id !== candidateId)
  } catch (err) {
    console.error('Errore nella cancellazione del candidato:', err)
  }
}

// Hook del ciclo di vita: carica i dati quando il componente viene montato
onMounted(fetchCandidates)
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
          placeholder="Name"
          required
        />
        <input
          v-model="newCandidate.surname"
          type="text"
          placeholder="Surname"
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
        <button type="submit" class="save-btn">Add Candidate</button>
      </div>
    </form>

    <div v-if="isLoading">
      <p>Loading candidates...</p>
    </div>
    <div v-else-if="error">
      <p style="color: red;">{{ error }}</p>
    </div>

    <ul v-else>
      <li v-for="candidate in candidates" :key="candidate.id">
        
        <div v-if="editingCandidateId === candidate.id" class="editing-form">
          <input type="text" v-model="editingCandidateData.name" placeholder="Name" />
          <input type="text" v-model="editingCandidateData.surname" placeholder="Surname" />
          <input type="text" v-model="editingCandidateData.title" placeholder="Job Title" />
          <select v-model="editingCandidateData.status">
            <option>Applied</option>
            <option>Interview</option>
            <option>Hired</option>
            <option>Rejected</option>
          </select>
          <div class="actions">
            <button @click="handleUpdate" class="save-btn">Save</button>
            <button @click="cancelEditing" class="cancel-btn">Cancel</button>
          </div>
        </div>

        <div v-else class="display-view">
          <div class="candidate-info">
            <strong>{{ candidate.name }} {{ candidate.surname }}</strong>
            <span>{{ candidate.title }}</span>
            <span class="status-badge">Status: {{ candidate.status }}</span>
          </div>
          <div class="actions">
            <button @click="startEditing(candidate)" class="edit-btn">Edit</button>
            <button @click="handleDelete(candidate.id)" class="delete-btn">Delete</button>
          </div>
        </div>

      </li>
    </ul>
  </main>
</template>

<style scoped>
/* Stili Generali */
main {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  max-width: 900px;
  margin: 40px auto;
  padding: 20px;
  color: #333;
}

h1, h3 {
  color: #2c3e50;
  margin-top: 0;
}

/* Form di Creazione Principale */
.new-candidate-form {
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
  border: 1px solid #dee2e6;
}

.form-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
}

.form-row input,
.form-row select {
  padding: 10px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 1rem;
  flex: 1 1 150px; /* Flexbox per responsività */
}

/* Lista dei Candidati */
ul {
  list-style: none;
  padding: 0;
}

li {
  background-color: #ffffff;
  padding: 20px;
  margin-bottom: 10px;
  border-radius: 8px;
  border: 1px solid #e9ecef;
  transition: box-shadow 0.2s ease-in-out;
}

li:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

/* Contenitori interni al List Item */
.display-view,
.editing-form {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  gap: 15px;
}

.candidate-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex-grow: 1;
}

.candidate-info strong {
  font-size: 1.2em;
  color: #212529;
}

.candidate-info span {
  color: #6c757d;
}

.status-badge {
  background-color: #e9ecef;
  color: #495057;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 0.85em;
  font-weight: 500;
  align-self: flex-start;
}

/* Form di Modifica In Linea */
.editing-form input,
.editing-form select {
  padding: 8px;
  border: 1px solid #007bff;
  border-radius: 4px;
  flex: 1 1 120px;
}

/* Pulsanti */
.actions {
  display: flex;
  gap: 10px;
}

button {
  padding: 8px 16px;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s ease, transform 0.1s ease;
}

button:hover {
  transform: translateY(-1px);
}

.save-btn { background-color: #28a745; }
.save-btn:hover { background-color: #218838; }

.edit-btn { background-color: #007bff; }
.edit-btn:hover { background-color: #0056b3; }

.delete-btn { background-color: #dc3545; }
.delete-btn:hover { background-color: #c82333; }

.cancel-btn { background-color: #6c757d; }
.cancel-btn:hover { background-color: #5a6268; }
</style>