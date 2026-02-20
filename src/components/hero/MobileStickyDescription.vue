<template>
  <div class="mobile-sticky-bar">
    <div class="sticky-content">
      <!-- Menu Button - Left side -->
      <button class="menu-btn" @click.stop="$emit('toggle-sidebar')">
        <span class="menu-icon">☰</span>
      </button>
      
      <!-- Icon and Title - Clickable area for expansion -->
      <div class="sticky-main" @click="toggleExpanded">
        <img v-if="iconSrc" :src="iconSrc" class="sticky-icon" :class="iconClass">
        <div class="sticky-info">
          <h4 class="sticky-title">{{ displayTitle }}</h4>
          <span class="sticky-subtitle">{{ displaySubtitle }}</span>
        </div>
        <span class="expand-icon" :class="{ expanded: isExpanded }">▼</span>
      </div>
      
      <!-- Dev Comments Badge -->
      <div v-if="devComment" class="dev-badge" @click.stop="toggleDevComments">
        <span class="dev-icon">💬</span>
        <span class="dev-text">Dev</span>
      </div>
    </div>
    
    <!-- Expanded Content -->
    <div v-show="isExpanded" class="sticky-expanded">
      <div class="expanded-scroll">
        <p class="sticky-description" v-html="formattedDescription"></p>
        
        <!-- Dev Comments Section -->
        <div v-if="showDevComments && devComment" class="sticky-dev-comments">
          <div class="dev-header">
            <span>💬 Developer Commentary</span>
          </div>
          <p><RichText v-if="findAbilityOrTalent" :text="devComment" :convert-fn="findAbilityOrTalent" /></p>
        </div>
        
        <!-- Quest/Rewards/Passives -->
        <div v-if="hasExtras" class="sticky-extras">
          <div v-if="quest" class="extra-section quest">
            <h5>❢ Quest</h5>
            <p v-html="formatText(quest)"></p>
          </div>
          <div v-if="rewards?.length" class="extra-section rewards">
            <h5>❢ Rewards</h5>
            <ul>
              <li v-for="(reward, i) in rewards" :key="i" v-html="formatText(reward)"></li>
            </ul>
          </div>
          <div v-if="passives?.length" class="extra-section passives">
            <h5>Passive</h5>
            <ul>
              <li v-for="(passive, i) in passives" :key="i" v-html="formatText(passive)"></li>
            </ul>
          </div>
          <div v-if="hasChanges" class="extra-section changes">
            <h5>Change Details</h5>
            <ul>
              <li v-for="(sub, i) in subtexts" :key="i" v-html="formatSubtext(sub)"></li>
            </ul>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Empty State - Hidden on mobile (controlled via CSS) -->
    <div v-if="!selectedAbility && !selectedTalent" class="sticky-empty mobile-hidden">
      <span>Select an ability or talent</span>
    </div>
  </div>
</template>

<script setup>
/* eslint-disable no-undef */
import { ref, computed, inject, watch } from 'vue'
import RichText from '@/components/RichText.vue'

const props = defineProps({
  selectedAbility: { type: Object, default: null },
  selectedTalent: { type: Object, default: null },
  selectedLevel: { type: Number, default: 1 },
  abilities: { type: Object, default: () => ({}) },
  talentType: { type: String, default: 'modified' },
  heroDevComment: { type: String, default: null },
  showHeroComment: { type: Boolean, default: false }
})

const heroName = inject('heroName')
const heroPortraitPath = inject('heroPortraitPath')
const formatText = inject('formatText')
const convertTextPlaceholders = inject('convertTextPlaceholders')
const findAbilityOrTalent = inject('findAbilityOrTalent', () => null)

const isExpanded = ref(false)
const showDevComments = ref(false)

// Expande automaticamente quando mostra o comentário do herói
watch(() => props.showHeroComment, (newVal) => {
  if (newVal) {
    isExpanded.value = true
  }
})

const toggleExpanded = () => {
  isExpanded.value = !isExpanded.value
}

const toggleDevComments = () => {
  showDevComments.value = !showDevComments.value
}

const heroDisplayName = computed(() => {
  return heroName.value ? heroName.value.charAt(0).toUpperCase() + heroName.value.slice(1) : ''
})

