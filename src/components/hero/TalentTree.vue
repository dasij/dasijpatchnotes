<template>
  <div class="talent-tree-panel">
    <!-- Header igual ao Abilities -->
    <h2 class="panel-title">Talent Tree</h2>
    
    <!-- Tabs -->
    <div class="tabs">
      <button 
        :class="{ active: activeTab === 'tree' }" 
        @click="activeTab = 'tree'"
      >
        Talents
      </button>
      <button 
        :class="{ active: activeTab === 'selected' }" 
        @click="activeTab = 'selected'"
        :disabled="!hasAnySelection"
      >
        Selected
      </button>
    </div>
    
    <!-- Tab Content -->
    <div ref="tabContent" class="tab-content" :class="{ 'has-overflow': hasOverflow && activeTab === 'tree', 'compact-mode': isCompact && activeTab === 'tree' }">
      <!-- Tree View - Ocupa espaço verticalmente -->
      <div v-if="activeTab === 'tree'" ref="treeContainer" class="tree-view">
        <div
          v-for="level in talentLevels"
          :key="level"
          class="talent-level-row"
          :class="{ 
            'has-selection': isAnySelected(level), 
            'active': selectedLevel === level 
          }"
        >
          <span 
            class="level-number" 
            :class="{ 'active': selectedLevel === level }"
            @click="$emit('selectLevel', level)"
          >
            {{ level }}
          </span>
          <div class="talent-options" :class="{ 'five-talents': talents[level]?.length > 4 }">
            <TalentNode
              v-for="(talent, index) in talents[level]"
              :key="talent.name"
              :talent="talent"
              :is-selected="isSelected(level, talent)"
              :is-active="selectedTalent === talent"
              :has-selection="isAnySelected(level)"
              @click="$emit('selectTalent', level, talent, index)"
              @dblclick="$emit('toggleDevComments')"
            />
            <div 
              v-for="n in spacerCount(level)" 
              :key="`spacer-${n}`" 
              class="talent-spacer"
            />
          </div>
        </div>
      </div>
      
      <!-- Selected View - Build completa com descrição em largura total -->
      <div v-else class="selected-view">
        <div v-if="hasAnySelection" class="build-list">
          <div 
            v-for="level in selectedLevels" 
            :key="level"
            class="build-item"
            @click="$emit('selectLevel', level)"
          >
            <div class="build-header">
              <span class="build-level">{{ level }}</span>
              <img :src="getTalentImage(level)" :alt="getTalentName(level)">
              <span class="build-name">{{ getTalentName(level) }}</span>
            </div>
            <p class="build-description" v-html="getTalentDescription(level)"></p>
          </div>
        </div>
        <div v-else class="no-selection">
          <p>No talents selected</p>
          <span class="hint">Click on talents to build your loadout</span>
        </div>
      </div>
    </div>
    
    <!-- Reset button - sempre no bottom -->
    <button @click="$emit('reset')" class="reset-btn">Reset All</button>
  </div>
</template>

<script setup>
/* eslint-disable no-undef */
import { ref, computed, inject, watch, onMounted, nextTick } from 'vue'
import TalentNode from './TalentNode.vue'

const props = defineProps({
  talents: { type: Object, default: () => ({}) },
  talentLevels: { type: Array, default: () => [1, 4, 7, 10, 13, 16, 20] },
  selectedLevel: { type: Number, default: 1 },
  selectedTalent: { type: Object, default: null },
  currentSelectedTalents: { type: Object, required: true }
})

defineEmits(['reset', 'selectLevel', 'selectTalent', 'toggleDevComments'])

const heroName = inject('heroName')
const formatText = inject('formatText')
const activeTab = ref('tree')

const isSelected = (level, talent) => props.currentSelectedTalents[level]?.name === talent.name
const isAnySelected = (level) => props.currentSelectedTalents[level] !== null
const spacerCount = (level) => Math.max(0, 4 - (props.talents[level]?.length || 0))

const hasAnySelection = computed(() => {
  return Object.values(props.currentSelectedTalents).some(t => t !== null)
})

const selectedLevels = computed(() => {
  return props.talentLevels.filter(level => props.currentSelectedTalents[level] !== null)
})

