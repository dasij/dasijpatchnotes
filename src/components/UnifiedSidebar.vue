<template>
  <div class="unified-sidebar">
    <!-- Category Tabs -->
    <div class="category-tabs">
      <button
        v-for="category in categories"
        :key="category.id"
        class="category-tab"
        :class="{ active: activeCategory === category.id }"
        @click="selectCategory(category.id)"
      >
        <img :src="category.icon" :alt="category.name" class="category-icon" />
        <span class="category-name">{{ category.name }}</span>
      </button>
    </div>

    <!-- Search Box (only for heroes) -->
    <div v-if="activeCategory === 'heroes'" class="search-box">
      <input
        id="unified-hero-search"
        v-model="searchQuery"
        type="text"
        placeholder="Search hero..."
        class="search-input"
        autocomplete="off"
      />
      <span class="search-icon">🔍</span>
    </div>

    <!-- HEROES TAB CONTENT -->
    <div v-if="activeCategory === 'heroes'" class="tab-content">
      <div class="heroes-list-container">
        <div v-if="loading" class="loading">Loading...</div>
        <div v-else-if="filteredHeroes.length === 0" class="no-heroes">
          No heroes found
        </div>
        <template v-else>
          <div
            v-for="role in availableRoles"
            :key="role.id"
            class="role-section"
          >
            <div class="role-header" @click="toggleRole(role.id)">
              <img :src="getRoleIcon(role.image)" :alt="role.name" class="role-icon" />
              <span class="role-name">{{ role.name }}</span>
              <span class="toggle-icon">{{ isExpanded(role.id) ? '▼' : '▶' }}</span>
            </div>
            
            <div v-show="isExpanded(role.id)" class="role-heroes">
              <div
                v-for="hero in getHeroesByRole(role.name)"
                :key="hero.id"
                class="hero-item"
                :class="{ active: isSelected(hero) }"
                @click="selectItem(hero)"
              >
                <img 
                  :src="getHeroPortrait(hero.name)" 
                  :alt="hero.name"
                  class="hero-icon"
                />
                <span class="hero-name">{{ formatName(hero.name) }}</span>
              </div>
            </div>
          </div>
        </template>
      </div>
    </div>

    <!-- MAPS TAB CONTENT -->
    <div v-else-if="activeCategory === 'maps'" class="tab-content">
      <div class="items-list-container" :key="'maps-' + maps.length">
        <div v-if="loading || maps.length === 0" class="loading">Loading...</div>
        <template v-else>
          <div
            v-for="map in filteredMaps"
            :key="`map-${map.id}`"
            class="clickable-item map-item"
            :class="{ selected: isSelected(map) }"
            @click="selectItem(map)"
          >
            <div class="image-wrapper map-image-wrapper">
              <img 
                :src="getItemImage(map)" 
                :alt="map.name"
                class="item-image map-image"
              />
              <div class="item-name-overlay">
                <span class="item-name-large">{{ map.name }}</span>
              </div>
              <div v-if="!map.changed" class="wip-overlay">
                <span class="wip-text">WIP</span>
              </div>
            </div>
          </div>
        </template>
      </div>
    </div>

    <!-- GENERAL TAB CONTENT -->
    <div v-else-if="activeCategory === 'general'" class="tab-content">
      <div class="items-list-container" :key="'general-' + generalItems.length">
        <div v-if="loading || generalItems.length === 0" class="loading">Loading...</div>
        <template v-else>
          <div
            v-for="item in filteredGeneral"
            :key="`general-${item.id}`"
            class="clickable-item large-item"
            :class="{ selected: isSelected(item) }"
            @click="selectItem(item)"
          >
            <div class="image-wrapper large-image-wrapper">
              <img 
                :src="getItemImage(item)" 
                :alt="item.name"
                class="item-image large-image"
              />
              <div class="item-name-overlay">
                <span class="item-name-large">{{ formatName(item.name) }}</span>
              </div>
            </div>
          </div>
        </template>
      </div>
    </div>

    <!-- GAME MODES TAB CONTENT -->
    <div v-else-if="activeCategory === 'gamemodes'" class="tab-content">
      <div class="items-list-container" :key="'gamemodes-' + gameModes.length">
        <div v-if="loading || gameModes.length === 0" class="loading">Loading...</div>
        <template v-else>
          <div
            v-for="mode in filteredGameModes"
            :key="`mode-${mode.id}`"
            class="clickable-item large-item"
            :class="{ selected: isSelected(mode) }"
            @click="selectItem(mode)"
          >
            <div class="image-wrapper large-image-wrapper">
              <img 
                :src="getItemImage(mode)" 
                :alt="mode.name"
                class="item-image large-image"
              />
              <div class="item-name-overlay">
                <span class="item-name-large">{{ formatName(mode.name) }}</span>
              </div>
            </div>
          </div>
        </template>
      </div>
    </div>

    <!-- Close button for mobile -->
    <button v-if="isMobile" class="mobile-close-btn" @click="$emit('close-sidebar')">
      ✕ Close
    </button>
  </div>