const iconSrc = computed(() => {
  if (props.showHeroComment) {
    return heroPortraitPath.value
  }
  if (props.selectedAbility) {
    if (props.abilities?.general === props.selectedAbility) {
      return heroPortraitPath.value
    }
    try {
      return require(`@/assets/talents/${heroName.value}/${props.selectedAbility.image}`)
    } catch {
      return ''
    }
  }
  if (props.selectedTalent?.image) {
    try {
      return require(`@/assets/talents/${heroName.value}/${props.selectedTalent.image}`)
    } catch {
      return ''
    }
  }
  return ''
})

const iconClass = computed(() => {
  if (!props.selectedAbility) return ''
  if (props.abilities?.trait === props.selectedAbility) return 'trait-border'
  if (props.abilities?.heroic?.includes(props.selectedAbility)) return 'heroic-border'
  if (props.abilities?.general === props.selectedAbility) return 'base-border'
  return 'basic-border'
})

const displayTitle = computed(() => {
  if (props.showHeroComment) {
    return heroDisplayName.value
  }
  return props.selectedAbility?.name || props.selectedTalent?.name || 'Select Ability/Talent'
})

const displaySubtitle = computed(() => {
  if (props.showHeroComment) {
    return 'Developer Commentary'
  }
  if (props.selectedAbility) {
    if (props.abilities?.trait === props.selectedAbility) return 'Trait'
    if (props.abilities?.heroic?.includes(props.selectedAbility)) return 'Heroic'
    if (props.abilities?.general === props.selectedAbility) return 'Base Changes'
    return 'Basic Ability'
  }
  if (props.selectedTalent) {
    return `Level ${props.selectedLevel} Talent`
  }
  return ''
})

const heroDescription = computed(() => {
  if (props.showHeroComment && props.heroDevComment) {
    return props.heroDevComment
  }
  return null
})

const formattedDescription = computed(() => {
  if (heroDescription.value) {
    return formatText(heroDescription.value)
  }
  const desc = props.selectedAbility?.description || props.selectedTalent?.description || ''
  return formatText(desc)
})

const devComment = computed(() => {
  // Não mostra dev badge quando é comentário do herói (já é o conteúdo principal)
  if (props.showHeroComment) {
    return null
  }
  return props.selectedAbility?.developerCommentary || props.selectedTalent?.developerCommentary
})



const quest = computed(() => props.selectedTalent?.quest)
const rewards = computed(() => props.selectedTalent?.rewards)
const passives = computed(() => props.selectedTalent?.passives)
const subtexts = computed(() => {
  const item = props.selectedAbility || props.selectedTalent
  return item?.subtexts || []
})

const hasChanges = computed(() => 
  props.talentType === 'modified' && subtexts.value.length > 0
)

const hasExtras = computed(() => 
  quest.value || rewards.value?.length || passives.value?.length || hasChanges.value
)

const formatSubtext = (sub) => convertTextPlaceholders(sub)
</script>

<style scoped>
.mobile-sticky-bar {
  position: fixed;
  top: 0; /* Colada no topo */
  left: 0;
  right: 0;
  z-index: 500;
  background: rgba(15, 10, 25, 0.98);
  border-bottom: 2px solid #444;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6);
}

.sticky-content {
  display: flex;
  align-items: center;
  padding: 10px 15px;
  min-height: 50px;
  gap: 12px;
}

/* Menu Button */
.menu-btn {
  background: rgba(116, 42, 255, 0.2);
  border: 1px solid #742aff;
  border-radius: 6px;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  flex-shrink: 0;
  transition: background 0.2s;
}

.menu-btn:hover {
  background: rgba(116, 42, 255, 0.4);
}

.menu-icon {
  color: #fff;
  font-size: 18px;
  line-height: 1;
}

.sticky-main {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
  min-width: 0;
}

.sticky-icon {
  width: 44px;
  height: 44px;
  border-radius: 8px;
  object-fit: cover;
  border: 2px solid #0099ff;
  flex-shrink: 0;
}

