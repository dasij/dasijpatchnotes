<template>
  <div class="bg-hots-repeat bg-repeat-y bg-contain bg-center min-h-screen">
    <MetaTags :title="pageTitle" :description="pageDescription" :image="pageImage" />

    <div class="container mx-auto py-20">
      <!-- Header -->
      <div class="mb-8 text-center">
        <h1 class="text-4xl font-bold text-white mb-4">{{ hero.name }} TALENT CALCULATOR</h1>
        <p class="text-gray-400">Click on any talent to view developer comments and changes</p>
      </div>

      <!-- Toggle Switch -->
      <div class="toggle-switch mb-8">
        <span :class="{ 'active': talentType === 'vanilla' }">Vanilla</span>
        <label class="switch">
          <input type="checkbox" @change="toggleTalentType" :checked="talentType === 'modified'">
          <span class="slider"></span>
        </label>
        <span :class="{ 'active': talentType === 'modified' }">Modified</span>
      </div>

      <!-- Main Content Grid -->
      <div class="main-grid">
        <!-- Left Side: Abilities and Talent Calculator -->
        <div class="left-panel">
          <!-- Abilities Section - All in one row -->
          <div class="abilities-section">
            <div class="abilities-row">
              <!-- Basic Abilities Block -->
              <div class="ability-block">
                <h3 class="block-title">Basic</h3>
                <div class="abilities-grid">
                  <div v-for="ability in talents.abilities?.basic" :key="ability.name" class="ability"
                    @click="selectAbility(ability)" :class="{ 'selected': selectedItem === ability }">
                    <div class="hexagon-border" :class="{ 'ability-changed': ability.abilityChanged }">
                      <img :src="getImagePath(heroName, ability.image)" alt="ability image"
                        class="ability-image">
                    </div>
                  </div>
                </div>
              </div>

              <!-- Heroic Abilities Block -->
              <div class="ability-block">
                <h3 class="block-title">Heroic</h3>
                <div class="abilities-grid">
                  <div v-for="ability in talents.abilities?.heroic" :key="ability.name" class="ability"
                    @click="selectAbility(ability)" :class="{ 'selected': selectedItem === ability }">
                    <div class="hexagon-border" :class="{ 'ability-changed': ability.abilityChanged }">
                      <img :src="getImagePath(heroName, ability.image)" alt="ability image"
                        class="ability-image">
                    </div>
                  </div>
                </div>
              </div>

              <!-- Trait Block -->
              <div class="ability-block" v-if="talents.abilities?.trait">
                <h3 class="block-title">Trait</h3>
                <div class="abilities-grid">
                  <div class="ability" @click="selectAbility(talents.abilities.trait)" 
                    :class="{ 'selected': selectedItem === talents.abilities.trait }">
                    <div class="hexagon-border" :class="{ 'ability-changed': talents.abilities.trait.abilityChanged }">
                      <img :src="getImagePath(heroName, talents.abilities.trait.image)" alt="trait image"
                        class="ability-image">
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Talent Calculator -->
          <div class="talent-calculator-wrapper">
            <h2 class="text-2xl font-bold text-white mb-4">Talent Calculator</h2>
            <div class="talent-calculator-container"
              :style="{ backgroundImage: `url(${require('@/assets/talents/talents_bg.webp')})` }">
              <div class="flex flex-col space-y-4">
                <div class="flex justify-center mb-4">
                  <button @click="resetTalents" class="reset-button">Reset selection</button>
                </div>
                <div v-for="level in talentLevels" :key="level" class="flex items-center">
                  <h3 class="text-xl font-semibold mr-4 w-20" style="color: #9900ff;"> Level {{ level }}</h3>
                  <div class="flex ml-12">
                    <div v-for="(talent, index) in talents[level]" :key="talent.name" class="talent-column"
                      :class="{ 'ml-8': index > 0, 'selected': isSelected(level, talent), 'not-selected': !isSelected(level, talent) && isAnySelected(level), 'active-info': selectedItem === talent }"
                      @click="selectTalent(level, talent, index)">
                      <div class="talent-image-container" :class="{ 'talent-changed': talent.talentChanged }">
                        <img :src="getImagePath(heroName, talent.image)" :alt="talent.name"
                          class="talent-image" />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Side: Info Panel -->
        <div class="right-panel" :class="{ 'visible': selectedItem !== null }">
          <div v-if="selectedItem" class="info-content">
            <button class="close-btn" @click="closeInfoPanel">×</button>

            <!-- Item Header -->
            <div class="info-header">
              <img v-if="selectedItem.image" :src="getItemImage(selectedItem)" :alt="selectedItem.name" class="info-image">
              <div class="info-title">
                <h3 class="text-2xl font-semibold" style="color: #0099ff;">{{ selectedItem.name }}</h3>
                <span v-if="selectedItemType" class="info-type">{{ selectedItemType }}</span>
              </div>
            </div>

            <!-- Stats -->
            <div class="info-stats">
              <div v-if="selectedItem.cooldown" class="stat-item">
                <span class="stat-label">Cooldown:</span>
                <span class="stat-value" v-html="formatText(selectedItem.cooldown)"></span>
              </div>
              <div v-if="selectedItem.manaCost" class="stat-item">
                <span class="stat-label">Mana Cost:</span>
                <span class="stat-value" v-html="formatText(selectedItem.manaCost)"></span>
              </div>
            </div>

            <!-- Description -->
            <div v-if="selectedItem.description" class="info-section">
              <h4>Description</h4>
              <p v-html="formatText(selectedItem.description)"></p>
            </div>

            <!-- Quest -->
            <div v-if="selectedItem.quest" class="info-section quest-section">
              <h4 class="quest-text">❢ Quest</h4>
              <p v-html="formatText(selectedItem.quest)"></p>
            </div>

            <!-- Rewards -->
            <div v-if="selectedItem.rewards && selectedItem.rewards.length > 0" class="info-section reward-section">
              <h4 class="reward-text">❢ Rewards</h4>
              <ul>
                <li v-for="(reward, index) in selectedItem.rewards" :key="index" v-html="formatText(reward)"></li>
              </ul>
            </div>

            <!-- Passives -->
            <div v-if="selectedItem.passives && selectedItem.passives.length > 0" class="info-section passive-section">
              <h4 class="passive-text">Passive</h4>
              <ul>
                <li v-for="(passive, index) in selectedItem.passives" :key="index" v-html="formatText(passive)"></li>
              </ul>
            </div>

            <!-- Subtexts (Change Details) - Só mostra em modo modified -->
            <div v-if="selectedItem.subtexts && selectedItem.subtexts.length > 0 && talentType === 'modified'" class="info-section change-details-section">
              <h4>Change Details</h4>
              <ul class="subtexts-list">
                <li v-for="(sub, idx) in selectedItem.subtexts" :key="idx" v-html="convertTextPlaceholders(sub)"></li>
              </ul>
            </div>

            <!-- Developer Comments - Só mostra em modo modified -->
            <div v-if="selectedItem.developerCommentary && talentType === 'modified'" class="info-section dev-commentary">
              <h4>Developer Comment</h4>
              <div class="commentary-box">
                <p v-html="convertTextPlaceholders(selectedItem.developerCommentary)"></p>
              </div>
            </div>
          </div>

          <div v-else class="empty-state">
            <p>Select a talent or ability to view details</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, ref } from 'vue'
