<template>
  <div class="practice-container" v-if="document">
    <!-- Top Nav Bar -->
    <header class="practice-header">
      <div class="header-left">
        <button class="back-btn" @click="goBack">
          ← Back
        </button>
        <div class="doc-meta-info">
          <h2 class="doc-title">{{ document.title }}</h2>
          <div class="meta-sub">
            <span class="author">{{ document.author || 'Unknown Author' }}</span>
            <span class="dot">•</span>
            <span class="stats-text">{{ document.word_count }} words</span>
            <span class="dot">•</span>
            <span class="stats-text">{{ document.char_count }} chars</span>
            <button class="bookmark-btn" 
                    :class="{ 'active': document.bookmarked }"
                    @click="toggleBookmark">
              <svg class="icon-svg heart-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
              </svg>
              <span>{{ document.bookmarked ? 'Bookmarked' : 'Bookmark' }}</span>
            </button>
          </div>
        </div>
      </div>

      <div class="header-right">
        <!-- Live Stats -->
        <div class="live-stats">
          <div class="stat-item">
            <span class="stat-label">Time</span>
            <span class="stat-value font-mono">{{ formatTime(elapsedSeconds) }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Speed (WPM)</span>
            <span class="stat-value font-mono">{{ wpm }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Accuracy</span>
            <span class="stat-value font-mono">{{ accuracy }}%</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Progress</span>
            <span class="stat-value font-mono">{{ progress }}%</span>
          </div>
        </div>

        <div class="nav-actions">
          <button class="nav-action-btn" @click="restartPractice" title="Restart">
            <svg class="icon-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
              <path d="M23 4v6h-6"></path>
              <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"></path>
            </svg>
          </button>
          <button class="nav-action-btn" @click="showSettings = !showSettings" title="Settings">
            <svg class="icon-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
              <circle cx="12" cy="12" r="3"></circle>
              <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
            </svg>
          </button>
        </div>
      </div>
    </header>

    <!-- Settings Pane (Dropdown) -->
    <div class="settings-dropdown" v-if="showSettings">
      <div class="settings-title">Text Settings</div>
      
      <div class="setting-item">
        <label>Font Family</label>
        <div class="font-selector">
          <button v-for="font in availableFonts" :key="font"
                  :class="{ 'active': selectedFont === font }"
                  :style="{ fontFamily: font }"
                  @click="selectedFont = font">
            {{ font }}
          </button>
        </div>
      </div>

      <div class="setting-item">
        <label>Font Size: {{ fontSize }}px</label>
        <input type="range" min="18" max="30" step="1" v-model.number="fontSize" />
      </div>

      <div class="setting-item">
        <label>Line Height: {{ lineHeight }}</label>
        <input type="range" min="1.6" max="2.2" step="0.1" v-model.number="lineHeight" />
      </div>

      <div class="setting-item">
        <label class="checkbox-label">
          <input type="checkbox" v-model="enableSound" />
          <span>Sound Effects</span>
        </label>
      </div>

      <div class="setting-item" v-if="enableSound">
        <label class="checkbox-label">
          <input type="checkbox" v-model="enableErrorSound" />
          <span>Play Error Sound</span>
        </label>
      </div>

      <div class="setting-item" v-if="enableSound">
        <label>Sound Profile</label>
        <div class="sound-selector">
          <button v-for="p in soundProfiles" :key="p.value"
                  :class="{ 'active': selectedSoundProfile === p.value }"
                  @click="changeSoundProfile(p.value)">
            {{ p.label }}
          </button>
        </div>
      </div>
      
      <button class="close-settings-btn" @click="showSettings = false">Done</button>
    </div>

    <!-- Center Area (Typing Zone) -->
    <div class="typing-zone" @click="focusTyping">
      <!-- Hidden textarea to capture text input including Vietnamese IME -->
      <textarea
        ref="hiddenInput"
        class="hidden-typing-input"
        @input="handleInput"
        @keydown="handleSpecialKeys"
        @blur="isFocused = false"
        @focus="isFocused = true"
        :value="inputValue"
        autocomplete="off"
        autocorrect="off"
        autocapitalize="off"
        spellcheck="false"
      ></textarea>

      <div class="typing-content-wrapper" 
           :style="wrapperStyle"
           ref="scrollContainer">
        <!-- We prompt focus if the user loses it -->
        <div class="focus-overlay" v-if="!isFocused && !showResults" @click="focusTyping">
          <div class="focus-prompt">Click here to resume typing</div>
        </div>

        <div class="typing-text-flow" 
             :style="textFlowStyle"
             ref="textFlow">
          <span v-for="(charObj, idx) in chars" 
                :key="idx"
                :class="getCharClass(charObj, idx)"
                :id="'char-' + idx">
            {{ getDisplayChar(charObj.char) }}
          </span>
        </div>
      </div>
    </div>

    <!-- Results Modal (Popup) -->
    <div class="modal-backdrop" v-if="showResults">
      <div class="results-modal">
        <h2>Practice Results</h2>
        <p class="doc-title-result">« {{ document.title }} »</p>

        <div class="results-grid">
          <div class="result-card">
            <span class="result-val font-mono">{{ wpm }}</span>
            <span class="result-lbl">Words/Min (WPM)</span>
          </div>
          <div class="result-card">
            <span class="result-val font-mono">{{ accuracy }}%</span>
            <span class="result-lbl">Accuracy</span>
          </div>
          <div class="result-card">
            <span class="result-val font-mono">{{ formatTime(elapsedSeconds) }}</span>
            <span class="result-lbl">Time Elapsed</span>
          </div>
          <div class="result-card">
            <span class="result-val font-mono">{{ errorCount }}</span>
            <span class="result-lbl">Key Errors</span>
          </div>
        </div>

        <div class="result-feedback">
          <p v-if="wpm >= 60">Incredible typing speed! You type like a professional writer.</p>
          <p v-else-if="wpm >= 40">Good speed! Keep practicing to achieve even higher WPM.</p>
          <p v-else>Focus on accuracy first; speed will naturally follow with practice.</p>
        </div>

        <div class="modal-actions">
          <button class="btn btn-primary" @click="restartPractice">Restart Document</button>
          <button class="btn btn-secondary" @click="goBack">Choose Another</button>
        </div>
      </div>
    </div>
  </div>
  <div class="loading-state" v-else>
    <span>Loading document...</span>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'

const props = defineProps({
  docId: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['back'])

const document = ref(null)
const chars = ref([])
const currentIndex = ref(0)
const startTime = ref(null)
const elapsedSeconds = ref(0)
const timerInterval = ref(null)
const typedCharCount = ref(0)
const errorCount = ref(0)
const showResults = ref(false)
const showSettings = ref(false)
const isFocused = ref(true)

// Settings state
const selectedFont = ref('Lora')
const fontSize = ref(22)
const lineHeight = ref(1.9)
const scrollContainer = ref(null)
const hiddenInput = ref(null)
const inputValue = ref('')
const scrollTranslateY = ref(0)
const lastLineOffsetTop = ref(-1)
const lineH = computed(() => fontSize.value * lineHeight.value)
const wrapperStyle = computed(() => ({
  height: (4 * lineH.value) + 'px',
  overflow: 'hidden',
  position: 'relative'
}))
const textFlowStyle = computed(() => ({
  fontFamily: selectedFont.value,
  fontSize: fontSize.value + 'px',
  lineHeight: lineHeight.value,
  transform: `translateY(${scrollTranslateY.value}px)`,
  transition: 'transform 0.25s ease-out',
  position: 'relative'
}))

watch([fontSize, lineHeight], () => {
  nextTick(() => {
    autoScroll()
  })
})
const enableSound = ref(localStorage.getItem('typeit_sound') !== 'false')
const enableErrorSound = ref(localStorage.getItem('typeit_error_sound') !== 'false')
const selectedSoundProfile = ref(localStorage.getItem('typeit_sound_profile') || 'mechanical')

const availableFonts = ['Lora', 'Merriweather', 'Crimson Pro', 'Literata']
const soundProfiles = [
  { label: 'Mechanical Tactile', value: 'mechanical' },
  { label: 'Clicky Blue Switch', value: 'clicky_blue' },
  { label: 'Linear Red Thock', value: 'linear_red' },
  { label: 'Laptop Chiclet', value: 'laptop' },
  { label: 'Vintage Typewriter', value: 'typewriter' },
  { label: 'Wood Block', value: 'wooden' },
  { label: 'Digital Beep', value: 'digital' }
]

watch(enableSound, (newVal) => {
  localStorage.setItem('typeit_sound', String(newVal))
})

watch(enableErrorSound, (newVal) => {
  localStorage.setItem('typeit_error_sound', String(newVal))
})

watch(selectedSoundProfile, (newVal) => {
  localStorage.setItem('typeit_sound_profile', newVal)
})

const changeSoundProfile = (value) => {
  selectedSoundProfile.value = value
  playClickSound(true)
}

const playClickSound = (isCorrect) => {
  if (!enableSound.value) return
  if (!isCorrect && !enableErrorSound.value) return
  try {
    const AudioContext = window.AudioContext || window.webkitAudioContext
    if (!AudioContext) return
    if (!window.audioCtx) {
      window.audioCtx = new AudioContext()
    }
    const ctx = window.audioCtx
    if (ctx.state === 'suspended') {
      ctx.resume()
    }
    
    const now = ctx.currentTime
    const profile = selectedSoundProfile.value
    
    if (isCorrect) {
      if (profile === 'mechanical') {
        // Crisp mechanical key press clack (tactile Brown switch)
        const osc1 = ctx.createOscillator()
        const gain1 = ctx.createGain()
        osc1.type = 'triangle'
        osc1.frequency.setValueAtTime(1200, now)
        osc1.frequency.exponentialRampToValueAtTime(600, now + 0.03)
        
        gain1.gain.setValueAtTime(0.08, now)
        gain1.gain.exponentialRampToValueAtTime(0.001, now + 0.03)
        
        osc1.connect(gain1)
        gain1.connect(ctx.destination)
        osc1.start(now)
        osc1.stop(now + 0.03)
        
        const osc2 = ctx.createOscillator()
        const gain2 = ctx.createGain()
        osc2.type = 'sine'
        osc2.frequency.setValueAtTime(300, now)
        osc2.frequency.exponentialRampToValueAtTime(100, now + 0.04)
        
        gain2.gain.setValueAtTime(0.12, now)
        gain2.gain.exponentialRampToValueAtTime(0.001, now + 0.04)
        
        osc2.connect(gain2)
        gain2.connect(ctx.destination)
        osc2.start(now)
        osc2.stop(now + 0.04)
      } else if (profile === 'clicky_blue') {
        // Sharp metallic snap (MX Blue switch click)
        const osc1 = ctx.createOscillator()
        const gain1 = ctx.createGain()
        osc1.type = 'sine'
        osc1.frequency.setValueAtTime(2500, now)
        osc1.frequency.exponentialRampToValueAtTime(1200, now + 0.01)
        
        gain1.gain.setValueAtTime(0.08, now)
        gain1.gain.exponentialRampToValueAtTime(0.001, now + 0.015)
        
        osc1.connect(gain1)
        gain1.connect(ctx.destination)
        osc1.start(now)
        osc1.stop(now + 0.015)
        
        const osc2 = ctx.createOscillator()
        const gain2 = ctx.createGain()
        osc2.type = 'triangle'
        osc2.frequency.setValueAtTime(700, now)
        osc2.frequency.exponentialRampToValueAtTime(300, now + 0.025)
        
        gain2.gain.setValueAtTime(0.06, now)
        gain2.gain.exponentialRampToValueAtTime(0.001, now + 0.025)
        
        osc2.connect(gain2)
        gain2.connect(ctx.destination)
        osc2.start(now)
        osc2.stop(now + 0.025)
      } else if (profile === 'linear_red') {
        // Deep thocky switch (lubed MX Cream/Red switch)
        const osc1 = ctx.createOscillator()
        const gain1 = ctx.createGain()
        osc1.type = 'sine'
        osc1.frequency.setValueAtTime(280, now)
        osc1.frequency.exponentialRampToValueAtTime(120, now + 0.035)
        
        gain1.gain.setValueAtTime(0.18, now)
        gain1.gain.exponentialRampToValueAtTime(0.001, now + 0.035)
        
        osc1.connect(gain1)
        gain1.connect(ctx.destination)
        osc1.start(now)
        osc1.stop(now + 0.035)
        
        const osc2 = ctx.createOscillator()
        const gain2 = ctx.createGain()
        osc2.type = 'triangle'
        osc2.frequency.setValueAtTime(160, now)
        osc2.frequency.exponentialRampToValueAtTime(70, now + 0.04)
        
        gain2.gain.setValueAtTime(0.08, now)
        gain2.gain.exponentialRampToValueAtTime(0.001, now + 0.04)
        
        osc2.connect(gain2)
        gain2.connect(ctx.destination)
        osc2.start(now)
        osc2.stop(now + 0.04)
      } else if (profile === 'laptop') {
        // Short flat chiclet keyboard snip (modern MacBook-like snap)
        const osc = ctx.createOscillator()
        const gain = ctx.createGain()
        osc.type = 'triangle'
        osc.frequency.setValueAtTime(1600, now)
        osc.frequency.exponentialRampToValueAtTime(800, now + 0.012)
        
        gain.gain.setValueAtTime(0.05, now)
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.012)
        
        osc.connect(gain)
        gain.connect(ctx.destination)
        osc.start(now)
        osc.stop(now + 0.012)
      } else if (profile === 'typewriter') {
        // Sharp metallic typewriter key strike
        const osc1 = ctx.createOscillator()
        const gain1 = ctx.createGain()
        osc1.type = 'sine'
        osc1.frequency.setValueAtTime(2200, now)
        osc1.frequency.exponentialRampToValueAtTime(800, now + 0.02)
        
        gain1.gain.setValueAtTime(0.05, now)
        gain1.gain.exponentialRampToValueAtTime(0.001, now + 0.02)
        
        osc1.connect(gain1)
        gain1.connect(ctx.destination)
        osc1.start(now)
        osc1.stop(now + 0.02)
        
        const osc2 = ctx.createOscillator()
        const gain2 = ctx.createGain()
        osc2.type = 'triangle'
        osc2.frequency.setValueAtTime(600, now)
        osc2.frequency.exponentialRampToValueAtTime(150, now + 0.03)
        
        gain2.gain.setValueAtTime(0.08, now)
        gain2.gain.exponentialRampToValueAtTime(0.001, now + 0.03)
        
        osc2.connect(gain2)
        gain2.connect(ctx.destination)
        osc2.start(now)
        osc2.stop(now + 0.03)
      } else if (profile === 'wooden') {
        // Wood block "tock"
        const osc = ctx.createOscillator()
        const gain = ctx.createGain()
        osc.type = 'sine'
        osc.frequency.setValueAtTime(880, now)
        osc.frequency.exponentialRampToValueAtTime(440, now + 0.04)
        
        gain.gain.setValueAtTime(0.18, now)
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.04)
        
        osc.connect(gain)
        gain.connect(ctx.destination)
        osc.start(now)
        osc.stop(now + 0.04)
      } else if (profile === 'digital') {
        // Clean high digital beep
        const osc = ctx.createOscillator()
        const gain = ctx.createGain()
        osc.type = 'sine'
        osc.frequency.setValueAtTime(1500, now)
        
        gain.gain.setValueAtTime(0.06, now)
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.03)
        
        osc.connect(gain)
        gain.connect(ctx.destination)
        osc.start(now)
        osc.stop(now + 0.03)
      }
    } else {
      // Custom error thuds depending on profile type
      if (profile === 'mechanical' || profile === 'clicky_blue') {
        const osc = ctx.createOscillator()
        const gain = ctx.createGain()
        osc.type = 'sawtooth'
        osc.frequency.setValueAtTime(130, now)
        osc.frequency.linearRampToValueAtTime(60, now + 0.12)
        
        gain.gain.setValueAtTime(0.15, now)
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.12)
        
        osc.connect(gain)
        gain.connect(ctx.destination)
        osc.start(now)
        osc.stop(now + 0.12)
      } else if (profile === 'linear_red') {
        // Deep thocky thud for linear switches
        const osc = ctx.createOscillator()
        const gain = ctx.createGain()
        osc.type = 'sine'
        osc.frequency.setValueAtTime(110, now)
        osc.frequency.exponentialRampToValueAtTime(40, now + 0.12)
        
        gain.gain.setValueAtTime(0.2, now)
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.12)
        
        osc.connect(gain)
        gain.connect(ctx.destination)
        osc.start(now)
        osc.stop(now + 0.12)
      } else if (profile === 'laptop') {
        // Quick flat thud for chiclets
        const osc = ctx.createOscillator()
        const gain = ctx.createGain()
        osc.type = 'triangle'
        osc.frequency.setValueAtTime(180, now)
        osc.frequency.linearRampToValueAtTime(90, now + 0.08)
        
        gain.gain.setValueAtTime(0.12, now)
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.08)
        
        osc.connect(gain)
        gain.connect(ctx.destination)
        osc.start(now)
        osc.stop(now + 0.08)
      } else if (profile === 'typewriter') {
        const osc = ctx.createOscillator()
        const gain = ctx.createGain()
        osc.type = 'sine'
        osc.frequency.setValueAtTime(880, now)
        osc.frequency.linearRampToValueAtTime(660, now + 0.15)
        
        gain.gain.setValueAtTime(0.12, now)
        gain.gain.linearRampToValueAtTime(0.12, now + 0.05)
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.15)
        
        osc.connect(gain)
        gain.connect(ctx.destination)
        osc.start(now)
        osc.stop(now + 0.15)
      } else if (profile === 'wooden') {
        const osc = ctx.createOscillator()
        const gain = ctx.createGain()
        osc.type = 'square'
        osc.frequency.setValueAtTime(180, now)
        osc.frequency.exponentialRampToValueAtTime(50, now + 0.08)
        
        gain.gain.setValueAtTime(0.2, now)
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.08)
        
        osc.connect(gain)
        gain.connect(ctx.destination)
        osc.start(now)
        osc.stop(now + 0.08)
      } else if (profile === 'digital') {
        const osc = ctx.createOscillator()
        const gain = ctx.createGain()
        osc.type = 'square'
        osc.frequency.setValueAtTime(220, now)
        osc.frequency.linearRampToValueAtTime(110, now + 0.15)
        
        gain.gain.setValueAtTime(0.1, now)
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.15)
        
        osc.connect(gain)
        gain.connect(ctx.destination)
        osc.start(now)
        osc.stop(now + 0.15)
      }
    }
  } catch (err) {
    console.warn('Web Audio error:', err)
  }
}

