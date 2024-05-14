<template>
  <div class="bg-hots-repeat min-h-screen">
    <div class="container mx-auto py-8">
      <nav class="mb-8">
        <button @click="selectTab('patchNotes')"
          :class="['px-14 py-8 text-white font-semibold rounded mr-4 nav-tabs', { 'selected': selectedTab === 'patchNotes' }]">
          Patch Notes
        </button>
        <a href="https://discord.gg/EJCMyy44ej">
          <button
            :class="['px-14 py-8 text-white font-semibold rounded mr-4 nav-tabs', { 'selected': selectedTab === 'communityApproval' }]">
            Vote on Discord
          </button>
        </a>
      </nav>

      <div v-if="selectedTab === 'patchNotes'" class="mt-8">
        <h1 class="text-4xl font-bold text-white mb-4">{{ gameModeItem.name }}</h1>
        <div v-for="patchNote in patchNotes" :key="patchNote.id" class="mb-12">

          <p class="text-gray-400 text-sm mb-6">{{ patchNote.date }}</p>
          <div v-if="patchNote.developerCommentary"
            class="mt-4 bg-[#742aff] bg-opacity-5 border-l-4 border-[#742aff] p-4 text-white italic">
            <p class="font-semibold mb-2">Developer Comment:</p>
            <p v-for="(paragraph, index) in patchNote.developerCommentary.split('\n\n')" :key="index">
              {{ paragraph }}
            </p>
          </div>
          <div v-if="patchNote.general && patchNote.general.length > 0" class="mt-8">
            <h3 class="text-xl font-semibold" style="color: #9900ff;">General Changes</h3>
            <ul class="list-disc list-inside space-y-4" style="color: #ccc8d3;">
              <li v-for="(item, index) in patchNote.general" :key="index">
                <span class="text-lg font-medium" style="color: #0099ff;">{{ item.change }}</span>
                <ul class="list-disc list-inside ml-4">
                  <li v-for="(textItem, textIndex) in item.texts" :key="textIndex">
                    <span style="color: #ccc8d3;">{{ textItem.text }}</span>
                    <div v-if="textItem.image" class="mt-2">
                      <img :src="require(`@/assets/${textItem.image}`)" alt="Patch Note Image"
                        class="max-w-[400px] rounded-[10%] border-4 border-purple-500 mb-7">
                    </div>
                    <ul v-if="textItem.subtexts" class="list-disc list-inside ml-8">
                      <li v-for="(subtext, subtextIndex) in textItem.subtexts" :key="subtextIndex" class="text-sm"
                        style="color: #ccc8d3;">
                        {{ subtext }}
                      </li>
                    </ul>
                  </li>
                </ul>
                <div v-if="item.developerCommentary"
                  class="mt-4 bg-[#742aff] bg-opacity-5 border-l-4 border-[#742aff] p-4 text-white italic">
                  <p class="font-semibold mb-2">Developer Comment:</p>
                  <p>{{ item.developerCommentary }}</p>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>

      <div v-if="selectedTab === 'details'" class="mt-8">
        <div class="general-details-container mt-8">
          <h2 class="text-2xl font-bold text-white mb-4">General Details</h2>
          <p class="text-white">{{ gameModeItem.details }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { watch, ref } from 'vue';
import { useRoute } from 'vue-router';

export default {
  name: 'GameModesPatchNotesPage',
  setup() {
    const route = useRoute();
    const gameModeItem = ref({});
    const patchNotes = ref([]);
    const selectedTab = ref('patchNotes');

    const loadGameModeData = async (gameModeName) => {
      try {
        const gameModeData = await import(`../data/gamemodes/${gameModeName}.json`);
        gameModeItem.value = gameModeData.default;
        patchNotes.value = gameModeData.default.patchNotes;
        console.log('Loaded game mode data:', gameModeData.default);
      } catch (error) {
        console.error('Failed to load game mode data', error);
      }
    };

    watch(
      () => route.params.name,
      (newName) => {
        const gameModeName = newName.toLowerCase().replace(/ /g, '_');
        loadGameModeData(gameModeName);
      },
      { immediate: true }
    );

    const selectTab = (tab) => {
      selectedTab.value = tab;
    };

    return {
      gameModeItem,
      patchNotes,
      selectedTab,
      selectTab,
    };
  },
};
</script>

<style scoped>
@import '@/assets/css/common.css';

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  z-index: 1;
}

.container {
  position: relative;
  z-index: 2;
}

.nav-tabs {
  background-color: #4a148c;
  /* Darker purple */
  transition: background-color 0.3s ease-in-out;
}

.nav-tabs.selected {
  background-color: #6a1b9a;
  /* Slightly lighter purple */
}

.general-details-container {
  background-color: rgba(0, 0, 0, 0.7);
  padding: 20px;
  border-radius: 10px;
}
</style>
