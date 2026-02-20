<template>
  <div class="hero-sidebar">
    <!-- Tabs -->
    <div class="tabs">
      <div 
        class="tab" 
        :class="{ active: activeTab === 'heroes' }"
        @click="activeTab = 'heroes'"
      >
        Heroes
      </div>
      <div 
        class="tab" 
        :class="{ active: activeTab === 'maps' }"
        @click="activeTab = 'maps'"
      >
        Maps
      </div>
      <div 
        class="tab" 
        :class="{ active: activeTab === 'general' }"
        @click="activeTab = 'general'"
      >
        General
      </div>
      <div 
        class="tab" 
        :class="{ active: activeTab === 'gamemodes' }"
        @click="activeTab = 'gamemodes'"
      >
        Modes
      </div>
    </div>

    <!-- Heroes Tab Content -->
    <div v-if="activeTab === 'heroes'" class="tab-content">
      <!-- Search Bar -->
      <div class="search-container">
        <input
          id="hero-search"
          v-model="searchQuery"
          type="text"
          placeholder="Search hero..."
          class="search-input"
          autocomplete="off"
        />
        <span class="search-icon">🔍</span>
      </div>

      <!-- Heroes List by Role -->
      <div class="heroes-list-container">
        <div v-if="loading" class="loading">Loading...</div>
        <div v-else-if="filteredHeroes.length === 0" class="no-heroes">
          No heroes found
          <div v-if="debugInfo" class="debug">{{ debugInfo }}</div>
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
                :class="{ active: selectedHeroName === hero.name }"
                @click="selectHero(hero)"
              >
                <img 
                  :src="getHeroIcon(hero.image)" 
                  :alt="hero.name"
                  class="hero-icon"
                />
                <span class="hero-name">{{ formatHeroName(hero.name) }}</span>
              </div>
            </div>
          </div>
        </template>
      </div>
    </div>

    <!-- Maps Tab Content -->
    <div v-else-if="activeTab === 'maps'" class="tab-content">
      <div class="items-list-container">
        <div v-if="loading" class="loading">Loading...</div>
        <template v-else>
          <div
            v-for="map in maps"
            :key="map.id"
            class="clickable-item map-item"
            @click="navigateToItem('map', map.name)"
          >
            <div class="image-wrapper map-image-wrapper">
              <img 
                :src="getItemImage(map.image)" 
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

    <!-- General Tab Content -->
    <div v-else-if="activeTab === 'general'" class="tab-content">
      <div class="items-list-container">
        <div v-if="loading" class="loading">Loading...</div>
        <template v-else>
          <div
            v-for="item in generalItems"
            :key="item.id"
            class="clickable-item large-item"
            @click="navigateToItem('general', item.name)"
          >
            <div class="image-wrapper large-image-wrapper">
              <img 
                :src="getItemImage(item.image)" 
                :alt="item.name"
                class="item-image large-image"
              />
              <div class="item-name-overlay">
                <span class="item-name-large">{{ formatItemName(item.name) }}</span>
              </div>
            </div>
          </div>
        </template>
      </div>
    </div>

    <!-- Game Modes Tab Content -->
    <div v-else-if="activeTab === 'gamemodes'" class="tab-content">
      <div class="items-list-container">
        <div v-if="loading" class="loading">Loading...</div>
        <template v-else>
          <div
            v-for="mode in gameModes"
            :key="mode.id"
            class="clickable-item large-item"
            @click="navigateToItem('gamemode', mode.name)"
          >
            <div class="image-wrapper large-image-wrapper">
              <img 
                :src="getItemImage(mode.image)" 
                :alt="mode.name"
                class="item-image large-image"
              />
              <div class="item-name-overlay">
                <span class="item-name-large">{{ formatItemName(mode.name) }}</span>
              </div>
            </div>
          </div>
        </template>
      </div>
    </div>

    <!-- Close Button (bottom) - Mobile only -->
    <button v-if="isMobile" class="sidebar-close-btn" @click="$emit('close-sidebar')">
      <span>◀</span>
      <span class="close-text">Close</span>
    </button>
  </div>
