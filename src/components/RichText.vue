<template>
  <span class="rich-text">
    <template v-for="(segment, index) in parsedSegments" :key="index">
      <template v-if="segment.type === 'text'">{{ segment.content }}</template>
      <AbilityTooltip 
        v-else-if="segment.type === 'ref'" 
        :item="segment.item"
        :hero-name="segment.heroName"
      />
    </template>
  </span>
</template>

<script setup>
/* eslint-disable no-undef */
import { computed } from 'vue'
import AbilityTooltip from './AbilityTooltip.vue'

const props = defineProps({
  text: { type: String, default: '' },
  convertFn: { type: Function, required: true }
})

const parsedSegments = computed(() => {
  if (!props.text) return []
  
  // Regex para encontrar referências: <type, section, category, index, targetHero?>
  const regex = /<([^,]+),\s*([^,]+),\s*([^,]+),\s*(\d+)(?:,\s*([^>]+))?>/g
  const segments = []
  let lastIndex = 0
  let match
  
  while ((match = regex.exec(props.text)) !== null) {
    // Texto antes da referência
    if (match.index > lastIndex) {
      segments.push({
        type: 'text',
        content: props.text.slice(lastIndex, match.index)
      })
    }
    
    // A referência em si
    const [, type, section, category, index, targetHero] = match
    const item = props.convertFn(type, section, category, parseInt(index, 10), targetHero)
    
    if (item) {
      segments.push({
        type: 'ref',
        item,
        heroName: targetHero || ''
      })
    } else {
      segments.push({
        type: 'text',
        content: match[0]
      })
    }
    
    lastIndex = match.index + match[0].length
  }
  
  // Texto restante após a última referência
  if (lastIndex < props.text.length) {
    segments.push({
      type: 'text',
      content: props.text.slice(lastIndex)
    })
  }
  
  return segments
})
</script>

<style scoped>
.rich-text {
  display: inline;
}
</style>
