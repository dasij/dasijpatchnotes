<template>
  <div class="talent-code-panel">
    <div class="code-header">
      <span class="code-title">Build Code</span>
      <button 
        class="copy-btn" 
        @click="copyToClipboard"
        :class="{ copied: copied }"
        :disabled="!codeText"
      >
        {{ copied ? 'Copied!' : 'Copy' }}
      </button>
    </div>
    
    <div class="code-input-wrapper">
      <input 
        id="talent-code"
        ref="codeInput"
        v-model="codeText"
        type="text" 
        class="code-input"
        placeholder="Hero[Vanilla][Modified]"
        autocomplete="off"
        @keyup.enter="loadCode"
      />
    </div>
    
    <div class="code-actions">
      <button class="action-btn load" @click="loadCode" :disabled="!isValidCode">
        <span class="btn-icon">📥</span>
        Load
      </button>
      <button class="action-btn generate" @click="generateCode">
        <span class="btn-icon">⚙️</span>
        Generate
      </button>
    </div>
    
    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>
    
    <div v-if="successMessage" class="success-message">
      {{ successMessage }}
    </div>
  </div>
</template>

<script setup>
/* eslint-disable no-undef */
import { ref, computed, watch } from 'vue'

const props = defineProps({
  heroName: { type: String, default: '' },
  heroDisplayName: { type: String, default: '' },
  vanillaTalents: { type: Object, default: () => ({}) },
  modifiedTalents: { type: Object, default: () => ({}) },
  vanillaTalentsData: { type: Object, default: () => ({}) },
  modifiedTalentsData: { type: Object, default: () => ({}) }
})

const emit = defineEmits(['loadCode'])

const codeText = ref('')
const codeInput = ref(null)
const copied = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

const talentLevels = [1, 4, 7, 10, 13, 16, 20]

// Regex para validar o código: Hero[XXXXXXX][XXXXXXX] - aceita 1-5 talentos
const codeRegex = /^([a-zA-Z][a-zA-Z0-9]*)\[([Nn1-5]{7})\]\[([Nn1-5]{7})\]$/

const isValidCode = computed(() => {
  return codeRegex.test(codeText.value.trim())
})

// Limpa mensagens após 3 segundos
const clearMessages = () => {
  setTimeout(() => {
    errorMessage.value = ''
    successMessage.value = ''
  }, 3000)
}

// Converte seleções de talentos para código (1-5 ou N)
const talentsToCode = (talents, talentsData) => {
  // Verifica se os dados são válidos
  if (!talents || !talentsData) {
    return 'NNNNNNN'
  }
  
  return talentLevels.map(level => {
    const talent = talents[level]
    if (!talent || !talent.name) return 'N'
    
    // Encontrar o índice do talento na lista de talentos do nível
    const levelTalents = talentsData[level] || []
    if (!Array.isArray(levelTalents) || levelTalents.length === 0) {
      return 'N'
    }
    
    const index = levelTalents.findIndex(t => t && t.name === talent.name)
    
    // Retorna 1-5 baseado na posição, ou N se não encontrado
    return index >= 0 ? (index + 1).toString() : 'N'
  }).join('')
}

// Converte código para seleções de talentos
const codeToTalents = (code, talentsData) => {
  const selections = {}
  
  for (let i = 0; i < talentLevels.length; i++) {
    const level = talentLevels[i]
    const char = code[i]
    
    if (char === 'N' || char === 'n') {
      selections[level] = null
    } else {
      const index = parseInt(char, 10) - 1
      const levelTalents = talentsData[level] || []
      
      if (index >= 0 && index < levelTalents.length) {
        selections[level] = levelTalents[index]
      } else {
        selections[level] = null
      }
    }
  }
  
  return selections
}

const generateCode = () => {
  if (!props.heroDisplayName) {
    errorMessage.value = 'No hero selected'
    clearMessages()
    return
  }
  
  // Log para debug
  console.log('Generating code...')
  console.log('Vanilla talents:', props.vanillaTalents)
  console.log('Vanilla talents data:', props.vanillaTalentsData)
  console.log('Modified talents:', props.modifiedTalents)
  console.log('Modified talents data:', props.modifiedTalentsData)
  
  const vanillaCode = talentsToCode(props.vanillaTalents, props.vanillaTalentsData)
  const modifiedCode = talentsToCode(props.modifiedTalents, props.modifiedTalentsData)
  
  // Remove espaços e caracteres especiais do nome do herói
  const cleanHeroName = props.heroDisplayName.replace(/\s+/g, '')
  
  codeText.value = `${cleanHeroName}[${vanillaCode}][${modifiedCode}]`
  successMessage.value = 'Code generated!'
  clearMessages()
}

