<template>
  <div class="bg-hots-repeat bg-repeat-y bg-contain bg-center min-h-screen">
    <MetaTags :title="pageTitle" :description="pageDescription" :image="pageImage" />

    <div class="container mx-auto py-8 px-4">
      <!-- Main Grid: 3 Columns -->
      <div class="main-layout">
        <!-- LEFT COLUMN: Abilities Vertical -->
        <div class="left-column">
          <div class="abilities-panel">
            <h2 class="panel-title">Abilities</h2>
            
            <div class="abilities-vertical">
              <!-- Basic Abilities -->
              <div v-for="(ability, index) in talents.abilities?.basic" :key="ability.name" 
                   class="ability-row"
                   @click="selectAbility(ability)"
                   @dblclick="toggleDevComments()"
                   :class="{ 'active': selectedAbility === ability, 'changed': ability.abilityChanged }">
                <div class="ability-icon">
                  <img :src="getImagePath(heroName, ability.image)" :alt="ability.name">
                  <span class="key-bind">{{ ['Q','W','E'][index] }}</span>
                </div>
                <span class="ability-name-small">{{ ability.name }}</span>
              </div>

              <!-- Heroic Abilities -->
              <div v-for="(ability, index) in talents.abilities?.heroic" :key="ability.name" 
                   class="ability-row heroic"
                   @click="selectAbility(ability)"
                   @dblclick="toggleDevComments()"
                   :class="{ 'active': selectedAbility === ability, 'changed': ability.abilityChanged }">
                <div class="ability-icon">
                  <img :src="getImagePath(heroName, ability.image)" :alt="ability.name">
                  <span class="key-bind">{{ index === 0 ? 'R1' : 'R2' }}</span>
                </div>
                <span class="ability-name-small">{{ ability.name }}</span>
              </div>

              <!-- Trait -->
              <div v-if="talents.abilities?.trait" 
                   class="ability-row trait"
                   @click="selectAbility(talents.abilities.trait)"
                   @dblclick="toggleDevComments()"
                   :class="{ 'active': selectedAbility === talents.abilities.trait, 'changed': talents.abilities.trait.abilityChanged }">
                <div class="ability-icon">
                  <img :src="getImagePath(heroName, talents.abilities.trait.image)" :alt="talents.abilities.trait.name">
                  <span class="key-bind">T</span>
                </div>
                <span class="ability-name-small">{{ talents.abilities.trait.name }}</span>
              </div>

              <!-- Base/General -->
              <div v-if="talents.abilities?.general" 
                   class="ability-row base"
                   @click="selectAbility(talents.abilities.general)"
                   @dblclick="toggleDevComments()"
                   :class="{ 'active': selectedAbility === talents.abilities.general, 'changed': talents.abilities.general.talentChanged || talents.abilities.general.abilityChanged }">
                <div class="ability-icon">
                  <img :src="heroPortraitPath" :alt="hero.name">
                  <span class="key-bind">B</span>
                </div>
                <span class="ability-name-small">Base Changes</span>
              </div>
            </div>
          </div>
        </div>

        <!-- CENTER COLUMN: Splash Art & Description -->
        <div class="center-column">
          <div class="center-container">
            <!-- Splash Art com Header Overlay -->
            <div class="splash-art" :style="{ backgroundImage: `url(${heroSplashPath})` }">
              <div class="hero-overlay"></div>
              
              <!-- NOVO: Header dentro da Splash Art -->
              <div class="splash-header">
                <h1 class="hero-title">{{ hero.name }}</h1>
                
                <!-- Controles horizontais lado a lado no canto direito -->
                <div class="splash-controls">
                  <!-- Toggle Vanilla/Modified Horizontal -->
                  <div class="horizontal-toggle">
                    <span :class="{ 'active': talentType === 'vanilla' }">Vanilla</span>
                    <label class="switch">
                      <input type="checkbox" @change="toggleTalentType" :checked="talentType === 'modified'">
                      <span class="slider"></span>
                    </label>
                    <span :class="{ 'active': talentType === 'modified' }">Modified</span>
                  </div>

                  <!-- Checkbox Dev Comments -->
                  <label class="dev-comments-toggle">
                    <input type="checkbox" v-model="showDevCommentsAlways">
                    <span class="checkmark-box">✓</span>
                    <span class="label-text">Dev Notes</span>
                  </label>
                </div>
              </div>
            </div>

            <!-- Info Box - Descrição com Aba de Dev Comments DENTRO -->
            <div class="info-display-box">
              <!-- Aba de Dev Comments - SAI DA PARTE DE CIMA DA CAIXA DE DESCRIÇÃO -->
              <div class="dev-comments-drawer" :class="{ 'open': showDevComments }">
                <div class="dev-comments-tab" @click="toggleDevCommentsPanel">
                  <span>{{ showDevComments ? '▼' : '▲' }}</span>
                </div>
                <div class="dev-comments-content" v-if="currentDevComment">
                  <p v-html="convertTextPlaceholders(currentDevComment)"></p>
                </div>
                <div v-else class="dev-comments-content no-comment">
                  <p>No developer comments available.</p>
                </div>
              </div>

              <!-- MODO HABILIDADE SELECIONADA -->
              <div v-if="selectedAbility && !selectedTalent" class="ability-detail-view">
                <div class="detail-header">
                  <img :src="getAbilityImage(selectedAbility)" class="detail-icon" :class="getAbilityIconClass(selectedAbility)">
                  <div class="detail-title">
                    <h3>{{ selectedAbility.name }}</h3>
                    <span class="detail-type">{{ getAbilityTypeLabel(selectedAbility) }}</span>
                  </div>
                </div>
                
                <div class="detail-stats" v-if="selectedAbility.cooldown || selectedAbility.manaCost">
                  <span v-if="selectedAbility.cooldown" class="detail-stat">
                    <span class="stat-label">Cooldown:</span> {{ selectedAbility.cooldown }}
                  </span>
                  <span v-if="selectedAbility.manaCost" class="detail-stat">
                    <span class="stat-label">Mana Cost:</span> {{ selectedAbility.manaCost }}
                  </span>
                </div>

                <p class="detail-description" v-html="formatText(selectedAbility.description)"></p>

                <div v-if="selectedAbility.subtexts?.length && talentType === 'modified'" class="detail-extra changes">
                  <h4>Change Details</h4>
                  <ul>
                    <li v-for="(sub, i) in selectedAbility.subtexts" :key="i" v-html="convertTextPlaceholders(sub)"></li>
                  </ul>
                </div>
              </div>

              <!-- MODO TALENTO SELECIONADO -->
              <div v-else-if="selectedTalent" class="talent-detail-view">
                <div class="detail-header">
                  <img :src="getImagePath(heroName, selectedTalent.image)" class="detail-icon">
                  <div class="detail-title">
                    <h3>{{ selectedTalent.name }}</h3>
                    <span class="detail-level">Level {{ selectedTalentLevel }} Talent</span>
                  </div>
                </div>
                
                <div class="detail-stats" v-if="selectedTalent.cooldown || selectedTalent.manaCost">
                  <span v-if="selectedTalent.cooldown" class="detail-stat">
                    <span class="stat-label">Cooldown:</span> {{ selectedTalent.cooldown }}
                  </span>
                  <span v-if="selectedTalent.manaCost" class="detail-stat">
                    <span class="stat-label">Mana Cost:</span> {{ selectedTalent.manaCost }}
                  </span>
                </div>

                <p class="detail-description" v-html="formatText(selectedTalent.description)"></p>

                <div v-if="selectedTalent.quest" class="detail-extra quest">
                  <h4>❢ Quest</h4>
                  <p v-html="formatText(selectedTalent.quest)"></p>
                </div>
                <div v-if="selectedTalent.rewards?.length" class="detail-extra rewards">
                  <h4>❢ Rewards</h4>
                  <ul>
                    <li v-for="(reward, i) in selectedTalent.rewards" :key="i" v-html="formatText(reward)"></li>
                  </ul>
                </div>
                <div v-if="selectedTalent.passives?.length" class="detail-extra passives">
                  <h4>Passive</h4>
                  <ul>
                    <li v-for="(passive, i) in selectedTalent.passives" :key="i" v-html="formatText(passive)"></li>
                  </ul>
                </div>
                <div v-if="selectedTalent.subtexts?.length && talentType === 'modified'" class="detail-extra changes">
                  <h4>Change Details</h4>
                  <ul>
                    <li v-for="(sub, i) in selectedTalent.subtexts" :key="i" v-html="convertTextPlaceholders(sub)"></li>
                  </ul>
                </div>
              </div>

              <!-- PLACEHOLDER -->
              <div v-else class="empty-placeholder">
                <p>Select an ability or talent to view details</p>
                <p class="hint">Double-click to toggle developer comments</p>
              </div>
            </div>
          </div>
        </div>

        <!-- RIGHT COLUMN: Talent Tree (SEMPRE 4 ícones por linha) -->
        <div class="right-column">
          <div class="talent-tree-panel">
            <h2 class="panel-title">Talent Tree</h2>
            <button @click="resetAll" class="reset-btn">Reset All</button>
            
            <div class="talent-levels">
              <div v-for="level in talentLevels" :key="level" class="talent-level-row"
                   :class="{ 'has-selection': isAnySelected(level), 'active': selectedTalentLevel === level }">
                <span class="level-number" 
                      :class="{ 'active': selectedTalentLevel === level }"
                      @click="selectLevel(level)">{{ level }}</span>
                <div class="talent-options">
                  <div v-for="(talent, index) in talents[level]" :key="talent.name"
                       class="talent-node"
                       :class="{ 
                         'selected': isSelected(level, talent), 
                         'not-selected': !isSelected(level, talent) && isAnySelected(level),
                         'active': selectedTalent === talent,
                         'changed': talent.talentChanged
                       }"
                       @click="selectTalent(level, talent, index)"
                       @dblclick="toggleDevComments()">
                    <img :src="getImagePath(heroName, talent.image)" :alt="talent.name">
                    <div class="checkmark" v-if="isSelected(level, talent)">✓</div>
                  </div>
                  <div v-for="n in (4 - (talents[level]?.length || 0))" :key="'spacer-'+n" class="talent-spacer"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- BOTTOM SECTION: Level Talent Details - SEMPRE VISÍVEL, iniciando no level 1 -->
      <div class="bottom-section">
        <div class="level-header">
          <h2>Level {{ selectedTalentLevel }} Talents</h2>
          <div class="level-selector">
            <button v-for="level in talentLevels" :key="level"
                    :class="{ 'active': selectedTalentLevel === level }"
                    @click="selectLevel(level)">
              {{ level }}
            </button>
          </div>
        </div>
            
        <div class="talents-comparison-container" :class="{ 'centered': talents[selectedTalentLevel]?.length < 4 }">
          <div class="talents-comparison-grid" :style="getGridStyle(talents[selectedTalentLevel]?.length || 0)">
            <div v-for="(talent, index) in (talents[selectedTalentLevel] || [])" :key="talent.name"
                 class="talent-card"
                 :class="{ 
                   'selected': isSelected(selectedTalentLevel, talent),
                   'active': selectedTalent === talent,
                   'changed': talent.talentChanged
                 }"
                 @click="selectTalent(selectedTalentLevel, talent, index)"
                 @dblclick="toggleDevComments()">
              <div class="card-header">
                <img :src="getImagePath(heroName, talent.image)" :alt="talent.name">
                <div class="card-title">
                  <h4>{{ talent.name }}</h4>
                  <span v-if="isSelected(selectedTalentLevel, talent)" class="selected-badge">Selected</span>
                </div>
              </div>
              <div class="card-body">
                <p v-html="formatText(talent.description)"></p>
                <div v-if="talent.talentChanged" class="changed-indicator">Modified</div>
              </div>
            </div>
            
            <div v-for="n in (4 - (talents[selectedTalentLevel]?.length || 0))" :key="'card-spacer-'+n" class="talent-card-spacer"></div>
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
  components: { MetaTags },

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
      selectedAbility: null,
      selectedTalent: null,
      selectedTalentLevel: 1, // INICIALIZADO COM 1
      selectedTalentIndex: null,
      talentType: 'modified',
      showDevComments: false,
      showDevCommentsAlways: false,
      currentDevComment: null,
      selectedTalentsModified: { 1: null, 4: null, 7: null, 10: null, 13: null, 16: null, 20: null },
      selectedTalentsVanilla: { 1: null, 4: null, 7: null, 10: null, 13: null, 16: null, 20: null },
      talentLevels: [1, 4, 7, 10, 13, 16, 20]
    };
  },

  computed: {
    heroName() {
      return this.$route.params.name.toLowerCase();
    },
    
    heroPortraitPath() {
      try {
        return require(`@/assets/heroes_portraits/${this.heroName}.png`);
      } catch (error) {
        return '';
      }
    },

    heroSplashPath() {
      try {
        return require(`@/assets/heroes_splash/${this.heroName}.webp`);
      } catch (error) {
        try {
          return require(`@/assets/heroes_splash/${this.heroName}.jpg`);
        } catch {
          return '';
        }
      }
    },

    // Computed para pegar o dev comment do item atual
    activeDevComment() {
      const item = this.selectedTalent || this.selectedAbility;
      if (!item) return null;
      return item.developerCommentary || null;
    }
  },

  watch: {
    // Quando mudar o item selecionado, atualiza o comentário automaticamente
    activeDevComment: {
      immediate: true,
      handler(newComment) {
        this.currentDevComment = newComment;
      }
    },
    
    // Quando marcar o checkbox, abre a aba
    showDevCommentsAlways(newVal) {
      if (newVal) {
        this.showDevComments = true;
      } else {
        this.showDevComments = false;
      }
    }
  },

  created() {
    this.loadHeroData();
  },

  methods: {
    getImagePath(heroName, imageName) {
      try {
        return require(`@/assets/talents/${heroName}/${imageName}`);
      } catch (error) {
        return '';
      }
    },

    getAbilityImage(ability) {
      if (!ability) return '';
      if (this.talents.abilities?.general === ability) {
        return this.heroPortraitPath;
      }
      return this.getImagePath(this.heroName, ability.image);
    },

    getAbilityIconClass(ability) {
      if (!this.talents.abilities) return '';
      if (this.talents.abilities.trait === ability) return 'trait-border';
      if (this.talents.abilities.heroic?.includes(ability)) return 'heroic-border';
      if (this.talents.abilities.general === ability) return 'base-border';
      return 'basic-border';
    },

    getAbilityTypeLabel(ability) {
      if (!this.talents.abilities) return 'Ability';
      if (this.talents.abilities.trait === ability) return 'Trait';
      if (this.talents.abilities.heroic?.includes(ability)) return 'Heroic Ability';
      if (this.talents.abilities.general === ability) return 'Base Change';
      return 'Basic Ability';
    },

    loadHeroData() {
      try {
        const heroData = require(`../data/heroes/${this.heroName}.json`);
        if (heroData) {
          this.hero = heroData;
          this.loadTalents();
          this.pageTitle = `${heroData.name} - Talent Calculator`;
          this.pageDescription = `Interactive talent calculator for ${heroData.name}`;
          this.pageImage = this.heroPortraitPath;
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
      } catch (error) {
        console.error('Error loading talents:', error);
        this.talents = { abilities: { basic: [], heroic: [], trait: null, general: null } };
      }
    },

    toggleTalentType() {
      this.talentType = this.talentType === 'modified' ? 'vanilla' : 'modified';
      this.loadTalents();
      this.resetAll();
    },

    selectAbility(ability) {
      this.selectedAbility = ability;
      this.selectedTalent = null;
      // Não reseta o selectedTalentLevel para manter a seção inferior ativa
      this.selectedTalentIndex = null;
      // Dev comment atualiza automaticamente via computed/watch
    },

    selectTalent(level, talent, index) {
      this.selectedTalent = talent;
      this.selectedTalentLevel = level;
      this.selectedTalentIndex = index;
      this.selectedAbility = null;
      
      this.toggleTalentSelection(level, talent);
      // Dev comment atualiza automaticamente via computed/watch
    },

    selectLevel(level) {
      this.selectedTalentLevel = level;
      const selectedAtLevel = this.talentType === 'modified' 
        ? this.selectedTalentsModified[level] 
        : this.selectedTalentsVanilla[level];
      if (selectedAtLevel) {
        this.selectedTalent = selectedAtLevel;
        this.selectedAbility = null;
      } else {
        // Se não houver talento selecionado neste level, limpa o talento selecionado
        // mas mantém o level ativo na seção inferior
        this.selectedTalent = null;
      }
    },

    // Toggle simples - apenas abre/fecha a aba
    toggleDevComments() {
      this.showDevComments = !this.showDevComments;
      // Se abriu manualmente, não afeta o checkbox "sempre"
    },

    toggleDevCommentsPanel() {
      this.showDevComments = !this.showDevComments;
      // Se fechou manualmente e o "sempre" estava ligado, desliga
      if (!this.showDevComments && this.showDevCommentsAlways) {
        this.showDevCommentsAlways = false;
      }
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

    resetAll() {
      this.selectedTalentsModified = { 1: null, 4: null, 7: null, 10: null, 13: null, 16: null, 20: null };
      this.selectedTalentsVanilla = { 1: null, 4: null, 7: null, 10: null, 13: null, 16: null, 20: null };
      this.selectedAbility = null;
      this.selectedTalent = null;
      this.selectedTalentLevel = 1; // RESETA PARA 1
      this.selectedTalentIndex = null;
      this.showDevComments = false;
      this.showDevCommentsAlways = false;
      this.currentDevComment = null;
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
      
      return text.replace(/<([^,]+),\s*([^,]+),\s*([^,]+),\s*(\d+)(?:,\s*([^>]+))?>/g, 
        function(match, type, section, category, index, heroName) {
          const targetHero = heroName || self.heroName;
          const item = self.findAbilityOrTalent(type, section, category, parseInt(index, 10), targetHero);
          
          if (item && item.image) {
            return `<span class="inline-ref">${item.name}</span>`;
          }
          return match;
        });
    },
    
    getGridStyle(count) {
      // Se tiver 4 ou mais, ocupa todo o espaço (grid de 4 colunas)
      if (count >= 4) {
        return {
          gridTemplateColumns: 'repeat(4, 1fr)',
          maxWidth: '100%'
        };
      }
      // Se tiver menos de 4, ajusta para centralizar
      // Cada card tem ~280px de largura mínima + gap de 20px
      const cardWidth = 280;
      const gap = 20;
      const totalWidth = (count * cardWidth) + ((count - 1) * gap);
      
      return {
        gridTemplateColumns: `repeat(${count}, minmax(250px, 280px))`,
        maxWidth: `${totalWidth}px`,
        margin: '0 auto'
      };
    },
    
    findAbilityOrTalent(type, section, category, index, heroName) {
      const targetHero = heroName || this.heroName;
      try {
        const talentsFileName = type === 'modified' 
          ? `${targetHero}_talents.json` 
          : `${targetHero}_talents_vanilla.json`;
        const talentsData = require(`../data/heroes/talents/${talentsFileName}`);
        
        if (section === 'abilities') {
          if (category === 'trait') return talentsData.abilities.trait;
          if (category === 'basic') return talentsData.abilities.basic[index];
          if (category === 'heroic') return talentsData.abilities.heroic[index];
          if (category === 'general') return talentsData.abilities.general;
        } else if (section === 'talents') {
          return talentsData[category][index];
        }
      } catch (error) {
        return null;
      }
    }
  }
});
</script>

