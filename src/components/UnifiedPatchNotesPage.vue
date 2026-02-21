<template>
  <div class="page-wrapper bg-hots-repeat">
    <MetaTags 
      :title="pageTitle" 
      :description="pageDescription" 
      :image="itemImagePath" 
    />

    <!-- LEFT SIDEBAR: Full height fixed -->
    <div class="sidebar-fixed" :class="{ hidden: !showSidebar }">
      <UnifiedSidebar
        :selected-item-name="itemName"
        :selected-item-type="itemType"
        :active-category="activeCategory"
        :is-mobile="isMobile"
        @select-item="onSelectItem"
        @select-category="onSelectCategory"
        @close-sidebar="toggleSidebar"
      />
      <!-- Toggle Button at bottom (desktop/tablet only) -->
      <button class="sidebar-toggle" @click="toggleSidebar" title="Hide sidebar">
        <span>◀</span>
        <span class="toggle-text">Hide</span>
      </button>
    </div>

    <!-- MAIN CONTENT -->
    <div class="main-content" :class="{ 'full-width': !showSidebar }">
      <div v-if="itemName" class="content-area">
        <!-- Left: Changes List -->
        <div class="changes-sidebar">
          <ChangesList
            :changes="allChanges"
            :selected-change="selectedChange"
            @select-change="onSelectChange"
          />
        </div>

        <!-- Right: Splash & Change Details -->
        <div class="details-area">
          <div class="details-container">
            <div class="splash-section" :style="splashStyle">
              <div class="splash-overlay"></div>
              <div class="splash-header">
                <h1 class="item-title">{{ item.name }}</h1>
              </div>
            </div>

            <div class="detail-box">
              <ChangeDetailView :change="selectedChange" />
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="empty-state">
        <div class="empty-message">
          <h2>Welcome to Dasij Patch Notes</h2>
          <p>Here you'll find patch notes based on my personal vision for Heroes of the Storm.</p>
          <p>These changes prioritize fun over competitive balance, focusing on modifying heroes based on their lore and current gameplay.</p>
          <br />
          <p><strong>Choose a category from the sidebar to get started:</strong></p>
          <div class="welcome-links">
            <router-link to="/heroes" class="welcome-link">🦸 Heroes</router-link>
            <router-link to="/maps" class="welcome-link">🗺️ Maps</router-link>
            <router-link to="/general" class="welcome-link">⚙️ General</router-link>
            <router-link to="/gamemodes" class="welcome-link">🎮 Game Modes</router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Floating button to show sidebar when hidden (desktop) -->
    <button v-if="!showSidebar && !isMobile" class="sidebar-show-btn" @click="toggleSidebar" title="Show sidebar">
      <span>▶</span>
    </button>

    <!-- Mobile Sticky Menu (always visible on mobile) -->
    <MobileMenuSticky 
      v-if="isMobile" 
      :title="itemName ? item.name : 'Select an Item'"
      @toggle-sidebar="toggleSidebar"
    />
  </div>
</template>

<script setup>
/* eslint-disable no-undef */
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import MetaTags from './MetaTags.vue'
import UnifiedSidebar from './UnifiedSidebar.vue'
import MobileMenuSticky from './MobileMenuSticky.vue'
import ChangesList from './patchnotes/ChangesList.vue'
import ChangeDetailView from './patchnotes/ChangeDetailView.vue'

// Router
const route = useRoute()
const router = useRouter()

// Sidebar visibility state - começa fechado
const showSidebar = ref(false)

// Responsive detection
const windowWidth = ref(window.innerWidth)
const isMobile = computed(() => windowWidth.value <= 767)

const updateWindowWidth = () => {
  windowWidth.value = window.innerWidth
}
onMounted(() => window.addEventListener('resize', updateWindowWidth))
onUnmounted(() => window.removeEventListener('resize', updateWindowWidth))

// Detectar tipo baseado na rota atual
const detectTypeFromRoute = () => {
  const path = route.path
  if (path.includes('/general')) return 'general'
  if (path.includes('/gamemode')) return 'gamemode'
  if (path.includes('/hero')) return 'hero'
  if (path.includes('/map')) return 'map'
  return null
}

// Detectar categoria ativa baseada na rota (para abrir o sidebar na aba correta)
const detectCategoryFromRoute = () => {
  const path = route.path
  if (path === '/heroes' || path.includes('/hero/')) return 'heroes'
  if (path === '/maps' || path.includes('/map/')) return 'maps'
  if (path === '/general' || path.includes('/general/')) return 'general'
  if (path === '/gamemodes' || path.includes('/gamemode/')) return 'gamemodes'
  return 'heroes' // default
}

// Data state
const item = ref({})
const itemType = ref(detectTypeFromRoute())
const itemName = ref('')
const activeCategory = ref(detectCategoryFromRoute())
const patchNotes = ref([])
const selectedChange = ref(null)