const getCharClass = (charObj, idx) => {
  return {
    'char': true,
    'char-untyped': charObj.status === 'untyped' && idx > currentIndex.value,
    'char-correct': charObj.status === 'correct',
    'char-incorrect': charObj.status === 'incorrect',
    'char-current': idx === currentIndex.value,
    'char-space': charObj.char === ' ',
    'char-nl': charObj.char === '\n'
  }
}

const getDisplayChar = (char) => {
  if (char === '\n') {
    return '\n'
  }
  return char
}

// Format seconds into MM:SS
const formatTime = (seconds) => {
  const m = Math.floor(seconds / 60).toString().padStart(2, '0')
  const s = (seconds % 60).toString().padStart(2, '0')
  return `${m}:${s}`
}

// Fetch document on mount
const fetchDocument = async () => {
  try {
    const res = await fetch(`/api/documents/${props.docId}`)
    if (res.ok) {
      const doc = await res.json()
      document.value = doc
      
      // Parse characters
      chars.value = doc.content.split('').map(c => ({
        char: c,
        status: 'untyped'
      }))
      
      resetPracticeState()
      nextTick(() => {
        focusTyping()
      })
    } else {
      console.error('Document not found')
emit('back')
    }
  } catch (err) {
    console.error('Error loading document:', err)
    emit('back')
  }
}

