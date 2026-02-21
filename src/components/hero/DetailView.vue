<template>
  <!-- Ability Detail View -->
  <div v-if="selectedAbility && !selectedTalent" class="ability-detail-view">
    <div class="detail-header">
      <img :src="abilityImage" class="detail-icon" :class="abilityIconClass">
      <div class="detail-title">
        <h3>{{ selectedAbility.name }}</h3>
        <span class="detail-type">{{ abilityTypeLabel }}</span>
      </div>
    </div>
    
    <div class="detail-stats" v-if="selectedAbility.cooldown || selectedAbility.manaCost">
      <span v-if="selectedAbility.cooldown" class="detail-stat">
        <span class="stat-label">Cooldown:</span> <span v-html="formatText(selectedAbility.cooldown)"></span>
      </span>
      <span v-if="selectedAbility.manaCost" class="detail-stat">
        <span class="stat-label">Mana Cost:</span> <span v-html="formatText(selectedAbility.manaCost)"></span>
      </span>
    </div>

    <div class="detail-scrollable">
      <p class="detail-description" v-html="formattedDescription"></p>

      <div v-if="hasChanges" class="detail-extra changes">
        <h4>Change Details</h4>
        <ul>
          <li v-for="(sub, i) in selectedAbility.subtexts" :key="i"><RichText v-if="findAbilityOrTalent" :text="sub" :convert-fn="findAbilityOrTalent" /></li>
        </ul>
      </div>
    </div>
  </div>

  <!-- Talent Detail View -->
  <div v-else-if="selectedTalent" class="talent-detail-view">
    <div class="detail-header">
      <img :src="talentImage" class="detail-icon">
      <div class="detail-title">
        <h3>{{ selectedTalent.name }}</h3>
        <span class="detail-level">Level {{ selectedLevel }} Talent</span>
      </div>
    </div>
    
    <div class="detail-stats" v-if="selectedTalent.cooldown || selectedTalent.manaCost">
      <span v-if="selectedTalent.cooldown" class="detail-stat">
        <span class="stat-label">Cooldown:</span> <span v-html="formatText(selectedTalent.cooldown)"></span>
      </span>
      <span v-if="selectedTalent.manaCost" class="detail-stat">
        <span class="stat-label">Mana Cost:</span> <span v-html="formatText(selectedTalent.manaCost)"></span>
      </span>
    </div>

    <div class="detail-scrollable">
      <p class="detail-description" v-html="formattedTalentDescription"></p>

      <div v-if="selectedTalent.passives?.length" class="detail-extra passives">
        <h4>Passive</h4>
        <ul>
          <li v-for="(passive, i) in selectedTalent.passives" :key="i" v-html="formatText(passive)"></li>
        </ul>
      </div>
      <div v-if="hasTalentChanges" class="detail-extra changes">
        <h4>Change Details</h4>
        <ul>
          <li v-for="(sub, i) in selectedTalent.subtexts" :key="i"><RichText v-if="findAbilityOrTalent" :text="sub" :convert-fn="findAbilityOrTalent" /></li>
        </ul>
      </div>
    </div>
  </div>

  <!-- Hero Developer Commentary View -->
  <div v-else-if="showHeroComment && heroDevComment" class="hero-comment-view">
    <div class="detail-header">
      <img :src="heroPortraitPath" class="detail-icon base-border">
      <div class="detail-title">
        <h3>{{ heroDisplayName }}</h3>
        <span class="detail-type">Developer Commentary</span>
      </div>
    </div>
    
    <div class="detail-scrollable">
      <div class="hero-comment-content">
        <p><RichText v-if="findAbilityOrTalent" :text="heroDevComment" :convert-fn="findAbilityOrTalent" /></p>
      </div>
    </div>
  </div>

  <!-- Placeholder -->
  <div v-else class="empty-placeholder">
    <p>Select an ability or talent to view details</p>
    <p class="hint">Double-click to toggle developer comments</p>
  </div>
</template>

<script setup>
/* eslint-disable no-undef */
import { computed, inject } from 'vue'
import RichText from '@/components/RichText.vue'

const props = defineProps({
  selectedAbility: { type: Object, default: null },
  selectedTalent: { type: Object, default: null },
  selectedLevel: { type: Number, default: 1 },
  abilities: { type: Object, default: () => ({}) },
  talentType: { type: String, default: 'modified' },
  showHeroComment: { type: Boolean, default: false },
  heroDevComment: { type: String, default: null }
})