const getTalentName = (level) => {
  return props.currentSelectedTalents[level]?.name || ''
}

const getTalentDescription = (level) => {
  const talent = props.currentSelectedTalents[level]
  return formatText(talent?.description || '')
}

const getTalentImage = (level) => {
  const talent = props.currentSelectedTalents[level]
  if (!talent?.image) return ''
  try {
    return require(`@/assets/talents/${heroName.value}/${talent.image}`)
  } catch {
    return ''
  }
}

// Detect overflow to show scrollbar only when needed
const tabContent = ref(null)
const treeContainer = ref(null)
const hasOverflow = ref(false)
const isCompact = ref(false)

const checkOverflow = async () => {
  // Wait for DOM update
  await nextTick()
  
  // Only check on tree tab
  if (activeTab.value !== 'tree' || !treeContainer.value || !tabContent.value) {
    return
  }
  
  const container = tabContent.value
  const content = treeContainer.value
  const containerHeight = container.clientHeight
  
  console.log('Container height:', containerHeight)
  
  // Step 1: Start with normal size
  isCompact.value = false
  await nextTick()
  
  const normalHeight = content.scrollHeight
  console.log('Normal height:', normalHeight, 'Fits:', normalHeight <= containerHeight + 1)
  
  // If fits in normal mode, done
  if (normalHeight <= containerHeight + 1) {
    hasOverflow.value = false
    return
  }
  
  // Step 2: Try compact mode
  isCompact.value = true
  await nextTick()
  
  const compactHeight = content.scrollHeight
  console.log('Compact height:', compactHeight, 'Needs scroll:', compactHeight > containerHeight + 1)
  
  // If still doesn't fit, show scrollbar
  hasOverflow.value = compactHeight > containerHeight + 1
}

onMounted(() => {
  // Initial check with delay to ensure DOM is ready
  setTimeout(checkOverflow, 200)
})

// Watch for tab changes
watch(activeTab, (newVal) => {
  if (newVal === 'tree') {
    setTimeout(checkOverflow, 100)
  }
})

// Watch for window resize
let resizeTimeout = null
window.addEventListener('resize', () => {
  clearTimeout(resizeTimeout)
  resizeTimeout = setTimeout(checkOverflow, 100)
})
</script>

<style scoped>
.talent-tree-panel {
  height: 100%;
  display: flex;
  flex-direction: column;
}

/* Header */
.panel-title {
  color: #fff;
  font-size: 16px;
  text-transform: uppercase;
  letter-spacing: 2px;
  margin-bottom: 10px;
  text-align: center;
  border-bottom: 1px solid #444;
  padding-bottom: 8px;
  flex-shrink: 0;
}

/* Tabs */
.tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 12px;
  flex-shrink: 0;
}

.tabs button {
  flex: 1;
  padding: 10px 14px;
  background: #222;
  border: 1px solid #444;
  color: #888;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
  font-weight: bold;
  text-transform: uppercase;
  transition: all 0.2s;
}

.tabs button:hover:not(:disabled) {
  background: #333;
  border-color: #555;
}

.tabs button.active {
  background: #0099ff;
  border-color: #0099ff;
  color: #fff;
}

.tabs button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* Tab Content */
.tab-content {
  flex: 1;
  overflow: hidden;
  min-height: 0;
  margin-bottom: 10px;
}

/* Show scrollbar only when there's overflow */
.tab-content.has-overflow {
  overflow-y: auto;
}

/* Firefox scrollbar */
.tab-content.has-overflow {
  scrollbar-width: thin;
  scrollbar-color: #444 transparent;
}

/* Webkit scrollbar - only visible when has-overflow */
.tab-content.has-overflow::-webkit-scrollbar {
  width: 6px;
}

.tab-content.has-overflow::-webkit-scrollbar-track {
  background: transparent;
}

.tab-content.has-overflow::-webkit-scrollbar-thumb {
  background: #444;
  border-radius: 3px;
}

/* Tree View - Mantém tamanho fixo, scrollbar no pai quando necessário */
.tree-view {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  gap: 4px;
}

.talent-level-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 6px 10px;
  border-radius: 10px;
  transition: background 0.2s;
  flex-shrink: 0;
  height: auto;
  min-height: 56px;
}