const resetPracticeState = () => {
  if (timerInterval.value) {
    clearInterval(timerInterval.value)
    timerInterval.value = null
  }
  
  currentIndex.value = 0
  startTime.value = null
  elapsedSeconds.value = 0
  typedCharCount.value = 0
  errorCount.value = 0
  showResults.value = false
  isFocused.value = true
  inputValue.value = ''
  scrollTranslateY.value = 0
  lastLineOffsetTop.value = -1
  
  chars.value.forEach(c => c.status = 'untyped')
  
  nextTick(() => {
    autoScroll()
    if (scrollContainer.value) {
      scrollContainer.value.scrollTop = 0
    }
  })
}

const restartPractice = () => {
  resetPracticeState()
  focusTyping()
}

const goBack = () => {
  cleanup()
  emit('back')
}

const toggleBookmark = async () => {
  if (!document.value) return
  try {
    const res = await fetch(`/api/documents/toggle-bookmark/${document.value.id}`, {
      method: 'POST'
    })
    if (res.ok) {
      const data = await res.json()
      document.value.bookmarked = data.bookmarked
    }
  } catch (err) {
    console.error('Error bookmarking document:', err)
  }
}

// WPM: words per minute. Math.round((correct_characters / 5) / time_elapsed_in_minutes)
const wpm = computed(() => {
  if (elapsedSeconds.value === 0) return 0
  const correctCount = chars.value.filter(c => c.status === 'correct').length
  const minutes = elapsedSeconds.value / 60
  return Math.round((correctCount / 5) / minutes)
})

