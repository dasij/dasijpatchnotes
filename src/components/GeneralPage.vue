<template>
  <div class="page-wrapper bg-hots-repeat">
    <!-- LEFT SIDEBAR: Full height fixed -->
    <div class="sidebar-fixed" :class="{ hidden: !showSidebar }">
      <UnifiedSidebar
        :selected-item-name="selectedItemName"
        selected-item-type="general"
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

    <!-- Mobile Sticky Menu (always visible on mobile) -->
    <MobileMenuSticky 
      v-if="isMobile" 
      title="General"
      @toggle-sidebar="toggleSidebar"
    />

    <!-- MAIN CONTENT -->
    <div class="main-content" :class="{ 'full-width': !showSidebar }">
      <div class="content-wrapper">
        <div class="content-header">
          <h1 class="page-title">General</h1>
        </div>
        
        <div class="general-grid">
        <div 
          v-for="item in sortedGeneralItems" 
          :key="item.id" 
          class="general-card"
          @click="selectItem(item)"
        >
          <div class="image-wrapper">
            <img :src="require(`@/assets/${item.image}`)" :alt="item.name" class="item-image" />
            <div class="overlay"></div>
            <span class="item-name">{{ formatItemName(item.name) }}</span>
          </div>
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
import MobileMenuSticky from './MobileMenuSticky.vue'

export default {
  name: 'GeneralPage',
  components: {
    MobileMenuSticky
  },
  data() {
    return {
      generalItems: [],
      showSidebar: true,
      windowWidth: window.innerWidth,
      selectedItemName: ''
    };
  },
  computed: {
    isMobile() {
      return this.windowWidth <= 767;
    },
    isTablet() {
      return this.windowWidth >= 768 && this.windowWidth <= 991;
    },
    sortedGeneralItems() {
      return [...this.generalItems].sort((a, b) => a.name.localeCompare(b.name));
    }
  },
  async created() {
    window.addEventListener('resize', this.updateWindowWidth);
    
    const generalFiles = require.context('@/data/general', false, /\.json$/);
    const items = await Promise.all(
      generalFiles.keys().map(async (key) => {
        const itemData = await generalFiles(key);
        return {
          id: itemData.id,
          name: itemData.name,
          image: itemData.image,
          description: itemData.description,
        };
      })
    );
    this.generalItems = items;
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
    selectItem(item) {
      this.selectedItemName = item.name.toLowerCase();
      const pathName = item.name.toLowerCase().replace(/ /g, '_');
      this.$router.push(`/general/${pathName}`);
    },
    onSelectItem(payload) {
      const { type, name } = payload || {};
      if (!type || !name) return;
      
      if (type === 'general') {
        this.selectedItemName = name.toLowerCase();
        const pathName = name.toLowerCase().replace(/ /g, '_');
        this.$router.push(`/general/${pathName}`);
      } else {
        this.$router.push(`/${type}/${name.toLowerCase().replace(/ /g, '_')}`);
      }
    },
    onSelectCategory(categoryId) {
      if (categoryId === 'heroes') {
        this.$router.push('/heroes');
      } else if (categoryId === 'maps') {
        this.$router.push('/maps');
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
  background-image: url('@/assets/general_page_background.jpg');
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

/* Content Wrapper - Limita e centraliza o conteúdo */
.content-wrapper {
  display: flex;
  flex-direction: column;
  gap: 10px;
  height: auto;
  max-height: 1200px;
  width: 100%;
  max-width: 1200px;
  margin: auto;
  background-color: rgba(0, 0, 0, 0.7);
  border-radius: 12px;
  padding: 20px 30px;
  overflow: hidden;
  box-sizing: border-box;
}

/* Para monitores grandes - centraliza o conteúdo */
@media (min-height: 1080px) and (min-width: 1024px) {
  .main-content {
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .content-wrapper {
    height: 100%;
    max-height: 1200px;
    margin: auto;
  }
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

/* General Grid */
.general-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding-right: 10px;
}

.general-grid::-webkit-scrollbar {
  width: 8px;
}

.general-grid::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.3);
  border-radius: 4px;
}

.general-grid::-webkit-scrollbar-thumb {
  background: #444;
  border-radius: 4px;
}

.general-grid::-webkit-scrollbar-thumb:hover {
  background: #742aff;
}

.general-card {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  box-shadow: 0 4px 8px rgba(46, 25, 57, 0.5);
}

.general-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(116, 42, 255, 0.3);
}

.image-wrapper {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
}

.item-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease, filter 0.3s ease;
  filter: brightness(50%);
}

.general-card:hover .item-image {
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

.general-card:hover .overlay {
  opacity: 0;
}

.item-name {
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

.general-card:hover .item-name {
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
  
  .content-wrapper {
    padding: 15px 20px;
  }
  
  .page-title {
    font-size: 28px;
  }
  
  .image-wrapper {
    height: 180px;
  }
  
  .item-name {
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
  
  .content-wrapper {
    max-height: none;
    height: auto;
    padding: 15px 20px;
  }
  
  .general-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
  }
  
  .image-wrapper {
    height: 160px;
  }
  
  .item-name {
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
    padding: 60px 15px 15px 15px; /* Espaço para barra sticky no topo */
  }
  
  .content-wrapper {
    max-height: none;
    height: auto;
    padding: 15px;
  }
  
  .page-title {
    font-size: 24px;
    text-align: center;
  }
  
  .general-grid {
    grid-template-columns: 1fr;
    gap: 12px;
    max-height: none;
  }
  
  .image-wrapper {
    height: 180px;
  }
  
  .item-name {
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
  
  .item-name {
    font-size: 18px;
  }
}
</style>
