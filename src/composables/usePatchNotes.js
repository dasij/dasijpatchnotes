// src/composables/usePatchNotes.js
import { ref, watch } from 'vue';
import { useRoute } from 'vue-router';

export default function usePatchNotes() {
    const route = useRoute();
    const item = ref({});
    const patchNotes = ref([]);
    const selectedTab = ref('patchNotes');

    const loadData = async (type, name) => {
        try {
            const data = await import(`../data/${type}/${name}.json`);
            item.value = data.default;
            patchNotes.value = data.default.patchNotes;
            console.log(`Loaded ${type} data:`, data.default);
        } catch (error) {
            console.error(`Failed to load ${type} data`, error);
        }
    };

    const loadGameModeData = (gameModeName) => loadData('gamemodes', gameModeName);
    const loadMapData = (mapName) => loadData('maps', mapName);
    const loadGeneralData = (generalName) => loadData('general', generalName);
    const loadHeroData = (heroName) => loadData('heroes', heroName);

    watch(
        () => route.params.name,
        (newName) => {
            const name = newName.toLowerCase().replace(/ /g, '_');
            if (route.path.includes('gamemodes')) loadGameModeData(name);
            else if (route.path.includes('maps')) loadMapData(name);
            else if (route.path.includes('general')) loadGeneralData(name);
            else if (route.path.includes('heroes')) loadHeroData(name);
        },
        { immediate: true }
    );

    const selectTab = (tab) => {
        selectedTab.value = tab;
    };

    return {
        item,
        patchNotes,
        selectedTab,
        selectTab,
    };
}
