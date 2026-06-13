<template>
  <div class="dashboard">
    <header class="dash-header">
      <h1 class="logo">TypeIt.</h1>
      <p class="tagline">Type literary works to practice your 10-finger typing skills</p>
    </header>

    <div class="dash-content">
      <!-- Left sidebar: Upload and Quick info -->
      <aside class="sidebar">
        <div class="upload-section">
          <h3>Upload New Document</h3>
          <p class="upload-desc">Upload a personal text (.txt), Word (.docx), or PDF (.pdf) file to practice.</p>
          
          <form @submit.prevent="handleUpload" class="upload-form">
            <div class="file-dropzone" :class="{ 'dragover': isDragOver }"
                 @dragover.prevent="isDragOver = true"
                 @dragleave.prevent="isDragOver = false"
                 @drop.prevent="handleDrop">
              <input type="file" ref="fileInput" id="file" @change="handleFileChange" accept=".txt,.docx,.pdf" class="hidden-input" required />
              <label for="file" class="dropzone-label">
                <svg class="icon-svg icon-folder" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                  <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path>
                </svg>
                <span class="text" v-if="!selectedFile">Choose file or drag & drop here</span>
                <span class="text filename" v-else>{{ selectedFile.name }}</span>
                <span class="support">Supports .txt, .docx, .pdf</span>
              </label>
            </div>

            <div class="input-group" v-if="selectedFile">
              <label for="title">Title (Optional)</label>
              <input type="text" id="title" v-model="uploadTitle" placeholder="e.g. Sherlock Holmes" />
            </div>

            <div class="input-group" v-if="selectedFile">
              <label for="author">Author (Optional)</label>
              <input type="text" id="author" v-model="uploadAuthor" placeholder="e.g. Arthur Conan Doyle" />
            </div>

            <div class="actions">
              <button type="submit" class="btn btn-primary" :disabled="isUploading || !selectedFile">
                {{ isUploading ? 'Uploading...' : 'Upload & Start' }}
              </button>
              <button type="button" class="btn btn-secondary" v-if="selectedFile" @click="cancelUpload">
                Cancel
              </button>
            </div>
          </form>
          
          <p class="error-msg" v-if="uploadError">{{ uploadError }}</p>
        </div>

        <div class="keyboard-guide">
          <h3>Posture & Guide</h3>
          <ul>
            <li>Place your 8 fingers on the home row keys (ASDF - JKL;).</li>
            <li>Use both thumbs to press the Spacebar.</li>
            <li>Type at a relaxed pace, feeling the rhythm of the prose.</li>
            <li>Press <strong>Enter</strong> when you encounter the return symbol <strong>↵</strong>.</li>
          </ul>
        </div>
      </aside>

      <!-- Main section: List and filter -->
      <main class="main-content">
        <div class="filter-bar">
          <div class="search-box">
            <svg class="icon-svg search-icon-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
              <circle cx="11" cy="11" r="8"></circle>
              <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>
            <input type="text" v-model="searchQuery" placeholder="Search by title or author..." />
          </div>

          <div class="tabs">
            <button v-for="tab in tabs" :key="tab.value" 
                    class="tab-btn" 
                    :class="{ 'active': currentTab === tab.value }"
                    @click="currentTab = tab.value">
              {{ tab.label }}
            </button>
          </div>
        </div>

        <!-- Document List -->
        <div class="doc-list" v-if="filteredDocuments.length > 0">
          <div v-for="doc in filteredDocuments" :key="doc.id" class="doc-card" @click="$emit('select', doc.id)">
            <div class="doc-info">
              <div class="doc-title-row">
                <span class="doc-type-badge" :class="doc.type">{{ formatType(doc.type) }}</span>
                <h2 class="doc-title">{{ doc.title }}</h2>
              </div>
              <p class="doc-author">{{ doc.author || 'Unknown Author' }}</p>
              <div class="doc-meta">
                <span>{{ doc.word_count }} words</span>
                <span class="dot">•</span>
                <span>{{ doc.char_count }} chars</span>
              </div>
            </div>
            
            <div class="doc-actions" @click.stop>
              <!-- Bookmark toggle button -->
              <button class="action-btn bookmark-btn" 
                      :class="{ 'active': doc.bookmarked }"
                      @click="toggleBookmark(doc.id)"
                      title="Bookmark document">
                <svg class="icon-svg heart-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                  <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
                </svg>
              </button>
              <!-- Delete button if uploaded -->
              <button v-if="doc.type === 'uploaded'" 
                      class="action-btn delete-btn" 
                      @click="deleteDocument(doc.id)"
                      title="Delete document">
                <svg class="icon-svg trash-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                  <polyline points="3 6 5 6 21 6"></polyline>
                  <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                </svg>
              </button>
            </div>
          </div>
        </div>
        
        <div class="empty-state" v-else>
          <svg class="icon-svg icon-empty" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <path d="M18 8h1a4 4 0 0 1 0 8h-1"></path>
            <path d="M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V8z"></path>
            <line x1="6" y1="1" x2="6" y2="4"></line>
            <line x1="10" y1="1" x2="10" y2="4"></line>
            <line x1="14" y1="1" x2="14" y2="4"></line>
          </svg>
          <p>No matching documents found.</p>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const emit = defineEmits(['select'])

