<template>
  <div class="page-wrapper bg-hots-repeat">
    <MetaTags 
      :title="pageTitle" 
      :description="pageDescription" 
      :image="heroPortraitPath" 
    />

    <!-- LEFT SIDEBAR: Full height fixed -->
    <div class="sidebar-fixed">
      <HeroSidebar
        :selected-hero-name="heroName"
        @select-hero="onSelectHero"
      />
    </div>

    <!-- MAIN CONTENT: Full width with margin for sidebar -->
    <div class="main-content">
      <div v-if="heroName" class="hero-content">
        <!-- Top Section: Abilities | Splash/Details | Talent Tree -->
        <div class="top-section">
          <!-- Abilities Column -->
          <div class="abilities-column">
            <AbilityList
              :abilities="talents.abilities"
              :selected-ability="selectedAbility"
              :hero-portrait-path="heroPortraitPath"
              @select="selectAbility"
              @toggle-dev-comments="toggleDevComments"
            />
          </div>

          <!-- Center Column: Splash & Details -->
          <div class="center-column">
            <div class="center-container">
              <div class="splash-art" :style="splashStyle">
                <div class="hero-overlay"></div>
                
                <div class="splash-header">
                  <h1 class="hero-title">{{ hero.name }}</h1>
                  <TalentTypeToggle
                    v-model="talentType"
                    v-model:dev-comments-always="showDevCommentsAlways"
                    @update:model-value="onTalentTypeChange"
                  />
                </div>
              </div>

              <div class="info-display-box">
                <DevCommentsDrawer
                  :is-open="showDevComments"
                  :comment="activeDevComment"
                  @toggle="toggleDevCommentsPanel"
                />

                <DetailView
                  :selected-ability="selectedAbility"
                  :selected-talent="selectedTalent"
                  :selected-level="selectedTalentLevel"
                  :abilities="talents.abilities"
                  :talent-type="talentType"
                />
              </div>
            </div>
          </div>

          <!-- Talent Tree Column - 15% maior -->
          <div class="talent-tree-column">
            <TalentTree
              :talents="talents"
              :talent-levels="talentLevels"
              :selected-level="selectedTalentLevel"
              :selected-talent="selectedTalent"
              :current-selected-talents="currentSelectedTalents"
              @reset="resetAll"
              @select-level="selectLevel"
              @select-talent="selectTalent"
              @toggle-dev-comments="toggleDevComments"
            />
          </div>
        </div>

        <!-- Bottom Section: Talent Cards -->
        <TalentCards
          :talents="talents"
          :talent-levels="talentLevels"
          :selected-level="selectedTalentLevel"
          :selected-talent="selectedTalent"
          :current-selected-talents="currentSelectedTalents"
          @select-level="selectLevel"
          @select-talent="selectTalent"
          @toggle-dev-comments="toggleDevComments"
        />
      </div>

      <!-- Empty State -->
      <div v-else class="empty-state">
        <div class="empty-message">
          <h2>Select a Hero</h2>
          <p>Choose a hero from the sidebar to view their talents and abilities</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
/* eslint-disable no-undef */
import { ref, computed, watch, provide } from 'vue'
import { useHeroData } from '@/composables/useHeroData'
import MetaTags from './MetaTags.vue'
import HeroSidebar from './hero/HeroSidebar.vue'
import AbilityList from './hero/AbilityList.vue'
import TalentTree from './hero/TalentTree.vue'
import TalentCards from './hero/TalentCards.vue'
import DevCommentsDrawer from './hero/DevCommentsDrawer.vue'
import TalentTypeToggle from './hero/TalentTypeToggle.vue'
import DetailView from './hero/DetailView.vue'

// Constants
const talentLevels = [1, 4, 7, 10, 13, 16, 20]

// Hero data composable
const {
  hero,
  talents,
  heroName,
  heroPortraitPath,
  heroSplashPath,
  talentType,
  currentSelectedTalents,
  // eslint-disable-next-line no-unused-vars
  selectedHeroName,
  // eslint-disable-next-line no-unused-vars
  loadHeroData,
  selectHero,
  toggleTalentType,
  toggleTalentSelection,
  resetSelections,
  findAbilityOrTalent
} = useHeroData()

// Local state
const selectedAbility = ref(null)
const selectedTalent = ref(null)
const selectedTalentLevel = ref(1)
const showDevComments = ref(false)
const showDevCommentsAlways = ref(false)

