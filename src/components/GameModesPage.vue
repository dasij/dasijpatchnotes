<template>
  <div class="page-wrapper bg-hots-repeat">
    <!-- LEFT SIDEBAR: Full height fixed -->
    <div class="sidebar-fixed" :class="{ hidden: !showSidebar }">
      <UnifiedSidebar
        :selected-item-name="selectedModeName"
        selected-item-type="gamemode"
        :is-mobile="isMobile"
        @select-item="onSelectItem"
        @select-category="onSelectCategory"
        @close-sidebar="toggleSidebar"
      />
      <!-- Toggle Button at bottom (desktop/tablet only) -->
      <button v-if="!isMobile" class="sidebar-toggle" @click="toggleSidebar" title="Hide sidebar">
        <span>◀</span>
        <span class="toggle-text">Hide</span>
      </button>
    </div>

    <!-- Mobile Menu Button (fixed at top) -->
    <button v-if="isMobile && !showSidebar" class="mobile-menu-btn" @click="toggleSidebar">
      <span>☰</span>
    </button>

    <!-- MAIN CONTENT -->
    <div class="main-content" :class="{ 'full-width': !showSidebar }">
      <div class="content-header">
        <h1 class="page-title">Game Modes</h1>
      </div>
      
      <div class="modes-grid">
        <div 
          v-for="mode in sortedGameModes" 
          :key="mode.id" 
          class="mode-card"
          @click="selectMode(mode)"
        >
          <div class="image-wrapper">
            <img :src="require(`@/assets/${mode.image}`)" :alt="mode.name" class="mode-image" />
            <div class="overlay"></div>
            <span class="mode-name">{{ formatItemName(mode.name) }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Floating button to show sidebar when hidden -->
    <button v-if="!showSidebar && !isMobile" class="sidebar-show-btn" @click="toggleSidebar" title="Show sidebar">
      <span>▶</span>
    </button>
  </div>
</template>

<script>
export default {
  name: 'GameModesPage',
  data() {
    return {
      gameModes: [],
      showSidebar: true,
      windowWidth: window.innerWidth,
      selectedModeName: ''
    };
  },
  computed: {
    isMobile() {
      return this.windowWidth <= 767;
    },
    isTablet() {
      return this.windowWidth >= 768 && this.windowWidth <= 991;
    },
    sortedGameModes() {
      return [...this.gameModes].sort((a, b) => a.name.localeCompare(b.name));
    }
  },
  async created() {
    window.addEventListener('resize', this.updateWindowWidth);
    
    const gameModeFiles = require.context('@/data/gamemodes', false, /\.json$/);
    const modes = await Promise.all(
      gameModeFiles.keys().map(async (key) => {
        const modeData = await gameModeFiles(key);
        return {
          id: modeData.id,
          name: modeData.name,
          image: modeData.image,
          description: modeData.description,
        };
      })
    );
    this.gameModes = modes;
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.updateWindowWidth);
  },
  methods: {
    updateWindowWidth() {
      this.windowWidth = window.innerWidth;
    },
    toggleSidebar() {
      this.showSidebar = !this.showSidebar;
    },
    formatItemName(name) {
      return name.split(/[-_]/).map(part => 
        part.charAt(0).toUpperCase() + part.slice(1).toLowerCase()
      ).join(' ');
    },
    selectMode(mode) {
      this.selectedModeName = mode.name.toLowerCase();
      const pathName = mode.name.toLowerCase().replace(/ /g, '_');
      this.$router.push(`/gamemode/${pathName}`);
    },
    onSelectItem(payload) {
      const { type, name } = payload || {};
      if (!type || !name) return;
      
      if (type === 'gamemode') {
        this.selectedModeName = name.toLowerCase();
        const pathName = name.toLowerCase().replace(/ /g, '_');
        this.$router.push(`/gamemode/${pathName}`);
      } else {
        this.$router.push(`/${type}/${name.toLowerCase().replace(/ /g, '_')}`);
      }
    },
    onSelectCategory(categoryId) {
      if (categoryId === 'heroes') {
        this.$router.push('/heroes');
      } else if (categoryId === 'maps') {
        this.$router.push('/maps');
      } else if (categoryId === 'general') {
        this.$router.push('/general');
      }
    }
  }
};
</script>