const documents = ref([])
const searchQuery = ref('')
const currentTab = ref('all')
const isDragOver = ref(false)
const selectedFile = ref(null)
const uploadTitle = ref('')
const uploadAuthor = ref('')
const isUploading = ref(false)
const uploadError = ref('')
const fileInput = ref(null)

const tabs = [
  { label: 'All', value: 'all' },
  { label: 'Novels', value: 'novel' },
  { label: 'Poems', value: 'poem' },
  { label: 'Essays', value: 'essay' },
  { label: 'Uploaded', value: 'uploaded' },
  { label: 'Bookmarked', value: 'bookmarked' }
]

// Fetch documents from backend
const fetchDocuments = async () => {
  try {
    const res = await fetch('/api/documents')
    if (res.ok) {
      documents.value = await res.json()
    }
  } catch (err) {
    console.error('Error loading documents list:', err)
  }
}

onMounted(() => {
  fetchDocuments()
})

// Filter documents based on tab and search query
const filteredDocuments = computed(() => {
  return documents.value.filter(doc => {
    // 1. Filter by search query
    const query = searchQuery.value.toLowerCase().trim()
    const matchesQuery = !query || 
      doc.title.toLowerCase().includes(query) || 
      (doc.author && doc.author.toLowerCase().includes(query))
      
    if (!matchesQuery) return false

    // 2. Filter by tab
    if (currentTab.value === 'all') return true
    if (currentTab.value === 'bookmarked') return doc.bookmarked
    return doc.type === currentTab.value
  })
})

const formatType = (type) => {
  switch (type) {
    case 'novel': return 'Novel'
    case 'poem': return 'Poem'
    case 'essay': return 'Essay'
    case 'uploaded': return 'Uploaded'
    default: return 'Other'
  }
}

// Bookmark handling
const toggleBookmark = async (id) => {
  try {
    const res = await fetch(`/api/documents/toggle-bookmark/${id}`, {
      method: 'POST'
    })
    if (res.ok) {
      const data = await res.json()
      const doc = documents.value.find(d => d.id === id)
      if (doc) {
        doc.bookmarked = data.bookmarked
      }
    }
  } catch (err) {
    console.error('Error bookmarking document:', err)
  }
}

// Delete document
const deleteDocument = async (id) => {
  if (!confirm('Are you sure you want to delete this document?')) return
  
  try {
    const res = await fetch(`/api/documents/${id}`, {
      method: 'DELETE'
    })
    if (res.ok) {
      documents.value = documents.value.filter(d => d.id !== id)
    } else {
      alert('Unable to delete the document.')
    }
  } catch (err) {
    console.error('Error deleting document:', err)
  }
}

// Upload handling
const handleFileChange = (e) => {
  const file = e.target.files[0]
  if (file) {
    selectFile(file)
  }
}

const handleDrop = (e) => {
  isDragOver.value = false
  const file = e.dataTransfer.files[0]
  if (file) {
    selectFile(file)
  }
}

const selectFile = (file) => {
  const ext = file.name.substring(file.name.lastIndexOf('.')).toLowerCase()
  if (!['.txt', '.docx', '.pdf'].includes(ext)) {
    uploadError.value = 'Only .txt, .docx, and .pdf files are supported.'
    selectedFile.value = null
    return
  }
  uploadError.value = ''
  selectedFile.value = file
  // Auto fill title from filename
  uploadTitle.value = file.name.substring(0, file.name.lastIndexOf('.'))
}

