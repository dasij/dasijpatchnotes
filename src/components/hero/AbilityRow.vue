<template>
  <div
    class="ability-row"
    :class="[type, { active: isSelected, changed: isChanged }]"
    @click="$emit('select')"
    @dblclick="$emit('toggleDevComments')"
  >
    <div class="ability-icon">
      <img :src="displayImage" :alt="displayName">
      <span class="key-bind">{{ keyBind }}</span>
    </div>
    <span class="ability-name-small">{{ displayName }}</span>
  </div>
</template>

<script setup>
/* eslint-disable no-undef */
import { computed, inject } from 'vue'

const props = defineProps({
  ability: { type: Object, required: true },
  name: { type: String, default: null },
  keyBind: { type: String, required: true },
  image: { type: String, default: null },
  isSelected: { type: Boolean, default: false },
  isChanged: { type: Boolean, default: false },
  type: { type: String, default: 'basic' }
})

defineEmits(['select', 'toggleDevComments'])

const heroName = inject('heroName')

const displayName = computed(() => props.name || props.ability.name)

const displayImage = computed(() => {
  if (props.image) return props.image
  if (!props.ability.image) return ''
  try {
    return require(`@/assets/talents/${heroName.value}/${props.ability.image}`)
  } catch {
    return ''
  }
})
</script>

<style scoped>
.ability-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
  border: 2px solid transparent;
  background: rgba(255, 255, 255, 0.03);
}

.ability-row:hover {
  background: rgba(255, 255, 255, 0.08);
  transform: translateX(5px);
}

.ability-row.active {
  border-color: #0099ff;
  background: rgba(0, 153, 255, 0.15);
  box-shadow: 0 0 15px rgba(0, 153, 255, 0.3);
}

.ability-row.changed {
  border-left: 4px solid #ff4444;
}

.ability-row.heroic.active {
  border-color: #ff6600;
  background: rgba(255, 102, 0, 0.15);
  box-shadow: 0 0 15px rgba(255, 102, 0, 0.3);
}

.ability-row.trait.active {
  border-color: #9900ff;
  background: rgba(153, 0, 255, 0.15);
  box-shadow: 0 0 15px rgba(153, 0, 255, 0.3);
}

.ability-row.base.active {
  border-color: #ffaa00;
  background: rgba(255, 170, 0, 0.15);
  box-shadow: 0 0 15px rgba(255, 170, 0, 0.3);
}

.ability-icon {
  position: relative;
  width: 56px;
  height: 56px;
  border-radius: 10px;
  overflow: hidden;
  border: 2px solid #444;
  flex-shrink: 0;
  background: #222;
}

.ability-icon img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.key-bind {
  position: absolute;
  bottom: 2px;
  right: 2px;
  background: rgba(0, 0, 0, 0.9);
  color: #fff;
  font-size: 10px;
  padding: 2px 5px;
  border-radius: 3px;
  font-weight: bold;
  border: 1px solid rgba(255,255,255,0.2);
}

.ability-name-small {
  color: #ccc;
  font-size: 12px;
  font-weight: 500;
  line-height: 1.3;
  flex: 1;
}

.ability-row.active .ability-name-small {
  color: #fff;
}
</style>
