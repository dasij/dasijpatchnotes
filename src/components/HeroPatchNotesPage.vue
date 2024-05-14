<template>
  <div class="bg-hots-repeat bg-repeat-y bg-contain bg-center bg-no-repeat min-h-screen">
    <div class="container mx-auto py-8">

      <nav class="mb-8">


        <button @click="selectTab('patchNotes')" :class="{ 'selected': selectedTab === 'patchNotes' }"
          class="px-14 py-8 text-white font-semibold rounded mr-4 nav-tabs">
          Patch Notes
        </button>
        <button @click="selectTab('talents')" :class="{ 'selected': selectedTab === 'talents' }"
          class="px-14 py-8 text-white font-semibold rounded mr-4 nav-tabs">
          Talent Selector
        </button>
        <a href="https://discord.gg/EJCMyy44ej">
          <button :class="{ 'selected': selectedTab === 'communityApproval' }"
            class="px-14 py-8 text-white font-semibold rounded mr-4 nav-tabs">
            Vote on Discord
          </button>
        </a>


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
        <div class="abilities-container mt-8">
          <h2 class="text-2xl font-bold text-white mb-4">Basic Abilities</h2>
          <div class="flex justify-start">
            <div v-for="ability in talents.abilities.basic" :key="ability.name" class="ability"
              @mouseover="tooltipAbility = ability" @mouseleave="tooltipAbility = null">
              <div class="hexagon-border" :class="{ 'ability-changed': ability.abilityChanged }">
                <img :src="require(`@/assets/talents/${heroName}/${ability.image}`)" alt="ability image"
                  class="ability-image">
              </div>
              <div v-if="tooltipAbility === ability"
                class="absolute bg-black bg-opacity-95 text-white p-4 rounded border border-purple-800"
                style="top: 50%; left: calc(100% + 10px); transform: translateY(-50%); width: 250px; z-index: 1;">
                <h3 class="text-xl font-semibold" style="color: #0099ff;">{{ ability.name }}</h3>
                <div class="flex items-center text-xs mb-2">
                  <div v-if="ability.cooldown" class="mr-2">
                    <span class="font-semibold">Cooldown:</span> <span v-html="formatText(ability.cooldown)"></span>
                  </div>
                  <div v-if="ability.manaCost">
                    <span class="font-semibold">Mana Cost:</span> <span v-html="formatText(ability.manaCost)"></span>
                  </div>
                </div>
                <p class="text-sm" v-html="formatText(ability.description)"></p>
                <div v-if="ability.passives && ability.passives.length > 0" class="mt-2">
                  <ul>
                    <li v-for="(passive, index) in ability.passives" :key="index" class="text-sm text-gray-400"
                      v-html="formatText(passive)">
                    </li>
                  </ul>
                </div>
              </div>

            </div>
          </div>
          <h2 class="text-2xl font-bold text-white mb-4">Heroic Abilities</h2>
          <div class="flex justify-start">
            <div v-for="ability in talents.abilities.heroic" :key="ability.name" class="ability"
              @mouseover="tooltipAbility = ability" @mouseleave="tooltipAbility = null">
              <div class="hexagon-border" :class="{ 'ability-changed': ability.abilityChanged }">
                <img :src="require(`@/assets/talents/${heroName}/${ability.image}`)" alt="ability image"
                  class="ability-image">
              </div>
              <div v-if="tooltipAbility === ability"
                class="absolute bg-black bg-opacity-95 text-white p-4 rounded border border-purple-800"
                style="top: 50%; left: calc(100% + 10px); transform: translateY(-50%); width: 250px; z-index: 1;">
                <h3 class="text-xl font-semibold" style="color: #0099ff;">{{ ability.name }}</h3>
                <div class="flex items-center text-xs mb-2">
                  <div v-if="ability.cooldown" class="mr-2">
                    <span class="font-semibold">Cooldown:</span> <span v-html="formatText(ability.cooldown)"></span>
                  </div>
                  <div v-if="ability.manaCost">
                    <span class="font-semibold">Mana Cost:</span> <span v-html="formatText(ability.manaCost)"></span>
                  </div>
                </div>
                <p class="text-sm" v-html="formatText(ability.description)"></p>
                <div v-if="ability.passives && ability.passives.length > 0" class="mt-2">
                  <ul>
                    <li v-for="(passive, index) in ability.passives" :key="index" class="text-sm text-gray-400"
                      v-html="formatText(passive)">
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>

          <h2 class="text-2xl font-bold text-white mb-4">Trait</h2>
          <div class="flex justify-start">
            <div class="ability" @mouseover="tooltipAbility = talents.abilities.trait"
              @mouseleave="tooltipAbility = null">
              <div class="hexagon-border" :class="{ 'ability-changed': talents.abilities.trait.abilityChanged }">
                <img :src="require(`@/assets/talents/${heroName}/${talents.abilities.trait.image}`)" alt="trait image"
                  class="ability-image">
              </div>
              <div v-if="tooltipAbility === talents.abilities.trait"
                class="absolute bg-black bg-opacity-95 text-white p-4 rounded border border-purple-800"
                style="top: 50%; left: calc(100% + 10px); transform: translateY(-50%); width: 250px; z-index: 1;">
                <h3 class="text-xl font-semibold" style="color: #0099ff;">{{ talents.abilities.trait.name }}</h3>
                <p class="text-sm" v-html="formatText(talents.abilities.trait.description)"></p>
                <div v-if="talents.abilities.trait.passives && talents.abilities.trait.passives.length > 0"
                  class="mt-2">
                  <ul>
                    <li v-for="(passive, index) in talents.abilities.trait.passives" :key="index" class="text-sm">
                      <span class="font-semibold" style="color: #78da5b;">Passive: </span>
                      <span v-html="formatText(passive)"></span>
                    </li>
                  </ul>
                </div>
              </div>

            </div>
          </div>
        </div>

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
                        <p class="text-sm" v-html="formatText(talent.description)"></p>
                        <div v-if="talent.passives && talent.passives.length > 0" class="mt-2">
                          <p v-for="(passive, index) in talent.passives" :key="index" class="text-sm">
                            <span class="font-semibold" style="color: #78da5b;">Passive:</span>
                            <span v-html="formatText(passive)"></span>
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

      <div v-if="selectedTab === 'communityApproval'" class="mt-8">
        <h2 class="text-2xl font-bold text-white mb-4">Community Approval</h2>
        <p class="text-white">Thumbs Up Count: {{ thumbsUpCount }}.</p>
        <!-- Additional content can be added here -->
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

