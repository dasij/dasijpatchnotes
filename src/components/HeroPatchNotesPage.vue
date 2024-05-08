<template>

  <div class="bg-hots-repeat bg-repeat-y bg-contain bg-center bg-no-repeat min-h-screen">
    <div class="container mx-auto py-8">
      <h1 class="text-4xl font-bold text-white mb-4">{{ hero.name }} PATCH NOTES</h1>

      <nav class="mb-8">

        <button @click="selectedTab = 'patchNotes'" :class="{ 'bg-purple-600': selectedTab === 'patchNotes' }"
          class="px-4 py-2 text-white font-semibold rounded">
          Patch Notes
        </button>
        <button @click="selectedTab = 'talents'" :class="{ 'bg-purple-600': selectedTab === 'talents' }"
          class="px-4 py-2 text-white font-semibold rounded mr-4">
          Talent Selector
        </button>

      </nav>



      <div v-if="selectedTab === 'patchNotes'" class="mt-8">
        <div class="bg-hots-repeat bg-repeat-y bg-contain bg-center bg-no-repeat min-h-screen">
          <div class="container mx-auto py-8">
            <h1 class="text-4xl font-bold text-white mb-4">{{ hero.name }} PATCH NOTES</h1>

            <div v-for="patchNote in patchNotes" :key="patchNote.id" class="mb-12">
              <h2 class="text-2xl font-bold text-white mb-2">{{ patchNote.title }}</h2>
              <p class="text-gray-400 text-sm mb-6">{{ patchNote.date }}</p>

              <div v-if="patchNote.developerCommentary"
                class="mt-4 bg-[#742aff] bg-opacity-5 border-l-4 border-[#742aff] p-4 text-white italic">
                <p class="font-semibold mb-2">Developer Comment:</p>
                <p v-for="(paragraph, index) in patchNote.developerCommentary.split('\n\n')" :key="index">
                  {{ paragraph }}
                </p>
              </div>

              <div v-if="patchNote.general && patchNote.general.length > 0" class="mt-8">
                <h3 class="text-xl font-semibold" style="color: #9900ff;">Base</h3>
                <ul class="list-disc list-inside space-y-4" style="color: #ccc8d3;">
                  <li v-for="(item, index) in patchNote.general" :key="index">
                    <span class="text-lg font-medium" style="color: #0099ff;">{{ item.change }}</span>
                    <ul class="list-disc list-inside ml-4">
                      <li v-for="(textItem, textIndex) in item.texts" :key="textIndex">
                        <span style="color: #ccc8d3;">{{ textItem.text }}</span>
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

              <div v-if="patchNote.sections" class="mt-8">
                <h3 class="text-xl font-semibold" style="color: #9900ff;">Talent</h3>
                <ul class="list-disc list-inside space-y-4" style="color: #ccc8d3;">
                  <li v-for="(section, sectionIndex) in patchNote.sections" :key="sectionIndex">
                    <span class="text-lg font-medium">{{ section.name }}</span>
                    <ul class="list-disc list-inside ml-4">
                      <li v-for="(change, changeIndex) in section.changes" :key="changeIndex">
                        <span class="text-lg font-medium" style="color: #0099ff;">{{ change.name }}</span>
                        <ul class="list-disc list-inside ml-4">
                          <li v-for="(textItem, textIndex) in change.texts" :key="textIndex">
                            <span style="color: #ccc8d3;">{{ textItem.text }}</span>
                            <ul v-if="textItem.subtexts" class="list-disc list-inside ml-8">
                              <li v-for="(subtext, subtextIndex) in textItem.subtexts" :key="subtextIndex"
                                class="text-sm" style="color: #ccc8d3;">
                                {{ subtext }}
                              </li>
                            </ul>
                          </li>
                        </ul>
                        <div v-if="change.developerCommentary"
                          class="mt-4 bg-[#742aff] bg-opacity-5 border-l-4 border-[#742aff] p-4 text-white italic">
                          <p class="font-semibold mb-2">Developer Comment:</p>
                          <p>{{ change.developerCommentary }}</p>
                        </div>
                      </li>
                    </ul>
                  </li>
                </ul>
              </div>
            </div>


          </div>
        </div>
      </div>

      <div v-if="selectedTab === 'talents'" class="mt-8">
        <div class="mt-8">
          <h2 class="text-2xl font-bold text-white mb-4">Talent Calculator</h2>
          <div class="talent-calculator-container"
            :style="{ backgroundImage: `url(${require('@/assets/talents/talents_bg.webp')})` }">
            <div class="flex flex-col space-y-4">
              <div v-for="level in [1, 4, 7, 10, 13, 16, 20]" :key="level" class="flex items-center">
                <h3 class="text-xl font-semibold mr-4 w-20" style="color: #9900ff;"> Level {{ level }}</h3>
                <div class="flex ml-12">
                  <div v-for="(talent, index) in talents[level]" :key="talent.name" class="talent-column"
                    :class="{ 'ml-8': index > 0 }">
                    <div class="talent-image-container" :class="{ 'talent-changed': talent.talentChanged }"
                      @mouseover="showTooltip(talent)" @mouseleave="hideTooltip">
                      <img :src="require(`@/assets/talents/${heroName}/${talent.image}`)" :alt="talent.name"
                        class="talent-image" />
                      <div v-if="tooltipTalent === talent"
                        class="absolute bg-black bg-opacity-95 text-white p-4 rounded border border-purple-800"
                        style="top: 50%; left: calc(100% + 10px); transform: translateY(-50%); width: 250px; z-index: 1;">
                        <h4 class="text-xl font-semibold mb-2" style="color: #0099ff;">{{ talent.name }}</h4>
                        <div class="flex items-center text-xs mb-2">
                          <div v-if="talent.manaCost" class="mr-2">
                            <span class="font-semibold">Mana Cost:</span> {{ talent.manaCost }}
                          </div>
                          <div v-if="talent.cooldown">
                            <span class="font-semibold">Cooldown:</span> {{ talent.cooldown }}
                          </div>
                        </div>
                        <p class="text-sm">{{ talent.description }}</p>
                        <div v-if="talent.passives && talent.passives.length > 0" class="mt-2">
                          <p v-for="(passive, index) in talent.passives" :key="index" class="text-sm">
                            <span class="font-semibold" style="color: #78da5b;">Passive:</span> {{ passive }}
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>



    </div>
  </div>