// Accuracy: (correct keypresses / total keypresses) * 100
const accuracy = computed(() => {
  if (typedCharCount.value === 0) return 100
  const accuracyVal = Math.round(((typedCharCount.value - errorCount.value) / typedCharCount.value) * 100)
  return Math.max(0, accuracyVal)
})

const progress = computed(() => {
  if (chars.value.length === 0) return 0
  return Math.round((currentIndex.value / chars.value.length) * 100)
})

// Keep the active typing line vertically centered in the container.
const autoScroll = () => {
  const activeSpan = window.document.getElementById(`char-${currentIndex.value}`)
  const container = scrollContainer.value
  if (!activeSpan || !container) return

  const spanTop = activeSpan.offsetTop

  // Keep the active line centered vertically.
  // We cap translation at 0 so we don't translate down at the start (Line 1 & 2).
  scrollTranslateY.value = Math.min(0, lineH.value - spanTop)
  lastLineOffsetTop.value = spanTop
}

const focusTyping = () => {
  isFocused.value = true
  nextTick(() => {
    if (hiddenInput.value) {
      hiddenInput.value.focus()
      hiddenInput.value.setSelectionRange(inputValue.value.length, inputValue.value.length)
    }
  })
}

// Helper to strip diacritics and normalize characters for IME precursor matching (e.g. o -> ô -> ố)
const getBaseChar = (char) => {
  if (!char) return ''
  return char
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/đ/g, "d")
    .replace(/Đ/g, "D")
}