const cancelUpload = () => {
  selectedFile.value = null
  uploadTitle.value = ''
  uploadAuthor.value = ''
  uploadError.value = ''
  if (fileInput.value) fileInput.value.value = ''
}

const handleUpload = async () => {
  if (!selectedFile.value) return
  
  isUploading.value = true
  uploadError.value = ''
  
  const formData = new FormData()
  formData.append('file', selectedFile.value)
  if (uploadTitle.value) formData.append('title', uploadTitle.value)
  if (uploadAuthor.value) formData.append('author', uploadAuthor.value)
  
  try {
    const res = await fetch('/api/documents/upload', {
      method: 'POST',
      body: formData
    })
    
    if (res.ok) {
      const newDoc = await res.json()
      await fetchDocuments()
      cancelUpload()
      // Transition directly to typing practice
      emit('select', newDoc.id)
    } else {
      const errData = await res.json()
      uploadError.value = errData.detail || 'An error occurred while uploading the file.'
    }
  } catch (err) {
    uploadError.value = 'Cannot connect to the server.'
    console.error(err)
  } finally {
    isUploading.value = false
  }
}
</script>

<style scoped>
.dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.dash-header {
  margin-bottom: 40px;
  border-bottom: 1px solid var(--ui-border);
  padding-bottom: 20px;
}

.logo {
  font-family: var(--font-typing);
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--text-correct);
  margin-bottom: 5px;
}

.tagline {
  color: var(--ui-muted);
  font-size: 1rem;
}

.dash-content {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 40px;
}

@media (max-width: 768px) {
  .dash-content {
    grid-template-columns: 1fr;
  }
}