</template>

<script setup>
/* eslint-disable no-undef */
import { ref, computed, watch, onMounted } from 'vue'

const props = defineProps({
  selectedItemName: {
    type: String,
    default: ''
  },
  selectedItemType: {
    type: String,
    default: 'hero'
  },
  isMobile: {
    type: Boolean,
    default: false
  }
})

// Estado interno para seleção - independente das props
const internalSelectedName = ref('')
const internalSelectedType = ref('hero')

const emit = defineEmits(['select-item', 'select-category', 'close-sidebar'])

// Categories
const categories = [
  { id: 'heroes', name: 'Heroes', icon: require('@/assets/roles/all.png') },
  { id: 'maps', name: 'Maps', icon: require('@/assets/mainpage/maps.webp') },
  { id: 'general', name: 'General', icon: require('@/assets/mainpage/general.webp') },
  { id: 'gamemodes', name: 'Modes', icon: require('@/assets/mainpage/gamemodes.webp') }
]

// State
const activeCategory = ref('heroes')  // Sempre começa com heroes, ajusta via watcher
const searchQuery = ref('')
const heroes = ref([])
const maps = ref([])
const generalItems = ref([])
const gameModes = ref([])
const roles = ref([])
const expandedRoles = ref(new Set())
const loading = ref(true)
const categoryLoading = ref({
  heroes: false,
  maps: false,
  general: false,
  gamemodes: false
})

// Hero name mapping
const heroNameToFileMap = {
  'li-ming': 'liming',
  'lt-morales': 'ltmorales',
  'sgt-hammer': 'sgthammer',
  'the-butcher': 'thebutcher',
  'the-lost-vikings': 'lostvikings',
  'cho': 'chogall',
  'gall': 'chogall'
}

// Computed
const filteredHeroes = computed(() => {
  let items = heroes.value
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    items = items.filter(hero => hero.name.toLowerCase().includes(query))
  }
  return items
})

const availableRoles = computed(() => {
  const rolesWithHeroes = new Set(filteredHeroes.value.map(h => h.role))
  return roles.value.filter(role => rolesWithHeroes.has(role.name))
})

const filteredMaps = computed(() => {
  let items = [...maps.value].sort((a, b) => a.name.localeCompare(b.name))
  // Sort changed first
  const changed = items.filter(item => item.changed)
  const unchanged = items.filter(item => !item.changed)
  return [...changed, ...unchanged]
})

const filteredGeneral = computed(() => {
  return [...generalItems.value].sort((a, b) => a.name.localeCompare(b.name))
})

const filteredGameModes = computed(() => {
  return [...gameModes.value].sort((a, b) => a.name.localeCompare(b.name))
})

// Methods
const selectCategory = async (categoryId) => {
  // Só atualiza se for diferente
  if (activeCategory.value === categoryId) return
  
  activeCategory.value = categoryId
  searchQuery.value = ''
  
  // Limpa seleção interna ao trocar de categoria
  internalSelectedName.value = ''
  internalSelectedType.value = ''
  
  // Garante que os dados da categoria estejam carregados antes de emitir o evento
  if (categoryId === 'general' && generalItems.value.length === 0) {
    await loadGeneral()
  } else if (categoryId === 'gamemodes' && gameModes.value.length === 0) {
    await loadGameModes()
  } else if (categoryId === 'maps' && maps.value.length === 0) {
    await loadMaps()
  } else if (categoryId === 'heroes' && heroes.value.length === 0) {
    await loadHeroes()
  }
  
  emit('select-category', categoryId)
}