let pendingDeletionTimeout = null

// Processes the final state after resolving any potential simulated backspaces from IMEs
const processInputState = (typedText, newIndex, isAdditionOrUpdate) => {
  const oldIndex = currentIndex.value
  
  // Compare characters dynamically
  for (let i = 0; i < chars.value.length; i++) {
    if (i < newIndex) {
      const targetChar = chars.value[i].char
      const typedChar = typedText[i]
      
      const isLastChar = i === newIndex - 1
      
      // If it's the last character (currently being typed/composed), we accept base character matches.
      // Otherwise, we require an exact match.
      let isCorrect = false
      if (isLastChar) {
        isCorrect = typedChar === targetChar || getBaseChar(typedChar) === getBaseChar(targetChar)
      } else {
        isCorrect = typedChar === targetChar
      }
      
      if (isCorrect) {
        chars.value[i].status = 'correct'
      } else {
        chars.value[i].status = 'incorrect'
      }
    } else {
      chars.value[i].status = 'untyped'
    }
  }

  // Handle sounds and stats
  if (isAdditionOrUpdate) {
    // Determine if it was a true addition or just an IME replacement update
    const isNewKey = newIndex > oldIndex
    
    if (isNewKey) {
      typedCharCount.value++
    }
    
    // Check correctness of the last character
    const replacedIdx = newIndex - 1
    if (replacedIdx >= 0) {
      const targetChar = chars.value[replacedIdx].char
      const typedChar = typedText[replacedIdx]
      const isCorrect = typedChar === targetChar || getBaseChar(typedChar) === getBaseChar(targetChar)
      
      if (isCorrect) {
        playClickSound(true)
      } else {
        if (isNewKey) {
          errorCount.value++
        }
        playClickSound(false)
      }
    }
  } else {
    // This is a true manual backspace (the 30ms timeout fired)
    playClickSound(true) // Play click sound for backspace
  }

  // Determine if the last character is currently under composition.
  // In Vietnamese, a character is under composition if it matches the target
  // character's base form but is not yet an exact match.
  let lastCharNeedsComposition = false
  if (newIndex > 0) {
    const lastIdx = newIndex - 1
    const targetChar = chars.value[lastIdx].char
    const typedChar = typedText[lastIdx]
    if (typedChar !== targetChar && getBaseChar(typedChar) === getBaseChar(targetChar)) {
      lastCharNeedsComposition = true
    }
  }

  currentIndex.value = lastCharNeedsComposition ? newIndex - 1 : newIndex
  nextTick(autoScroll)

  // Check end of document
  if (currentIndex.value >= chars.value.length) {
    if (timerInterval.value) {
      clearInterval(timerInterval.value)
    }
    showResults.value = true
  }
}