</template>

<style scoped>
.talent-calculator-container {
  background-size: cover;
  background-position: center;
  padding: 50px;
  border-radius: 10px;
  display: inline-block;
  border: 2px solid #18192D;
  box-shadow: 0 0 5px 2px rgba(90, 188, 227, 0.8);
}

.talent-column {
  position: relative;
}

.talent-image-container {
  width: 64px;
  height: 64px;
  overflow: hidden;
  border-radius: 10%;
}

.talent-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.talent-changed {
  border: 2px solid red;
}

.talent-image-container:hover {
  box-shadow: 0 0 10px 5px rgba(90, 188, 227, 0.8);
}
</style>

<script>
export default {
  name: 'HeroPatchNotesPage',
  data() {
    return {
      hero: {},
      patchNotes: [],
      talents: {},
      tooltipTalent: null,
      selectedTab: 'patchNotes',
    }
  },
  computed: {
    heroName() {
      return this.$route.params.name.toLowerCase();
    },
  },
  created() {
    const heroData = require(`../data/heroes/${this.heroName}.json`);
    this.hero = heroData;
    this.patchNotes = heroData.patchNotes;
    this.talents = require(`../data/heroes/talents/${this.heroName}.json`);
  },
  methods: {
    showTooltip(talent) {
      this.tooltipTalent = talent;
    },
    hideTooltip() {
      this.tooltipTalent = null;
    },
  },
}
</script>