.sidebar {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.upload-section, .keyboard-guide {
  background-color: #FFFFFF;
  border: 1px solid var(--ui-border);
  padding: 24px;
  border-radius: 8px;
}

.upload-section h3, .keyboard-guide h3 {
  font-size: 1.1rem;
  margin-bottom: 12px;
  color: var(--text-correct);
  font-weight: 600;
}

.upload-desc {
  font-size: 0.85rem;
  color: var(--ui-muted);
  margin-bottom: 16px;
  line-height: 1.4;
}

.upload-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.file-dropzone {
  border: 2px dashed var(--ui-border);
  border-radius: 6px;
  padding: 20px 10px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s ease;
  background-color: var(--bg-color);
}

.file-dropzone:hover, .file-dropzone.dragover {
  border-color: var(--ui-primary);
  background-color: rgba(71, 85, 105, 0.05);
}

.hidden-input {
  display: none;
}

.dropzone-label {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  gap: 8px;
}

.dropzone-label .icon-folder {
  font-size: 1.6rem;
  color: var(--ui-muted);
  width: 2rem;
  height: 2rem;
}

.dropzone-label .text {
  font-size: 0.85rem;
  font-weight: 500;
  color: var(--ui-primary);
}

.dropzone-label .filename {
  font-weight: bold;
  word-break: break-all;
  color: var(--text-correct);
}

.dropzone-label .support {
  font-size: 0.75rem;
  color: var(--ui-muted);
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.input-group label {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--ui-primary);
}

.input-group input {
  padding: 8px 12px;
  font-size: 0.9rem;
  border: 1px solid var(--ui-border);
  border-radius: 4px;
  outline: none;
  background-color: var(--bg-color);
  font-family: inherit;
  transition: border-color 0.2s;
}

.input-group input:focus {
  border-color: var(--ui-primary);
}

.actions {
  display: flex;
  gap: 10px;
  margin-top: 5px;
}

.btn {
  flex: 1;
  padding: 10px;
  font-size: 0.9rem;
  font-weight: 600;
  border-radius: 4px;
  text-align: center;
  transition: background-color 0.2s;
}

.btn-primary {
  background-color: var(--ui-primary);
  color: #FFFFFF;
}

.btn-primary:hover:not(:disabled) {
  background-color: #334155;
}

.btn-primary:disabled {
  background-color: var(--ui-border);
  cursor: not-allowed;
}

.btn-secondary {
  background-color: transparent;
  color: var(--ui-primary);
  border: 1px solid var(--ui-border);
}

.btn-secondary:hover {
  background-color: var(--bg-color);
}

.error-msg {
  font-size: 0.8rem;
  color: #DC2626;
  margin-top: 10px;
}

.keyboard-guide ul {
  padding-left: 18px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  font-size: 0.85rem;
  color: var(--ui-primary);
  line-height: 1.5;
}

.keyboard-guide li strong {
  color: var(--text-correct);
}

/* Main content: list of documents */
.main-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.filter-bar {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

@media (min-width: 900px) {
  .filter-bar {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }
}

.search-box {
  display: flex;
  align-items: center;
  background-color: #FFFFFF;
  border: 1px solid var(--ui-border);
  border-radius: 6px;
  padding: 8px 16px;
  flex: 1;
  max-width: 400px;
}

.search-icon-svg {
  color: var(--ui-muted);
}

.search-box input {
  border: none;
  background: transparent;
  outline: none;
  font-family: inherit;
  font-size: 0.95rem;
  margin-left: 8px;
  width: 100%;
}

.tabs {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding-bottom: 4px;
}

.tab-btn {
  padding: 8px 14px;
  font-size: 0.85rem;
  font-weight: 500;
  color: var(--ui-primary);
  border: 1px solid transparent;
  border-radius: 20px;
  white-space: nowrap;
  background-color: transparent;
  transition: all 0.2s ease;
}

.tab-btn:hover {
  background-color: rgba(71, 85, 105, 0.08);
}

.tab-btn.active {
  background-color: var(--ui-primary);
  color: #FFFFFF;
}

.doc-list {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: 16px;
  grid-auto-rows: 1fr;
}

@media (min-width: 1000px) {
  .doc-list {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

.doc-card {
  background-color: #FFFFFF;
  border: 1px solid var(--ui-border);
  border-radius: 8px;
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: stretch;
  cursor: pointer;
  transition: transform 0.15s, border-color 0.15s;
  height: 100%;
  min-height: 125px;
  min-width: 0;
}

.doc-card:hover {
  transform: translateY(-2px);
  border-color: var(--ui-primary);
}

.doc-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1;
  min-width: 0;
}

.doc-title-row {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 0;
  width: 100%;
}

.doc-title {
  font-family: var(--font-typing);
  font-size: 1.15rem;
  font-weight: 600;
  color: var(--text-correct);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex: 1;
  min-width: 0;
}

.doc-type-badge {
  font-family: var(--font-sans);
  font-size: 0.65rem;
  font-weight: 700;
  text-transform: uppercase;
  padding: 2px 6px;
  border-radius: 4px;
  white-space: nowrap;
  flex-shrink: 0;
}

.doc-type-badge.novel {
  background-color: #DBEAFE;
  color: #1E40AF;
}

.doc-type-badge.poem {
  background-color: #FCE7F3;
  color: #9D174D;
}

.doc-type-badge.essay {
  background-color: #FEF3C7;
  color: #92400E;
}

.doc-type-badge.uploaded {
  background-color: #E2E8F0;
  color: #475569;
}

.doc-author {
  font-size: 0.9rem;
  color: var(--ui-primary);
}

.doc-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: var(--ui-muted);
  margin-top: auto;
  padding-top: 12px;
}

.dot {
  font-size: 0.5rem;
}

.doc-actions {
  display: flex;
  gap: 8px;
  margin-left: 12px;
  align-items: flex-start;
}

.action-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  color: var(--ui-muted);
  border: 1px solid var(--ui-border);
  transition: all 0.15s;
  background-color: transparent;
}

.action-btn:hover {
  background-color: var(--bg-color);
  color: var(--text-correct);
}

.bookmark-btn.active {
  color: #EF4444;
  border-color: #FCA5A5;
  background-color: #FEF2F2;
}

.bookmark-btn.active .heart-icon {
  fill: #EF4444;
  stroke: #EF4444;
}

.delete-btn:hover {
  color: #DC2626;
  border-color: #FCA5A5;
  background-color: #FEF2F2;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  background-color: #FFFFFF;
  border: 1px solid var(--ui-border);
  border-radius: 8px;
  color: var(--ui-muted);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.icon-empty {
  font-size: 2.5rem;
  width: 3rem;
  height: 3rem;
  color: var(--ui-muted);
}
</style>