// Captures typing inputs including Vietnamese diacritics / IME composition
const handleInput = (e) => {
  if (showResults.value) return

  // Read raw value directly from the DOM to bypass Vue's composition lock
  const typedText = e.target.value
  inputValue.value = typedText

  // Start timer on first keystroke
  if (startTime.value === null) {
    startTime.value = Date.now()
    timerInterval.value = setInterval(() => {
      elapsedSeconds.value++
    }, 1000)
  }

  const typedLength = typedText.length
  const newIndex = Math.min(typedLength, chars.value.length)
  
  const isAddition = newIndex > currentIndex.value
  const isDeletion = newIndex < currentIndex.value

  // Defer backspace processing to filter out simulated backspaces from third-party IMEs (Telex)
  if (isDeletion) {
    if (pendingDeletionTimeout) {
      clearTimeout(pendingDeletionTimeout)
    }
    pendingDeletionTimeout = setTimeout(() => {
      processInputState(typedText, newIndex, false)
      pendingDeletionTimeout = null
    }, 30) // 30ms is enough to catch simulated key sequences from IMEs (like UniKey or EVKey)
  } else {
    // If it's an addition or update, cancel any pending deletion and process immediately
    if (pendingDeletionTimeout) {
      clearTimeout(pendingDeletionTimeout)
      pendingDeletionTimeout = null
    }
    processInputState(typedText, newIndex, true)
  }
}

// Disables arrow keys and other commands that shift focus inside the input
const handleSpecialKeys = (e) => {
  if (
    e.key === 'ArrowLeft' || 
    e.key === 'ArrowRight' || 
    e.key === 'ArrowUp' || 
    e.key === 'ArrowDown' || 
    e.key === 'Home' || 
    e.key === 'End' || 
    e.key === 'PageUp' || 
    e.key === 'PageDown'
  ) {
    e.preventDefault()
  }
}

const handleGlobalKeydown = (e) => {
  if (showResults.value || showSettings.value) return

  const activeEl = window.document.activeElement
  if (activeEl && (activeEl.tagName === 'INPUT' || activeEl.tagName === 'TEXTAREA' || activeEl.isContentEditable)) {
    if (activeEl === hiddenInput.value) return
    return
  }

  if (e.ctrlKey || e.altKey || e.metaKey) return

  if (hiddenInput.value) {
    hiddenInput.value.focus()
  }
}

