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

const isNotSelected = computed(() => !props.isSelected && props.hasSelection)

const imagePath = computed(() => {
  try {
    return require(`@/assets/talents/${heroName.value}/${props.talent.image}`)
  } catch {
    return ''
  }
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
</style>
