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
        <span v-if="isSelected" class="selected-badge">Selected</span>
        <span v-else class="placeholder-badge"></span>
      </div>
    </div>
    <div class="card-body">
      <p v-html="formattedDescription"></p>
    </div>
    <!-- Sempre renderiza o footer, mesmo que vazio, para manter altura consistente -->
    <div class="card-footer">
      <span v-if="talent.talentChanged" class="changed-indicator">Modified</span>
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

const imagePath = computed(() => {
  try {
    return require(`@/assets/talents/${heroName.value}/${props.talent.image}`)
  } catch {
    return ''
  }
})

const formattedDescription = computed(() => formatText(props.talent.description))
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
  margin: 0 0 6px 0;
  line-height: 1.3;
}

.selected-badge {
  display: inline-block;
  background: #78da5b;
  color: #000;
  font-size: 11px;
  padding: 3px 10px;
  border-radius: 4px;
  text-transform: uppercase;
  font-weight: bold;
}

/* Placeholder invisível para manter altura consistente */
.placeholder-badge {
  display: inline-block;
  height: 21px; /* Mesma altura do selected-badge */
  min-height: 21px;
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

.card-body p {
  margin: 0;
  flex: 1;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

/* Footer sempre presente para manter altura consistente */
.card-footer {
  height: 24px;
  min-height: 24px;
  margin-top: 8px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
}

.changed-indicator {
  color: #ff4444;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: bold;
}
</style>
