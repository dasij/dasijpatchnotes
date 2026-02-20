<template>
  <div class="bottom-section">
    <div class="talents-layout">
      <!-- Left: Level Selector em grid 2x3 + 20 centralizado -->
      <div class="level-selector">
        <div class="level-grid">
          <button
            v-for="level in [1, 4, 7, 10, 13, 16]"
            :key="level"
            :class="{ active: selectedLevel === level }"
            @click="$emit('selectLevel', level)"
          >
            {{ level }}
          </button>
        </div>
        <!-- Level 20 centralizado embaixo -->
        <button
          class="level-20"
          :class="{ active: selectedLevel === 20 }"
          @click="$emit('selectLevel', 20)"
        >
          20
        </button>
      </div>
          
      <!-- Divider -->
      <div class="divider"></div>
          
      <!-- Center: Talent Cards -->
      <div class="cards-container">
        <div class="cards-grid">
          <TalentCard
            v-for="(talent, index) in (talents[selectedLevel] || [])"
            :key="talent.name"
            :talent="talent"
            :is-selected="isSelected(talent)"
            :is-active="selectedTalent === talent"
            @click="$emit('selectTalent', selectedLevel, talent, index)"
            @dblclick="$emit('toggleDevComments')"
          />
        </div>
      </div>

      <!-- Divider -->
      <div class="divider"></div>

      <!-- Right: Talent Code Panel -->
      <div class="code-panel-container">
        <TalentCodePanel
          :hero-name="heroName"
          :hero-display-name="heroDisplayName"
          :vanilla-talents="vanillaTalents"
          :modified-talents="modifiedTalents"
          :vanilla-talents-data="vanillaTalentsData"
          :modified-talents-data="modifiedTalentsData"
          @load-code="$emit('loadCode', $event)"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
/* eslint-disable no-undef */
import { computed, unref } from 'vue'
import TalentCard from './TalentCard.vue'
import TalentCodePanel from './TalentCodePanel.vue'

const props = defineProps({
  talents: { type: Object, default: () => ({}) },
  talentLevels: { type: Array, default: () => [1, 4, 7, 10, 13, 16, 20] },
  selectedLevel: { type: Number, default: 1 },
  selectedTalent: { type: Object, default: null },
  currentSelectedTalents: { type: Object, required: true },
  selectedTalents: { 
    type: Object, 
    default: () => ({
      vanilla: { 1: null, 4: null, 7: null, 10: null, 13: null, 16: null, 20: null },
      modified: { 1: null, 4: null, 7: null, 10: null, 13: null, 16: null, 20: null }
    })
  },
  vanillaTalentsData: { type: Object, default: () => ({}) },
  modifiedTalentsData: { type: Object, default: () => ({}) },
  heroName: { type: String, default: '' },
  heroDisplayName: { type: String, default: '' }
})

defineEmits(['selectLevel', 'selectTalent', 'toggleDevComments', 'loadCode'])

const isSelected = (talent) => props.currentSelectedTalents[props.selectedLevel]?.name === talent.name

// Computed properties para garantir acesso correto aos valores (mesmo se for ref)
const vanillaTalents = computed(() => {
  const st = unref(props.selectedTalents)
  return st?.vanilla || { 1: null, 4: null, 7: null, 10: null, 13: null, 16: null, 20: null }
})

const modifiedTalents = computed(() => {
  const st = unref(props.selectedTalents)
  return st?.modified || { 1: null, 4: null, 7: null, 10: null, 13: null, 16: null, 20: null }
})
</script>

<style scoped>
.bottom-section {
  background: rgba(0, 0, 0, 0.75);
  border: 1px solid #444;
  border-radius: 12px;
  padding: 12px 16px;
  height: calc(28% - 5px);
  min-height: 0;
  overflow: hidden;
}

.talents-layout {
  display: flex;
  gap: 12px;
  height: 100%;
  align-items: center;
}

/* Left: Level selector - grid 2x3 + 20 embaixo, centralizado verticalmente */
.level-selector {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  flex-shrink: 0;
  width: 100px;
  height: 100%;
}

.level-grid {
  display: grid;
  grid-template-columns: repeat(2, 44px);
  grid-template-rows: repeat(3, 44px);
  gap: 6px;
}

.level-grid button,
.level-20 {
  width: 44px;
  height: 44px;
  background: #222;
  border: 2px solid #444;
  color: #888;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
  font-weight: bold;
  transition: all 0.2s;
}

.level-grid button:hover,
.level-20:hover {
  background: #333;
  border-color: #555;
}

.level-grid button.active,
.level-20.active {
  background: #0099ff;
  border-color: #0099ff;
  color: #fff;
}

/* Level 20 centralizado embaixo */
.level-20 {
  margin-top: 4px;
}

/* Divider */
.divider {
  width: 1px;
  background: #444;
  align-self: stretch;
  margin: 4px 0;
}

/* Center: Cards container - centralizado */
.cards-container {
  flex: 1 1 auto;
  display: flex;
  align-items: stretch;
  justify-content: flex-start;
  min-width: 0;
  overflow: hidden;
  height: 100%;
}

/* Cards grid - SEMPRE centralizado */
.cards-grid {
  display: flex;
  gap: 12px;
  align-items: stretch;
  justify-content: flex-start;
  flex-wrap: nowrap;
  width: 100%;
  max-width: 100%;
  height: 100%;
}