<style scoped>
/* Layout Principal */
.main-layout {
  display: grid;
  grid-template-columns: 200px 1fr 320px;
  gap: 25px;
  margin-bottom: 30px;
  min-height: 700px;
}

/* Colunas */
.left-column, .right-column {
  background: rgba(0, 0, 0, 0.7);
  border: 1px solid #333;
  border-radius: 12px;
  padding: 20px;
}

.center-column {
  display: flex;
  flex-direction: column;
}

/* Splash Art com Header Overlay */
.splash-art {
  flex: 1;
  background-size: cover;
  background-position: center top;
  position: relative;
  min-height: 200px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.hero-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 100%;
  background: linear-gradient(to bottom, rgba(0,0,0,0.7) 0%, transparent 40%, transparent 60%, rgba(0,0,0,0.95) 100%);
  pointer-events: none;
}

/* NOVO: Header dentro da Splash Art */
.splash-header {
  position: relative;
  z-index: 10;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 25px 30px;
  pointer-events: none; /* Permite clicar através do container */
}

/* Título do herói - CSS ORIGINAL RESTAURADO */
.hero-title {
  color: #fff;
  font-size: 42px;
  font-weight: bold;
  margin: 0;
  text-shadow: 0 2px 4px rgba(0,0,0,0.8);
  pointer-events: auto;
  letter-spacing: 0.05em;
}

