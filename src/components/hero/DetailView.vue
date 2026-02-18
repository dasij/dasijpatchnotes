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
        <span class="stat-label">Cooldown:</span> {{ selectedAbility.cooldown }}
      </span>
      <span v-if="selectedAbility.manaCost" class="detail-stat">
        <span class="stat-label">Mana Cost:</span> {{ selectedAbility.manaCost }}
      </span>
    </div>

    <div class="detail-scrollable">
      <p class="detail-description" v-html="formattedDescription"></p>

      <div v-if="hasChanges" class="detail-extra changes">
        <h4>Change Details</h4>
        <ul>
          <li v-for="(sub, i) in selectedAbility.subtexts" :key="i" v-html="formatSubtext(sub)"></li>
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
        <span class="stat-label">Cooldown:</span> {{ selectedTalent.cooldown }}
      </span>
      <span v-if="selectedTalent.manaCost" class="detail-stat">
        <span class="stat-label">Mana Cost:</span> {{ selectedTalent.manaCost }}
      </span>
    </div>

    <div class="detail-scrollable">
      <p class="detail-description" v-html="formattedTalentDescription"></p>

      <div v-if="selectedTalent.quest" class="detail-extra quest">
        <h4>❢ Quest</h4>
        <p v-html="formatText(selectedTalent.quest)"></p>
      </div>
      <div v-if="selectedTalent.rewards?.length" class="detail-extra rewards">
        <h4>❢ Rewards</h4>
        <ul>
          <li v-for="(reward, i) in selectedTalent.rewards" :key="i" v-html="formatText(reward)"></li>
        </ul>
      </div>
      <div v-if="selectedTalent.passives?.length" class="detail-extra passives">
        <h4>Passive</h4>
        <ul>
          <li v-for="(passive, i) in selectedTalent.passives" :key="i" v-html="formatText(passive)"></li>
        </ul>
      </div>
      <div v-if="hasTalentChanges" class="detail-extra changes">
        <h4>Change Details</h4>
        <ul>
          <li v-for="(sub, i) in selectedTalent.subtexts" :key="i" v-html="formatSubtext(sub)"></li>
        </ul>
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

const props = defineProps({
  selectedAbility: { type: Object, default: null },
  selectedTalent: { type: Object, default: null },
  selectedLevel: { type: Number, default: 1 },
  abilities: { type: Object, default: () => ({}) },
  talentType: { type: String, default: 'modified' }
})

const heroName = inject('heroName')
const heroPortraitPath = inject('heroPortraitPath')
const formatText = inject('formatText')
const convertTextPlaceholders = inject('convertTextPlaceholders')

const abilityImage = computed(() => {
  if (!props.selectedAbility) return ''
  if (props.abilities?.general === props.selectedAbility) {
    return heroPortraitPath.value
  }
  try {
    return require(`@/assets/talents/${heroName.value}/${props.selectedAbility.image}`)
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
  try {
    return require(`@/assets/talents/${heroName.value}/${props.selectedTalent.image}`)
  } catch {
    return ''
  }
})

const hasTalentChanges = computed(() => 
  props.talentType === 'modified' && props.selectedTalent?.subtexts?.length
)

const formattedDescription = computed(() => formatText(props.selectedAbility?.description))
const formattedTalentDescription = computed(() => formatText(props.selectedTalent?.description))
const formatSubtext = (sub) => convertTextPlaceholders(sub)
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
</style>
