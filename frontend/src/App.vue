<script setup>
import { ref } from 'vue'
import Dashboard from './components/Dashboard.vue'
import Practice from './components/Practice.vue'

const currentView = ref('dashboard')
const selectedDocId = ref(null)

const onDocSelect = (id) => {
  selectedDocId.value = id
  currentView.value = 'practice'
}

const onBackToDashboard = () => {
  selectedDocId.value = null
  currentView.value = 'dashboard'
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