/* Controles horizontais lado a lado no canto direito */
.splash-controls {
  display: flex;
  align-items: center;
  gap: 20px;
  pointer-events: auto;
}

/* Toggle Horizontal Vanilla/Modified */
.horizontal-toggle {
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(10px);
  padding: 10px 15px;
  border-radius: 30px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.horizontal-toggle span {
  color: #666;
  text-transform: uppercase;
  font-size: 12px;
  letter-spacing: 1px;
  font-weight: 500;
  transition: all 0.3s;
}

.horizontal-toggle span.active {
  color: #fff;
  font-weight: bold;
}

/* Switch Horizontal */
.switch {
  position: relative;
  display: inline-block;
  width: 48px;
  height: 26px;
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
  transition: .3s;
  border-radius: 26px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 20px;
  width: 20px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: .3s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: #742aff;
}

input:checked + .slider:before {
  transform: translateX(22px);
}

/* Checkbox Dev Notes */
.dev-comments-toggle {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(10px);
  padding: 10px 15px;
  border-radius: 30px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.2s;
}

.dev-comments-toggle:hover {
  background: rgba(0, 0, 0, 0.8);
  border-color: rgba(116, 42, 255, 0.5);
}

.dev-comments-toggle input {
  display: none;
}

.checkmark-box {
  width: 18px;
  height: 18px;
  border: 2px solid #444;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  color: transparent;
  transition: all 0.2s;
  background: rgba(255,255,255,0.05);
}

.dev-comments-toggle input:checked + .checkmark-box {
  background: #742aff;
  border-color: #742aff;
  color: #fff;
  box-shadow: 0 0 10px rgba(116, 42, 255, 0.5);
}

.dev-comments-toggle .label-text {
  color: #888;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: 500;
  transition: all 0.2s;
}

.dev-comments-toggle:hover .label-text,
.dev-comments-toggle input:checked ~ .label-text {
  color: #fff;
}

/* Títulos dos Painéis */
.panel-title {
  color: #fff;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 2px;
  margin-bottom: 20px;
  text-align: center;
  border-bottom: 1px solid #444;
  padding-bottom: 10px;
}

/* LEFT COLUMN: Abilities Vertical */
.abilities-vertical {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.ability-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
  border: 2px solid transparent;
  background: rgba(255, 255, 255, 0.03);
}

.ability-row:hover {
  background: rgba(255, 255, 255, 0.08);
  transform: translateX(5px);
}

.ability-row.active {
  border-color: #0099ff;
  background: rgba(0, 153, 255, 0.15);
  box-shadow: 0 0 15px rgba(0, 153, 255, 0.3);
}

.ability-row.changed {
  border-left: 4px solid #ff4444;
}

.ability-row.heroic.active {
  border-color: #ff6600;
  background: rgba(255, 102, 0, 0.15);
  box-shadow: 0 0 15px rgba(255, 102, 0, 0.3);
}

.ability-row.trait.active {
  border-color: #9900ff;
  background: rgba(153, 0, 255, 0.15);
  box-shadow: 0 0 15px rgba(153, 0, 255, 0.3);
}

.ability-row.base.active {
  border-color: #ffaa00;
  background: rgba(255, 170, 0, 0.15);
  box-shadow: 0 0 15px rgba(255, 170, 0, 0.3);
}

.ability-icon {
  position: relative;
  width: 56px;
  height: 56px;
  border-radius: 10px;
  overflow: hidden;
  border: 2px solid #444;
  flex-shrink: 0;
  background: #222;
}

.ability-icon img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.key-bind {
  position: absolute;
  bottom: 2px;
  right: 2px;
  background: rgba(0, 0, 0, 0.9);
  color: #fff;
  font-size: 10px;
  padding: 2px 5px;
  border-radius: 3px;
  font-weight: bold;
  border: 1px solid rgba(255,255,255,0.2);
}

.ability-name-small {
  color: #ccc;
  font-size: 12px;
  font-weight: 500;
  line-height: 1.3;
  flex: 1;
}

.ability-row.active .ability-name-small {
  color: #fff;
}

/* Center Column - Container */
.center-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid #333;
  background: rgba(0, 0, 0, 0.5);
}