</template>

<script>
export default {
  name: 'HeroSidebar',
  props: {
    selectedHeroName: { type: String, default: '' },
    isMobile: { type: Boolean, default: false }
  },
  emits: ['selectHero', 'close-sidebar'],
  data() {
    return {
      activeTab: 'heroes',
      allHeroes: [],
      roles: [],
      maps: [],
      generalItems: [],
      gameModes: [],
      searchQuery: '',
      expandedRoles: new Set(),
      loading: true,
      debugInfo: '',
      windowWidth: typeof window !== 'undefined' ? window.innerWidth : 1024
    }
  },
  computed: {
    isTablet() {
      return this.windowWidth >= 768 && this.windowWidth <= 991
    },
    filteredHeroes() {
      if (!this.searchQuery || this.searchQuery.trim() === '') {
        return this.allHeroes
      }
      const query = this.searchQuery.toLowerCase().trim()
      return this.allHeroes.filter(hero => 
        hero.name.toLowerCase().includes(query) ||
        hero.role.toLowerCase().includes(query)
      )
    },
    availableRoles() {
      const rolesWithHeroes = new Set(this.filteredHeroes.map(h => h.role))
      return this.roles.filter(role => rolesWithHeroes.has(role.name))
    }
  },
  async created() {
    // Add resize listener for tablet detection
    if (typeof window !== 'undefined') {
      window.addEventListener('resize', this.updateWindowWidth)
    }
    
    try {
      // Carregar roles
      const roleData = require('@/data/roles.json')
      this.roles = roleData.filter(r => r.name !== 'All')
      
      // Carregar heróis
      const heroFiles = require.context('@/data/heroes', false, /\.json$/)
      const heroes = await Promise.all(
        heroFiles.keys().map(async (key) => {
          const heroData = await heroFiles(key)
          return {
            id: heroData.id,
            name: heroData.name,
            image: heroData.image,
            role: heroData.role,
            show: heroData.show,
          }
        })
      )
      
      // Filtrar apenas heróis modificados
      const modifiedHeroes = heroes.filter(hero => {
        if (hero.show === 'false') return false
        try {
          require(`@/data/heroes/talents/${hero.name.toLowerCase()}_talents.json`)
          return true
        } catch {
          return false
        }
      })
      
      this.allHeroes = modifiedHeroes.sort((a, b) => a.name.localeCompare(b.name))
      
      // Expandir todas as roles por padrão
      this.roles.forEach(role => this.expandedRoles.add(role.id))

      // Carregar mapas
      const mapFiles = require.context('@/data/maps', false, /\.json$/)
      const maps = await Promise.all(
        mapFiles.keys().map(async (key) => {
          const mapData = await mapFiles(key)
          return {
            id: mapData.id,
            name: mapData.name,
            image: mapData.image,
          }
        })
      )
      this.maps = maps.sort((a, b) => a.name.localeCompare(b.name))

      // Carregar itens gerais
      const generalFiles = require.context('@/data/general', false, /\.json$/)
      const generalItems = await Promise.all(
        generalFiles.keys().map(async (key) => {
          const itemData = await generalFiles(key)
          return {
            id: itemData.id,
            name: itemData.name,
            image: itemData.image,
          }
        })
      )
      this.generalItems = generalItems.sort((a, b) => a.name.localeCompare(b.name))

      // Carregar modos de jogo
      const gameModeFiles = require.context('@/data/gamemodes', false, /\.json$/)
      const gameModes = await Promise.all(
        gameModeFiles.keys().map(async (key) => {
          const modeData = await gameModeFiles(key)
          return {
            id: modeData.id,
            name: modeData.name,
            image: modeData.image,
          }
        })
      )
      this.gameModes = gameModes.sort((a, b) => a.name.localeCompare(b.name))
    } catch (error) {
      console.error('Error loading data:', error)
      this.debugInfo = `Error: ${error.message}`
    } finally {
      this.loading = false
    }
  },
  methods: {
    navigateToItem(type, name) {
      // Navega para a rota apropriada
      const path = `/${type}/${name.toLowerCase().replace(/ /g, '_')}`
      this.$router.push(path)
      this.$emit('close-sidebar')
    },
    getHeroesByRole(roleName) {
      return this.filteredHeroes.filter(hero => hero.role === roleName)
    },
    toggleRole(roleId) {
      if (this.expandedRoles.has(roleId)) {
        this.expandedRoles.delete(roleId)
      } else {
        this.expandedRoles.add(roleId)
      }
    },
    isExpanded(roleId) {
      return this.expandedRoles.has(roleId)
    },
    selectHero(hero) {
      this.$emit('selectHero', hero.name)
    },
    formatHeroName(name) {
      if (!name) return ''
      return name.split('-').map(part => 
        part.charAt(0).toUpperCase() + part.slice(1).toLowerCase()
      ).join(' ')
    },
    formatItemName(name) {
      if (!name) return ''
      return name.split(/[-_]/).map(part => 
        part.charAt(0).toUpperCase() + part.slice(1).toLowerCase()
      ).join(' ')
    },
    getRoleIcon(imageName) {
      try {
        return require(`@/assets/roles/${imageName}`)
      } catch {
        return ''
      }
    },
    getHeroIcon(imagePath) {
      try {
        return require(`@/assets/${imagePath}`)
      } catch {
        return ''
      }
    },
    getItemImage(imagePath) {
      try {
        return require(`@/assets/${imagePath}`)
      } catch {
        return ''
      }
    },
    updateWindowWidth() {
      this.windowWidth = window.innerWidth
    }
  },
  beforeUnmount() {
    if (typeof window !== 'undefined') {
      window.removeEventListener('resize', this.updateWindowWidth)
    }
  }
}
</script>