// Computed
const pageTitle = computed(() => hero.value.name ? `${hero.value.name} - Talent Calculator` : 'Hero Talent Calculator')
const pageDescription = computed(() => hero.value.name ? `Interactive talent calculator for ${hero.value.name}` : 'Interactive hero talent calculator')

const splashStyle = computed(() => ({
  backgroundImage: `url(${heroSplashPath.value})`
}))

const activeDevComment = computed(() => {
  const item = selectedTalent.value || selectedAbility.value
  return item?.developerCommentary || null
})

// Methods
const onSelectHero = (heroName) => {
  selectHero(heroName)
  selectedAbility.value = null
  selectedTalent.value = null
  selectedTalentLevel.value = 1
  showDevComments.value = false
  showDevCommentsAlways.value = false
}

const selectAbility = (ability) => {
  selectedAbility.value = ability
  selectedTalent.value = null
}

const selectTalent = (level, talent) => {
  selectedTalent.value = talent
  selectedTalentLevel.value = level
  selectedAbility.value = null
  toggleTalentSelection(level, talent)
}

const selectLevel = (level) => {
  selectedTalentLevel.value = level
  const selectedAtLevel = currentSelectedTalents.value[level]
  if (selectedAtLevel) {
    selectedTalent.value = selectedAtLevel
    selectedAbility.value = null
  } else {
    selectedTalent.value = null
  }
}

const toggleDevComments = () => {
  showDevComments.value = !showDevComments.value
}

const toggleDevCommentsPanel = () => {
  showDevComments.value = !showDevComments.value
  if (!showDevComments.value && showDevCommentsAlways.value) {
    showDevCommentsAlways.value = false
  }
}

const onTalentTypeChange = () => {
  toggleTalentType()
  resetAll()
}

const resetAll = () => {
  resetSelections()
  selectedAbility.value = null
  selectedTalent.value = null
  selectedTalentLevel.value = 1
  showDevComments.value = false
  showDevCommentsAlways.value = false
}

// Formatting utilities
const formatText = (text) => {
  if (!text) return ''
  return text.replace(/\{highlight\}(.*?)\{\/highlight\}/g, 
    '<span class="highlight-text">$1</span>')
}

const convertTextPlaceholders = (text) => {
  if (!text) return ''
  return text.replace(/<([^,]+),\s*([^,]+),\s*([^,]+),\s*(\d+)(?:,\s*([^>]+))?>/g, 
    (match, type, section, category, index, targetHero) => {
      const item = findAbilityOrTalent(type, section, category, parseInt(index, 10), targetHero)
      if (item?.image) {
        return `<span class="inline-ref">${item.name}</span>`
      }
      return match
    })
}

// Watchers
watch(showDevCommentsAlways, (val) => {
  showDevComments.value = val
})

// Provide dependencies to child components
provide('heroName', heroName)
provide('heroPortraitPath', heroPortraitPath)
provide('formatText', formatText)
provide('convertTextPlaceholders', convertTextPlaceholders)
</script>

<style scoped>
/* Page Wrapper - Full viewport with HOTS background, no scroll */
.page-wrapper {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  background-repeat: repeat-y;
  background-size: contain;
  background-position: center;
  background-attachment: fixed;
}

/* Sidebar - Fixed full height on left */
.sidebar-fixed {
  position: fixed;
  left: 0;
  top: 0;
  width: 280px;
  height: 100vh;
  z-index: 100;
  overflow: hidden;
  border-right: 2px solid #333;
}

/* Main Content - Takes remaining space */
.main-content {
  margin-left: 280px;
  flex: 1;
  height: 100vh;
  padding: 10px 15px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* Hero Content - Fill available space */
.hero-content {
  display: flex;
  flex-direction: column;
  gap: 10px;
  height: 100%;
  width: 100%;
  max-width: 1600px;
  margin: 0 auto;
}

/* Top Section: 3 columns - 72% height */
/* Coluna da direita aumentada: 290px -> 380px (+30%) */
.top-section {
  display: grid;
  grid-template-columns: 220px 1fr 380px;
  gap: 12px;
  height: 72%;
  min-height: 0;
}

/* Columns */
.abilities-column, .talent-tree-column {
  background: rgba(0, 0, 0, 0.75);
  border: 1px solid #444;
  border-radius: 12px;
  padding: 15px;
  overflow: hidden;
  height: 100%;
}

.center-column {
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 0;
}

/* Splash Art - 55% da coluna central */
.splash-art {
  height: 55%;
  min-height: 200px;
  background-size: cover;
  background-position: center 15%;
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  border-radius: 12px 12px 0 0;
  flex-shrink: 0;
}

.hero-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 100%;
  background: linear-gradient(to bottom, 
    rgba(0,0,0,0.6) 0%, 
    transparent 25%, 
    transparent 60%, 
    rgba(0,0,0,0.85) 90%,
    rgba(0,0,0,0.95) 100%);
  pointer-events: none;
  border-radius: 12px 12px 0 0;
}