/* Info Display Box - Container da descrição */
.info-display-box {
  padding: 20px;
  background: rgba(10, 10, 10, 0.98);
  border-top: 2px solid #444;
  min-height: 180px;
  position: relative;
  /* Importante: overflow visível para a aba subir */
  overflow: visible;
}

/* ABA DE DEV COMMENTS - SAI DA PARTE DE CIMA DA CAIXA DE DESCRIÇÃO */
.dev-comments-drawer {
  position: absolute;
  bottom: 100%; /* Começa na parte de cima da caixa, cresce para cima */
  left: 0;
  right: 0;
  background: rgba(20, 15, 30, 0.98);
  border-bottom: 3px solid #742aff;
  border-radius: 12px 12px 0 0;
  transform: translateY(20px);
  opacity: 0;
  pointer-events: none;
  transition: all 0.3s ease;
  max-height: 200px;
  z-index: 100;
}

.dev-comments-drawer.open {
  transform: translateY(0);
  opacity: 1;
  pointer-events: all;
}

/* Aba/tab pequena que fica visível */
.dev-comments-tab {
  position: absolute;
  top: -30px;
  left: 50%;
  transform: translateX(-50%);
  background: #742aff;
  color: #fff;
  padding: 5px 20px;
  border-radius: 8px 8px 0 0;
  cursor: pointer;
  font-size: 12px;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 1px;
  box-shadow: 0 -2px 10px rgba(116, 42, 255, 0.5);
  transition: all 0.2s;
}

