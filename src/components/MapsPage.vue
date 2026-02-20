<template>
  <div class="page-wrapper bg-hots-repeat">
    <!-- LEFT SIDEBAR: Full height fixed -->
    <div class="sidebar-fixed" :class="{ hidden: !showSidebar }">
      <UnifiedSidebar
        :selected-item-name="selectedMapName"
        selected-item-type="map"
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
        <h1 class="page-title">Maps</h1>
      </div>
      
      <div class="maps-grid">
        <div 
          v-for="map in sortedMaps" 
          :key="map.id" 
          class="map-card"
          :class="{ 'unchanged': !map.changed }"
          @click="selectMap(map)"
        >
          <div class="image-wrapper">
            <img :src="require(`@/assets/${map.image}`)" :alt="map.name" class="map-image" />
            <div class="overlay"></div>
            <span class="map-name">{{ map.name }}</span>
            <div v-if="!map.changed" class="wip-badge">Under Construction</div>
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
  name: 'MapsPage',
  data() {
    return {
      maps: [],
      showSidebar: true,
      windowWidth: window.innerWidth,
      selectedMapName: ''
    };
  },
  computed: {
    isMobile() {
      return this.windowWidth <= 767;
    },
    isTablet() {
      return this.windowWidth >= 768 && this.windowWidth <= 991;
    },
    sortedMaps() {
      const sortedByName = [...this.maps].sort((a, b) => a.name.localeCompare(b.name));
      const changed = sortedByName.filter(map => map.changed);
      const unchanged = sortedByName.filter(map => !map.changed);
      return [...changed, ...unchanged];
    }
  },
  async created() {
    window.addEventListener('resize', this.updateWindowWidth);
    
    const mapFiles = require.context('@/data/maps', false, /\.json$/);
    const maps = await Promise.all(
      mapFiles.keys().map(async (key) => {
        const mapData = await mapFiles(key);
        return {
          id: mapData.id,
          name: mapData.name,
          image: mapData.image,
          changed: mapData.changed === 'true' || mapData.changed === true
        };
      })
    );
    this.maps = maps;
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
    selectMap(map) {
      this.selectedMapName = map.name.toLowerCase();
      this.$router.push(`/map/${map.name.toLowerCase()}`);
    },
    onSelectItem(payload) {
      const { type, name } = payload || {};
      if (!type || !name) return;
      
      if (type === 'map') {
        this.selectedMapName = name.toLowerCase();
        this.$router.push(`/map/${name.toLowerCase()}`);
      } else {
        this.$router.push(`/${type}/${name.toLowerCase().replace(/ /g, '_')}`);
      }
    },
    onSelectCategory(categoryId) {
      if (categoryId === 'heroes') {
        this.$router.push('/heroes');
      } else if (categoryId === 'general') {
        this.$router.push('/general');
      } else if (categoryId === 'gamemodes') {
        this.$router.push('/gamemodes');
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
  background-image: url('@/assets/maps_page_background.jpg');
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

/* Floating button to show sidebar (desktop only) */
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

/* Maps Grid */
.maps-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
  overflow-y: auto;
  padding-right: 10px;
}

.maps-grid::-webkit-scrollbar {
  width: 8px;
}

.maps-grid::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.3);
  border-radius: 4px;
}

.maps-grid::-webkit-scrollbar-thumb {
  background: #444;
  border-radius: 4px;
}

.maps-grid::-webkit-scrollbar-thumb:hover {
  background: #742aff;
}

.map-card {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  box-shadow: 0 4px 8px rgba(46, 25, 57, 0.5);
}

.map-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(116, 42, 255, 0.3);
}

.image-wrapper {
  position: relative;
  width: 100%;
  height: 180px;
  overflow: hidden;
}

.map-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.map-card:hover .map-image {
  transform: scale(1.05);
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
  transition: opacity 0.3s ease;
}

.map-card.unchanged .overlay {
  background: rgba(0, 0, 0, 0.7);
}

.map-card:hover .overlay {
  opacity: 0;
}

.map-name {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #CCE5FA;
  font-size: 22px;
  font-weight: bold;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.9);
  transition: all 0.3s ease;
  text-align: center;
  padding: 0 10px;
}

.map-card:hover .map-name {
  color: #fff;
  text-shadow: 4px 4px 8px rgba(0, 0, 0, 1);
}

.wip-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(0, 0, 0, 0.8);
  color: #888;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  padding: 6px 12px;
  border-radius: 4px;
  letter-spacing: 0.5px;
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
  
  .image-wrapper {
    height: 160px;
  }
  
  .map-name {
    font-size: 20px;
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
  
  .maps-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }
  
  .image-wrapper {
    height: 140px;
  }
  
  .map-name {
    font-size: 18px;
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
  
  .maps-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }
  
  .image-wrapper {
    height: 160px;
  }
  
  .map-name {
    font-size: 20px;
  }
  
  .wip-badge {
    font-size: 10px;
    padding: 4px 8px;
  }
}

/* SMALL MOBILE (< 480px) */
@media (max-width: 480px) {
  .page-title {
    font-size: 20px;
  }
  
  .image-wrapper {
    height: 140px;
  }
  
  .map-name {
    font-size: 16px;
  }
}
</style>