// Add/Remove event listeners
onMounted(() => {
  fetchDocument()
  
  window.addEventListener('click', handleGlobalClick)
  window.addEventListener('keydown', handleGlobalKeydown)
})

const handleGlobalClick = (e) => {
  const zone = window.document.querySelector('.typing-zone')
  const settings = window.document.querySelector('.settings-dropdown')
  const header = window.document.querySelector('.practice-header')
  
  if (zone && !zone.contains(e.target) && 
      (!settings || !settings.contains(e.target)) && 
      (!header || !header.contains(e.target))) {
    isFocused.value = false
  }
}

const cleanup = () => {
  if (timerInterval.value) {
    clearInterval(timerInterval.value)
  }
  window.removeEventListener('click', handleGlobalClick)
  window.removeEventListener('keydown', handleGlobalKeydown)
}

onUnmounted(() => {
  cleanup()
})

// Clean up timer if we switch pages
watch(() => props.docId, () => {
  cleanup()
  fetchDocument()
})
</script>

<style scoped>
.practice-container {
  max-width: var(--max-content-width);
  margin: 0 auto;
  padding: 30px 20px;
  position: relative;
}

/* Header & Navigation */
.practice-header {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  border-bottom: 1px solid var(--ui-border);
  padding-bottom: 16px;
  margin-bottom: 24px;
  gap: 16px;
}

@media (min-width: 768px) {
  .practice-header {
    flex-direction: row;
    align-items: center;
  }
}

.header-left {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.back-btn {
  padding: 6px 12px;
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--ui-primary);
  border: 1px solid var(--ui-border);
  border-radius: 4px;
  background-color: #FFFFFF;
  transition: all 0.2s;
  white-space: nowrap;
}

.back-btn:hover {
  background-color: var(--bg-color);
  color: var(--text-correct);
}

.doc-meta-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.doc-title {
  font-family: var(--font-typing);
  font-size: 1.3rem;
  font-weight: 600;
  color: var(--text-correct);
}

.meta-sub {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  font-size: 0.8rem;
  color: var(--ui-muted);
}

.bookmark-btn {
  font-family: var(--font-sans);
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--ui-primary);
  background: transparent;
  padding: 2px 6px;
  border: 1px solid var(--ui-border);
  border-radius: 4px;
  transition: all 0.15s;
  display: inline-flex;
  align-items: center;
  gap: 4px;
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

/* Sound checkbox styling */
.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: 500;
  color: var(--ui-primary);
  user-select: none;
  margin-top: 4px;
}

.checkbox-label input[type="checkbox"] {
  width: 16px;
  height: 16px;
  accent-color: var(--ui-primary);
  cursor: pointer;
}

/* Sound profile selector styling */
.sound-selector {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6px;
  margin-top: 4px;
}

.sound-selector button {
  padding: 6px;
  font-size: 0.8rem;
  border: 1px solid var(--ui-border);
  border-radius: 4px;
  background-color: transparent;
  transition: all 0.15s;
  color: var(--ui-primary);
  text-align: center;
}

.sound-selector button.active {
  background-color: var(--ui-primary);
  color: #FFFFFF;
  border-color: var(--ui-primary);
}

.bookmark-btn:hover {
  background-color: #F8FAFC;
}

/* Live Stats */
.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.live-stats {
  display: flex;
  gap: 16px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.stat-label {
  font-size: 0.7rem;
  color: var(--ui-muted);
  text-transform: uppercase;
}

.stat-value {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-correct);
}

.font-mono {
  font-family: var(--font-mono);
}

.nav-actions {
  display: flex;
  gap: 8px;
}

.nav-action-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  border: 1px solid var(--ui-border);
  background-color: #FFFFFF;
  transition: all 0.15s;
  color: var(--ui-primary);
}

.nav-action-btn:hover {
  background-color: var(--bg-color);
  color: var(--text-correct);
}

/* Settings Dropdown Pane */
.settings-dropdown {
  position: absolute;
  top: 90px;
  right: 20px;
  background-color: #FFFFFF;
  border: 1px solid var(--ui-border);
  border-radius: 8px;
  padding: 20px;
  width: 320px;
  z-index: 100;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.settings-title {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text-correct);
  border-bottom: 1px solid var(--ui-border);
  padding-bottom: 8px;
}

.setting-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.setting-item label {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--ui-primary);
}

.font-selector {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6px;
}

.font-selector button {
  padding: 6px;
  font-size: 0.85rem;
  border: 1px solid var(--ui-border);
  border-radius: 4px;
  background-color: transparent;
  transition: all 0.15s;
}

.font-selector button.active {
  background-color: var(--ui-primary);
  color: #FFFFFF;
  border-color: var(--ui-primary);
}

