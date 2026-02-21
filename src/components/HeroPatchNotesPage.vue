<template>
  <div class="page-wrapper bg-hots-repeat">
    <MetaTags 
      :title="pageTitle" 
      :description="pageDescription" 
      :image="heroPortraitPath" 
    />

    <!-- LEFT SIDEBAR: Full height fixed -->
    <div class="sidebar-fixed" :class="{ hidden: !showSidebar }">
      <UnifiedSidebar
        :selected-item-name="heroName"
        selected-item-type="hero"
        :is-mobile="isMobile"
        @select-item="onSelectItem"
        @select-category="onSelectCategory"
        @close-sidebar="toggleSidebar"
      />
      <!-- Toggle Button at bottom (desktop and tablet) -->
      <button v-if="!isMobile" class="sidebar-toggle" @click="toggleSidebar" title="Hide sidebar">
        <span>◀</span>
        <span class="toggle-text">Hide</span>
      </button>
    </div>

    <!-- MOBILE STICKY DESCRIPTION: Only visible on mobile -->
    <MobileStickyDescription
      v-if="isMobile"
      :selected-ability="selectedAbility"
      :selected-talent="selectedTalent"
      :selected-level="selectedTalentLevel"
      :abilities="talents.abilities"
      :talent-type="talentType"
      @toggle-sidebar="toggleSidebar"
    />

    <!-- MAIN CONTENT: Full width with margin for sidebar -->
    <div class="main-content" :class="{ 'full-width': !showSidebar }">
      <div v-if="heroName" class="hero-content">
        <!-- Top Section: Abilities | Splash/Details | Talent Tree -->
        <div class="top-section">
          <!-- Abilities Column -->
          <div class="abilities-column">
            <!-- Build Code Panel: Tablet - divide espaço horizontalmente com abilities -->
            <div class="build-code-mobile-wrapper tablet-only" v-if="isTabletOrMobile && !isMobile && heroName">
              <TalentCodePanel
                :hero-name="heroName"
                :hero-display-name="hero.name"
                :vanilla-talents="selectedTalents.vanilla"
                :modified-talents="selectedTalents.modified"
                :vanilla-talents-data="vanillaTalentsData"
                :modified-talents-data="modifiedTalentsData"
                @load-code="loadTalentCode"
              />
            </div>
            <!-- Build Code Panel: Mobile - acima das abilities -->
            <div class="build-code-mobile-wrapper mobile-only" v-if="isMobile && heroName">
              <TalentCodePanel
                :hero-name="heroName"
                :hero-display-name="hero.name"
                :vanilla-talents="selectedTalents.vanilla"
                :modified-talents="selectedTalents.modified"
                :vanilla-talents-data="vanillaTalentsData"
                :modified-talents-data="modifiedTalentsData"
                @load-code="loadTalentCode"
              />
            </div>
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
                  <h1 class="hero-title clickable" @click="showHeroDeveloperCommentary" title="Click to view developer commentary">{{ hero.name }}</h1>
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
                  :show-hero-comment="showHeroComment"
                  :hero-dev-comment="heroDevComment"
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

        <!-- Bottom Section: Talent Cards (DESKTOP ONLY - hidden on tablet and mobile) -->
        <TalentCards
          v-if="!isTabletOrMobile"
          :talents="talents"
          :talent-levels="talentLevels"
          :selected-level="selectedTalentLevel"
          :selected-talent="selectedTalent"
          :current-selected-talents="currentSelectedTalents"
          :selected-talents="selectedTalents"
          :vanilla-talents-data="vanillaTalentsData"
          :modified-talents-data="modifiedTalentsData"
          :hero-name="heroName"
          :hero-display-name="hero.name"
          @select-level="selectLevel"
          @select-talent="selectTalent"
          @toggle-dev-comments="toggleDevComments"
          @load-code="loadTalentCode"
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

    <!-- Floating button to show sidebar when hidden (desktop and tablet only) -->
    <button v-if="!showSidebar && !isMobile" class="sidebar-show-btn" @click="toggleSidebar" title="Show sidebar">
      <span>▶</span>
    </button>
  </div>
</template>