// Computed
const pageTitle = computed(() => {
  return item.value.name ? `${item.value.name} - Patch Notes` : 'Patch Notes'
})

const pageDescription = computed(() => {
  return item.value.name ? `Patch notes for ${item.value.name}` : 'View patch notes'
})

const itemImagePath = computed(() => {
  if (!itemName.value) return ''
  try {
    // Usa o caminho da imagem do JSON se disponível
    if (item.value && item.value.image) {
      return require(`@/assets/${item.value.image}`)
    }
    
    // Fallback para caminhos padrão se não houver image no JSON
    if (itemType.value === 'map') {
      return require(`@/assets/maps/menu/${itemName.value}-banner.png`)
    } else if (itemType.value === 'general') {
      return require(`@/assets/general/${itemName.value}.jpg`)
    } else if (itemType.value === 'gamemode') {
      return require(`@/assets/gamemodes/${itemName.value}.webp`)
    }
  } catch {
    return ''
  }
  return ''
})

const splashStyle = computed(() => {
  if (!itemImagePath.value) return {}
  return {
    backgroundImage: `url(${itemImagePath.value})`
  }
})

// Todas as mudanças flatten
const allChanges = computed(() => {
  const changes = []
  patchNotes.value.forEach(patchNote => {
    if (patchNote.general && patchNote.general.length > 0) {
      patchNote.general.forEach((change) => {
        changes.push({
          ...change,
          patchNoteId: patchNote.id,
          patchNoteTitle: patchNote.title,
          patchNoteDate: patchNote.date,
          changeNumber: changes.length + 1
        })
      })
    }
  })
  return changes
})

// Methods
const loadItemData = async (type, name) => {
  if (!name) return
  
  itemType.value = type
  itemName.value = name.toLowerCase()
  
  // Convert name to filename format (lowercase, spaces to underscores)
  const fileName = name.toLowerCase().replace(/ /g, '_')
  
  try {
    if (type === 'map') {
      const mapData = await import(`@/data/maps/${fileName}.json`)
      item.value = mapData.default
      patchNotes.value = mapData.default.patchNotes || []
    } else if (type === 'general') {
      const generalData = await import(`@/data/general/${fileName}.json`)
      item.value = generalData.default
      patchNotes.value = generalData.default.patchNotes || []
    } else if (type === 'gamemode') {
      const gameModeData = await import(`@/data/gamemodes/${fileName}.json`)
      item.value = gameModeData.default
      patchNotes.value = gameModeData.default.patchNotes || []
    }
    
    // Seleciona a primeira mudança por padrão
    if (allChanges.value.length > 0) {
      selectedChange.value = allChanges.value[0]
    }
  } catch (error) {
    console.error(`Error loading ${type} data:`, error)
  }
}