/* Compact mode - smaller icons like tablet */
.tab-content.compact-mode .talent-level-row {
  padding: 6px 8px;
  gap: 10px;
  min-height: 48px;
}

.tab-content.compact-mode .level-number {
  width: 36px;
  height: 36px;
  font-size: 13px;
}

.tab-content.compact-mode .talent-options {
  gap: 8px;
}

.tab-content.compact-mode .talent-spacer {
  width: 44px;
  height: 44px;
}

.tab-content.compact-mode :deep(.talent-node) {
  width: 44px !important;
  height: 44px !important;
  border-radius: 8px;
  border-width: 2px;
}

.talent-level-row:hover {
  background: rgba(255, 255, 255, 0.05);
}

.talent-level-row.has-selection {
  background: rgba(0, 153, 255, 0.1);
}

.talent-level-row.active {
  background: rgba(116, 42, 255, 0.15);
  border: 1px solid rgba(116, 42, 255, 0.3);
}

.level-number {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #222;
  border: 2px solid #444;
  border-radius: 8px;
  color: #888;
  font-size: 15px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s;
  flex-shrink: 0;
}

.level-number:hover, .level-number.active {
  background: #0099ff;
  border-color: #0099ff;
  color: #fff;
}

.talent-options {
  display: flex;
  gap: 10px;
  flex: 1;
  justify-content: space-evenly;
  align-items: center;
}

/* When there are 5 talents, scale them down proportionally */
.talent-options.five-talents {
  gap: 6px;
}

.talent-options.five-talents :deep(.talent-node) {
  width: 44px !important;
  height: 44px !important;
  border-radius: 8px;
  border-width: 2px;
}

.talent-options.five-talents .talent-spacer {
  width: 44px;
  height: 44px;
}

.talent-spacer {
  width: 56px;
  height: 56px;
  flex-shrink: 0;
}

/* Selected View - Build List */
.selected-view {
  height: 100%;
  overflow-y: auto;
  padding: 4px;
}

.build-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.build-item {
  padding: 14px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid #333;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
}

.build-item:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: #444;
}

.build-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 10px;
}

.build-level {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #0099ff;
  color: #fff;
  font-size: 14px;
  font-weight: bold;
  border-radius: 8px;
  flex-shrink: 0;
}

.build-header img {
  width: 44px;
  height: 44px;
  border-radius: 8px;
  border: 2px solid #78da5b;
  flex-shrink: 0;
}

.build-name {
  color: #fff;
  font-size: 16px;
  font-weight: 600;
  flex: 1;
}

/* Descrição ocupa largura total, sem indentação */
.build-description {
  color: #bbb;
  font-size: 14px;
  line-height: 1.5;
  margin: 0;
  padding-left: 0; /* Remove indentação */
}

.no-selection {
  text-align: center;
  padding: 40px 20px;
  color: #666;
}

.no-selection p {
  font-size: 16px;
  margin: 0 0 8px 0;
}

.no-selection .hint {
  font-size: 13px;
}

/* Reset button - sempre no bottom */
.reset-btn {
  background: transparent;
  border: 1px solid #444;
  color: #888;
  padding: 12px 24px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 12px;
  text-transform: uppercase;
  transition: all 0.2s;
  flex-shrink: 0;
  width: 100%;
  margin-top: auto;
}

.reset-btn:hover {
  border-color: #ff4444;
  color: #ff4444;
  background: rgba(255, 68, 68, 0.1);
}

/* ===========================================
   RESPONSIVE STYLES
   =========================================== */