<script setup>
/* eslint-disable no-undef */
import { ref, computed, watch, provide, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useHeroData } from '@/composables/useHeroData'
import MetaTags from './MetaTags.vue'
import UnifiedSidebar from './UnifiedSidebar.vue'
import AbilityList from './hero/AbilityList.vue'
import TalentTree from './hero/TalentTree.vue'
import TalentCards from './hero/TalentCards.vue'
import DevCommentsDrawer from './hero/DevCommentsDrawer.vue'
import TalentTypeToggle from './hero/TalentTypeToggle.vue'
import DetailView from './hero/DetailView.vue'
import MobileStickyDescription from './hero/MobileStickyDescription.vue'
import TalentCodePanel from './hero/TalentCodePanel.vue'

// Constants
const talentLevels = [1, 4, 7, 10, 13, 16, 20]

// Sidebar visibility state
const showSidebar = ref(true)

// Router
const router = useRouter()

// Responsive detection
const windowWidth = ref(window.innerWidth)
const isTabletOrMobile = computed(() => windowWidth.value <= 991)
const isMobile = computed(() => windowWidth.value <= 767)

const updateWindowWidth = () => {
  windowWidth.value = window.innerWidth
}
onMounted(() => window.addEventListener('resize', updateWindowWidth))
onUnmounted(() => window.removeEventListener('resize', updateWindowWidth))

// Hero data composable
const {
  hero,
  talents,
  heroName,
  heroPortraitPath,
  heroSplashPath,
  talentType,
  selectedTalents,
  currentSelectedTalents,
  vanillaTalentsData,
  modifiedTalentsData,
  // eslint-disable-next-line no-unused-vars
  selectedHeroName,
  // eslint-disable-next-line no-unused-vars
  loadHeroData,
  selectHero,
  toggleTalentSelection,
  resetSelections,
  setSelectedTalents,
  findAbilityOrTalent,
  getTalentImagePath
} = useHeroData()

// Local state
const selectedAbility = ref(null)
const selectedTalent = ref(null)
const selectedTalentLevel = ref(1)
const showDevComments = ref(false)
const showDevCommentsAlways = ref(false)
const showHeroComment = ref(false)

// Pending selections for cross-hero load
const pendingSelections = ref(null)

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

const heroDevComment = computed(() => {
  // Pega o developerCommentary do nível raiz do JSON de talentos
  const currentTalents = talentType.value === 'modified' ? modifiedTalentsData.value : vanillaTalentsData.value
  return currentTalents?.developerCommentary || null
})

// Methods
const onSelectItem = (payload) => {
  const { type, name } = payload || {}
  if (!type || !name) return
  
  if (type === 'hero') {
    // Navigate to hero page
    router.push(`/hero/${name.toLowerCase()}`)
    selectHero(name)
    selectedAbility.value = null
    selectedTalent.value = null
    selectedTalentLevel.value = 1
    showDevComments.value = false
    showDevCommentsAlways.value = false
  } else {
    // Navigate to other pages (maps, general, gamemodes)
    router.push(`/${type}/${name.toLowerCase().replace(/ /g, '_')}`)
  }
}

const onSelectCategory = (categoryId) => {
  if (categoryId === 'heroes') {
    router.push('/heroes')
  } else if (categoryId === 'maps') {
    router.push('/maps')
  } else if (categoryId === 'general') {
    router.push('/general')
  } else if (categoryId === 'gamemodes') {
    router.push('/gamemodes')
  }
}



const toggleSidebar = () => {
  showSidebar.value = !showSidebar.value
}

const selectAbility = (ability) => {
  selectedAbility.value = ability
  selectedTalent.value = null
  showHeroComment.value = false
}

