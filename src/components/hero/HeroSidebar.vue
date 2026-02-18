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
          v-model="searchQuery"
          type="text"
          placeholder="Search hero..."
          class="search-input"
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

    <!-- Other Tabs (placeholder for now) -->
    <div v-else class="tab-content placeholder">
      <div class="placeholder-text">{{ activeTab }} coming soon...</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HeroSidebar',
  props: {
    selectedHeroName: { type: String, default: '' }
  },
  emits: ['selectHero'],
  data() {
    return {
      activeTab: 'heroes',
      allHeroes: [],
      roles: [],
      searchQuery: '',
      expandedRoles: new Set(),
      loading: true,
      debugInfo: ''
    }
  },
  computed: {
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
    } catch (error) {
      console.error('Error loading heroes:', error)
      this.debugInfo = `Error: ${error.message}`
    } finally {
      this.loading = false
    }
  },
  methods: {
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
}

.tab-content.placeholder {
  align-items: center;
  justify-content: center;
}

.placeholder-text {
  color: #666;
  font-size: 14px;
  text-transform: capitalize;
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
.heroes-list-container {
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

.heroes-list-container::-webkit-scrollbar {
  width: 6px;
}

.heroes-list-container::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.3);
}

.heroes-list-container::-webkit-scrollbar-thumb {
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
</style>
