<template>
  <div
    class="talent-card"
    :class="{ 
      selected: isSelected,
      active: isActive,
      changed: talent.talentChanged
    }"
    @click="$emit('click')"
    @dblclick="$emit('dblclick')"
  >
    <div class="card-header">
      <img :src="imagePath" :alt="talent.name">
      <div class="card-title">
        <h4>{{ talent.name }}</h4>
        <span v-if="talent.talentChanged" class="changed-indicator">Modified</span>
        <span v-else-if="isSelected" class="selected-badge">Selected</span>
        <span v-else class="placeholder-badge"></span>
      </div>
    </div>
    <div class="card-body">
      <p v-html="formattedDescription"></p>
    </div>
  </div>
</template>

<script setup>
/* eslint-disable no-undef */
import { computed, inject } from 'vue'

const props = defineProps({
  talent: { type: Object, required: true },
  isSelected: { type: Boolean, default: false },
  isActive: { type: Boolean, default: false }
})

defineEmits(['click', 'dblclick'])

const heroName = inject('heroName')
const formatText = inject('formatText')
const getTalentImagePath = inject('getTalentImagePath', null)

const imagePath = computed(() => {
  if (!props.talent?.image) return ''
  if (getTalentImagePath) {
    return getTalentImagePath(heroName.value, props.talent.image)
  }
  return `talents/${heroName.value}/${props.talent.image}`
})

// Junta descrição + quest + rewards no mesmo formato do Tissue Regeneration
const formattedDescription = computed(() => {
  let fullText = props.talent.description || ''
  
  // Se tiver quest separado, adiciona com tag
  if (props.talent.quest) {
    if (fullText) fullText += ' '
    fullText += `{quest}Quest:{/quest} ${props.talent.quest}`
  }
  
  // Se tiver rewards separados, adiciona com tags
  if (props.talent.rewards?.length) {
    props.talent.rewards.forEach(reward => {
      if (fullText) fullText += ' '
      fullText += `{reward}Reward:{/reward} ${reward}`
    })
  }
  
  return formatText(fullText)
})
</script>

<style scoped>
.talent-card {
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid #333;
  border-radius: 12px;
  padding: 16px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  flex-direction: column;
  width: 280px;
  flex: 1;
  min-height: 160px;
  overflow: hidden;
}

.talent-card:hover {
  background: rgba(255, 255, 255, 0.08);
  transform: translateY(-2px);
  border-color: #444;
}

.talent-card.selected {
  border-color: #78da5b;
  background: rgba(120, 218, 91, 0.1);
}

.talent-card.active {
  border-color: #0099ff;
  box-shadow: 0 0 20px rgba(0, 153, 255, 0.3);
}

.talent-card.changed {
  border-left: 4px solid #ff4444;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
  flex-shrink: 0;
}

.card-header img {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  border: 2px solid #444;
  flex-shrink: 0;
}

.card-title h4 {
  color: #fff;
  font-size: 16px;
  margin: 0 0 4px 0;
  line-height: 1.3;
}

.selected-badge {
  display: inline-block;
  background: #78da5b;
  color: #000;
  font-size: 10px;
  padding: 2px 8px;
  border-radius: 4px;
  text-transform: uppercase;
  font-weight: bold;
}

/* Modified agora fica abaixo do título */
.changed-indicator {
  color: #ff4444;
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: bold;
}

/* Placeholder invisível para manter altura consistente */
.placeholder-badge {
  display: inline-block;
  height: 18px;
  min-height: 18px;
}

.card-body {
  color: #bbb;
  font-size: 14px;
  line-height: 1.5;
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.card-body > p {
  margin: 0;
  flex: 1;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

/* Quest/Rewards sections (formato Dehaka) */
.quest-section,
.rewards-section {
  margin-top: 4px;
}

.quest-section .quest-label {
  margin: 0 0 2px 0;
  color: #ffd700;
  font-weight: bold;
  font-size: 14px;
}

.quest-section .quest-text {
  margin: 0;
  color: #bbb;
  font-size: 14px;
  line-height: 1.5;
}

.reward-item {
  margin: 4px 0 0 0;
  color: #bbb;
  font-size: 14px;
  line-height: 1.5;
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.reward-label {
  color: #ffd700;
  font-weight: bold;
}

.reward-text {
  color: #bbb;
}

.repeatable-quest-label {
  color: #ffaa00;
  font-weight: bold;
  display: inline;
}

/* Estilos para quest/reward labels dentro do card */
.card-body :deep(.quest-label),
.card-body :deep(.reward-label),
.card-body :deep(.repeatable-quest-label) {
  color: #ffd700;
  font-weight: bold;
}

.card-body :deep(.mythic-label) {
  color: #c77dff;
  font-weight: bold;
}

.card-body :deep(.repeatable-quest-label) {
  color: #ffaa00;
}

/* ===========================================
   RESPONSIVE STYLES
   =========================================== */

/* Tablet */
@media (max-width: 991px) {
  .talent-card {
    padding: 12px;
    width: 240px;
    min-height: 140px;
  }
  
  .card-header {
    gap: 10px;
    margin-bottom: 10px;
  }
  
  .card-header img {
    width: 40px;
    height: 40px;
  }
  
  .card-title h4 {
    font-size: 14px;
    margin-bottom: 4px;
  }
  
  .selected-badge {
    font-size: 10px;
    padding: 2px 8px;
  }
  
  .placeholder-badge {
    height: 18px;
    min-height: 18px;
  }
  
  .card-body {
    font-size: 12px;
    line-height: 1.4;
  }
  
  .card-body > p {
    -webkit-line-clamp: 2;
  }
  
  .quest-section .quest-label,
  .quest-section .quest-text,
  .reward-item,
  .reward-label,
  .reward-text {
    font-size: 12px;
    line-height: 1.4;
  }
}

/* Mobile */
@media (max-width: 767px) {
  .talent-card {
    padding: 10px;
    width: 200px;
    min-height: 120px;
  }
  
  .card-header {
    gap: 8px;
    margin-bottom: 8px;
  }
  
  .card-header img {
    width: 36px;
    height: 36px;
    border-radius: 6px;
  }
  
  .card-title h4 {
    font-size: 12px;
    margin-bottom: 3px;
  }
  
  .selected-badge {
    font-size: 9px;
    padding: 2px 6px;
  }
  
  .placeholder-badge {
    height: 16px;
    min-height: 16px;
  }
  
  .card-body {
    font-size: 11px;
    line-height: 1.4;
  }
  
  .quest-section .quest-label,
  .quest-section .quest-text,
  .reward-item,
  .reward-label,
  .reward-text {
    font-size: 11px;
    line-height: 1.4;
  }
  
  .changed-indicator {
    font-size: 9px;
    letter-spacing: 0.5px;
  }
}

/* Small Mobile */
@media (max-width: 480px) {
  .talent-card {
    width: 180px;
    min-height: 110px;
    padding: 8px;
  }
  
  .card-header img {
    width: 32px;
    height: 32px;
  }
  
  .card-title h4 {
    font-size: 11px;
  }
  
  .quest-section .quest-label,
  .quest-section .quest-text,
  .reward-item,
  .reward-label,
  .reward-text {
    font-size: 10px;
    line-height: 1.3;
  }
}
</style>
