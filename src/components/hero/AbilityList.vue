<template>
  <div class="abilities-panel">
    <h2 class="panel-title">Abilities</h2>
    <div ref="scrollContainer" class="abilities-vertical" :class="{ 'has-overflow': hasOverflow }">
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
import { computed, ref, onMounted, onUpdated, onUnmounted, nextTick } from 'vue'
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
      image: props.abilities.general.image || props.heroPortraitPath,
      isChanged: props.abilities.general.talentChanged || props.abilities.general.abilityChanged,
      type: 'base'
    })
  }
  
  return list
})

const getAbilityAtIndex = (index) => {
  return abilityList.value[index] || null
}

// Detect overflow to show scrollbar only when needed
const scrollContainer = ref(null)
const hasOverflow = ref(false)

let checkTimeout = null

const checkOverflow = () => {
  if (scrollContainer.value) {
    const el = scrollContainer.value
    hasOverflow.value = el.scrollHeight > el.clientHeight + 1 // +1px tolerance
  }
}

const debouncedCheck = () => {
  clearTimeout(checkTimeout)
  checkTimeout = setTimeout(checkOverflow, 50)
}

onMounted(() => {
  // Initial checks with delay to ensure DOM is ready
  setTimeout(checkOverflow, 100)
  setTimeout(checkOverflow, 300) // Double check after images load
  
  // Listen for window resize
  window.addEventListener('resize', debouncedCheck)
})

onUpdated(() => {
  nextTick(checkOverflow)
})

onUnmounted(() => {
  window.removeEventListener('resize', debouncedCheck)
  clearTimeout(checkTimeout)
})
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
  gap: 6px;
  flex: 1;
  justify-content: flex-start;
  min-height: 0;
  overflow-y: hidden;
  overflow-x: hidden;
}

/* Show scrollbar only when there's overflow */
.abilities-vertical.has-overflow {
  overflow-y: auto;
}

/* Firefox scrollbar */
.abilities-vertical.has-overflow {
  scrollbar-width: thin;
  scrollbar-color: #444 transparent;
}

/* Webkit scrollbar - only visible when has-overflow */
.abilities-vertical.has-overflow::-webkit-scrollbar {
  width: 6px;
}

.abilities-vertical.has-overflow::-webkit-scrollbar-track {
  background: transparent;
}

.abilities-vertical.has-overflow::-webkit-scrollbar-thumb {
  background: #444;
  border-radius: 3px;
}

.ability-placeholder {
  height: 0;
  min-height: 0;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.02);
  border: 2px dashed rgba(255, 255, 255, 0.05);
  flex-shrink: 0;
  opacity: 0;
}

/* ===========================================
   RESPONSIVE STYLES
   =========================================== */

/* Tablet - Abilities em grid de 3 colunas bem distribuído */
@media (max-width: 991px) {
  .abilities-panel {
    flex-direction: column;
    gap: 8px;
    height: 100%;
    overflow: hidden;
    padding: 10px;
  }
  
  .panel-title {
    font-size: 12px;
    margin-bottom: 6px;
    padding-bottom: 6px;
    flex-shrink: 0;
    text-align: center;
  }
  
  /* Grid de 3 colunas x 3 linhas - com altura mínima para ícones */
  .abilities-vertical {
    display: grid !important;
    grid-template-columns: repeat(3, 1fr) !important;
    grid-template-rows: repeat(3, minmax(70px, 1fr)) !important;
    gap: 10px;
    overflow: hidden;
    height: auto;
    min-height: 0;
    padding: 2px;
  }
  
  .ability-placeholder {
    height: 100%;
    min-height: 70px;
    width: 100%;
    min-width: 0;
    border-radius: 10px;
  }
}

/* Mobile - Abilities em grid de 3 colunas compacto */
@media (max-width: 767px) {
  .abilities-panel {
    flex-direction: column;
    padding: 10px;
  }
  
  .panel-title {
    font-size: 12px;
    margin-bottom: 8px;
    padding-bottom: 8px;
  }
  
  /* Grid de 3 colunas (3-3-3) - altura fixa para evitar células gigantes */
  .abilities-vertical {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: repeat(3, 90px);
    gap: 8px;
    overflow: visible;
    height: auto;
    min-height: auto;
    align-items: center;
    justify-items: center;
  }
  
  .ability-placeholder {
    height: 100%;
    min-height: 90px;
    width: 100%;
    border-radius: 10px;
  }
}

/* Small Mobile - Grid mais compacto */
@media (max-width: 480px) {
  .abilities-panel {
    padding: 8px;
  }
  
  .abilities-vertical {
    grid-template-columns: repeat(3, 1fr);
    gap: 6px;
  }
  
  .ability-placeholder {
    min-height: 50px;
    border-radius: 8px;
  }
}
</style>
