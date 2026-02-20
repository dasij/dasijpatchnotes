<template>
    <div class="bg-hots-repeat min-h-screen">
        <div class="container mx-auto py-8">
            <nav class="mb-8">
                <button @click="selectTab('patchNotes')" :class="{ 'selected': selectedTab === 'patchNotes' }"
                    class="px-14 py-8 text-white font-semibold rounded mr-4 nav-tabs">
                    Patch Notes
                </button>
            </nav>

            <div v-if="selectedTab === 'patchNotes'" class="mt-8">
                <div class="bg-hots-repeat min-h-screen">
                    <div class="container mx-auto py-8">
                        <h1 class="text-4xl font-bold text-white mb-4">{{ map.name }} PATCH NOTES</h1>
                        
                        <!-- Empty State - No Content -->
                        <div v-if="!patchNotes || patchNotes.length === 0" class="empty-state">
                            <div class="empty-content">
                                <span class="empty-icon">🗺️</span>
                                <h2 class="empty-title">No Patch Notes Available</h2>
                                <p class="empty-text">This map doesn't have any changes yet.</p>
                                <p class="empty-subtext">Please select another map from the sidebar.</p>
                            </div>
                        </div>
                        
                        <div v-for="patchNote in patchNotes" :key="patchNote.id" class="mb-12">
                            <h2 class="text-2xl font-bold text-white mb-2">{{ patchNote.title }}</h2>
                            <p class="text-gray-400 text-sm mb-6">{{ patchNote.date }}</p>
                            <div v-if="patchNote.developerCommentary"
                                class="mt-4 bg-[#742aff] bg-opacity-5 border-l-4 border-[#742aff] p-4 text-white italic">
                                <p class="font-semibold mb-2">Developer Comment:</p>
                                <p v-for="(paragraph, index) in patchNote.developerCommentary.split('\n\n')"
                                    :key="index">
                                    {{ paragraph }}
                                </p>
                            </div>
                            <div v-if="patchNote.general && patchNote.general.length > 0" class="mt-8">
                                <h3 class="text-xl font-semibold" style="color: #9900ff;">General Changes</h3>
                                <ul class="list-disc list-inside space-y-4" style="color: #ccc8d3;">
                                    <li v-for="(item, index) in patchNote.general" :key="index">
                                        <span class="text-lg font-medium" style="color: #0099ff;">{{ item.change
                                            }}</span>
                                        <ul class="list-disc list-inside ml-4">
                                            <li v-for="(textItem, textIndex) in item.texts" :key="textIndex">
                                                <span style="color: #ccc8d3;">{{ textItem.text }}</span>
                                                <div v-if="textItem.image" class="mt-2">
                                                    <img :src="require(`@/assets/${textItem.image}`)"
                                                        alt="Patch Note Image"
                                                        class="max-w-[400px] rounded-[10%] border-4 border-purple-500 mb-7">
                                                </div>
                                                <ul v-if="textItem.subtexts" class="list-disc list-inside ml-8">
                                                    <li v-for="(subtext, subtextIndex) in textItem.subtexts"
                                                        :key="subtextIndex" class="text-sm" style="color: #ccc8d3;">
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
                </div>
            </div>

            <div v-if="selectedTab === 'details'" class="mt-8">
                <div class="map-details-container mt-8">
                    <h2 class="text-2xl font-bold text-white mb-4">Map Details</h2>
                    <p class="text-white">{{ map.details }}</p>
                </div>
            </div>
        </div>
    </div>
</template>


<script>
import { watch, ref } from 'vue';
import { useRoute } from 'vue-router';

export default {
    name: 'MapPatchNotesPage',
    setup() {
        const route = useRoute();
        const map = ref({});
        const patchNotes = ref([]);
        const selectedTab = ref('patchNotes');

        const loadMapData = async (mapName) => {
            try {
                const mapData = await import(`../data/maps/${mapName}.json`);
                map.value = mapData.default;
                patchNotes.value = mapData.default.patchNotes;
            } catch (error) {
                console.error('Failed to load map data', error);
            }
        };

        watch(
            () => route.params.name,
            (newName) => {
                const mapName = newName.toLowerCase().replace(/ /g, '_');
                loadMapData(mapName);
            },
            { immediate: true }
        );

        const selectTab = (tab) => {
            selectedTab.value = tab;
        };

        return {
            map,
            patchNotes,
            selectedTab,
            selectTab,
        };
    },
};
</script>


<style scoped>
@import '@/assets/css/common.css';

/* Empty State Styles */
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
</style>
