<template>
  <span ref="triggerRef" class="ability-ref" @mouseenter="showTooltip" @mouseleave="hideTooltip">
    <img 
      :src="imagePath" 
      :alt="item.name"
      class="ability-icon-small"
      @error="onImageError"
    />
    <span class="ability-name">{{ item.name }}</span>
  </span>
  
  <!-- Tooltip usando Teleport para sair da hierarquia do container -->
  <Teleport to="body">
    <Transition name="tooltip">
      <div 
        v-if="isVisible" 
        ref="tooltipRef"
        class="ability-tooltip" 
        :style="tooltipStyle"
      >
        <div class="tooltip-header">
          <img 
            :src="imagePath" 
            :alt="item.name"
            class="tooltip-icon"
            @error="onImageError"
          />
          <span class="tooltip-name">{{ item.name }}</span>
        </div>
        <div class="tooltip-body" v-if="item.description">
          <p v-html="formattedDescription"></p>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
/* eslint-disable no-undef */
import { ref, computed, inject, nextTick } from 'vue'

const props = defineProps({
  item: { type: Object, required: true },
  heroName: { type: String, default: '' }
})

const currentHeroName = inject('heroName')
const formatText = inject('formatText', (text) => text)

const isVisible = ref(false)
const triggerRef = ref(null)
const tooltipRef = ref(null)
const tooltipPosition = ref({ x: 0, y: 0 })

const targetHeroName = computed(() => {
  // Se foi especificado um herói alvo, usa ele. Senão, usa o herói atual
  return props.heroName || currentHeroName?.value || ''
})

const imagePath = computed(() => {
  if (!targetHeroName.value || !props.item.image) return ''
  try {
    return require(`@/assets/talents/${targetHeroName.value}/${props.item.image}`)
  } catch {
    return ''
  }
})

const formattedDescription = computed(() => {
  return formatText(props.item.description || '')
})

const tooltipStyle = computed(() => {
  return {
    left: `${tooltipPosition.value.x}px`,
    top: `${tooltipPosition.value.y}px`,
    position: 'fixed',
    zIndex: 99999
  }
})

const showTooltip = async () => {
  isVisible.value = true
  // Aguarda o DOM atualizar para calcular a posição
  await nextTick()
  updateTooltipPosition()
}

const hideTooltip = () => {
  isVisible.value = false
}

const updateTooltipPosition = () => {
  if (!triggerRef.value || !tooltipRef.value) return
  
  const triggerRect = triggerRef.value.getBoundingClientRect()
  const tooltipRect = tooltipRef.value.getBoundingClientRect()
  
  // Calcula a posição centralizada acima do elemento
  let x = triggerRect.left + (triggerRect.width / 2) - (tooltipRect.width / 2)
  let y = triggerRect.top - tooltipRect.height - 8
  
  // Garante que não saia da tela pelos lados
  const margin = 10
  if (x < margin) x = margin
  if (x + tooltipRect.width > window.innerWidth - margin) {
    x = window.innerWidth - tooltipRect.width - margin
  }
  
  // Se não couber acima, coloca abaixo
  if (y < margin) {
    y = triggerRect.bottom + 8
  }
  
  tooltipPosition.value = { x, y }
}

const onImageError = (e) => {
  e.target.style.display = 'none'
}
</script>

<style scoped>
.ability-ref {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  color: #0099ff;
  font-weight: 500;
  cursor: pointer;
  vertical-align: middle;
}

.ability-ref:hover {
  color: #33bbff;
}

.ability-icon-small {
  width: 20px;
  height: 20px;
  border-radius: 4px;
  border: 1px solid #444;
  flex-shrink: 0;
}

.ability-name {
  display: inline;
}

/* Tooltip - agora fixo no body */
.ability-tooltip {
  background: rgba(20, 15, 30, 0.98);
  border: 1px solid #444;
  border-radius: 8px;
  padding: 12px;
  min-width: 280px;
  max-width: 320px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.8);
  pointer-events: none;
}

.tooltip-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
  padding-bottom: 8px;
  border-bottom: 1px solid #333;
}

.tooltip-icon {
  width: 40px;
  height: 40px;
  border-radius: 6px;
  border: 2px solid #444;
  flex-shrink: 0;
}

.tooltip-name {
  color: #fff;
  font-size: 14px;
  font-weight: 600;
}

.tooltip-body {
  color: #ccc;
  font-size: 12px;
  line-height: 1.5;
}

.tooltip-body :deep(.highlight-text) {
  color: rgb(209, 119, 119);
}

/* Transição do tooltip */
.tooltip-enter-active,
.tooltip-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.tooltip-enter-from,
.tooltip-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}

/* Responsivo */
@media (max-width: 991px) {
  .ability-tooltip {
    min-width: 240px;
    max-width: 280px;
    padding: 10px;
  }
  
  .tooltip-icon {
    width: 36px;
    height: 36px;
  }
  
  .tooltip-name {
    font-size: 13px;
  }
  
  .tooltip-body {
    font-size: 11px;
  }
}

@media (max-width: 767px) {
  .ability-tooltip {
    min-width: 200px;
    max-width: 260px;
    padding: 8px;
  }
  
  .tooltip-icon {
    width: 32px;
    height: 32px;
  }
  
  .tooltip-name {
    font-size: 12px;
  }
  
  .tooltip-body {
    font-size: 10px;
  }
}
</style>
