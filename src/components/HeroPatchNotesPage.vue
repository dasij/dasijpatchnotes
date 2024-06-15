<template>
  <div class="bg-hots-repeat bg-repeat-y bg-contain bg-center min-h-screen">
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

      </nav>

      <div ref="patchNotesContainer" v-if="selectedTab === 'patchNotes'" class="mt-8">
        <div class="bg-hots-repeat bg-contain bg-center bg-no-repeat min-h-screen">
          <div class="container mx-auto py-8">
            <h1 class="text-4xl font-bold text-white mb-4">{{ hero.name }} PATCH NOTES</h1>
            <div v-for="patchNote in patchNotes" :key="patchNote.id" class="mb-12">
              <h2 class="text-2xl font-bold text-white mb-2">{{ patchNote.title }}</h2>
              <p class="text-gray-400 text-sm mb-6">{{ patchNote.date }}</p>
              <div v-if="patchNote.developerCommentary"
                class="mt-4 bg-[#742aff] bg-opacity-5 border-l-4 border-[#742aff] p-4 text-white italic">
                <p class="font-semibold mb-2">Developer Comment:</p>
                <p v-for="(paragraph, index) in patchNote.developerCommentary.split('\n\n')" :key="index">
                  <span v-html="convertTextPlaceholders(paragraph)"></span>
                </p>
              </div>
              <div v-if="patchNote.general && patchNote.general.length > 0" class="mt-8">
                <h3 class="text-xl font-semibold" style="color: #9900ff;">Base</h3>
                <ul class="list-disc list-inside space-y-4" style="color: #ccc8d3;">
                  <li v-for="(item, index) in patchNote.general" :key="index">
                    <span class="text-lg font-medium" style="color: #0099ff;"
                      v-html="convertTextPlaceholders(item.change)"></span>
                    <ul class="list-disc list-inside ml-4">
                      <li v-for="(textItem, textIndex) in item.texts" :key="textIndex">
                        <span style="color: #ccc8d3;" v-html="convertTextPlaceholders(textItem.text)"></span>
                        <ul v-if="textItem.subtexts" class="list-disc list-inside ml-8">
                          <li v-for="(subtext, subtextIndex) in textItem.subtexts" :key="subtextIndex" class="text-sm"
                            style="color: #ccc8d3;">
                            <span v-html="convertTextPlaceholders(subtext)"></span>
                          </li>
                        </ul>
                      </li>
                    </ul>
                    <div v-if="item.developerCommentary"
                      class="mt-4 bg-[#742aff] bg-opacity-5 border-l-4 border-[#742aff] p-4 text-white italic">
                      <p class="font-semibold mb-2">Developer Comment:</p>
                      <p v-html="convertTextPlaceholders(item.developerCommentary)"></p>
                    </div>
                    <button @click="likeChange(patchNote.id, item.change_id)"
                      :class="['like-button', { 'loading': isLoading, 'liked': item.likedBy && item.likedBy[userId] }]">
                      👍 {{ item.likes || 0 }}
                    </button>
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
                        <span class="text-lg font-medium" style="color: #0099ff;"
                          v-html="convertTextPlaceholders(change.name)"></span>
                        <ul class="list-disc list-inside ml-4">
                          <li v-for="(textItem, textIndex) in change.texts" :key="textIndex">
                            <span style="color: #ccc8d3;" v-html="convertTextPlaceholders(textItem.text)"></span>
                            <ul v-if="textItem.subtexts" class="list-disc list-inside ml-8">
                              <li v-for="(subtext, subtextIndex) in textItem.subtexts" :key="subtextIndex"
                                class="text-sm" style="color: #ccc8d3;">
                                <span v-html="convertTextPlaceholders(subtext)"></span>
                              </li>
                            </ul>
                          </li>
                        </ul>
                        <div v-if="change.developerCommentary"
                          class="mt-4 bg-[#742aff] bg-opacity-5 border-l-4 border-[#742aff] p-4 text-white italic">
                          <p class="font-semibold mb-2">Developer Comment:</p>
                          <p v-html="convertTextPlaceholders(change.developerCommentary)"></p>
                        </div>
                        <button @click="likeChange(patchNote.id, change.change_id)"
                          :class="['like-button', { 'loading': isLoading, 'liked': change.likedBy && change.likedBy[userId] }]">
                          👍 {{ change.likes || 0 }}
                        </button>
                      </li>
                    </ul>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="tooltipAbility" ref="tooltipAbilityElement" class="tooltip">
        <p class="text-sm font-semibold" style="color: #0099ff;">
          {{ tooltipAbilityType === 'modified' ? 'Modified Version' : 'Vanilla Version' }}</p>
        <h3 class="text-xl font-semibold" style="color: #0099ff;">{{ tooltipAbility.name }}</h3>
        <div class="flex items-center text-xs mb-2">
          <div v-if="tooltipAbility.cooldown" class="mr-2">
            <span class="font-semibold">Cooldown:</span> <span v-html="formatText(tooltipAbility.cooldown)"></span>
          </div>
          <div v-if="tooltipAbility.manaCost">
            <span class="font-semibold">Mana Cost:</span> <span v-html="formatText(tooltipAbility.manaCost)"></span>
          </div>
        </div>
        <p class="text-sm" v-html="formatText(tooltipAbility.description)"></p>
        <div v-if="tooltipAbility.passives && tooltipAbility.passives.length > 0" class="mt-2">
          <ul>
            <li v-for="(passive, index) in tooltipAbility.passives" :key="index" class="text-sm text-gray-400"
              v-html="formatText(passive)">
            </li>
          </ul>
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
                <div class="flex items-center text-xs mb-2">
                  <div v-if="talents.abilities.trait.cooldown" class="mr-2">
                    <span class="font-semibold">Cooldown:</span> <span
                      v-html="formatText(talents.abilities.trait.cooldown)"></span>
                  </div>
                </div>
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

        <div class="toggle-switch">
          <span :class="{ 'active': talentType === 'vanilla' }">Vanilla</span>
          <label class="switch">
            <input type="checkbox" @change="toggleTalentType" :checked="talentType === 'modified'">
            <span class="slider"></span>
          </label>
          <span :class="{ 'active': talentType === 'modified' }">Modified</span>
        </div>


        <div class="mt-8">
          <h2 class="text-2xl font-bold text-white mb-4">Talent Calculator</h2>
          <div class="talent-calculator-container"
            :style="{ backgroundImage: `url(${require('@/assets/talents/talents_bg.webp')})` }">
            <div class="flex flex-col space-y-4">
              <div class="flex justify-center mb-4">
                <button @click="resetTalents" class="reset-button">Reset selection</button>
              </div>
              <div v-for="level in [1, 4, 7, 10, 13, 16, 20]" :key="level" class="flex items-center">
                <h3 class="text-xl font-semibold mr-4 w-20" style="color: #9900ff;"> Level {{ level }}</h3>
                <div class="flex ml-12">
                  <div v-for="(talent, index) in talents[level]" :key="talent.name" class="talent-column"
                    :class="{ 'ml-8': index > 0, 'selected': isSelected(level, talent), 'not-selected': !isSelected(level, talent) && isAnySelected(level) }"
                    @click="toggleTalentSelection(level, talent)" @mouseenter="showTooltip(talent)"
                    @mouseleave="hideTooltip">
                    <div class="talent-image-container" :class="{ 'talent-changed': talent.talentChanged }">
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
                        <div v-if="talent.quest" class="mt-2">
                          <p class="text-sm" v-html="formatText('Quest: ' + talent.quest)"></p>
                        </div>
                        <div v-if="talent.rewards && talent.rewards.length > 0" class="mt-2">
                          <ul>
                            <li v-for="(reward, index) in talent.rewards" :key="index" class="text-sm "
                              v-html="formatText('Reward: ' + reward)"></li>
                          </ul>
                        </div>
                        <div v-if="talent.passives && talent.passives.length > 0" class="mt-2">
                          <ul>
                            <li v-for="(passive, index) in talent.passives" :key="index" class="text-sm "
                              v-html="formatText(passive)"></li>
                          </ul>
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