.splash-header {
  position: relative;
  z-index: 10;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 15px 20px;
  pointer-events: none;
}

.hero-title {
  color: #fff;
  font-size: 32px;
  font-weight: bold;
  margin: 0;
  text-shadow: 0 2px 4px rgba(0,0,0,0.9), 0 0 15px rgba(0,0,0,0.7);
  pointer-events: auto;
  letter-spacing: 0.05em;
}

/* Center Container */
.center-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid #444;
  background: rgba(0, 0, 0, 0.6);
}

/* Info Display Box - 45% da altura */
.info-display-box {
  flex: 1;
  padding: 15px 20px;
  background: rgba(10, 10, 10, 0.95);
  border-top: 2px solid #444;
  position: relative;
  overflow: visible;
  min-height: 0;
}

/* Bottom Section: Talent Cards - 28% height */
:deep(.bottom-section) {
  height: 28%;
  min-height: 0;
  margin-top: 0;
}

/* Empty State */
.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.empty-message {
  text-align: center;
  color: #666;
  background: rgba(0, 0, 0, 0.7);
  padding: 50px 70px;
  border-radius: 16px;
  border: 1px solid #444;
}

.empty-message h2 {
  color: #fff;
  font-size: 36px;
  margin-bottom: 15px;
  text-shadow: 0 2px 4px rgba(0,0,0,0.8);
}

.empty-message p {
  font-size: 18px;
}

/* Highlight Text */
:global(.highlight-text) {
  background-color: rgba(255, 100, 100, 0.3);
  padding: 2px 6px;
  border-radius: 4px;
  color: #ffcccc;
}

:global(.inline-ref) {
  color: #0099ff;
  font-weight: 500;
}

/* Responsive - 1400px e menor */
@media (max-width: 1400px) {
  .top-section {
    grid-template-columns: 200px 1fr 350px;
  }
  
  .hero-title {
    font-size: 28px;
  }
}

/* Responsive - 1200px e menor */
@media (max-width: 1200px) {
  .sidebar-fixed {
    width: 260px;
  }
  
  .main-content {
    margin-left: 260px;
    padding: 8px 12px;
  }
  
  .top-section {
    grid-template-columns: 180px 1fr 320px;
    gap: 10px;
  }
  
  .hero-title {
    font-size: 26px;
  }
  
  .abilities-column, .talent-tree-column {
    padding: 12px;
  }
}

/* Responsive - 992px e menor (tablet) */
@media (max-width: 992px) {
  .page-wrapper {
    flex-direction: column;
    overflow-y: auto;
    height: auto;
    min-height: 100vh;
  }
  
  .sidebar-fixed {
    position: relative;
    width: 100%;
    height: auto;
    max-height: 300px;
    border-right: none;
    border-bottom: 2px solid #333;
  }
  
  .main-content {
    margin-left: 0;
    height: auto;
    min-height: calc(100vh - 300px);
    overflow: visible;
    padding: 10px;
  }
  
  .hero-content {
    height: auto;
    gap: 15px;
  }
  
  .top-section {
    grid-template-columns: 1fr;
    grid-template-rows: auto auto auto;
    height: auto;
    min-height: 800px;
    gap: 15px;
  }
  
  .abilities-column {
    max-height: 350px;
  }
  
  .talent-tree-column {
    max-height: 400px;
  }
  
  .center-column {
    order: -1;
    min-height: 450px;
  }
  
  .splash-art {
    height: 220px;
  }
  
  :deep(.bottom-section) {
    height: 350px;
    min-height: 350px;
  }
}

/* Responsive - 768px e menor (mobile) */
@media (max-width: 768px) {
  .hero-title {
    font-size: 24px;
  }
  
  .main-content {
    padding: 8px;
  }
  
  .hero-content {
    gap: 10px;
  }
}
</style>