/* Cards ocupam todo o espaço disponível com largura igual */
.cards-grid :deep(.talent-card) {
  flex: 1 1 0 !important;
  min-width: 0;
  max-width: none;
  width: auto !important;
  padding: 12px;
  min-height: 150px;
}

.cards-grid :deep(.card-header img) {
  width: 44px;
  height: 44px;
}

.cards-grid :deep(.card-title h4) {
  font-size: 14px;
}

.cards-grid :deep(.card-body) {
  font-size: 12px;
  line-height: 1.4;
}

/* Right: Code panel container */
.code-panel-container {
  flex: 0 0 auto;
  width: 240px;
  height: 100%;
  overflow-y: auto;
  display: flex;
  align-items: center; /* Centraliza verticalmente */
  justify-content: center;
}

.code-panel-container :deep(.talent-code-panel) {
  min-height: 95%; /* Ocupa 95% da altura vertical */
  height: 95%;
  width: 100%;
  min-width: auto;
  display: flex;
  flex-direction: column;
  justify-content: center; /* Centraliza conteúdo verticalmente */
}

/* ===========================================
   RESPONSIVE STYLES
   =========================================== */

/* Quando tem mais cards que cabem, permite scroll horizontal */
@media (max-width: 1400px) {
  .cards-grid {
    flex-wrap: nowrap;
    justify-content: flex-start;
    overflow-x: auto;
    width: 100%;
    padding-right: 10px;
  }
}

/* 1280px - Ajustes para o painel de código e cards menores */
@media (max-width: 1280px) {
  .code-panel-container {
    width: 220px;
  }
  
  .cards-grid :deep(.talent-card) {
    flex: 1 1 0 !important;
    min-width: 0;
    max-width: none;
    width: auto !important;
    padding: 10px;
    min-height: 140px;
  }
  
  .cards-grid :deep(.card-title h4) {
    font-size: 13px;
  }
  
  .cards-grid :deep(.card-body) {
    font-size: 11px;
  }
  
  .level-selector {
    width: 90px;
  }
  
  .level-grid {
    grid-template-columns: repeat(2, 40px);
    grid-template-rows: repeat(3, 40px);
    gap: 5px;
  }
  
  .level-grid button,
  .level-20 {
    width: 40px;
    height: 40px;
    font-size: 12px;
  }
}

/* 1200px - Painel de código mais compacto */
@media (max-width: 1200px) {
  .code-panel-container {
    width: 200px;
  }
  
  .cards-grid :deep(.talent-card) {
    flex: 1 1 0 !important;
    min-width: 0;
    max-width: none;
    width: auto !important;
    padding: 8px;
    min-height: 130px;
  }
  
  :deep(.code-title) {
    font-size: 10px;
  }
  
  :deep(.copy-btn) {
    padding: 3px 6px;
    font-size: 9px;
  }
  
  :deep(.code-input) {
    padding: 6px 8px;
    font-size: 10px;
  }
  
  :deep(.action-btn) {
    padding: 6px 4px;
    font-size: 9px;
  }
  
  :deep(.btn-icon) {
    font-size: 10px;
  }
}

/* 1100px - Botões empilhados verticalmente */
@media (max-width: 1100px) {
  .talents-layout {
    gap: 10px;
  }
  
  .code-panel-container {
    width: 160px;
  }
  
  .cards-grid :deep(.talent-card) {
    flex: 1 1 0 !important;
    min-width: 0;
    max-width: none;
    width: auto !important;
    padding: 8px;
    min-height: 125px;
  }
  
  :deep(.talent-code-panel) {
    gap: 6px;
    padding: 8px;
  }
  
  :deep(.code-header) {
    flex-direction: column;
    gap: 4px;
    align-items: flex-start;
  }
  
  :deep(.code-title) {
    font-size: 10px;
  }
  
  :deep(.copy-btn) {
    padding: 2px 6px;
    font-size: 9px;
  }
  
  :deep(.code-input) {
    padding: 6px;
    font-size: 10px;
  }
  
  /* Botões empilhados verticalmente */
  :deep(.code-actions) {
    flex-direction: column;
    gap: 4px;
  }
  
  :deep(.action-btn) {
    padding: 6px 4px;
    font-size: 9px;
    width: 100%;
  }
}

/* 1050px - Painel mínimo, apenas essencial */
@media (max-width: 1050px) {
  .code-panel-container {
    width: 130px;
  }
  
  .cards-grid :deep(.talent-card) {
    flex: 1 1 0 !important;
    min-width: 0;
    max-width: none;
    width: auto !important;
    padding: 6px;
    min-height: 115px;
  }
  
  :deep(.talent-code-panel) {
    padding: 6px;
    gap: 5px;
  }
  
  :deep(.code-title) {
    font-size: 9px;
  }
  
  /* Esconde o botão Copy, deixa só o ícone implícito */
  :deep(.copy-btn) {
    display: none;
  }
  
  :deep(.code-input) {
    padding: 5px;
    font-size: 9px;
  }
  
  :deep(.code-input::placeholder) {
    font-size: 8px;
  }
  
  :deep(.action-btn) {
    padding: 5px 3px;
    font-size: 8px;
  }
  
  :deep(.btn-icon) {
    font-size: 9px;
  }
}

/* 991px e menor - Esconde o painel de código (tablet e mobile) */
@media (max-width: 991px) {
  .code-panel-container {
    display: none;
  }
  
  .divider:last-of-type {
    display: none;
  }
}
</style>