import MetaTags from './MetaTags.vue'

export default defineComponent({
  components: {
    MetaTags
  },

  setup() {
    const pageTitle = ref('')
    const pageDescription = ref('')
    const pageImage = ref('')
    return { pageTitle, pageDescription, pageImage }
  },

  data() {
    return {
      hero: {},
      talents: {},
      selectedItem: null,
      selectedItemType: '',
      selectedItemLevel: null,
      selectedItemIndex: null,
      isLoading: true,
      talentType: 'modified',
      selectedTalentsModified: { 1: null, 4: null, 7: null, 10: null, 13: null, 16: null, 20: null },
      selectedTalentsVanilla: { 1: null, 4: null, 7: null, 10: null, 13: null, 16: null, 20: null },
      talentLevels: [1, 4, 7, 10, 13, 16, 20]
    };
  },

  computed: {
    heroName() {
      return this.$route.params.name.toLowerCase();
    },
  },

  created() {
    this.loadHeroData();
  },

  methods: {
    // Helper para obter path da imagem sem erro
    getImagePath(heroName, imageName) {
      try {
        return require(`@/assets/talents/${heroName}/${imageName}`);
      } catch (error) {
        console.warn(`Image not found: ${heroName}/${imageName}`);
        return '';
      }
    },

    loadHeroData() {
      try {
        const heroData = require(`../data/heroes/${this.heroName}.json`);
        if (heroData) {
          this.hero = heroData;
          this.loadTalents();
          this.pageTitle = `${heroData.name} - Talent Calculator`;
          this.pageDescription = `Interactive talent calculator for ${heroData.name} in Heroes of the Storm`;
          this.pageImage = require(`@/assets/${heroData.image}`);
        }
      } catch (error) {
        console.error('Error loading hero data:', error);
      }
    },

    loadTalents() {
      try {
        const talentsFileName = this.talentType === 'modified' 
          ? `${this.heroName}_talents.json` 
          : `${this.heroName}_talents_vanilla.json`;
        this.talents = require(`../data/heroes/talents/${talentsFileName}`);
        this.selectedItem = null;
      } catch (error) {
        console.error('Error loading talents:', error);
        this.talents = { abilities: { basic: [], heroic: [], trait: {} } };
      }
    },

    toggleTalentType() {
      this.talentType = this.talentType === 'modified' ? 'vanilla' : 'modified';
      this.loadTalents();
      this.resetTalents();
    },

    selectTalent(level, talent, index) {
      this.toggleTalentSelection(level, talent);
      this.selectedItem = talent;
      this.selectedItemType = `Level ${level} Talent`;
      this.selectedItemLevel = level;
      this.selectedItemIndex = index;
    },

    selectAbility(ability) {
      this.selectedItem = ability;
      this.selectedItemType = this.getAbilityType(ability);
      this.selectedItemLevel = null;
      this.selectedItemIndex = null;
    },

    getAbilityType(ability) {
      if (!this.talents.abilities) return 'Ability';
      if (this.talents.abilities.trait === ability) return 'Trait';
      if (this.talents.abilities.heroic && this.talents.abilities.heroic.includes(ability)) return 'Heroic Ability';
      return 'Basic Ability';
    },

    getItemImage(item) {
      if (!item || !item.image) return '';
      return this.getImagePath(this.heroName, item.image);
    },

    closeInfoPanel() {
      this.selectedItem = null;
      this.selectedItemType = '';
      this.selectedItemLevel = null;
      this.selectedItemIndex = null;
    },

    toggleTalentSelection(level, talent) {
      const selectedTalents = this.talentType === 'modified' 
        ? this.selectedTalentsModified 
        : this.selectedTalentsVanilla;
      if (selectedTalents[level] === talent) {
        selectedTalents[level] = null;
      } else {
        selectedTalents[level] = talent;
      }
    },

    isSelected(level, talent) {
      const selectedTalents = this.talentType === 'modified' 
        ? this.selectedTalentsModified 
        : this.selectedTalentsVanilla;
      return selectedTalents[level] === talent;
    },

    isAnySelected(level) {
      const selectedTalents = this.talentType === 'modified' 
        ? this.selectedTalentsModified 
        : this.selectedTalentsVanilla;
      return selectedTalents[level] !== null;
    },

    resetTalents() {
      if (this.talentType === 'modified') {
        this.selectedTalentsModified = { 1: null, 4: null, 7: null, 10: null, 13: null, 16: null, 20: null };
      } else {
        this.selectedTalentsVanilla = { 1: null, 4: null, 7: null, 10: null, 13: null, 16: null, 20: null };
      }
    },

    formatText(text) {
      if (!text) return '';
      let result = text;
      const openTag = '{highlight}';
      const closeTag = '{/highlight}';
      
      while (result.includes(openTag) && result.includes(closeTag)) {
        const start = result.indexOf(openTag);
        const end = result.indexOf(closeTag);
        if (start !== -1 && end !== -1 && end > start) {
          const before = result.substring(0, start);
          const middle = result.substring(start + openTag.length, end);
          const after = result.substring(end + closeTag.length);
          result = before + '<span class="highlight-text">' + middle + '</span>' + after;
        } else {
          break;
        }
      }
      return result;
    },

    convertTextPlaceholders(text) {
      if (!text) return '';
      
      const self = this;
      
      // Regex para capturar tags como <vanilla, abilities, basic, 1> ou <modified, talents, 13, 2, dehaka>
      return text.replace(/<([^,]+),\s*([^,]+),\s*([^,]+),\s*(\d+)(?:,\s*([^>]+))?>/g, function(match, type, section, category, index, heroName) {
        const targetHero = heroName || self.heroName;
        const item = self.findAbilityOrTalent(type, section, category, parseInt(index, 10), targetHero);
        
        if (item) {
          try {
            const imagePath = self.getImagePath(targetHero, item.image);
            const className = type === 'modified' ? 'modified-text' : 'vanilla-text';
            
            let heroPrefix = '';
            if (heroName && heroName !== self.heroName) {
              const displayHeroName = heroName.replace(/-/g, ' ')
                .split(' ')
                .map(word => word.charAt(0).toUpperCase() + word.slice(1))
                .join(' ');
              heroPrefix = `<span class="hero-prefix">${displayHeroName}'s </span>`;
            }
            
            return `<span class="ability-reference ${className}">
              ${heroPrefix}<img src="${imagePath}" alt="${item.name}" class="inline-image" />
              <span class="reference-name">${item.name}</span>
            </span>`;
          } catch (e) {
            return match;
          }
        }
        return match;
      });
    },

    findAbilityOrTalent(type, section, category, index, heroName) {
      const targetHero = heroName || this.heroName;
      try {
        const talentsFileName = type === 'modified' 
          ? `${targetHero}_talents.json` 
          : `${targetHero}_talents_vanilla.json`;
        const talentsData = require(`../data/heroes/talents/${talentsFileName}`);
        
        if (section === 'abilities') {
          if (category === 'trait') {
            return talentsData.abilities.trait;
          } else if (category === 'basic' || category === 'heroic') {
            return talentsData.abilities[category][index];
          }
        } else if (section === 'talents') {
          return talentsData[category][index];
        }
      } catch (error) {
        console.error(`Error loading talent for ${targetHero}:`, error);
      }
      return null;
    }
  }
});
</script>