const selectItem = (item) => {
  // Map category to type
  const typeMap = {
    'heroes': 'hero',
    'maps': 'map',
    'general': 'general',
    'gamemodes': 'gamemode'
  }
  const type = typeMap[activeCategory.value] || activeCategory.value
  
  // Atualiza estado interno imediatamente
  internalSelectedName.value = item.name
  internalSelectedType.value = type
  
  emit('select-item', { type, name: item.name })
}

const isSelected = (item) => {
  return internalSelectedName.value.toLowerCase() === item.name.toLowerCase()
}

const getHeroesByRole = (roleName) => {
  return filteredHeroes.value.filter(hero => hero.role === roleName)
}

const toggleRole = (roleId) => {
  if (expandedRoles.value.has(roleId)) {
    expandedRoles.value.delete(roleId)
  } else {
    expandedRoles.value.add(roleId)
  }
}

const isExpanded = (roleId) => {
  return expandedRoles.value.has(roleId)
}

const getHeroPortrait = (heroName) => {
  const fileName = heroNameToFileMap[heroName.toLowerCase()] || heroName.toLowerCase()
  return `/heroes_portraits/${fileName}.png`
}

const getItemImage = (item) => {
  try {
    return require(`@/assets/${item.image}`)
  } catch {
    return ''
  }
}

const getRoleIcon = (imageName) => {
  try {
    return require(`@/assets/roles/${imageName}`)
  } catch {
    return ''
  }
}

const formatName = (name) => {
  return name.split(/[-_]/).map(part => 
    part.charAt(0).toUpperCase() + part.slice(1).toLowerCase()
  ).join(' ')
}

// Data loading (com cache)
const loadHeroes = async () => {
  if (categoryLoading.value.heroes) return
  categoryLoading.value.heroes = true
  
  try {
    // Load roles first
    const roleData = require('@/data/roles.json')
    roles.value = roleData.filter(r => r.name !== 'All')
    
    // Expand all roles by default
    roles.value.forEach(role => expandedRoles.value.add(role.id))
    
    const heroFiles = require.context('@/data/heroes', false, /^(?!.*talents).*\.json$/)
    const loadedHeroes = await Promise.all(
      heroFiles.keys().map(async (key) => {
        const heroData = await heroFiles(key)
        return {
          id: heroData.id,
          name: heroData.name,
          role: heroData.role,
          show: heroData.show
        }
      })
    )
    heroes.value = loadedHeroes.filter(h => h.show !== 'false')
  } finally {
    categoryLoading.value.heroes = false
  }
}

const loadMaps = async () => {
  if (categoryLoading.value.maps) return
  categoryLoading.value.maps = true
  
  try {
    const mapFiles = require.context('@/data/maps', false, /\.json$/)
    const loadedMaps = await Promise.all(
      mapFiles.keys().map(async (key) => {
        const mapData = await mapFiles(key)
        return {
          id: mapData.id,
          name: mapData.name,
          image: mapData.image,
          changed: mapData.changed === 'true' || mapData.changed === true
        }
      })
    )
    maps.value = loadedMaps
  } finally {
    categoryLoading.value.maps = false
  }
}

const loadGeneral = async () => {
  if (categoryLoading.value.general) return
  categoryLoading.value.general = true
  
  try {
    const generalFiles = require.context('@/data/general', false, /\.json$/)
    const loadedGeneral = await Promise.all(
      generalFiles.keys().map(async (key) => {
        const itemData = await generalFiles(key)
        return {
          id: itemData.id,
          name: itemData.name,
          image: itemData.image
        }
      })
    )
    generalItems.value = loadedGeneral
  } finally {
    categoryLoading.value.general = false
  }
}

const loadGameModes = async () => {
  if (categoryLoading.value.gamemodes) return
  categoryLoading.value.gamemodes = true
  
  try {
    const gameModeFiles = require.context('@/data/gamemodes', false, /\.json$/)
    const loadedGameModes = await Promise.all(
      gameModeFiles.keys().map(async (key) => {
        const itemData = await gameModeFiles(key)
        return {
          id: itemData.id,
          name: itemData.name,
          image: itemData.image
        }
      })
    )
    gameModes.value = loadedGameModes
  } finally {
    categoryLoading.value.gamemodes = false
  }
}