.setting-item input[type="range"] {
  width: 100%;
  accent-color: var(--ui-primary);
  cursor: pointer;
}

.close-settings-btn {
  background-color: var(--ui-primary);
  color: #FFFFFF;
  padding: 8px;
  font-size: 0.85rem;
  font-weight: 600;
  border-radius: 4px;
  text-align: center;
  transition: background 0.15s;
}

.close-settings-btn:hover {
  background-color: #334155;
}

/* Hidden Input for Capturing Keyboard/IME Events */
.hidden-typing-input {
  position: absolute;
  top: 0;
  left: 0;
  width: 1px;
  height: 1px;
  opacity: 0;
  padding: 0;
  margin: 0;
  border: none;
  overflow: hidden;
  pointer-events: none;
  z-index: -999;
}

/* Typing Zone */
.typing-zone {
  position: relative;
  background-color: transparent;
  border: none;
  border-radius: 0;
  padding: 10px 0;
  outline: none;
}

.typing-content-wrapper {
  max-height: 420px;
  overflow-y: scroll;
  position: relative;
  scroll-padding: 180px 0;
  padding-right: 0px;
  scrollbar-width: none; /* Hide scrollbar in Firefox */
  -ms-overflow-style: none; /* Hide scrollbar in IE/Edge */
}

.typing-content-wrapper::-webkit-scrollbar {
  display: none; /* Hide scrollbar in Chrome/Safari/Webkit */
}

.focus-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(238, 242, 245, 0.85);
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 4px;
  z-index: 10;
  cursor: pointer;
}

.focus-prompt {
  background-color: var(--ui-primary);
  color: #FFFFFF;
  padding: 12px 24px;
  border-radius: 20px;
  font-weight: 500;
  font-size: 0.95rem;
  text-align: center;
}

.typing-text-flow {
  white-space: pre-wrap;
  word-break: break-word;
  transition: font-size 0.2s, line-height 0.2s;
  user-select: none;
}

/* Character states styling */
.char {
  position: relative;
}

.char-untyped {
  color: var(--text-upcoming);
}

.char-correct {
  color: var(--text-correct);
}

.char-incorrect {
  color: var(--error-text);
  background-color: var(--error-bg);
  border-radius: 2px;
}

.char-current {
  background-color: var(--cursor-highlight);
  color: var(--text-correct);
  border-radius: 2px;
}

/* Carriage return symbol style */
.char-nl {
  display: inline;
  pointer-events: none;
}

.char-space {
  position: relative;
}

/* For incorrect spaces, show a small visual block */
.char-space.char-incorrect::after {
  content: "␣";
  position: absolute;
  left: 0;
  right: 0;
  text-align: center;
  color: var(--error-text);
  opacity: 0.8;
  font-size: 0.9em;
}

/* Results Modal Backdrop & Content */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(71, 85, 105, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 200;
}

.results-modal {
  background-color: #FFFFFF;
  border-radius: 8px;
  padding: 40px;
  width: 100%;
  max-width: 600px;
  text-align: center;
  border: 1px solid var(--ui-border);
}

.results-modal h2 {
  font-family: var(--font-typing);
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 6px;
  color: var(--text-correct);
}

.doc-title-result {
  font-style: italic;
  color: var(--ui-primary);
  margin-bottom: 30px;
  font-size: 0.95rem;
}

.results-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 30px;
}

@media (min-width: 500px) {
  .results-grid {
    grid-template-columns: 1fr 1fr 1fr 1fr;
  }
}

.result-card {
  border: 1px solid var(--ui-border);
  border-radius: 6px;
  padding: 16px 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: var(--bg-color);
}

.result-val {
  font-size: 1.6rem;
  font-weight: 700;
  color: var(--text-correct);
  margin-bottom: 4px;
}

.result-lbl {
  font-size: 0.7rem;
  color: var(--ui-muted);
  text-transform: uppercase;
  font-weight: 500;
  text-align: center;
}

.result-feedback {
  font-size: 0.95rem;
  color: var(--ui-primary);
  line-height: 1.6;
  margin-bottom: 36px;
  padding: 0 10px;
}

.modal-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
}

.btn {
  padding: 12px 24px;
  font-size: 0.95rem;
  font-weight: 600;
  border-radius: 4px;
  min-width: 160px;
  transition: all 0.2s;
}

.btn-primary {
  background-color: var(--ui-primary);
  color: #FFFFFF;
}

.btn-primary:hover {
  background-color: #334155;
}

.btn-secondary {
  background-color: transparent;
  color: var(--ui-primary);
  border: 1px solid var(--ui-border);
}

.btn-secondary:hover {
  background-color: var(--bg-color);
}

.loading-state {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 300px;
  color: var(--ui-muted);
  font-size: 1.1rem;
}
</style>