.dev-comments-tab:hover {
  background: #9933ff;
  padding-bottom: 8px;
}

.dev-comments-content {
  padding: 20px;
  overflow-y: auto;
  max-height: 170px;
}

.dev-comments-content p {
  color: #ccc;
  font-size: 14px;
  line-height: 1.7;
  font-style: italic;
  margin: 0;
}

.dev-comments-content.no-comment p {
  color: #666;
}

/* Views de detalhe */
.ability-detail-view, .talent-detail-view {
  animation: fadeIn 0.3s;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.detail-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid #333;
}

.detail-icon {
  width: 64px;
  height: 64px;
  border-radius: 10px;
  object-fit: cover;
  border: 3px solid #0099ff;
}

.detail-icon.basic-border { border-color: #0099ff; }
.detail-icon.heroic-border { border-color: #ff6600; }
.detail-icon.trait-border { border-color: #9900ff; }
.detail-icon.base-border { border-color: #ffaa00; }

.detail-title h3 {
  color: #fff;
  font-size: 20px;
  margin: 0 0 5px 0;
}

.detail-type, .detail-level {
  color: #0099ff;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.detail-stats {
  display: flex;
  gap: 25px;
  margin-bottom: 15px;
  flex-wrap: wrap;
}

.detail-stat {
  color: #aaa;
  font-size: 13px;
}

.stat-label {
  color: #666;
  margin-right: 5px;
}

.detail-description {
  color: #ddd;
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 15px;
}

.detail-extra {
  margin-top: 15px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 8px;
  border-left: 4px solid #444;
}

.detail-extra h4 {
  font-size: 12px;
  text-transform: uppercase;
  margin-bottom: 8px;
  margin-top: 0;
  letter-spacing: 1px;
}

.detail-extra.quest { border-left-color: #DFCB00; }
.detail-extra.quest h4 { color: #DFCB00; }

.detail-extra.rewards { border-left-color: #78da5b; }
.detail-extra.rewards h4 { color: #78da5b; }

.detail-extra.passives { border-left-color: #9900ff; }
.detail-extra.passives h4 { color: #9900ff; }

.detail-extra.changes { border-left-color: #0099ff; }
.detail-extra.changes h4 { color: #0099ff; }

.detail-extra p, .detail-extra li {
  color: #bbb;
  font-size: 13px;
  line-height: 1.5;
  margin: 0;
}

.detail-extra ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.detail-extra li {
  padding-left: 18px;
  position: relative;
  margin-bottom: 6px;
}

.detail-extra li::before {
  content: "›";
  position: absolute;
  left: 0;
  color: #666;
  font-size: 16px;
}

.empty-placeholder {
  color: #666;
  text-align: center;
  padding: 40px 20px;
}

.hint {
  color: #444;
  font-size: 12px;
  margin-top: 8px;
}

/* RIGHT COLUMN: Talent Tree - SEMPRE 4 por linha */
.talent-tree-panel {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.reset-btn {
  background: transparent;
  border: 1px solid #444;
  color: #888;
  padding: 8px 15px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 11px;
  text-transform: uppercase;
  margin-bottom: 20px;
  transition: all 0.2s;
}

.reset-btn:hover {
  border-color: #ff4444;
  color: #ff4444;
  background: rgba(255, 68, 68, 0.1);
}

.talent-levels {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.talent-level-row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px;
  border-radius: 8px;
  transition: background 0.2s;
}

.talent-level-row:hover {
  background: rgba(255, 255, 255, 0.05);
}

.talent-level-row.has-selection {
  background: rgba(0, 153, 255, 0.1);
}

.talent-level-row.active {
  background: rgba(116, 42, 255, 0.15);
  border: 1px solid rgba(116, 42, 255, 0.3);
}

.level-number {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #222;
  border: 2px solid #444;
  border-radius: 6px;
  color: #888;
  font-size: 13px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s;
  flex-shrink: 0;
}

.level-number:hover, .level-number.active {
  background: #0099ff;
  border-color: #0099ff;
  color: #fff;
}

/* SEMPRE 4 ícones por linha */
.talent-options {
  display: flex;
  gap: 8px;
  flex: 1;
  justify-content: space-between;
}

.talent-node {
  position: relative;
  width: 44px;
  height: 44px;
  border-radius: 8px;
  overflow: hidden;
  border: 2px solid #444;
  cursor: pointer;
  transition: all 0.2s;
  opacity: 0.7;
  flex-shrink: 0;
}

.talent-node img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.talent-node:hover {
  opacity: 1;
  transform: scale(1.05);
  border-color: #0099ff;
}

.talent-node.selected {
  border-color: #78da5b;
  opacity: 1;
  box-shadow: 0 0 12px rgba(120, 218, 91, 0.5);
}

.talent-node.not-selected {
  opacity: 0.3;
}

.talent-node.active {
  border-color: #0099ff;
  box-shadow: 0 0 18px rgba(0, 153, 255, 0.7);
  opacity: 1;
}

.talent-node.changed {
  border-color: #ff4444;
}

.talent-spacer {
  width: 44px;
  height: 44px;
  flex-shrink: 0;
}

.checkmark {
  position: absolute;
  top: -6px;
  right: -6px;
  width: 20px;
  height: 20px;
  background: #78da5b;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #000;
  font-size: 12px;
  font-weight: bold;
  box-shadow: 0 2px 6px rgba(0,0,0,0.4);
  border: 2px solid #000;
}

/* Bottom Section - SEMPRE VISÍVEL */
.bottom-section {
  background: rgba(0, 0, 0, 0.7);
  border: 1px solid #333;
  border-radius: 12px;
  padding: 30px;
  margin-top: 20px;
  /* Garante que sempre esteja visível */
  display: block;
}

.level-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  padding-bottom: 20px;
  border-bottom: 1px solid #444;
}

.level-header h2 {
  color: #fff;
  font-size: 20px;
  text-transform: uppercase;
  letter-spacing: 2px;
  margin: 0;
}

.level-selector {
  display: flex;
  gap: 10px;
}

.level-selector button {
  width: 40px;
  height: 40px;
  background: #222;
  border: 2px solid #444;
  color: #888;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: bold;
  transition: all 0.2s;
}

.level-selector button:hover, .level-selector button.active {
  background: #0099ff;
  border-color: #0099ff;
  color: #fff;
}

.talents-comparison-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.talent-card {
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid #333;
  border-radius: 10px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.2s;
}

.talent-card:hover {
  background: rgba(255, 255, 255, 0.08);
  transform: translateY(-3px);
  border-color: #444;
}

.talent-card.selected {
  border-color: #78da5b;
  background: rgba(120, 218, 91, 0.1);
}

.talent-card.active {
  border-color: #0099ff;
  box-shadow: 0 0 25px rgba(0, 153, 255, 0.3);
}

.talent-card.changed {
  border-left: 4px solid #ff4444;
}

.talent-card-spacer {
  visibility: hidden;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 15px;
}

.card-header img {
  width: 56px;
  height: 56px;
  border-radius: 8px;
  border: 2px solid #444;
}

.card-title h4 {
  color: #fff;
  font-size: 16px;
  margin: 0 0 6px 0;
}

.selected-badge {
  display: inline-block;
  background: #78da5b;
  color: #000;
  font-size: 11px;
  padding: 3px 10px;
  border-radius: 4px;
  text-transform: uppercase;
  font-weight: bold;
}

.card-body {
  color: #aaa;
  font-size: 14px;
  line-height: 1.6;
}

.card-body p {
  margin: 0;
}

.changed-indicator {
  display: inline-block;
  margin-top: 12px;
  color: #ff4444;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: bold;
}

/* Highlight Text */
.highlight-text {
  background-color: rgba(255, 100, 100, 0.3);
  padding: 2px 6px;
  border-radius: 4px;
  color: #ffcccc;
}

.inline-ref {
  color: #0099ff;
  font-weight: 500;
}

/* Responsive */
@media (max-width: 1400px) {
  .main-layout {
    grid-template-columns: 180px 1fr 280px;
  }
  
  .talent-node, .talent-spacer {
    width: 48px;
    height: 48px;
  }
  
  .hero-title {
    font-size: 36px;
  }
}

@media (max-width: 1200px) {
  .main-layout {
    grid-template-columns: 1fr;
    grid-template-rows: auto auto auto;
  }
  
  .left-column, .right-column {
    width: 100%;
  }
  
  .abilities-vertical {
    flex-direction: row;
    flex-wrap: wrap;
  }
  
  .center-column {
    order: -1;
    min-height: 500px;
  }
  
  .talents-comparison-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .splash-header {
    flex-direction: column;
    gap: 20px;
    align-items: flex-start;
  }
  
  .splash-controls {
    width: 100%;
    justify-content: flex-end;
  }
}

@media (max-width: 768px) {
  .talents-comparison-grid {
    grid-template-columns: 1fr;
  }
  
  .hero-title {
    font-size: 28px;
  }
  
  .splash-controls {
    flex-direction: column;
    align-items: flex-end;
    gap: 10px;
  }
}

.talents-comparison-container {
  width: 100%;
  display: flex;
  justify-content: center; /* Centraliza o conteúdo */
}

/* Quando tem menos de 4 itens, força centralização */
.talents-comparison-container.centered {
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

/* Grid de talentos - agora com largura controlada */
.talents-comparison-grid {
  display: grid;
  gap: 20px;
  width: 100%;
}

/* Quando tem 4 itens, ocupa largura total */
.talents-comparison-grid:not([style*="maxWidth"]) {
  grid-template-columns: repeat(4, 1fr);
}

.talent-card {
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid #333;
  border-radius: 10px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.2s;
  min-width: 250px;
  max-width: 280px;
}
</style>