<script setup>
import { ref } from 'vue'
import Dashboard from './components/Dashboard.vue'
import Practice from './components/Practice.vue'

const savedView = localStorage.getItem('typeit_current_view')
const savedDocId = localStorage.getItem('typeit_selected_doc_id')

const currentView = ref(savedView === 'practice' && savedDocId ? 'practice' : 'dashboard')
const selectedDocId = ref(savedView === 'practice' && savedDocId ? savedDocId : null)

const onDocSelect = (id) => {
  selectedDocId.value = id
  currentView.value = 'practice'
  localStorage.setItem('typeit_current_view', 'practice')
  localStorage.setItem('typeit_selected_doc_id', id)
}

const onBackToDashboard = () => {
  selectedDocId.value = null
  currentView.value = 'dashboard'
  localStorage.setItem('typeit_current_view', 'dashboard')
  localStorage.removeItem('typeit_selected_doc_id')
}
</script>

<template>
  <div class="app-wrapper">
    <Dashboard v-if="currentView === 'dashboard'" @select="onDocSelect" />
    <Practice v-else-if="currentView === 'practice'" :docId="selectedDocId" @back="onBackToDashboard" />
  </div>
</template>

<style>
.app-wrapper {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
</style>