<script>
import { database, ref, auth, googleProvider, facebookProvider } from '../firebase';
import { set, get } from 'firebase/database';
import { signInWithPopup } from 'firebase/auth';
import axios from 'axios';

export default {
  data() {
    return {
      hero: {},
      patchNotes: [],
      talents: {},
      tooltipTalent: null,
      tooltipAbility: null,
      tooltipAbilityType: '',
      selectedTab: 'patchNotes',
      abilities: {},
      thumbsUpCount: 0,
      userId: null,
      isLoading: true,
      isUserLoggedIn: false,
      likesData: {},
      talentType: 'modified',
      selectedTalentsmodified: {
        1: null,
        4: null,
        7: null,
        10: null,
        13: null,
        16: null,
        20: null,
      },
      selectedTalentsVanilla: {
        1: null,
        4: null,
        7: null,
        10: null,
        13: null,
        16: null,
        20: null,
      },
    };
  },

  computed: {
    heroName() {
      return this.$route.params.name.toLowerCase();
    },
    versionText() {
      return this.talentType === 'modified' ? 'Modified Version' : 'Vanilla Version';
    },
  },
  created() {
    this.loadHeroData();
    this.authenticateUser();
    this.loadChanges();
  },
  methods: {
    handleMouseOver(event) {
      const target = event.target;
      if (target.classList.contains('ability-tooltip')) {
        const type = target.getAttribute('data-type');
        const section = target.getAttribute('data-section');
        const category = target.getAttribute('data-category');
        const index = parseInt(target.getAttribute('data-index'), 10);
        this.showTooltipAbility(type, section, category, index, event);
      }
    },

    handleMouseLeave(event) {
      const target = event.target;
      if (target.classList.contains('ability-tooltip')) {
        this.hideTooltipAbility();
      }
    },

    beforeDestroy() {
      const container = this.$refs.patchNotesContainer;
      if (container) {
        container.removeEventListener('mouseover', this.handleMouseOver);
        container.removeEventListener('mouseleave', this.handleMouseLeave);
      }
    },

    findAbilityOrTalent(type, section, category, index) {
      const talentsFileName = type === 'modified' ? `${this.heroName}_talents.json` : `${this.heroName}_talents_vanilla.json`;
      const talentsData = require(`../data/heroes/talents/${talentsFileName}`);
      if (section === 'abilities') {
        if (category === 'trait') {
          return talentsData.abilities.trait; // Retorna a trait diretamente
        } else {
          return talentsData.abilities[category][index];
        }
      } else {
        return talentsData[category][index];
      }
    },

    convertTextPlaceholders(text) {
      if (!text) return ''; // Return an empty string if text is undefined or null
      return text.replace(/<([^,]+),\s*([^,]+),\s*([^,]+),\s*(\d+)>/g, (match, type, section, category, index) => {
        const item = this.findAbilityOrTalent(type, section, category, parseInt(index, 10));
        if (item) {
          const className = type === 'modified' ? 'modified-text' : 'vanilla-text';
          return `<span class="ability-tooltip ${className}" 
          data-type="${type}" 
          data-section="${section}" 
          data-category="${category}" 
          data-index="${index}" 
          data-tooltip="${item.name}" 
          @mouseover="showTooltipAbility('${type}', '${section}', '${category}', ${index}, $event)"
          @mouseleave="hideTooltipAbility()">
          ${item.name}
        </span>`;
        }
        return match;
      });
    },

    showTooltipAbility(type, section, category, index, event) {
      this.tooltipAbility = this.findAbilityOrTalent(type, section, category, index);
      this.tooltipAbilityType = type; // Adicione esta linha para definir o tipo de habilidade
      const tooltipElement = this.$refs.tooltipAbilityElement;
      if (tooltipElement && event) {
        const spanElement = event.target;
        const rect = spanElement.getBoundingClientRect();
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const scrollLeft = window.pageXOffset || document.documentElement.scrollLeft;

        tooltipElement.style.top = `${rect.top + scrollTop}px`;
        tooltipElement.style.left = `${rect.right + scrollLeft + 10}px`; // 10px de margem à direita
        tooltipElement.style.display = 'block';
      }
    },

    hideTooltipAbility() {
      this.tooltipAbility = null;
      const tooltipElement = this.$refs.tooltipAbilityElement;
      if (tooltipElement) {
        tooltipElement.style.display = 'none';
      }
    },
    loadHeroData() {
      const heroData = require(`../data/heroes/${this.heroName}.json`);
      if (heroData) {
        this.hero = heroData;
        this.patchNotes = heroData.patchNotes;
        this.loadTalents(); // Modificado para chamar loadTalents
        this.loadLikes();
      } else {
        console.error('Failed to load hero data');
      }
    },
    loadTalents() { // Adicionado
      const talentsFileName = this.talentType === 'modified' ? `${this.heroName}_talents.json` : `${this.heroName}_talents_vanilla.json`;
      this.talents = require(`../data/heroes/talents/${talentsFileName}`);
      console.log(this.talents); // Log to check the loaded talents data
    },
    toggleTalentType() {
      this.talentType = this.talentType === 'modified' ? 'vanilla' : 'modified';
      this.loadTalents();
    },
    loadLikes() {
      const likesRef = ref(database, `heroes/${this.heroName}/likes`);
      get(likesRef).then(snapshot => {
        if (snapshot.exists()) {
          this.likesData = snapshot.val();
          this.applyLikes();
        }
      });
    },
    applyLikes() {
      this.patchNotes.forEach(patchNote => {
        patchNote.general.forEach(change => {
          const likeInfo = this.likesData[change.change_id];
          if (likeInfo) {
            change.likes = likeInfo.likes;
            change.likedBy = likeInfo.likedBy;
          }
        });
        patchNote.sections.forEach(section => {
          section.changes.forEach(change => {
            const likeInfo = this.likesData[change.change_id];
            if (likeInfo) {
              change.likes = likeInfo.likes;
              change.likedBy = likeInfo.likedBy;
            }
          });
        });
      });
    },
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
    likeChange(patchNoteId, changeId) {
      if (!this.isUserLoggedIn) {
        this.$emit('open-login-modal');
        return;
      }

      const patchNote = this.patchNotes.find(note => note.id === patchNoteId);
      let change = patchNote.general.find(item => item.change_id === changeId);

      if (!change) {
        patchNote.sections.forEach(section => {
          const sectionChange = section.changes.find(item => item.change_id === changeId);
          if (sectionChange) {
            change = sectionChange;
          }
        });
      }

      if (!change.likedBy) {
        change.likedBy = {};
      }

      const userId = this.getUserId();
      if (userId) {
        if (change.likedBy[userId]) {
          change.likes = (change.likes || 0) - 1;
          delete change.likedBy[userId];
        } else {
          change.likes = (change.likes || 0) + 1;
          change.likedBy[userId] = true;
        }
        this.saveChanges();
      }
    },
    saveChanges() {
      const changesRef = ref(database, `heroes/${this.heroName}/likes`);
      const likesToSave = {};

      this.patchNotes.forEach(patchNote => {
        patchNote.general.forEach(change => {
          likesToSave[change.change_id] = {
            likes: change.likes,
            likedBy: change.likedBy
          };
        });
        patchNote.sections.forEach(section => {
          section.changes.forEach(change => {
            likesToSave[change.change_id] = {
              likes: change.likes,
              likedBy: change.likedBy
            };
          });
        });
      });

      set(changesRef, likesToSave);
    },
    loadChanges() {
      const changesRef = ref(database, `heroes/${this.heroName}/patchNotes`);
      get(changesRef).then(snapshot => {
        if (snapshot.exists()) {
          this.patchNotes = snapshot.val();
        }
        this.isLoading = false; // Atualizar o estado de carregamento
      });
    },
    authenticateUser() {
      auth.onAuthStateChanged(user => {
        this.isUserLoggedIn = !!user;
        if (user) {
          this.userId = user.uid;
        }
      });
    },
    hasLocalStorage() {
      try {
        localStorage.setItem('test', 'test');
        localStorage.removeItem('test');
        return true;
      } catch (e) {
        return false;
      }
    },
    getUserId() {
      let userId = localStorage.getItem('userId');
      if (!userId) {
        userId = 'user-' + Math.random().toString(36).substr(2, 9);
        localStorage.setItem('userId', userId);
      }
      return userId;
    },
    handleLogin() {
      const provider = Math.random() > 0.5 ? googleProvider : facebookProvider; // Escolhe aleatoriamente entre Google e Facebook
      signInWithPopup(auth, provider)
        .then(result => {
          console.log('Usuário logado:', result.user);
        })
        .catch(error => {
          console.error('Erro ao tentar autenticar:', error);
        });
    },
    checkUserLogin() {
      auth.onAuthStateChanged(user => {
        this.isUserLoggedIn = !!user;
      });
    },
    toggleTalentSelection(level, talent) {
      const selectedTalents = this.talentType === 'modified' ? this.selectedTalentsmodified : this.selectedTalentsVanilla;
      if (selectedTalents[level] === talent) {
        selectedTalents[level] = null;
      } else {
        selectedTalents[level] = talent;
      }
    },
    isSelected(level, talent) {
      const selectedTalents = this.talentType === 'modified' ? this.selectedTalentsmodified : this.selectedTalentsVanilla;
      return selectedTalents[level] === talent;
    },
    isAnySelected(level) {
      const selectedTalents = this.talentType === 'modified' ? this.selectedTalentsmodified : this.selectedTalentsVanilla;
      return selectedTalents[level] !== null;
    },
    resetTalents() {
      if (this.talentType === 'modified') {
        this.selectedTalentsmodified = {
          1: null,
          4: null,
          7: null,
          10: null,
          13: null,
          16: null,
          20: null,
        };
      } else {
        this.selectedTalentsVanilla = {
          1: null,
          4: null,
          7: null,
          10: null,
          13: null,
          16: null,
          20: null,
        };
      }
    }

  },
  mounted() {
    this.checkUserLogin();
    this.authenticateUser();
    this.loadChanges();

    this.$nextTick(() => {
      const container = this.$refs.patchNotesContainer;
      if (container) {
        container.addEventListener('mouseover', this.handleMouseOver);
        container.addEventListener('mouseleave', this.handleMouseLeave);
      }


      const abilityTooltips = container.querySelectorAll('.ability-tooltip');
      abilityTooltips.forEach(span => {
        span.addEventListener('mouseover', (event) => {
          const type = span.getAttribute('data-type');
          const section = span.getAttribute('data-section');
          const category = span.getAttribute('data-category');
          const index = parseInt(span.getAttribute('data-index'), 10);
          this.showTooltipAbility(type, section, category, index, event);
        });
        span.addEventListener('mouseleave', this.hideTooltipAbility);
      });
    });
  },


  updated() {
    this.$nextTick(() => {
      const container = this.$refs.patchNotesContainer;
      if (container) {
        // Remover eventos antigos para evitar duplicação
        container.removeEventListener('mouseover', this.handleMouseOver);
        container.removeEventListener('mouseleave', this.handleMouseLeave);

        // Adicionar eventos novamente
        container.addEventListener('mouseover', this.handleMouseOver);
        container.addEventListener('mouseleave', this.handleMouseLeave);

        // Adicionando eventos para os spans gerados dinamicamente
        const abilityTooltips = container.querySelectorAll('.ability-tooltip');
        abilityTooltips.forEach(span => {
          span.removeEventListener('mouseover', this.handleMouseOver);
          span.removeEventListener('mouseleave', this.handleMouseLeave);

          span.addEventListener('mouseover', (event) => {
            const type = span.getAttribute('data-type');
            const section = span.getAttribute('data-section');
            const category = span.getAttribute('data-category');
            const index = parseInt(span.getAttribute('data-index'), 10);
            this.showTooltipAbility(type, section, category, index, event);
          });
          span.addEventListener('mouseleave', this.hideTooltipAbility);
        });
      }
    });
  },
}

</script>

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

.test-page {
  padding: 20px;
}

.change-line {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

button {
  margin-left: 10px;
}


.test-page {
  padding: 20px;
}

.change-line {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.reset-button {
  background: none;
  border: none;
  color: white;
  font-size: 22px;
  cursor: pointer;
  text-transform: uppercase;
  font-family: "Blizzard", sans-serif;
  text-shadow: 1px 1px 2px black;
}

.reset-button:hover {
  text-decoration: underline;
}

.talent-column .talent-image-container {
  transition: filter 0.3s ease;
}



.talent-column.not-selected .talent-image-container {
  filter: brightness(0.15);
}

.version-icon {
  width: 16px;
  height: 16px;
  margin-left: 5px;
  vertical-align: middle;
}



@import '@/assets/css/common.css';
</style>