<style scoped>
.hero-sidebar {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: rgba(0, 0, 0, 0.85);
}

/* Tabs */
.tabs {
  display: flex;
  border-bottom: 1px solid #333;
  background: rgba(0, 0, 0, 0.5);
}

.tab {
  flex: 1;
  padding: 12px 8px;
  text-align: center;
  color: #888;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  cursor: pointer;
  transition: all 0.2s;
  border-bottom: 2px solid transparent;
}

.tab:hover {
  color: #ccc;
  background: rgba(255, 255, 255, 0.05);
}

.tab.active {
  color: #fff;
  border-bottom-color: #742aff;
  background: rgba(116, 42, 255, 0.1);
}

/* Tab Content */
.tab-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  padding-bottom: 60px; /* Espaço para o botão de fechar (50px + margem) */
}

/* Search */
.search-container {
  position: relative;
  padding: 12px;
  border-bottom: 1px solid #333;
}

.search-input {
  width: 100%;
  padding: 10px 35px 10px 12px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid #444;
  border-radius: 8px;
  color: #fff;
  font-size: 13px;
}

.search-input:focus {
  outline: none;
  border-color: #742aff;
  background: rgba(255, 255, 255, 0.08);
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

/* Heroes List */
.heroes-list-container,
.items-list-container {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
}

.loading, .no-heroes {
  color: #666;
  text-align: center;
  padding: 20px;
  font-size: 14px;
}

.debug {
  color: #999;
  font-size: 11px;
  margin-top: 10px;
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

/* Role Section */
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

/* Role Heroes */
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

.hero-item.active {
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

.hero-item.active .hero-icon {
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

.hero-item.active .hero-name {
  color: #fff;
  font-weight: 600;
}

/* ===========================================
   CLICKABLE ITEMS (Maps, General, Modes)
   =========================================== */

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

/* Map items - 2x height (~96px) */
.coming-soon-item.map-item .map-image-wrapper {
  position: relative;
  width: 100%;
  height: 96px;
  overflow: hidden;
  border-radius: 6px;
}

.coming-soon-item .item-image,
.coming-soon-item.map-item .map-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

/* Large items (General and Modes) - 3x height (~144px) */
.coming-soon-item.large-item .large-image-wrapper {
  position: relative;
  width: 100%;
  height: 144px;
  overflow: hidden;
  border-radius: 6px;
}

.coming-soon-item.large-item .large-image {
  object-fit: cover;
  object-position: center;
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
    0 2px 4px rgba(0, 0, 0, 0.9),
    0 4px 8px rgba(0, 0, 0, 0.7),
    0 0 20px rgba(0, 0, 0, 0.8);
  text-align: center;
  padding: 0 10px;
  line-height: 1.2;
}

/* Coming Soon Overlay */
.coming-soon-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.75);
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
  z-index: 2;
}

.coming-soon-overlay.transparent {
  background: rgba(0, 0, 0, 0.5);
}

.coming-soon-text {
  color: #fff;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.8);
  background: rgba(116, 42, 255, 0.7);
  padding: 6px 12px;
  border-radius: 4px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}



/* ===========================================
   RESPONSIVE STYLES
   =========================================== */

/* Tablet (768px - 991px) */
@media (min-width: 768px) and (max-width: 991px) {
  .hero-sidebar {
    width: 320px;
    height: 100vh;
    background: rgba(10, 10, 15, 0.98);
  }
  
  /* Hide close button in tablet - usar o do parent */
  .sidebar-close-btn {
    display: none;
  }
  
  .tabs {
    padding-top: 0;
  }
  
  .tab {
    padding: 12px 6px;
    font-size: 11px;
  }
  
  .search-container {
    padding: 12px;
  }
  
  .heroes-list-container,
  .items-list-container {
    padding: 12px;
  }
  
  .role-header {
    padding: 10px 12px;
  }
  
  .role-icon {
    width: 26px;
    height: 26px;
  }
  
  .role-name {
    font-size: 13px;
  }
  
  .hero-item {
    padding: 8px 12px;
  }
  
  .hero-icon {
    width: 34px;
    height: 34px;
  }
  
  .hero-name {
    font-size: 14px;
  }
}

/* Mobile - Sidebar em tela cheia */
@media (max-width: 767px) {
  .hero-sidebar {
    width: 100vw;
    height: 100vh;
    background: rgba(10, 10, 15, 0.98);
    position: relative;
  }
  
  /* Close button at bottom - igual ao desktop */
  .sidebar-close-btn {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    width: 100%;
    height: 50px;
    background: rgba(20, 20, 20, 0.95);
    border: none;
    border-top: 2px solid #333;
    color: #888;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    font-size: 14px;
    transition: all 0.2s;
    z-index: 10;
  }
  
  .sidebar-close-btn:hover {
    background: #742aff;
    color: #fff;
    border-top-color: #742aff;
  }
  
  .sidebar-close-btn span:first-child {
    font-size: 12px;
  }
  
  .close-text {
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600;
  }
  
  .tabs {
    padding-top: 0;
  }
  
  .tab {
    padding: 15px 8px;
    font-size: 14px;
  }
  
  .search-container {
    padding: 15px;
  }
  
  .search-input {
    padding: 12px 40px 12px 15px;
    font-size: 15px;
  }
  
  .heroes-list-container,
  .items-list-container {
    padding: 15px;
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

  /* Mobile Coming Soon Items */
  .coming-soon-item.map-item .map-image-wrapper {
    height: 112px;
  }

  .coming-soon-item.large-item .large-image-wrapper {
    height: 168px;
  }

  .coming-soon-text {
    font-size: 14px;
    padding: 8px 16px;
  }

  .item-name-large {
    font-size: 22px;
    letter-spacing: 2px;
  }
}
</style>
