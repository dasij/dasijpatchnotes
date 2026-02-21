<template>
  <div class="page-wrapper bg-hots-repeat">
    <!-- LEFT SIDEBAR: Full height fixed -->
    <div class="sidebar-fixed" :class="{ hidden: !showSidebar }">
      <UnifiedSidebar
        :selected-item-name="modeName"
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

    <!-- Mobile Sticky Menu (always visible on mobile) -->
    <MobileMenuSticky 
      v-if="isMobile" 
      title="Game Modes"
      @toggle-sidebar="toggleSidebar"
    />

    <!-- MAIN CONTENT -->
    <div class="main-content" :class="{ 'full-width': !showSidebar }">
      <div class="content-wrapper">
        <!-- Header -->
        <div class="content-header">
          <h1 class="page-title">{{ gameModeItem.name }} PATCH NOTES</h1>
        </div>

        <!-- Content -->
        <div class="content-body">
          <!-- Empty State - No Content -->
          <div v-if="!patchNotes || patchNotes.length === 0" class="empty-state">
            <div class="empty-content">
              <span class="empty-icon">🎮</span>
              <h2 class="empty-title">No Patch Notes Available</h2>
              <p class="empty-text">This game mode doesn't have any changes yet.</p>
              <p class="empty-subtext">Please select another mode from the sidebar.</p>
            </div>
          </div>

          <!-- Patch Notes List -->
          <div v-else class="patch-notes-list">
            <div v-for="patchNote in patchNotes" :key="patchNote.id" class="patch-note-item">
              <h2 class="patch-note-title">{{ patchNote.title }}</h2>
              <p class="patch-note-date">{{ patchNote.date }}</p>
              
              <div v-if="patchNote.developerCommentary" class="dev-commentary">
                <p class="dev-label">Developer Comment:</p>
                <p v-for="(paragraph, index) in patchNote.developerCommentary.split('\n\n')" :key="index">
                  {{ paragraph }}
                </p>
              </div>

              <div v-if="patchNote.general && patchNote.general.length > 0" class="general-changes">
                <h3 class="changes-title">General Changes</h3>
                <ul class="changes-list">
                  <li v-for="(item, index) in patchNote.general" :key="index" class="change-item">
                    <span class="change-name">{{ item.change }}</span>
                    <ul class="texts-list">
                      <li v-for="(textItem, textIndex) in item.texts" :key="textIndex" class="text-item">
                        <span>{{ textItem.text }}</span>
                        <div v-if="textItem.image" class="image-container">
                          <img :src="require(`@/assets/${textItem.image}`)" alt="Patch Note Image" class="patch-image">
                        </div>
                        <ul v-if="textItem.subtexts" class="subtexts-list">
                          <li v-for="(subtext, subtextIndex) in textItem.subtexts" :key="subtextIndex" class="subtext-item">
                            {{ subtext }}
                          </li>
                        </ul>
                      </li>
                    </ul>
                    <div v-if="item.developerCommentary" class="dev-commentary-item">
                      <p class="dev-label">Developer Comment:</p>
                      <p>{{ item.developerCommentary }}</p>
                    </div>
                  </li>
                </ul>
              </div>
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
import { watch, ref, computed, onMounted, onUnmounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import MobileMenuSticky from './MobileMenuSticky.vue';

export default {
  name: 'GameModesPatchNotesPage',
  components: {
    MobileMenuSticky
  },
  setup() {
    const route = useRoute();
    const router = useRouter();
    const gameModeItem = ref({});
    const patchNotes = ref([]);
    const modeName = ref('');
    const showSidebar = ref(true);
    const windowWidth = ref(window.innerWidth);

    const isMobile = computed(() => windowWidth.value <= 767);

    const updateWindowWidth = () => {
      windowWidth.value = window.innerWidth;
    };

    onMounted(() => {
      window.addEventListener('resize', updateWindowWidth);
    });

    onUnmounted(() => {
      window.removeEventListener('resize', updateWindowWidth);
    });

    const loadGameModeData = async (name) => {
      try {
        const gameModeData = await import(`../data/gamemodes/${name}.json`);
        gameModeItem.value = gameModeData.default;
        patchNotes.value = gameModeData.default.patchNotes || [];
        modeName.value = name;
      } catch (error) {
        console.error('Failed to load game mode data', error);
      }
    };

    watch(
      () => route.params.name,
      (newName) => {
        const normalizedName = newName.toLowerCase().replace(/ /g, '_');
        loadGameModeData(normalizedName);
      },
      { immediate: true }
    );

    const toggleSidebar = () => {
      showSidebar.value = !showSidebar.value;
    };

    const onSelectItem = (payload) => {
      const { type, name } = payload || {};
      if (!type || !name) return;
      
      if (type === 'gamemode') {
        router.push(`/gamemode/${name.toLowerCase().replace(/ /g, '_')}`);
      } else {
        router.push(`/${type}/${name.toLowerCase().replace(/ /g, '_')}`);
      }
    };

    const onSelectCategory = (categoryId) => {
      if (categoryId === 'heroes') {
        router.push('/heroes');
      } else if (categoryId === 'maps') {
        router.push('/maps');
      } else if (categoryId === 'general') {
        router.push('/general');
      } else if (categoryId === 'gamemodes') {
        router.push('/gamemodes');
      }
    };

    return {
      gameModeItem,
      patchNotes,
      modeName,
      showSidebar,
      isMobile,
      toggleSidebar,
      onSelectItem,
      onSelectCategory,
    };
  },
};
</script>

<style scoped>
@import '@/assets/css/common.css';

/* Page Wrapper */
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

/* Main Content - Container para posicionamento absoluto */
.main-content {
  margin-left: 280px;
  flex: 1;
  height: 100vh;
  padding: 20px;
  position: relative;
  overflow: hidden;
  transition: margin-left 0.3s ease;
}

.main-content.full-width {
  margin-left: 0;
}

/* Content Wrapper - CENTRALIZADO ABSOLUTO */
.content-wrapper {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: calc(100% - 40px);
  max-width: 1200px;
  max-height: min(1200px, calc(100vh - 40px));
  background-color: rgba(0, 0, 0, 0.7);
  border-radius: 12px;
  padding: 20px 30px;
  overflow: hidden;
  box-sizing: border-box;
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

/* Content Body - SCROLLABLE */
.content-body {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding-right: 10px;
}

.content-body::-webkit-scrollbar {
  width: 8px;
}

.content-body::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.3);
  border-radius: 4px;
}