// Watch para activeCategory - carrega dados imediatamente quando muda de categoria
watch(() => activeCategory.value, (newCategory) => {
  if (newCategory === 'general' && generalItems.value.length === 0 && !categoryLoading.value.general) {
    loadGeneral()
  } else if (newCategory === 'gamemodes' && gameModes.value.length === 0 && !categoryLoading.value.gamemodes) {
    loadGameModes()
  } else if (newCategory === 'maps' && maps.value.length === 0 && !categoryLoading.value.maps) {
    loadMaps()
  } else if (newCategory === 'heroes' && heroes.value.length === 0 && !categoryLoading.value.heroes) {
    loadHeroes()
  }
}, { immediate: true })

// Mapeamento correto de tipo para categoria
const typeToCategory = {
  'hero': 'heroes',
  'map': 'maps',
  'general': 'general',
  'gamemode': 'gamemodes'
}

// Watch for external changes - apenas sincroniza se necessário
watch(() => props.selectedItemType, (newType) => {
  // Se newType estiver vazio, não faz nada (evita interferir quando troca categoria)
  if (!newType) return
  
  const category = typeToCategory[newType]
  if (category && category !== activeCategory.value) {
    activeCategory.value = category
  }
  internalSelectedType.value = newType
}, { immediate: true })

watch(() => props.selectedItemName, (newName) => {
  if (newName && newName !== internalSelectedName.value) {
    internalSelectedName.value = newName
  }
}, { immediate: true })

// Load data on mount - carrega tudo imediatamente
onMounted(async () => {
  // Inicializa estado interno com as props usando o mapeamento correto
  const category = typeToCategory[props.selectedItemType] || 'heroes'
  activeCategory.value = category
  internalSelectedType.value = props.selectedItemType
  internalSelectedName.value = props.selectedItemName
  
  await Promise.all([
    loadHeroes(),
    loadMaps(),
    loadGeneral(),
    loadGameModes()
  ])
  loading.value = false
})
</script>

<style scoped>
.unified-sidebar {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: rgba(10, 10, 10, 0.98);
  border-right: 2px solid #333;
  overflow: hidden;
}

/* Category Tabs */
.category-tabs {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 2px;
  background: #222;
  border-bottom: 2px solid #333;
}

.category-tab {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 10px 4px;
  background: #1a1a1a;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.category-tab:hover {
  background: #2a2a2a;
}

.category-tab.active {
  background: #742aff;
}

.category-icon {
  width: 24px;
  height: 24px;
  object-fit: contain;
  margin-bottom: 4px;
  filter: brightness(0.7);
  transition: filter 0.2s;
}

.category-tab:hover .category-icon,
.category-tab.active .category-icon {
  filter: brightness(1);
}

.category-name {
  color: #888;
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 600;
}

.category-tab.active .category-name {
  color: #fff;
}

/* Search Box */
.search-box {
  position: relative;
  padding: 12px;
  border-bottom: 1px solid #333;
}

.search-input {
  width: 100%;
  padding: 10px 35px 10px 12px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid #444;
  border-radius: 6px;
  color: #fff;
  font-size: 14px;
  outline: none;
  transition: all 0.2s;
}

.search-input:focus {
  border-color: #742aff;
  background: rgba(255, 255, 255, 0.15);
}

.search-input::placeholder {
  color: #666;
}

.search-icon {
  position: absolute;
  right: 22px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 14px;
  opacity: 0.5;
}

/* Tab Content */
.tab-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  padding-bottom: 60px;
}

/* Lists Container */
.heroes-list-container,
.items-list-container {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
}

.heroes-list-container::-webkit-scrollbar,
.items-list-container::-webkit-scrollbar {
  width: 6px;
}

.heroes-list-container::-webkit-scrollbar-track,
.items-list-container::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.3);
}

.heroes-list-container::-webkit-scrollbar-thumb,
.items-list-container::-webkit-scrollbar-thumb {
  background: #444;
  border-radius: 3px;
}

.heroes-list-container::-webkit-scrollbar-thumb:hover,
.items-list-container::-webkit-scrollbar-thumb:hover {
  background: #742aff;
}

.loading, .no-heroes, .no-items {
  color: #666;
  text-align: center;
  padding: 20px;
  font-size: 14px;
}