/* Tablet - Tree mais compacto com ícones menores */
@media (max-width: 991px) {
  .panel-title {
    font-size: 13px;
    margin-bottom: 8px;
    padding-bottom: 6px;
  }
  
  .tabs {
    margin-bottom: 8px;
  }
  
  .tabs button {
    padding: 8px 10px;
    font-size: 11px;
  }
  
  .talent-level-row {
    padding: 6px 8px;
    gap: 10px;
  }
  
  .level-number {
    width: 32px;
    height: 32px;
    font-size: 12px;
  }
  
  .talent-options {
    gap: 8px;
  }
  
  .talent-spacer {
    width: 36px;
    height: 36px;
  }
  
  /* 5 talents - tablet */
  .talent-options.five-talents {
    gap: 4px;
  }
  
  .talent-options.five-talents :deep(.talent-node) {
    width: 28px !important;
    height: 28px !important;
    border-radius: 5px;
    border-width: 1px;
  }
  
  .talent-options.five-talents .talent-spacer {
    width: 28px;
    height: 28px;
  }
  
  /* Ícones de talento menores no tablet */
  :deep(.talent-node) {
    width: 36px !important;
    height: 36px !important;
    border-radius: 6px;
    border-width: 2px;
  }
  
  :deep(.talent-node img) {
    width: 100%;
    height: 100%;
  }
  
  :deep(.talent-node .checkmark) {
    width: 14px;
    height: 14px;
    font-size: 9px;
    top: -5px;
    right: -5px;
  }
  
  .reset-btn {
    padding: 10px 16px;
    font-size: 11px;
  }
}

/* Mobile - Mais espaçamento e ícones maiores */
@media (max-width: 767px) {
  .talent-tree-panel {
    padding-bottom: 10px;
  }
  
  .panel-title {
    font-size: 13px;
    margin-bottom: 8px;
    padding-bottom: 6px;
  }
  
  .tabs {
    margin-bottom: 10px;
    gap: 8px;
  }
  
  .tabs button {
    padding: 8px 12px;
    font-size: 11px;
  }
  
  .tab-content {
    margin-bottom: 8px;
  }
  
  /* Mais espaço entre as linhas de talento */
  .tree-view {
    gap: 8px;
    justify-content: flex-start;
  }
  
  .talent-level-row {
    padding: 8px 10px;
    gap: 12px;
    min-height: 60px;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 10px;
  }
  
  /* Números de level maiores */
  .level-number {
    width: 44px;
    height: 44px;
    font-size: 14px;
    border-radius: 8px;
    border-width: 2px;
  }
  
  /* Ícones de talento maiores com mais espaço */
  .talent-options {
    gap: 10px;
    justify-content: space-around;
  }
  
  .talent-spacer {
    width: 52px;
    height: 52px;
  }
  
  /* Talent nodes maiores via deep selector */
  :deep(.talent-node) {
    width: 64px !important;
    height: 64px !important;
    border-radius: 12px;
    border-width: 2px;
  }
  
  /* 5 talents - mobile */
  .talent-options.five-talents {
    gap: 6px;
  }
  
  .talent-options.five-talents :deep(.talent-node) {
    width: 48px !important;
    height: 48px !important;
    border-radius: 8px;
    border-width: 2px;
  }
  
  .talent-options.five-talents .talent-spacer {
    width: 48px;
    height: 48px;
  }
  
  :deep(.talent-node img) {
    width: 100%;
    height: 100%;
  }
  
  .build-item {
    padding: 12px;
  }
  
  .build-header {
    gap: 10px;
    margin-bottom: 8px;
  }
  
  .build-level {
    width: 34px;
    height: 34px;
    font-size: 13px;
  }
  
  .build-header img {
    width: 40px;
    height: 40px;
  }
  
  .build-name {
    font-size: 14px;
  }
  
  .build-description {
    font-size: 12px;
  }
  
  .reset-btn {
    padding: 12px 16px;
    font-size: 11px;
    margin-top: 10px;
  }
}

/* Small Mobile */
@media (max-width: 480px) {
  .level-number {
    width: 36px;
    height: 36px;
    font-size: 12px;
  }
  
  .talent-spacer {
    width: 56px;
    height: 56px;
  }
  
  .talent-options {
    gap: 6px;
  }
  
  /* Ícones de talento maiores em telas pequenas */
  :deep(.talent-node) {
    width: 56px !important;
    height: 56px !important;
    border-radius: 10px;
  }
  
  /* 5 talents - small mobile */
  .talent-options.five-talents {
    gap: 4px;
  }
  
  .talent-options.five-talents :deep(.talent-node) {
    width: 44px !important;
    height: 44px !important;
    border-radius: 8px;
    border-width: 1px;
  }
  
  .talent-options.five-talents .talent-spacer {
    width: 44px;
    height: 44px;
  }
}
</style>