.highlight-text {
  color: #78da5b !important;
}

.quest-text {
  color: #DFCB00 !important;
}

.reward-text {
  color: #DFCB00 !important;
}

.passive-text {
  color: #78da5b !important;
}

.talent-tooltip .highlight-text {
  color: red !important;
  font-size: 30px !important;
  /* Adjust the color as needed */
}

.talent-changed {
  border: 2px solid red;
}

.talent-image-container:hover {
  box-shadow: 0 0 10px 5px rgba(90, 188, 227, 0.8);
}


.ability {
  margin: 10px;
  /* Adjust the spacing as needed */
  position: relative;
  display: inline-block;
  /* This helps in aligning the abilities next to each other with spacing */
}

.hexagon-border {
  position: relative;
  width: 79px;
  height: 90px;
  background: url('@/assets/talents/hexagon.png') center/contain no-repeat;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: visible;
  transition: filter 0.3s ease-in-out;

}

.hexagon-border::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 0, 0, 1);
  box-shadow: 0 0 30px 15px rgba(255, 0, 0, 1);
  -webkit-mask-image: url('@/assets/talents/hexagon.png');
  mask-image: url('@/assets/talents/hexagon.png');
  mask-mode: alpha;
  /* Different color to distinguish */
  opacity: 0;
  /* Hide initially */
  transition: opacity 0.3s ease-in-out;
}

.hexagon-border.ability-changed {
  filter: drop-shadow(0 0 20px rgba(255, 0, 0, 1));
  /* Apply a red border */
}

.hexagon-border:hover::before {
  opacity: 0.6;
  /* Show on hover */
}

.hexagon-border:hover {
  filter: drop-shadow(0 0 20px rgba(90, 188, 227, 0.8));
  /* Red shadow */
}

.ability-image {
  width: 64px;
  /* Adjust if necessary */
  height: 64px;
  /* Adjust if necessary */
  object-fit: cover;
  clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.ability-image,
.trait .ability-image {
  width: 64px;
  height: 64px;
  object-fit: cover;
  clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
}


.tooltip {
  position: absolute;
  background-color: #000;
  color: #fff;
  padding: 10px;
  border-radius: 5px;
  z-index: 10;
  width: 200px;
  top: 50%;
  left: 100%;
  transform: translateY(-50%);
  margin-left: 10px;
}


.ability,
.trait {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  position: relative;
}


.text-small {
  font-size: 0.8rem;
}

.text-primary {
  color: blue;
}

.text-secondary {
  color: green;
}

.text-danger {
  color: red;
}

.text-warning {
  color: orange;
}

.trait {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  width: 64px;
  /* Assuming the image width is 64px */
}

.trait .tooltip {
  position: absolute;
  background-color: #000;
  color: #fff;
  padding: 10px;
  border-radius: 5px;
  z-index: 10;
  width: 200px;
  top: 50%;
  left: 70px;
  /* Adjust this value to position the tooltip right next to the image */
  transform: translateY(-50%);
}

.nav-tabs {
  font-size: 20px;
  border: 1px #742AFF solid;
  background-color: #200B41;
}

.nav-tabs:hover {
  box-shadow: #742AFF;
  filter: drop-shadow(0 0 20px #742AFF);
}

.nav-tabs.selected {
  background-color: #6B21A8;
  /* This is the Tailwind CSS color for bg-purple-600 */
}
</style>

<script>
import axios from 'axios';

export default {
  name: 'HeroPatchNotesPage',
  data() {
    return {
      hero: {},
      patchNotes: [],
      talents: {},
      tooltipTalent: null,
      tooltipAbility: null,
      selectedTab: 'patchNotes',
      abilities: {},
      thumbsUpCount: 0,
    }
  },
  computed: {
    heroName() {
      return this.$route.params.name.toLowerCase();
    },
  },
  created() {
    const heroData = require(`../data/heroes/${this.heroName}.json`);
    if (heroData) {
      this.hero = heroData;
      this.patchNotes = heroData.patchNotes;
      this.talents = require(`../data/heroes/talents/${this.heroName}_talents.json`);
      console.log(this.talents); // Log to check the loaded talents data
    } else {
      console.error('Failed to load hero data');
    }
  },
  methods: {
    fetchThumbsUpCount() {
      axios.get('http://localhost:3000/api/reactions')
        .then(response => {
          this.thumbsUpCount = response.data.thumbsUpCount;
        })
        .catch(error => console.error('Error fetching thumbs-up count:', error));
    },
    selectTab(tab) {
      this.selectedTab = tab;
      if (tab === 'communityApproval') {
        this.fetchThumbsUpCount();
      }
    },
    showTooltip(talent) {
      this.tooltipTalent = talent;
    },
    hideTooltip() {
      this.tooltipTalent = null;
    },
    formatText(text) {
      // Highlight changes and important details
      return text.replace(/{highlight}(.*?){\/highlight}/g, '<span style="color: red;">$1</span>');
    },
  },
}
</script>