/* HEROES TAB STYLES */
.role-section {
  margin-bottom: 8px;
}

.role-header {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  user-select: none;
}

.role-header:hover {
  background: rgba(255, 255, 255, 0.1);
}

.role-icon {
  width: 24px;
  height: 24px;
  object-fit: contain;
  filter: brightness(0.9);
}

.role-name {
  flex: 1;
  color: #fff;
  font-size: 13px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.toggle-icon {
  color: #666;
  font-size: 10px;
}

.role-heroes {
  padding: 5px 0 5px 8px;
}

.hero-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.15s;
  margin-bottom: 2px;
}

.hero-item:hover {
  background: rgba(255, 255, 255, 0.08);
}

.hero-item.active,
.hero-item.selected {
  background: rgba(116, 42, 255, 0.2);
  border-left: 3px solid #742aff;
}

.hero-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #444;
}

.hero-item.active .hero-icon,
.hero-item.selected .hero-icon {
  border-color: #742aff;
  box-shadow: 0 0 8px rgba(116, 42, 255, 0.4);
}

.hero-name {
  color: #ccc;
  font-size: 13px;
  font-weight: 500;
}

.hero-item:hover .hero-name {
  color: #fff;
}

.hero-item.active .hero-name,
.hero-item.selected .hero-name {
  color: #fff;
  font-weight: 600;
}

/* MAPS / GENERAL / MODES STYLES */
.clickable-item {
  display: flex;
  flex-direction: column;
  margin-bottom: 8px;
  border-radius: 8px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.03);
  transition: all 0.2s;
  cursor: pointer;
}

.clickable-item:hover {
  background: rgba(116, 42, 255, 0.2);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.clickable-item.selected {
  box-shadow: 0 0 0 2px #742aff;
}

.image-wrapper {
  position: relative;
  width: 100%;
  overflow: hidden;
  border-radius: 6px;
}

/* Map items - 2x height (~96px) */
.map-image-wrapper {
  height: 96px;
}

.item-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

/* Large items (General and Modes) - 3x height (~144px) */
.large-image-wrapper {
  height: 144px;
}

/* Item Name Overlay - Inside the image */
.item-name-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
  z-index: 1;
}

.item-name-large {
  color: #fff;
  font-size: 18px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  text-shadow: 
    0 0 5px rgba(0, 0, 0, 1),
    0 2px 4px rgba(0, 0, 0, 0.95),
    0 4px 8px rgba(0, 0, 0, 0.9),
    0 8px 16px rgba(0, 0, 0, 0.8),
    0 0 30px rgba(0, 0, 0, 0.9);
  text-align: center;
  padding: 0 10px;
  line-height: 1.2;
}

/* WIP Overlay */
.wip-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
  z-index: 2;
}

.wip-text {
  color: #888;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  background: rgba(0, 0, 0, 0.7);
  padding: 6px 12px;
  border-radius: 4px;
}

/* Mobile Close Button */
.mobile-close-btn {
  padding: 15px;
  background: #742aff;
  border: none;
  color: #fff;
  font-size: 14px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.2s;
}

.mobile-close-btn:hover {
  background: #853aff;
}

/* Mobile Responsive */
@media (max-width: 767px) {
  .category-tab {
    padding: 15px 4px;
  }
  
  .category-icon {
    width: 28px;
    height: 28px;
  }
  
  .category-name {
    font-size: 11px;
  }
  
  .search-box {
    padding: 15px;
  }
  
  .heroes-list-container,
  .items-list-container {
    padding: 15px;
  }
  
  .map-image-wrapper {
    height: 112px;
  }
  
  .large-image-wrapper {
    height: 168px;
  }
  
  .item-name-large {
    font-size: 22px;
    letter-spacing: 2px;
  }
  
  .wip-text {
    font-size: 14px;
    padding: 8px 16px;
  }
  
  .role-header {
    padding: 12px 15px;
  }
  
  .role-icon {
    width: 28px;
    height: 28px;
  }
  
  .role-name {
    font-size: 14px;
  }
  
  .hero-item {
    padding: 10px 15px;
  }
  
  .hero-icon {
    width: 36px;
    height: 36px;
  }
  
  .hero-name {
    font-size: 15px;
  }
}
</style>