const heroName = inject('heroName')
const heroPortraitPath = inject('heroPortraitPath')
const formatText = inject('formatText')
const findAbilityOrTalent = inject('findAbilityOrTalent', () => null)
const getTalentImagePath = inject('getTalentImagePath', null)

const heroDisplayName = computed(() => {
  if (!heroName.value) return ''
  return heroName.value.charAt(0).toUpperCase() + heroName.value.slice(1)
})

const abilityImage = computed(() => {
  if (!props.selectedAbility) return ''
  if (props.abilities?.general === props.selectedAbility) {
    // If general has its own image defined, try to use it
    if (props.selectedAbility.image) {
      const imagePath = getTalentImagePath 
        ? getTalentImagePath(heroName.value, props.selectedAbility.image)
        : `talents/${heroName.value}/${props.selectedAbility.image}`
      return imagePath || heroPortraitPath.value
    }
    return heroPortraitPath.value
  }
  try {
    const imagePath = getTalentImagePath
      ? getTalentImagePath(heroName.value, props.selectedAbility.image)
      : `talents/${heroName.value}/${props.selectedAbility.image}`
    return imagePath
  } catch {
    return ''
  }
})

const abilityIconClass = computed(() => {
  if (!props.abilities) return 'basic-border'
  if (props.abilities.trait === props.selectedAbility) return 'trait-border'
  if (props.abilities.heroic?.includes(props.selectedAbility)) return 'heroic-border'
  if (props.abilities.general === props.selectedAbility) return 'base-border'
  return 'basic-border'
})

const abilityTypeLabel = computed(() => {
  if (!props.abilities) return 'Ability'
  if (props.abilities.trait === props.selectedAbility) return 'Trait'
  if (props.abilities.heroic?.includes(props.selectedAbility)) return 'Heroic Ability'
  if (props.abilities.general === props.selectedAbility) return 'Base Change'
  return 'Basic Ability'
})

const hasChanges = computed(() => 
  props.talentType === 'modified' && props.selectedAbility?.subtexts?.length
)

const talentImage = computed(() => {
  if (!props.selectedTalent?.image) return ''
  if (getTalentImagePath) {
    return getTalentImagePath(heroName.value, props.selectedTalent.image)
  }
  return `talents/${heroName.value}/${props.selectedTalent.image}`
})

const hasTalentChanges = computed(() => 
  props.talentType === 'modified' && props.selectedTalent?.subtexts?.length
)

const formattedDescription = computed(() => formatText(props.selectedAbility?.description))

// Junta descrição + quest + rewards no mesmo formato do Tissue Regeneration
const formattedTalentDescription = computed(() => {
  if (!props.selectedTalent) return ''
  
  let fullText = props.selectedTalent.description || ''
  
  // Se tiver quest separado, adiciona com tag
  if (props.selectedTalent.quest) {
    if (fullText) fullText += ' '
    fullText += `{quest}Quest:{/quest} ${props.selectedTalent.quest}`
  }
  
  // Se tiver rewards separados, adiciona com tags
  if (props.selectedTalent.rewards?.length) {
    props.selectedTalent.rewards.forEach(reward => {
      if (fullText) fullText += ' '
      fullText += `{reward}Reward:{/reward} ${reward}`
    })
  }
  
  return formatText(fullText)
})

</script>

<style scoped>
.ability-detail-view, .talent-detail-view {
  animation: fadeIn 0.3s;
  height: 100%;
  display: flex;
  flex-direction: column;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.detail-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid #333;
  flex-shrink: 0;
}

.detail-icon {
  width: 60px;
  height: 60px;
  border-radius: 10px;
  object-fit: cover;
  border: 3px solid #0099ff;
  flex-shrink: 0;
}