<style scoped>
.main-grid {
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 30px;
  align-items: start;
}

.left-panel {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.right-panel {
  position: sticky;
  top: 20px;
  background: rgba(0, 0, 0, 0.9);
  border: 2px solid #742aff;
  border-radius: 10px;
  padding: 20px;
  max-height: calc(100vh - 40px);
  overflow-y: auto;
  opacity: 0;
  transform: translateX(20px);
  transition: all 0.3s ease;
  pointer-events: none;
}

.right-panel.visible {
  opacity: 1;
  transform: translateX(0);
  pointer-events: all;
}

.info-content {
  position: relative;
}

.close-btn {
  position: absolute;
  top: -10px;
  right: -10px;
  background: #742aff;
  border: none;
  color: white;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  font-size: 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
}

.close-btn:hover {
  background: #9900ff;
}

.info-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #333;
}

.info-image {
  width: 64px;
  height: 64px;
  border-radius: 8px;
  object-fit: cover;
  border: 2px solid #0099ff;
}

.info-title {
  flex: 1;
}

.info-type {
  display: inline-block;
  background: #742aff;
  color: white;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  margin-top: 5px;
}

.info-stats {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.stat-item {
  background: rgba(116, 42, 255, 0.1);
  padding: 8px 12px;
  border-radius: 6px;
  border: 1px solid rgba(116, 42, 255, 0.3);
}

.stat-label {
  color: #888;
  font-size: 12px;
  margin-right: 5px;
}

.stat-value {
  color: #0099ff;
  font-weight: bold;
}

.info-section {
  margin-bottom: 20px;
}

.info-section h4 {
  color: #9900ff;
  font-size: 14px;
  text-transform: uppercase;
  margin-bottom: 8px;
  letter-spacing: 1px;
}

.info-section p, .info-section li {
  color: #ccc8d3;
  line-height: 1.6;
  font-size: 14px;
}

.info-section ul {
  list-style: none;
  padding-left: 0;
}

.info-section li {
  margin-bottom: 5px;
  padding-left: 15px;
  position: relative;
}

.info-section li::before {
  content: "›";
  position: absolute;
  left: 0;
  color: #742aff;
}

.dev-commentary {
  background: rgba(116, 42, 255, 0.05);
  border-left: 4px solid #742aff;
  padding: 15px;
  border-radius: 0 8px 8px 0;
}

.commentary-box {
  font-style: italic;
  color: #aaa;
}

.commentary-box p {
  margin-bottom: 10px;
}

.commentary-box p:last-child {
  margin-bottom: 0;
}

.empty-state {
  text-align: center;
  color: #666;
  padding: 40px 20px;
}

.abilities-section {
  background: rgba(0, 0, 0, 0.5);
  padding: 20px;
  border-radius: 10px;
  border: 1px solid #333;
}

.abilities-row {
  display: flex;
  flex-direction: row;
  gap: 20px;
  justify-content: flex-start;
  align-items: flex-start;
  flex-wrap: wrap;
}

.ability-block {
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid #444;
  border-radius: 8px;
  padding: 15px;
  min-width: 100px;
  flex: 0 0 auto;
}

.block-title {
  color: #9900ff;
  font-size: 14px;
  font-weight: bold;
  text-transform: uppercase;
  margin-bottom: 10px;
  text-align: center;
  letter-spacing: 1px;
}

.abilities-grid {
  display: flex;
  flex-direction: row;
  gap: 10px;
  justify-content: center;
  flex-wrap: wrap;
}

.ability {
  position: relative;
  display: inline-block;
  cursor: pointer;
  transition: transform 0.2s;
}

.ability:hover {
  transform: scale(1.1);
}

.ability.selected .hexagon-border {
  filter: drop-shadow(0 0 20px rgba(116, 42, 255, 0.8));
}

.hexagon-border {
  position: relative;
  width: 64px;
  height: 74px;
  background: url('@/assets/talents/hexagon.png') center/contain no-repeat;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: visible;
  transition: filter 0.3s ease-in-out;
}

.hexagon-border.ability-changed {
  filter: drop-shadow(0 0 20px rgba(255, 0, 0, 1));
}

.hexagon-border:hover {
  filter: drop-shadow(0 0 20px rgba(90, 188, 227, 0.8));
}

.ability-image {
  width: 56px;
  height: 56px;
  object-fit: cover;
  clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.talent-calculator-container {
  background-size: cover;
  background-position: center;
  padding: 30px;
  border-radius: 10px;
  display: inline-block;
  border: 2px solid #18192D;
  box-shadow: 0 0 5px 2px rgba(90, 188, 227, 0.8);
}

.talent-column {
  position: relative;
  cursor: pointer;
}

.talent-image-container {
  width: 64px;
  height: 64px;
  overflow: hidden;
  border-radius: 10%;
  transition: all 0.3s ease;
}

.talent-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.talent-column:hover .talent-image-container {
  box-shadow: 0 0 15px 5px rgba(90, 188, 227, 0.8);
  transform: scale(1.1);
}

.talent-column.selected .talent-image-container {
  box-shadow: 0 0 20px 5px rgba(0, 255, 0, 0.6);
  border: 2px solid #78da5b;
}

.talent-column.not-selected .talent-image-container {
  filter: brightness(0.15);
}

.talent-column.active-info .talent-image-container {
  box-shadow: 0 0 20px 5px rgba(116, 42, 255, 0.8);
  border: 2px solid #742aff;
}

.toggle-switch {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
  font-size: 18px;
  color: #666;
}

.toggle-switch span {
  transition: color 0.3s;
}

.toggle-switch span.active {
  color: #fff;
  font-weight: bold;
}

.switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #333;
  transition: .4s;
  border-radius: 34px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: #742aff;
}

input:checked + .slider:before {
  transform: translateX(26px);
}

.reset-button {
  background: none;
  border: none;
  color: white;
  font-size: 18px;
  cursor: pointer;
  text-transform: uppercase;
  font-family: "Blizzard", sans-serif;
  text-shadow: 1px 1px 2px black;
  transition: all 0.2s;
}

.reset-button:hover {
  text-decoration: underline;
  color: #742aff;
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

.talent-changed {
  border: 2px solid red;
}

.change-details-section {
  background: rgba(116, 42, 255, 0.1);
  border: 1px solid #742aff;
  border-radius: 8px;
  padding: 15px;
}

.subtexts-list {
  margin-top: 10px;
  padding-left: 20px;
  list-style-type: disc;
}

.subtexts-list li {
  color: #888;
  font-size: 13px;
  margin-bottom: 5px;
  line-height: 1.4;
  padding-left: 5px;
}

.subtexts-list li::before {
  content: none;
}

.subtexts-list li::marker {
  color: #742aff;
}

.ability-reference {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  background: rgba(0, 0, 0, 0.3);
  padding: 2px 6px;
  border-radius: 4px;
  margin: 0 2px;
  vertical-align: middle;
}

.ability-reference .inline-image {
  width: 24px;
  height: 24px;
  border-radius: 4px;
  object-fit: cover;
  border: 1px solid #333;
}

.ability-reference .reference-name {
  font-size: 13px;
  font-weight: 500;
}

.ability-reference.modified-text .reference-name {
  color: #78da5b;
}

.ability-reference.vanilla-text .reference-name {
  color: #0099ff;
}

.hero-prefix {
  color: #888;
  font-size: 12px;
  margin-right: 4px;
}

@media (max-width: 1200px) {
  .main-grid {
    grid-template-columns: 1fr;
  }

  .right-panel {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 90%;
    max-width: 500px;
    max-height: 80vh;
    z-index: 1000;
    opacity: 0;
    pointer-events: none;
  }

  .right-panel.visible {
    opacity: 1;
    pointer-events: all;
  }

  .abilities-row {
    flex-direction: column;
    align-items: stretch;
  }

  .ability-block {
    width: 100%;
  }
}

@import '@/assets/css/common.css';
</style>