.sticky-icon.basic-border { border-color: #0099ff; }
.sticky-icon.heroic-border { border-color: #ff6600; }
.sticky-icon.trait-border { border-color: #9900ff; }
.sticky-icon.base-border { border-color: #ffaa00; }

.sticky-info {
  flex: 1;
  min-width: 0;
  overflow: hidden;
}

.sticky-title {
  color: #fff;
  font-size: 15px;
  font-weight: 600;
  margin: 0 0 3px 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sticky-subtitle {
  color: #0099ff;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.expand-icon {
  color: #888;
  font-size: 12px;
  transition: transform 0.2s;
  margin-left: 10px;
  flex-shrink: 0;
}

.expand-icon.expanded {
  transform: rotate(180deg);
}

/* Dev Comments Badge */
.dev-badge {
  display: flex;
  align-items: center;
  gap: 4px;
  background: #742aff;
  padding: 6px 10px;
  border-radius: 16px;
  margin-left: 10px;
  flex-shrink: 0;
  cursor: pointer;
  transition: background 0.2s;
}

.dev-badge:hover {
  background: #9933ff;
}

.dev-icon {
  font-size: 12px;
}

.dev-text {
  color: #fff;
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
}

/* Expanded Content */
.sticky-expanded {
  max-height: 40vh;
  overflow-y: auto;
  border-top: 1px solid #333;
  background: rgba(0, 0, 0, 0.5);
}

.expanded-scroll {
  padding: 15px;
}

.sticky-description {
  color: #ddd;
  font-size: 13px;
  line-height: 1.6;
  margin: 0 0 12px 0;
}

/* Dev Comments in expanded */
.sticky-dev-comments {
  background: rgba(116, 42, 255, 0.15);
  border-left: 3px solid #742aff;
  padding: 12px;
  border-radius: 0 8px 8px 0;
  margin-bottom: 12px;
}

.dev-header {
  color: #b88aff;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 6px;
}

.sticky-dev-comments p {
  color: #eee;
  font-size: 12px;
  line-height: 1.5;
  font-style: italic;
  margin: 0;
}

/* Extras Section */
.sticky-extras {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.extra-section {
  padding: 10px;
  border-radius: 6px;
  border-left: 3px solid #444;
  background: rgba(255, 255, 255, 0.03);
}

.extra-section h5 {
  font-size: 10px;
  text-transform: uppercase;
  margin: 0 0 6px 0;
  letter-spacing: 0.5px;
}

.extra-section p,
.extra-section li {
  font-size: 12px;
  line-height: 1.4;
  margin: 0;
  color: #bbb;
}

.extra-section ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.extra-section li {
  padding-left: 14px;
  position: relative;
  margin-bottom: 4px;
}

.extra-section li::before {
  content: "›";
  position: absolute;
  left: 0;
  color: #666;
}

.extra-section.quest { border-left-color: #DFCB00; }
.extra-section.quest h5 { color: #DFCB00; }

.extra-section.rewards { border-left-color: #78da5b; }
.extra-section.rewards h5 { color: #78da5b; }

.extra-section.passives { border-left-color: #9900ff; }
.extra-section.passives h5 { color: #9900ff; }

.extra-section.changes { border-left-color: #0099ff; }
.extra-section.changes h5 { color: #0099ff; }

/* Empty State */
.sticky-empty {
  padding: 15px;
  text-align: center;
  color: #666;
  font-size: 13px;
}

/* Only show on mobile */
@media (min-width: 768px) {
  .mobile-sticky-bar {
    display: none;
  }
}

/* Esconde empty state no mobile */
@media (max-width: 767px) {
  .sticky-empty.mobile-hidden {
    display: none;
  }
}

/* Small mobile adjustments */
@media (max-width: 480px) {
  .sticky-content {
    padding: 8px 12px;
    min-height: 54px;
  }
  
  .sticky-icon {
    width: 38px;
    height: 38px;
  }
  
  .sticky-title {
    font-size: 14px;
  }
  
  .sticky-subtitle {
    font-size: 10px;
  }
  
  .dev-badge {
    padding: 5px 8px;
  }
  
  .dev-text {
    font-size: 9px;
  }
  
  .expanded-scroll {
    padding: 12px;
  }
  
  .sticky-description {
    font-size: 12px;
  }
}
</style>