.detail-icon.basic-border { border-color: #0099ff; }
.detail-icon.heroic-border { border-color: #ff6600; }
.detail-icon.trait-border { border-color: #9900ff; }
.detail-icon.base-border { border-color: #ffaa00; }

.detail-title h3 {
  color: #fff;
  font-size: 22px;
  margin: 0 0 5px 0;
}

.detail-type, .detail-level {
  color: #0099ff;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.detail-stats {
  display: flex;
  gap: 25px;
  margin-bottom: 12px;
  flex-wrap: wrap;
  flex-shrink: 0;
}

.detail-stat {
  color: #aaa;
  font-size: 14px;
}

.stat-label {
  color: #666;
  margin-right: 5px;
}

/* Scrollable content area */
.detail-scrollable {
  flex: 1;
  overflow-y: auto;
  min-height: 100px;
}

.detail-description {
  color: #ddd;
  font-size: 15px;
  line-height: 1.6;
  margin-bottom: 12px;
  white-space: pre-line;
}

.detail-extra {
  margin-top: 12px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 8px;
  border-left: 4px solid #444;
}

.detail-extra h4 {
  font-size: 13px;
  text-transform: uppercase;
  margin-bottom: 8px;
  margin-top: 0;
  letter-spacing: 1px;
}

.detail-extra.quest { border-left-color: #DFCB00; }
.detail-extra.quest h4 { color: #DFCB00; }

.detail-extra.rewards { border-left-color: #78da5b; }
.detail-extra.rewards h4 { color: #78da5b; }

.detail-extra.passives { border-left-color: #9900ff; }
.detail-extra.passives h4 { color: #9900ff; }

.detail-extra.changes { border-left-color: #0099ff; }
.detail-extra.changes h4 { color: #0099ff; }

.detail-extra p, .detail-extra li {
  color: #bbb;
  font-size: 14px;
  line-height: 1.5;
  margin: 0;
}

.detail-extra ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.detail-extra li {
  padding-left: 18px;
  position: relative;
  margin-bottom: 6px;
}

.detail-extra li::before {
  content: "›";
  position: absolute;
  left: 0;
  color: #666;
  font-size: 16px;
}

/* Hero Comment View */
.hero-comment-view {
  animation: fadeIn 0.3s;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.hero-comment-content {
  background: rgba(116, 42, 255, 0.1);
  border-left: 4px solid #742aff;
  padding: 15px;
  border-radius: 0 8px 8px 0;
}

.hero-comment-content p {
  color: #eee;
  font-size: 14px;
  line-height: 1.7;
  font-style: italic;
  margin: 0;
}

.empty-placeholder {
  color: #666;
  text-align: center;
  padding: 40px 20px;
  font-size: 15px;
}

.hint {
  color: #444;
  font-size: 13px;
  margin-top: 8px;
}

/* ===========================================
   RESPONSIVE STYLES
   =========================================== */

/* Tablet */
@media (max-width: 991px) {
  .detail-header {
    gap: 12px;
    margin-bottom: 10px;
    padding-bottom: 10px;
  }
  
  .detail-icon {
    width: 52px;
    height: 52px;
  }
  
  .detail-title h3 {
    font-size: 18px;
  }
  
  .detail-type, .detail-level {
    font-size: 11px;
  }
  
  .detail-stats {
    gap: 15px;
    margin-bottom: 10px;
  }
  
  .detail-stat {
    font-size: 12px;
  }
  
  .detail-description {
    font-size: 13px;
    line-height: 1.5;
  }
  
  .detail-extra {
    padding: 10px;
    margin-top: 10px;
  }
  
  .detail-extra h4 {
    font-size: 11px;
    margin-bottom: 6px;
  }
  
  .detail-extra p, .detail-extra li {
    font-size: 12px;
  }
}

/* Mobile */
@media (max-width: 767px) {
  .detail-header {
    gap: 10px;
    margin-bottom: 8px;
    padding-bottom: 8px;
  }
  
  .detail-icon {
    width: 48px;
    height: 48px;
    border-radius: 8px;
  }
  
  .detail-title h3 {
    font-size: 16px;
    margin-bottom: 3px;
  }
  
  .detail-type, .detail-level {
    font-size: 10px;
    letter-spacing: 0.5px;
  }
  
  .detail-stats {
    gap: 12px;
    margin-bottom: 8px;
  }
  
  .detail-stat {
    font-size: 11px;
  }
  
  .detail-description {
    font-size: 12px;
    line-height: 1.5;
  }
  
  .detail-extra {
    padding: 8px 10px;
    margin-top: 8px;
    border-left-width: 3px;
  }
  
  .detail-extra h4 {
    font-size: 10px;
    margin-bottom: 5px;
  }
  
  .detail-extra p, .detail-extra li {
    font-size: 11px;
    line-height: 1.4;
  }
  
  .detail-extra li {
    padding-left: 14px;
    margin-bottom: 4px;
  }
  
  .empty-placeholder {
    padding: 30px 15px;
    font-size: 13px;
  }
  
  .hint {
    font-size: 11px;
  }
}

/* Small Mobile */
@media (max-width: 480px) {
  .detail-icon {
    width: 44px;
    height: 44px;
  }
  
  .detail-title h3 {
    font-size: 14px;
  }
}
</style>