<style scoped>
.page-wrapper {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  background-image: url('@/assets/gamemodes_page_background.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
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

/* Mobile menu button (fixed at top) */
.mobile-menu-btn {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  width: 100%;
  height: 50px;
  background: rgba(20, 20, 20, 0.95);
  border: none;
  border-bottom: 2px solid #444;
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  z-index: 100;
}

.mobile-menu-btn:hover {
  background: #742aff;
}

/* Main Content */
.main-content {
  margin-left: 280px;
  flex: 1;
  height: 100vh;
  padding: 20px 30px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: margin-left 0.3s ease;
  background-color: rgba(0, 0, 0, 0.7);
}

.main-content.full-width {
  margin-left: 0;
}

.content-header {
  margin-bottom: 20px;
  flex-shrink: 0;
}

.page-title {
  color: #fff;
  font-size: 32px;
  font-weight: bold;
  margin: 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.8);
}

/* Modes Grid */
.modes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  overflow-y: auto;
  padding-right: 10px;
}

.modes-grid::-webkit-scrollbar {
  width: 8px;
}

.modes-grid::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.3);
  border-radius: 4px;
}

.modes-grid::-webkit-scrollbar-thumb {
  background: #444;
  border-radius: 4px;
}

.modes-grid::-webkit-scrollbar-thumb:hover {
  background: #742aff;
}

.mode-card {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  box-shadow: 0 4px 8px rgba(46, 25, 57, 0.5);
}

.mode-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(116, 42, 255, 0.3);
}

.image-wrapper {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
}

.mode-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease, filter 0.3s ease;
  filter: brightness(50%);
}

.mode-card:hover .mode-image {
  transform: scale(1.05);
  filter: brightness(100%);
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.2);
  transition: opacity 0.3s ease;
}

.mode-card:hover .overlay {
  opacity: 0;
}

.mode-name {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #CCE5FA;
  font-size: 24px;
  font-weight: bold;
  text-shadow: 
    0 0 5px rgba(0, 0, 0, 1),
    0 2px 4px rgba(0, 0, 0, 0.95),
    0 4px 8px rgba(0, 0, 0, 0.9),
    0 8px 16px rgba(0, 0, 0, 0.8),
    0 0 30px rgba(0, 0, 0, 0.9);
  transition: color 0.3s ease, text-shadow 0.3s ease;
  text-align: center;
  padding: 0 10px;
}

.mode-card:hover .mode-name {
  color: #fff;
  text-shadow: 
    0 0 10px rgba(0, 0, 0, 1),
    0 4px 8px rgba(0, 0, 0, 1),
    0 8px 16px rgba(0, 0, 0, 0.9);
}

/* Responsive - 1200px */
@media (max-width: 1200px) {
  .sidebar-fixed {
    width: 260px;
  }
  
  .main-content {
    margin-left: 260px;
    padding: 15px 20px;
  }
  
  .page-title {
    font-size: 28px;
  }
  
  .modes-grid {
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 15px;
  }
  
  .image-wrapper {
    height: 180px;
  }
  
  .mode-name {
    font-size: 22px;
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
    z-index: -1;
  }
  
  .main-content {
    margin-left: 0 !important;
    height: auto;
    min-height: 100vh;
    overflow: visible;
    padding: 70px 20px 20px 20px;
  }
  
  .modes-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
  }
  
  .image-wrapper {
    height: 160px;
  }
  
  .mode-name {
    font-size: 20px;
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
    padding: 15px;
  }
  
  .page-title {
    font-size: 24px;
    text-align: center;
  }
  
  .modes-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }
  
  .image-wrapper {
    height: 180px;
  }
  
  .mode-name {
    font-size: 22px;
  }
}

/* SMALL MOBILE (< 480px) */
@media (max-width: 480px) {
  .page-title {
    font-size: 20px;
  }
  
  .image-wrapper {
    height: 150px;
  }
  
  .mode-name {
    font-size: 18px;
  }
}
</style>
