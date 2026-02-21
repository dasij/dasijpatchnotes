<template>
  <div
    class="talent-node"
    :class="{ 
      selected: isSelected, 
      'not-selected': isNotSelected,
      active: isActive,
      changed: talent.talentChanged
    }"
    @click="$emit('click')"
    @dblclick="$emit('dblclick')"
  >
    <img :src="imagePath" :alt="talent.name">
    <div v-if="isSelected" class="checkmark">✓</div>
  </div>
</template>

<script setup>
/* eslint-disable no-undef */
import { computed, inject } from 'vue'

const props = defineProps({
  talent: { type: Object, required: true },
  isSelected: { type: Boolean, default: false },
  isActive: { type: Boolean, default: false },
  hasSelection: { type: Boolean, default: false }
})

defineEmits(['click', 'dblclick'])

const heroName = inject('heroName')
const getTalentImagePath = inject('getTalentImagePath', null)

const isNotSelected = computed(() => !props.isSelected && props.hasSelection)

const imagePath = computed(() => {
  if (!props.talent?.image) return ''
  if (getTalentImagePath) {
    return getTalentImagePath(heroName.value, props.talent.image)
  }
  return `talents/${heroName.value}/${props.talent.image}`
})
</script>

<style scoped>
.talent-node {
  position: relative;
  width: 56px;
  height: 56px;
  border-radius: 10px;
  overflow: hidden;
  border: 2px solid #444;
  cursor: pointer;
  transition: all 0.2s;
  opacity: 0.7;
  flex-shrink: 0;
}

.talent-node img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.talent-node:hover {
  opacity: 1;
  transform: scale(1.05);
  border-color: #0099ff;
}

.talent-node.selected {
  border-color: #78da5b;
  opacity: 1;
  box-shadow: 0 0 12px rgba(120, 218, 91, 0.5);
}

.talent-node.not-selected {
  opacity: 0.3;
}

.talent-node.active {
  border-color: #0099ff;
  box-shadow: 0 0 18px rgba(0, 153, 255, 0.7);
  opacity: 1;
}

.talent-node.changed {
  border-color: #ff4444;
}

.checkmark {
  position: absolute;
  top: -8px;
  right: -8px;
  width: 22px;
  height: 22px;
  background: #78da5b;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #000;
  font-size: 12px;
  font-weight: bold;
  box-shadow: 0 2px 6px rgba(0,0,0,0.4);
  border: 2px solid #000;
}

/* ===========================================
   RESPONSIVE STYLES
   =========================================== */

/* 1280px - Ícones menores */
@media (max-width: 1280px) {
  .talent-node {
    width: 48px;
    height: 48px;
  }
}

/* 1200px - Ícones ainda menores */
@media (max-width: 1200px) {
  .talent-node {
    width: 44px;
    height: 44px;
  }
  
  .checkmark {
    width: 18px;
    height: 18px;
    font-size: 10px;
    top: -6px;
    right: -6px;
  }
}

/* Tablet - Ícones menores */
@media (max-width: 991px) {
  .talent-node {
    width: 36px;
    height: 36px;
    border-radius: 6px;
  }
  
  .checkmark {
    width: 14px;
    height: 14px;
    font-size: 9px;
    top: -5px;
    right: -5px;
  }
}

/* Mobile - Ícones maiores */
@media (max-width: 767px) {
  .talent-node {
    width: 64px;
    height: 64px;
    border-radius: 12px;
    border-width: 2px;
  }
  
  .checkmark {
    width: 24px;
    height: 24px;
    font-size: 12px;
    top: -8px;
    right: -8px;
    border-width: 2px;
  }
}

/* Small Mobile */
@media (max-width: 480px) {
  .talent-node {
    width: 48px;
    height: 48px;
    border-radius: 8px;
  }
  
  .checkmark {
    width: 18px;
    height: 18px;
    font-size: 10px;
    top: -6px;
    right: -6px;
  }
}
</style>
