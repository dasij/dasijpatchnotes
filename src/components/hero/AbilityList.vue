<template>
  <div class="abilities-panel">
    <h2 class="panel-title">Abilities</h2>
    <div class="abilities-vertical">
      <!-- Render exactly 9 slots, fill with actual abilities or placeholders -->
      <template v-for="index in 9" :key="index">
        <!-- Actual abilities -->
        <AbilityRow
          v-if="getAbilityAtIndex(index - 1)"
          :ability="getAbilityAtIndex(index - 1).ability"
          :name="getAbilityAtIndex(index - 1).name"
          :key-bind="getAbilityAtIndex(index - 1).keyBind"
          :image="getAbilityAtIndex(index - 1).image"
          :is-selected="selectedAbility === getAbilityAtIndex(index - 1).ability"
          :is-changed="getAbilityAtIndex(index - 1).isChanged"
          :type="getAbilityAtIndex(index - 1).type"
          @select="$emit('select', getAbilityAtIndex(index - 1).ability)"
          @toggle-dev-comments="$emit('toggleDevComments')"
        />
        <!-- Placeholder for empty slots -->
        <div v-else class="ability-placeholder"></div>
      </template>
    </div>
  </div>
</template>

<script setup>
/* eslint-disable no-undef */
import { computed } from 'vue'
import AbilityRow from './AbilityRow.vue'

const props = defineProps({
  abilities: { type: Object, default: () => ({}) },
  selectedAbility: { type: Object, default: null },
  heroPortraitPath: { type: String, default: '' }
})

defineEmits(['select', 'toggleDevComments'])

// Build a flat list of exactly 9 ability slots
const abilityList = computed(() => {
  const list = []
  
  // Basic Abilities (Q, W, E) - max 3
  if (props.abilities?.basic) {
    props.abilities.basic.forEach((ability, index) => {
      list.push({
        ability,
        name: ability.name,
        keyBind: ['Q','W','E'][index],
        image: null,
        isChanged: ability.abilityChanged,
        type: 'basic'
      })
    })
  }
  
  // Heroic Abilities (R1, R2) - max 2
  if (props.abilities?.heroic) {
    props.abilities.heroic.forEach((ability, index) => {
      list.push({
        ability,
        name: ability.name,
        keyBind: index === 0 ? 'R1' : 'R2',
        image: null,
        isChanged: ability.abilityChanged,
        type: 'heroic'
      })
    })
  }
  
  // Trait (T) - 1
  if (props.abilities?.trait) {
    list.push({
      ability: props.abilities.trait,
      name: props.abilities.trait.name,
      keyBind: 'T',
      image: null,
      isChanged: props.abilities.trait.abilityChanged,
      type: 'trait'
    })
  }
  
  // Base/General (B) - 1
  if (props.abilities?.general) {
    list.push({
      ability: props.abilities.general,
      name: 'Base Changes',
      keyBind: 'B',
      image: props.heroPortraitPath,
      isChanged: props.abilities.general.talentChanged || props.abilities.general.abilityChanged,
      type: 'base'
    })
  }
  
  return list
})

const getAbilityAtIndex = (index) => {
  return abilityList.value[index] || null
}
</script>

<style scoped>
.abilities-panel {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.panel-title {
  color: #fff;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 2px;
  margin-bottom: 15px;
  text-align: center;
  border-bottom: 1px solid #444;
  padding-bottom: 10px;
  flex-shrink: 0;
}

.abilities-vertical {
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1;
  justify-content: flex-start;
}

.ability-placeholder {
  height: 56px;
  min-height: 56px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.02);
  border: 2px dashed rgba(255, 255, 255, 0.05);
}
</style>