const selectTalent = (level, talent) => {
  selectedTalent.value = talent
  selectedTalentLevel.value = level
  selectedAbility.value = null
  showHeroComment.value = false
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
  showHeroComment.value = false
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

const showHeroDeveloperCommentary = () => {
  // Limpa seleções de ability/talent e mostra o comentário do desenvolvedor do herói
  selectedAbility.value = null
  selectedTalent.value = null
  showHeroComment.value = true
}

const onTalentTypeChange = () => {
  // Não resetar seleções - cada tipo (vanilla/modified) mantém suas próprias seleções
  selectedAbility.value = null
  
  // Atualizar o talento selecionado baseado no tipo atual
  const selectedAtLevel = currentSelectedTalents.value[selectedTalentLevel.value]
  if (selectedAtLevel) {
    selectedTalent.value = selectedAtLevel
  } else {
    selectedTalent.value = null
  }
}

const resetAll = () => {
  resetSelections()
  selectedAbility.value = null
  selectedTalent.value = null
  selectedTalentLevel.value = 1
  showDevComments.value = false
  showDevCommentsAlways.value = false
  showHeroComment.value = false
}

const loadTalentCode = ({ heroName: codeHeroName, vanillaSelections, modifiedSelections, vanillaCode, modifiedCode }) => {
  // Verifica se é o mesmo herói
  const currentHeroName = heroName.value.toLowerCase()
  const targetHeroName = codeHeroName.toLowerCase()
  
  // Se for um herói diferente, navega para ele primeiro
  if (currentHeroName !== targetHeroName) {
    // Armazena os códigos pendentes para reconverter quando os dados carregarem
    // (os objetos vanillaSelections/modifiedSelections são do herói antigo)
    pendingSelections.value = { vanillaCode, modifiedCode }
    // Navega para o novo herói
    selectHero(targetHeroName)
    // O watcher em 'talents' vai detectar quando os dados carregarem e aplicar as seleções
  } else {
    // Mesmo herói, aplica diretamente
    applyTalentSelections(vanillaSelections, modifiedSelections)
  }
}

const applyTalentSelections = (vanillaSelections, modifiedSelections) => {
  // Aplica as seleções de vanilla
  setSelectedTalents('vanilla', vanillaSelections)
  
  // Aplica as seleções de modified
  setSelectedTalents('modified', modifiedSelections)
  
  // Atualiza a visualização para mostrar o primeiro talento selecionado
  const firstSelectedLevel = [1, 4, 7, 10, 13, 16, 20].find(
    level => currentSelectedTalents.value[level] !== null
  )
  
  if (firstSelectedLevel) {
    selectedTalentLevel.value = firstSelectedLevel
    selectedTalent.value = currentSelectedTalents.value[firstSelectedLevel]
    selectedAbility.value = null
  }
}

// Formatting utilities
const formatText = (text) => {
  if (!text) return ''
  
  // Remove quebras de linha e espaços extras do JSON
  let result = text.replace(/\n\s*/g, ' ').trim()
  
  // Substitui highlight primeiro
  result = result.replace(/\{highlight\}(.*?)\{\/highlight\}/g, '<span class="highlight-text">$1</span>')
  
  // Substitui as tags de quest/reward por versões com <br> antes e símbolo ❢
  result = result
    .replace(/\{quest\}Quest:\{\/quest\}/g, '<br><span class="quest-label">❢ Quest:</span>')
    .replace(/\{reward\}Reward:\{\/reward\}/g, '<br><span class="reward-label">❢ Reward:</span>')
    .replace(/\{repeatable_quest\}Repeatable Quest:\{\/repeatable_quest\}/g, '<br><span class="repeatable-quest-label">❢ Repeatable Quest:</span>')
  
  // Remove <br> no início se houver
  return result.replace(/^<br>/, '')
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

// Converte código para seleções de talentos (similar ao TalentCodePanel)
const codeToTalents = (code, talentsData) => {
  const selections = {}
  
  for (let i = 0; i < talentLevels.length; i++) {
    const level = talentLevels[i]
    const char = code[i]
    
    if (char === 'N' || char === 'n') {
      selections[level] = null
    } else {
      const index = parseInt(char, 10) - 1
      const levelTalents = talentsData[level] || []
      
      if (index >= 0 && index < levelTalents.length) {
        selections[level] = levelTalents[index]
      } else {
        selections[level] = null
      }
    }
  }
  
  return selections
}

// Watcher para detectar quando os dados do herói foram carregados
// e aplicar seleções pendentes de cross-hero load
watch(talents, (newTalents) => {
  if (pendingSelections.value && newTalents && Object.keys(newTalents).length > 0) {
    // Verifica se ambos os tipos de talentos estão carregados
    const vanillaData = vanillaTalentsData.value
    const modifiedData = modifiedTalentsData.value
    
    if (!vanillaData || !modifiedData || Object.keys(vanillaData).length === 0 || Object.keys(modifiedData).length === 0) {
      // Dados ainda não estão completos, aguarda
      return
    }
    
    // Dados carregados, reconverte os códigos usando os dados do novo herói
    const { vanillaCode, modifiedCode } = pendingSelections.value
    const vanillaSelections = codeToTalents(vanillaCode, vanillaData)
    const modifiedSelections = codeToTalents(modifiedCode, modifiedData)
    
    applyTalentSelections(vanillaSelections, modifiedSelections)
    // Limpa as seleções pendentes
    pendingSelections.value = null
  }
}, { immediate: true })

// Provide dependencies to child components
provide('heroName', heroName)
provide('heroPortraitPath', heroPortraitPath)
provide('formatText', formatText)
provide('convertTextPlaceholders', convertTextPlaceholders)
provide('findAbilityOrTalent', findAbilityOrTalent)
provide('getTalentImagePath', getTalentImagePath)
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
  transition: transform 0.3s ease;
}

.sidebar-fixed.hidden {
  transform: translateX(-100%);
}

/* Toggle Button at bottom */
.sidebar-toggle {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  width: 100%;
  height: 40px;
  background: rgba(20, 20, 20, 0.95);
  border: none;
  border-top: 2px solid #333;
  color: #888;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 12px;
  transition: all 0.2s;
  z-index: 102;
}

.sidebar-toggle:hover {
  background: #742aff;
  color: #fff;
  border-top-color: #742aff;
}

.toggle-text {
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: 600;
}

/* Floating button to show sidebar */
.sidebar-show-btn {
  position: fixed;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 36px;
  height: 80px;
  background: rgba(0, 0, 0, 0.9);
  border: 2px solid #444;
  border-left: none;
  border-radius: 0 8px 8px 0;
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  transition: all 0.2s;
  z-index: 99;
}

.sidebar-show-btn:hover {
  background: #742aff;
  border-color: #742aff;
  width: 44px;
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
  transition: margin-left 0.3s ease;
}

.main-content.full-width {
  margin-left: 0;
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

.hero-title.clickable {
  cursor: pointer;
  transition: all 0.2s ease;
}

.hero-title.clickable:hover {
  color: #742aff;
  text-shadow: 0 2px 4px rgba(0,0,0,0.9), 0 0 20px rgba(116, 42, 255, 0.5);
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
  color: rgb(209, 119, 119);
}

:global(.inline-ref) {
  color: #0099ff;
  font-weight: 500;
}

/* ===========================================
   DESKTOP ONLY (min-width: 992px)
   =========================================== */
@media (min-width: 992px) {
  /* Esconde o build code mobile no desktop */
  .build-code-mobile-wrapper {
    display: none;
  }
}

/* ===========================================
   TABLET ONLY (768px - 991px)
   =========================================== */
@media (min-width: 768px) and (max-width: 991px) {
  /* Esconde o build code mobile-only no tablet */
  .build-code-mobile-wrapper.mobile-only {
    display: none;
  }
  
  /* Mostra o build code tablet-only */
  .build-code-mobile-wrapper.tablet-only {
    display: block;
  }
}

/* ===========================================
   MOBILE ONLY (< 768px)
   =========================================== */
@media (max-width: 767px) {
  /* Esconde o build code tablet-only no mobile */
  .build-code-mobile-wrapper.tablet-only {
    display: none;
  }
  
  /* Mostra o build code mobile-only */
  .build-code-mobile-wrapper.mobile-only {
    display: block;
  }
}

/* ===========================================
   1280px - REDUÇÃO DE ÍCONES
   =========================================== */
@media (max-width: 1280px) {
  .top-section {
    grid-template-columns: 200px 1fr 320px;
  }
  
  /* Reduzir ícones na talent tree */
  :deep(.talent-node) {
    width: 48px;
    height: 48px;
  }
  
  :deep(.talent-spacer) {
    width: 48px;
    height: 48px;
  }
  
  :deep(.level-number) {
    width: 40px;
    height: 40px;
    font-size: 14px;
  }
  
  /* Reduzir ícones nas abilities */
  :deep(.ability-icon) {
    width: 48px;
    height: 48px;
  }
  
  :deep(.ability-row) {
    padding: 8px;
    gap: 10px;
  }
  
  :deep(.ability-name-small) {
    font-size: 11px;
  }
  
  :deep(.ability-placeholder) {
    height: 48px;
    min-height: 48px;
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
  
  .main-content.full-width {
    margin-left: 0;
  }
  
  .top-section {
    grid-template-columns: 180px 1fr 300px;
    gap: 10px;
  }
  
  .hero-title {
    font-size: 26px;
  }
  
  .abilities-column, .talent-tree-column {
    padding: 12px;
  }
  
  /* Ícones ainda menores */
  :deep(.talent-node) {
    width: 44px;
    height: 44px;
  }
  
  :deep(.talent-spacer) {
    width: 44px;
    height: 44px;
  }
  
  :deep(.level-number) {
    width: 38px;
    height: 38px;
    font-size: 13px;
  }
}

/* ===========================================
   TABLET LAYOUT (768px - 991px)
   Layout de 2 colunas: (Abilities+Center) | Tree
   =========================================== */
@media (max-width: 991px) {
  .page-wrapper {
    flex-direction: column;
    overflow-y: auto;
    height: auto;
    min-height: 100vh;
  }
  
  /* Sidebar vira um drawer compacto no topo */
  .sidebar-fixed {
    position: fixed;
    top: 0;
    left: 0;
    width: 320px;
    height: 100vh;
    z-index: 1000;
    transform: translateX(-100%);
    border-right: 2px solid #444;
  }
  
  .sidebar-fixed:not(.hidden) {
    transform: translateX(0);
  }
  
  .sidebar-fixed.hidden {
    transform: translateX(-100%);
  }
  
  /* Botão de toggle na parte inferior (igual desktop) */
  .sidebar-toggle {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    width: 100%;
    height: 40px;
    border-radius: 0;
    z-index: 102;
    background: rgba(20, 20, 20, 0.95);
    border: none;
    border-top: 2px solid #333;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
  }
  
  .sidebar-toggle .toggle-text {
    display: inline;
    font-size: 12px;
  }
  
  /* Botão flutuante para mostrar sidebar */
  .sidebar-show-btn {
    position: fixed;
    top: 10px;
    left: 10px;
    width: 48px;
    height: 48px;
    border-radius: 8px;
    z-index: 999;
    background: rgba(0, 0, 0, 0.9);
    border: 2px solid #444;
  }
  
  /* Overlay escuro quando sidebar aberta */
  .sidebar-fixed:not(.hidden)::before {
    content: '';
    position: fixed;
    top: 0;
    left: 320px;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.7);
    z-index: -1;
  }
  
  .main-content {
    margin-left: 0 !important;
    height: auto;
    min-height: 100vh;
    overflow: visible;
    padding: 70px 15px 20px 15px; /* Espaço pro botão do sidebar */
  }
  
  .hero-content {
    height: auto;
    gap: 15px;
  }
  
  /* Build Code Panel - Tablet: parte do grid, acima das abilities */
  .build-code-mobile-wrapper {
    grid-area: code;
    position: static;
    width: 100%;
  }
  
  .build-code-mobile-wrapper :deep(.talent-code-panel) {
    width: 100%;
    min-width: auto;
    flex-direction: row;
    flex-wrap: wrap;
    padding: 10px;
    gap: 8px;
  }
  
  .build-code-mobile-wrapper :deep(.code-header) {
    width: 100%;
  }
  
  .build-code-mobile-wrapper :deep(.code-input-wrapper) {
    flex: 1;
    min-width: 150px;
  }
  
  .build-code-mobile-wrapper :deep(.code-actions) {
    flex-shrink: 0;
  }
  
  .build-code-mobile-wrapper :deep(.action-btn) {
    padding: 8px 12px;
  }
  
  /* Layout de 2 colunas: Esquerda (Abilities + Center) | Direita (Tree) */
  .top-section {
    grid-template-columns: 1fr 260px;
    grid-template-rows: auto auto;
    grid-template-areas: 
      "center tree"
      "abilities tree";
    height: auto;
    min-height: 500px;
    max-height: 750px;
    gap: 12px;
    margin-top: 70px; /* Espaço apenas pro botão do sidebar */
  }
  
  /* Container para abilities + build code dividindo horizontalmente */
  .abilities-column {
    grid-area: abilities;
    max-height: 280px;
    min-height: 240px;
    display: flex;
    flex-direction: row;
    gap: 12px;
    padding: 12px;
    align-items: center; /* Centraliza verticalmente */
  }
  
  /* Build code dentro da coluna de abilities, dividindo horizontalmente */
  .abilities-column .build-code-mobile-wrapper {
    display: flex;
    width: 35%; /* Build code ocupa 35% */
    flex-shrink: 0;
    align-items: center; /* Centraliza verticalmente */
    justify-content: center;
  }
  
  .abilities-column .build-code-mobile-wrapper :deep(.talent-code-panel) {
    width: 100%;
    min-width: auto;
    padding: 10px;
    gap: 8px;
    min-height: 95%; /* Ocupa 95% da altura vertical */
    height: 95%;
    display: flex;
    flex-direction: column;
    justify-content: center; /* Centraliza conteúdo verticalmente */
  }
  
  .abilities-column .build-code-mobile-wrapper :deep(.code-header) {
    flex-direction: column;
    gap: 8px;
  }
  
  .abilities-column .build-code-mobile-wrapper :deep(.code-title) {
    font-size: 11px;
  }
  
  .abilities-column .build-code-mobile-wrapper :deep(.copy-btn) {
    padding: 4px 8px;
    font-size: 10px;
  }
  
  .abilities-column .build-code-mobile-wrapper :deep(.code-input) {
    font-size: 11px;
    padding: 8px;
  }
  
  .abilities-column .build-code-mobile-wrapper :deep(.action-btn) {
    padding: 8px 6px;
    font-size: 10px;
  }
  
  /* Ability list ocupa o resto do espaço */
  .abilities-column :deep(.abilities-vertical) {
    flex: 1;
    display: grid !important;
    grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
    grid-template-rows: repeat(3, minmax(0, 1fr)) !important;
    gap: 8px;
    height: 100%;
    padding: 4px;
  }
  
  .center-column {
    grid-area: center;
    min-height: 300px;
    max-height: 450px;
  }
  
  .talent-tree-column {
    grid-area: tree;
    max-height: 100%;
    height: 100%;
  }
  
  .splash-art {
    height: 180px;
    min-height: 160px;
  }
  
  /* REMOVENDO Talent Cards do iPad */
  :deep(.bottom-section) {
    display: none !important;
  }
  
  /* Abilities em 3 colunas no tablet - grid ajustado */
  :deep(.abilities-vertical) {
    display: grid !important;
    grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
    grid-template-rows: repeat(3, minmax(0, 1fr)) !important;
    gap: 8px;
    height: 100%;
    padding: 4px;
  }
  
  :deep(.ability-row) {
    min-width: 0;
    width: 100%;
    height: 100%;
  }
  
  /* Ícones de habilidade ajustados no tablet */
  :deep(.ability-icon) {
    width: 48px !important;
    height: 48px !important;
  }
  
  :deep(.ability-name-small) {
    font-size: 10px;
  }
}

/* ===========================================
   MOBILE LAYOUT (< 768px)
   Layout completamente reorganizado
   =========================================== */
@media (max-width: 767px) {
  .page-wrapper {
    flex-direction: column;
  }
  
  /* Sidebar ocupa tela inteira em mobile */
  .sidebar-fixed {
    width: 100vw;
    height: 100vh;
    z-index: 2000;
  }
  
  .sidebar-fixed:not(.hidden)::before {
    display: none; /* Remove overlay em mobile pois ocupa tela toda */
  }
  
  /* Botão do menu ocupa topo inteiro - SEM ANIMAÇÕES */
  .sidebar-toggle,
  .sidebar-show-btn {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    width: 100%;
    height: 50px;
    border-radius: 0;
    z-index: 1001;
    background: rgba(0, 0, 0, 0.95);
    border: none;
    border-bottom: 2px solid #444;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    /* Remover transições que causam bug */
    transition: none !important;
    transform: none !important;
  }
  
  .sidebar-toggle:hover,
  .sidebar-toggle:active,
  .sidebar-show-btn:hover,
  .sidebar-show-btn:active {
    /* Manter o mesmo estilo, sem animações */
    background: rgba(0, 0, 0, 0.95);
    border-bottom-color: #444;
    width: 100%;
    transform: none !important;
  }
  
  .sidebar-toggle .toggle-text {
    display: inline;
  }
  
  /* Build Code Panel dentro da abilities-column no mobile */
  .abilities-column .build-code-mobile-wrapper.mobile-only {
    display: block;
    width: 100%;
    margin-bottom: 10px;
  }
  
  .abilities-column .build-code-mobile-wrapper.mobile-only :deep(.talent-code-panel) {
    width: 100%;
    min-width: 100%;
    max-width: 100%;
    border-radius: 8px;
    border: 1px solid #444;
    box-sizing: border-box;
    flex-direction: row;
    flex-wrap: wrap;
    padding: 10px;
    gap: 8px;
  }
  
  .abilities-column .build-code-mobile-wrapper :deep(.code-header) {
    width: auto;
    flex: 1;
  }
  
  .abilities-column .build-code-mobile-wrapper :deep(.code-input-wrapper) {
    flex: 1;
    min-width: 120px;
  }
  
  .abilities-column .build-code-mobile-wrapper :deep(.code-input) {
    font-size: 12px;
    padding: 8px;
  }
  
  .abilities-column .build-code-mobile-wrapper :deep(.code-actions) {
    flex-shrink: 0;
    display: flex;
    gap: 6px;
  }
  
  .abilities-column .build-code-mobile-wrapper :deep(.action-btn) {
    padding: 8px 12px;
    font-size: 11px;
  }
  
  .abilities-column .build-code-mobile-wrapper :deep(.error-message),
  .abilities-column .build-code-mobile-wrapper :deep(.success-message) {
    width: 100%;
    font-size: 10px;
    padding: 4px 8px;
  }
  
  .main-content {
    margin-left: 0 !important;
    height: auto;
    min-height: 100vh;
    overflow: visible;
    padding: 50px 0 0 0; /* Padding top para o menu */
  }
  
  .hero-content {
    height: auto;
    gap: 0;
  }
  
  /* Layout em coluna única: Sem descrição (usamos sticky) */
  .top-section {
    grid-template-columns: 1fr;
    grid-template-rows: auto auto auto;
    grid-template-areas: 
      "splash"
      "abilities"
      "tree";
    height: auto;
    min-height: auto;
    max-height: none;
    gap: 12px;
    padding: 0 15px;
    margin-top: 50px; /* Espaço para o menu */
  }
  
  /* Center column escondida no mobile (usamos o sticky) */
  .center-column {
    grid-area: desc;
    min-height: auto;
    max-height: none;
    display: none; /* Esconde no mobile, usamos o sticky */
  }
  
  /* Esconde info-display-box no mobile (usamos sticky) */
  .info-display-box {
    display: none;
  }
  
  /* Esconde o center-container em mobile */
  .center-container {
    display: none;
  }
  
  /* Splash Art - SEGUNDO */
  .splash-art {
    grid-area: splash;
    height: 140px;
    min-height: 120px;
    border-radius: 8px;
    position: relative;
  }
  
  .splash-header {
    padding: 10px 15px;
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
  }
  
  .hero-title {
    font-size: 18px;
  }
  
  /* Esconde DevCommentsDrawer em mobile (já está na descrição) */
  :deep(.dev-comments-wrapper) {
    display: none;
  }
  
  /* Abilities em grid de 3 por linha - TERCEIRO */
  .abilities-column {
    grid-area: abilities;
    max-height: none;
    min-height: auto;
    padding: 10px;
    border-radius: 8px;
    display: block; /* Volta ao display normal, não flex */
  }
  
  /* Grid de abilities com altura fixa e centralização */
  .abilities-column :deep(.abilities-vertical) {
    display: grid !important;
    grid-template-columns: repeat(3, 1fr) !important;
    grid-template-rows: repeat(3, 90px) !important;
    gap: 8px;
    height: auto;
    min-height: auto;
    max-height: none;
    align-items: center;
    justify-items: center;
  }
  
  .abilities-column :deep(.ability-row) {
    height: 100%;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 6px;
  }
  
  /* Talent Tree - QUARTO */
  .talent-tree-column {
    grid-area: tree;
    max-height: none;
    min-height: auto;
    padding: 10px;
    border-radius: 8px;
  }
  
  /* Esconde Talent Cards em mobile */
  :deep(.bottom-section) {
    display: none;
  }
}

/* ===========================================
   SMALL MOBILE (< 480px)
   =========================================== */
@media (max-width: 480px) {
  .hero-title {
    font-size: 18px;
  }
  
  .splash-art {
    height: 100px;
    min-height: 90px;
  }
  
  .splash-header {
    padding: 8px 12px;
  }
  
  .mobile-sticky-title h4 {
    font-size: 14px;
  }
  
  .mobile-sticky-icon {
    width: 40px;
    height: 40px;
  }
  
  /* Ícones de habilidade maiores em telas pequenas */
  :deep(.ability-icon) {
    width: 56px !important;
    height: 56px !important;
  }
}
</style>