.content-body::-webkit-scrollbar-thumb {
  background: #444;
  border-radius: 4px;
}

.content-body::-webkit-scrollbar-thumb:hover {
  background: #742aff;
}

/* Empty State */
.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  padding: 40px 20px;
}

.empty-content {
  text-align: center;
  background: rgba(0, 0, 0, 0.5);
  border: 2px solid #444;
  border-radius: 16px;
  padding: 40px;
  max-width: 400px;
}

.empty-icon {
  font-size: 64px;
  display: block;
  margin-bottom: 20px;
}

.empty-title {
  color: #fff;
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 12px;
}

.empty-text {
  color: #ccc;
  font-size: 16px;
  margin-bottom: 8px;
}

.empty-subtext {
  color: #888;
  font-size: 14px;
}

/* Patch Notes Styles */
.patch-notes-list {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.patch-note-item {
  padding-bottom: 30px;
  border-bottom: 1px solid #333;
}

.patch-note-item:last-child {
  border-bottom: none;
}

.patch-note-title {
  color: #fff;
  font-size: 24px;
  font-weight: bold;
  margin: 0 0 8px 0;
}

.patch-note-date {
  color: #888;
  font-size: 14px;
  margin: 0 0 20px 0;
}

.dev-commentary {
  margin: 16px 0;
  background: rgba(116, 42, 255, 0.1);
  border-left: 4px solid #742aff;
  padding: 16px;
  color: #fff;
  font-style: italic;
  border-radius: 0 8px 8px 0;
}

.dev-commentary-item {
  margin: 16px 0;
  background: rgba(116, 42, 255, 0.1);
  border-left: 4px solid #742aff;
  padding: 16px;
  color: #fff;
  font-style: italic;
  border-radius: 0 8px 8px 0;
}

.dev-label {
  font-weight: 600;
  margin-bottom: 8px;
  color: #fff;
}

.general-changes {
  margin-top: 24px;
}

.changes-title {
  color: #9900ff;
  font-size: 20px;
  font-weight: 600;
  margin: 0 0 16px 0;
}

.changes-list {
  list-style: disc;
  list-style-position: inside;
  padding: 0;
  margin: 0;
  color: #ccc8d3;
}

.change-item {
  margin-bottom: 16px;
}

.change-name {
  color: #0099ff;
  font-size: 18px;
  font-weight: 500;
}

.texts-list {
  list-style: disc;
  list-style-position: inside;
  margin: 12px 0 0 16px;
  padding: 0;
}

.text-item {
  margin-bottom: 12px;
  color: #ccc8d3;
}

.image-container {
  margin: 16px 0;
}

.patch-image {
  max-width: 400px;
  border-radius: 10%;
  border: 4px solid #742aff;
  margin-bottom: 28px;
}

.subtexts-list {
  list-style: disc;
  list-style-position: inside;
  margin: 8px 0 0 24px;
  padding: 0;
}

.subtext-item {
  font-size: 14px;
  color: #ccc8d3;
  margin-bottom: 4px;
}

/* Responsive */
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
  
  .content-body {
    max-height: none;
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
    padding: 60px 15px 15px 15px;
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
  
  .patch-image {
    max-width: 100%;
  }
}
</style>