const loadCode = () => {
  const trimmedCode = codeText.value.trim()
  
  if (!trimmedCode) {
    errorMessage.value = 'Please enter a code'
    clearMessages()
    return
  }
  
  const match = trimmedCode.match(codeRegex)
  
  if (!match) {
    errorMessage.value = 'Invalid code format. Expected: Hero[Vanilla][Modified]'
    clearMessages()
    return
  }
  
  const [, heroName, vanillaCode, modifiedCode] = match
  
  // Converte os códigos para seleções usando os dados corretos de cada tipo
  const vanillaSelections = codeToTalents(vanillaCode.toUpperCase(), props.vanillaTalentsData)
  const modifiedSelections = codeToTalents(modifiedCode.toUpperCase(), props.modifiedTalentsData)
  
  // Emite evento para carregar o código
  // Também passa os códigos raw para reconverter se for um herói diferente
  emit('loadCode', {
    heroName: heroName.toLowerCase(),
    vanillaSelections,
    modifiedSelections,
    vanillaCode: vanillaCode.toUpperCase(),
    modifiedCode: modifiedCode.toUpperCase()
  })
  
  successMessage.value = 'Build loaded!'
  clearMessages()
}

const copyToClipboard = async () => {
  if (!codeText.value) return
  
  try {
    await navigator.clipboard.writeText(codeText.value)
    copied.value = true
    setTimeout(() => {
      copied.value = false
    }, 2000)
  } catch (err) {
    // Fallback para browsers antigos
    const input = codeInput.value
    input.select()
    document.execCommand('copy')
    copied.value = true
    setTimeout(() => {
      copied.value = false
    }, 2000)
  }
}

// Limpa mensagens quando o texto muda
watch(codeText, () => {
  errorMessage.value = ''
  successMessage.value = ''
})
</script>

<style scoped>
.talent-code-panel {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 12px;
  background: rgba(0, 0, 0, 0.5);
  border-radius: 10px;
  border: 1px solid #444;
  min-width: 200px;
  width: 220px;
  flex-shrink: 0;
}

.code-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.code-title {
  color: #fff;
  font-size: 13px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.copy-btn {
  background: transparent;
  border: 1px solid #555;
  color: #888;
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 11px;
  cursor: pointer;
  transition: all 0.2s;
}

.copy-btn:hover:not(:disabled) {
  border-color: #0099ff;
  color: #0099ff;
}

.copy-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.copy-btn.copied {
  border-color: #78da5b;
  color: #78da5b;
  background: rgba(120, 218, 91, 0.1);
}

.code-input-wrapper {
  position: relative;
}

.code-input {
  width: 100%;
  padding: 10px 12px;
  background: #1a1a1a;
  border: 1px solid #444;
  border-radius: 6px;
  color: #fff;
  font-size: 13px;
  font-family: 'Courier New', monospace;
  letter-spacing: 0.5px;
  box-sizing: border-box;
}

.code-input:focus {
  outline: none;
  border-color: #0099ff;
  box-shadow: 0 0 0 2px rgba(0, 153, 255, 0.2);
}

.code-input::placeholder {
  color: #666;
  font-size: 11px;
}

.code-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  flex: 1;
  padding: 10px 8px;
  border: none;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
}

.action-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.action-btn.load {
  background: #222;
  color: #fff;
  border: 1px solid #444;
}

.action-btn.load:hover:not(:disabled) {
  background: #333;
  border-color: #0099ff;
}

.action-btn.generate {
  background: #0099ff;
  color: #fff;
}

.action-btn.generate:hover {
  background: #0077cc;
}

.btn-icon {
  font-size: 12px;
}

.error-message {
  color: #ff4444;
  font-size: 11px;
  text-align: center;
  padding: 4px;
  background: rgba(255, 68, 68, 0.1);
  border-radius: 4px;
}

.success-message {
  color: #78da5b;
  font-size: 11px;
  text-align: center;
  padding: 4px;
  background: rgba(120, 218, 91, 0.1);
  border-radius: 4px;
}

/* ===========================================
   RESPONSIVE STYLES
   =========================================== */

/* Tablet */
@media (max-width: 991px) {
  .talent-code-panel {
    width: 100%;
    min-width: auto;
    padding: 10px;
    gap: 8px;
  }
  
  .code-title {
    font-size: 12px;
  }
  
  .code-input {
    padding: 8px 10px;
    font-size: 12px;
  }
  
  .action-btn {
    padding: 8px 6px;
    font-size: 11px;
  }
}

/* Mobile */
@media (max-width: 767px) {
  .talent-code-panel {
    padding: 10px;
    gap: 8px;
  }
  
  .code-title {
    font-size: 11px;
  }
  
  .copy-btn {
    padding: 3px 8px;
    font-size: 10px;
  }
  
  .code-input {
    padding: 8px;
    font-size: 12px;
  }
  
  .action-btn {
    padding: 10px 8px;
    font-size: 11px;
  }
  
  .btn-icon {
    font-size: 11px;
  }
}
</style>
