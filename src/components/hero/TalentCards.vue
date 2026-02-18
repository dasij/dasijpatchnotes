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
          
      <!-- Right: Talent Cards -->
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
    </div>
  </div>
</template>

<script setup>
/* eslint-disable no-undef */
import TalentCard from './TalentCard.vue'

const props = defineProps({
  talents: { type: Object, default: () => ({}) },
  talentLevels: { type: Array, default: () => [1, 4, 7, 10, 13, 16, 20] },
  selectedLevel: { type: Number, default: 1 },
  selectedTalent: { type: Object, default: null },
  currentSelectedTalents: { type: Object, required: true }
})

defineEmits(['selectLevel', 'selectTalent', 'toggleDevComments'])

const isSelected = (talent) => props.currentSelectedTalents[props.selectedLevel] === talent
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
  gap: 14px;
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

/* Right: Cards container - centralizado */
.cards-container {
  flex: 1;
  display: flex;
  align-items: stretch;
  justify-content: center;
  min-width: 0;
  overflow: hidden;
  height: 100%;
}

/* Cards grid - SEMPRE centralizado */
.cards-grid {
  display: flex;
  gap: 16px;
  align-items: stretch;
  justify-content: center;
  flex-wrap: wrap;
  max-width: 100%;
  height: 100%;
}

/* Quando tem mais de 4 cards ou não cabe, permite scroll horizontal */
@media (max-width: 1300px) {
  .cards-grid {
    flex-wrap: nowrap;
    justify-content: flex-start;
    overflow-x: auto;
    width: 100%;
    padding-right: 10px;
  }
}
</style>