const onSelectCategory = (categoryId) => {
  // Atualiza a categoria ativa
  activeCategory.value = categoryId
  
  // Navega para a página principal da categoria selecionada
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

const onSelectItem = (payload) => {
  const { type, name } = payload || {}
  if (!type || !name) return
  
  // Se for herói, navega para a página de heróis usando push
  if (type === 'hero') {
    const heroName = name.toLowerCase()
    router.push(`/hero/${heroName}`).catch(() => {})
    return
  }
  
  loadItemData(type, name)
  
  // Update URL
  let path = ''
  if (type === 'map') path = `/map/${name.toLowerCase()}`
  else if (type === 'general') path = `/general/${name.toLowerCase()}`
  else if (type === 'gamemode') path = `/gamemode/${name.toLowerCase()}`
  
  router.replace({ path, query: route.query }).catch(() => {})
}

const onSelectChange = (change) => {
  selectedChange.value = change
}

const toggleSidebar = () => {
  showSidebar.value = !showSidebar.value
}

// Watch for route changes to update itemType e activeCategory
watch(() => route.path, () => {
  itemType.value = detectTypeFromRoute()
  activeCategory.value = detectCategoryFromRoute()
  
  // Abre o sidebar automaticamente quando navegar para uma categoria
  const path = route.path
  if (path === '/heroes' || path === '/maps' || path === '/general' || path === '/gamemodes') {
    showSidebar.value = true
  }
}, { immediate: true })

// Initialize from URL
onMounted(() => {
  if (route.params.name) {
    loadItemData(itemType.value, route.params.name.toLowerCase())
  }
})

// Watch for route changes
watch(() => route.params.name, (newName) => {
  if (newName && newName.toLowerCase() !== itemName.value) {
    const path = route.path
    let type = 'map'
    if (path.includes('/general/')) type = 'general'
    else if (path.includes('/gamemode/')) type = 'gamemode'
    
    loadItemData(type, newName.toLowerCase())
  }
})
</script>

<style scoped>
/* Page Wrapper */
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

/* Sidebar */
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

/* Toggle Button */
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

/* Main Content */
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

/* Content Area */
.content-area {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 12px;
  height: 100%;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

/* Changes Sidebar */
.changes-sidebar {
  background: rgba(0, 0, 0, 0.75);
  border: 1px solid #444;
  border-radius: 12px;
  padding: 15px;
  overflow: hidden;
  height: 100%;
}

/* Details Area */
.details-area {
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 0;
}

.details-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid #444;
  background: rgba(0, 0, 0, 0.6);
}

/* Splash Section */
.splash-section {
  height: 27%; /* Reduzido 40% do original (45%) */
  min-height: 120px;
  background-size: cover;
  background-position: center;
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  border-radius: 12px 12px 0 0;
  flex-shrink: 0;
}

.splash-overlay {
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
  padding: 20px;
}

.item-title {
  color: #fff;
  font-size: 32px;
  font-weight: bold;
  margin: 0;
  text-shadow: 0 2px 4px rgba(0,0,0,0.9), 0 0 15px rgba(0,0,0,0.7);
  letter-spacing: 0.05em;
}

/* Detail Box */
.detail-box {
  flex: 1;
  padding: 20px;
  background: rgba(10, 10, 10, 0.95);
  border-top: 2px solid #444;
  position: relative;
  overflow: hidden;
  min-height: 0;
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

.welcome-links {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 15px;
  margin-top: 25px;
}

.welcome-link {
  display: inline-block;
  padding: 12px 24px;
  background: linear-gradient(135deg, #2E60A3 0%, #4a8fd9 100%);
  color: #fff;
  text-decoration: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  transition: all 0.2s ease;
  border: 2px solid #2E60A3;
}

.welcome-link:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(46, 96, 163, 0.4);
  background: linear-gradient(135deg, #3a7bc8 0%, #5aa0e8 100%);
}

/* Responsive - 1200px */
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
  
  .content-area {
    grid-template-columns: 240px 1fr;
  }
  
  .item-title {
    font-size: 26px;
  }
  
  .changes-sidebar {
    padding: 12px;
  }
}

/* TABLET LAYOUT (768px - 991px) */
@media (max-width: 991px) {
  .page-wrapper {
    flex-direction: column;
    overflow-y: auto;
    height: auto;
    min-height: 100vh;
  }
  
  .sidebar-fixed {
    position: fixed;
    top: 0;
    left: 0;
    width: 320px;
    height: 100vh;
    z-index: 2000;
    transform: translateX(-100%);
    border-right: 2px solid #444;
  }
  
  .sidebar-fixed:not(.hidden) {
    transform: translateX(0);
  }
  
  .sidebar-fixed.hidden {
    transform: translateX(-100%);
  }
  
  .sidebar-fixed:not(.hidden)::before {
    content: '';
    position: fixed;
    top: 0;
    left: 320px;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.7);
    z-index: 1998;
  }
  
  .main-content {
    margin-left: 0 !important;
    height: auto;
    min-height: 100vh;
    overflow: visible;
    padding: 70px 15px 20px 15px;
  }
  
  .content-area {
    grid-template-columns: 260px 1fr;
    height: calc(100vh - 100px);
  }
}

/* MOBILE LAYOUT (< 768px) */
@media (max-width: 767px) {
  .sidebar-fixed {
    width: 100vw;
    height: 100vh;
    z-index: 2000;
  }
  
  .sidebar-fixed:not(.hidden)::before {
    display: none;
  }
  
  .sidebar-toggle {
    display: none;
  }
  
  .sidebar-show-btn {
    display: none;
  }
  
  .main-content {
    margin-left: 0 !important;
    height: auto;
    min-height: 100vh;
    overflow: visible;
    padding: 60px 10px 10px 10px; /* Espaço para barra sticky no topo */
  }
  
  .content-area {
    grid-template-columns: 1fr;
    grid-template-rows: auto 1fr;
    gap: 10px;
    height: auto;
  }
  
  .changes-sidebar {
    max-height: 250px;
    min-height: 200px;
  }
  
  .splash-section {
    height: 150px;
    min-height: 120px;
  }
  
  .item-title {
    font-size: 22px;
  }
  
  .detail-box {
    max-height: 500px;
    overflow-y: auto;
  }
}

/* SMALL MOBILE (< 480px) */
@media (max-width: 480px) {
  .item-title {
    font-size: 18px;
  }
  
  .splash-section {
    height: 120px;
    min-height: 100px;
  }
  
  .empty-message {
    padding: 30px 40px;
  }
  
  .empty-message h2 {
    font-size: 24px;
  }
  
  .empty-message p {
    font-size: 14px;
  }
}
</style>
