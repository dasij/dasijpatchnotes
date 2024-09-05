<template>
  <div class="bg-hots-repeat bg-repeat-y bg-contain bg-center min-h-screen">
    <MetaTags :title="pageTitle" :description="pageDescription" :image="pageImage" />

    <div class="container mx-auto py-20">
      <nav class="mb-8">
        <button @click="selectTab('patchNotes')" :class="{ 'selected': selectedTab === 'patchNotes' }"
          class="px-14 py-8 text-white font-semibold rounded mr-4 nav-tabs">
          Patch Notes
        </button>
        <button @click="selectTab('talents')" :class="{ 'selected': selectedTab === 'talents' }"
          class="px-14 py-8 text-white font-semibold rounded mr-4 nav-tabs">
          Talent Selector
        </button>
      </nav>

      <HeroPatchNotes v-if="selectedTab === 'patchNotes'" :heroName="heroName" :patchNotes="patchNotes" />

      <div v-if="selectedTab === 'talents'">
        <HeroAbilities v-if="talents && talents.abilities" :abilities="talents.abilities" :heroName="heroName" />


        <HeroTalentCalculator :talents="talents" :heroName="heroName" :talentType="talentType"
          @toggle-talent-type="toggleTalentType" />
      </div>
    </div>
  </div>
</template>



<script>
import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import MetaTags from './MetaTags.vue';
import HeroPatchNotes from './HeroPatchNotes.vue';
import HeroTalentCalculator from './HeroTalentCalculator.vue';
import HeroAbilities from './HeroAbilities.vue';

export default {
  name: 'HeroPage',
  components: {
    MetaTags,
    HeroPatchNotes,
    HeroTalentCalculator,
    HeroAbilities
  },
  setup() {
    const route = useRoute();
    const heroName = ref('');
    const hero = ref(null);
    const patchNotes = ref([]);
    const talents = ref(null);
    const selectedTab = ref('patchNotes');
    const talentType = ref('modified');
    const pageTitle = ref('');
    const pageDescription = ref('Hero Description');
    const pageImage = ref('');

    const loadHeroData = () => {
      const heroData = require(`@/data/heroes/${heroName.value}.json`);
      if (heroData) {
        hero.value = heroData;
        patchNotes.value = heroData.patchNotes;
        talents.value = require(`@/data/heroes/talents/${heroName.value}_talents.json`);
        pageTitle.value = heroData.name;
        pageDescription.value = heroData.description || 'Hero Description';
        pageImage.value = require(`@/assets/${heroData.image}`);
      } else {
        console.error('Failed to load hero data');
      }
    };

    const selectTab = (tab) => {
      selectedTab.value = tab;
    };

    const loadTalents = () => {
      const talentFileName = talentType.value === 'vanilla'
        ? `${heroName.value}_talents_vanilla.json`
        : `${heroName.value}_talents.json`;

      talents.value = require(`@/data/heroes/talents/${talentFileName}`);
    };

    const toggleTalentType = () => {
      talentType.value = talentType.value === 'modified' ? 'vanilla' : 'modified';
      loadTalents();
    };

    onMounted(() => {
      heroName.value = route.params.name.toLowerCase();
      loadHeroData();
    });

    watch(() => route.params.name, (newName) => {
      heroName.value = newName.toLowerCase();
      loadHeroData();
    });

    return {
      heroName,
      hero,
      patchNotes,
      talents,
      selectedTab,
      talentType,
      pageTitle,
      pageDescription,
      pageImage,
      selectTab,
      toggleTalentType
    };
  }
};
</script>


<style scoped>
/* Estilos específicos da página principal */
</style>
