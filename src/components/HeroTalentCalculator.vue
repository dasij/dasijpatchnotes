<template>
  <div class="mt-8">

    <div class="toggle-switch mt-4">
      <span :class="{ 'active': talentType === 'vanilla' }">Vanilla</span>
      <label class="switch">
        <input type="checkbox" @change="toggleTalentType" :checked="talentType === 'modified'">
        <span class="slider"></span>
      </label>
      <span :class="{ 'active': talentType === 'modified' }">Modified</span>
    </div>

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
              @click="toggleTalentSelection(level, talent)" @mouseenter="showTooltip(talent, $event)"
              @mouseleave="hideTooltip">
              <div class="talent-image-container" :class="{ 'talent-changed': talent.talentChanged }">
                <img :src="require(`@/assets/talents/${heroName}/${talent.image}`)" :alt="talent.name"
                  class="talent-image" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>



    <TalentTooltip :talent="tooltipTalent" v-if="tooltipTalent" :style="tooltipStyle" />
  </div>
</template>

<script>
import TalentTooltip from './TalentTooltip.vue';
import tooltipMixin from './mixins/tooltipMixin';

export default {
  name: 'HeroTalentCalculator',
  components: {
    TalentTooltip
  },
  mixins: [tooltipMixin],
  props: {
    talents: {
      type: Object,
      required: true
    },
    heroName: {
      type: String,
      required: true
    },
    talentType: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      selectedTalentsModified: {
        1: null, 4: null, 7: null, 10: null, 13: null, 16: null, 20: null,
      },
      selectedTalentsVanilla: {
        1: null, 4: null, 7: null, 10: null, 13: null, 16: null, 20: null,
      },
      tooltipTalent: null,
      tooltipStyle: {
        top: '0px',
        left: '0px'
      }
    };
  },
  methods: {
    toggleTalentSelection(level, talent) {
      const selectedTalents = this.talentType === 'modified' ? this.selectedTalentsModified : this.selectedTalentsVanilla;
      if (selectedTalents[level] === talent) {
        selectedTalents[level] = null;
      } else {
        selectedTalents[level] = talent;
      }
    },
    isSelected(level, talent) {
      const selectedTalents = this.talentType === 'modified' ? this.selectedTalentsModified : this.selectedTalentsVanilla;
      return selectedTalents[level] === talent;
    },
    isAnySelected(level) {
      const selectedTalents = this.talentType === 'modified' ? this.selectedTalentsModified : this.selectedTalentsVanilla;
      return selectedTalents[level] !== null;
    },
    resetTalents() {
      const selectedTalents = this.talentType === 'modified' ? this.selectedTalentsModified : this.selectedTalentsVanilla;
      Object.keys(selectedTalents).forEach(level => {
        selectedTalents[level] = null;
      });
    },
    toggleTalentType() {
      this.$emit('toggle-talent-type');
    },
    showTooltip(talent, event) {
      this.tooltipTalent = talent;
      this.positionTooltip(event);
    },
    hideTooltip() {
      this.tooltipTalent = null;
    },
    positionTooltip(event) {
      const rect = event.target.getBoundingClientRect();
      this.tooltipStyle = {
        top: `${rect.top}px`,
        left: `${rect.right + 10}px`
      };
    }

  }
};
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
  transition: filter 0.3s ease;
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

.talent-column.not-selected .talent-image-container {
  filter: brightness(0.15);
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

.toggle-switch {
  display: flex;
  padding-bottom: 20px;
}

.switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
  margin: 0 10px;
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
  background-color: #ccc;
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

input:checked+.slider {
  background-color: #2196F3;
}

input:checked+.slider:before {
  transform: translateX(26px);
}

.toggle-switch span {
  color: white;
  font-weight: bold;
}

.toggle-switch span.active {
  color: #2196F3;
}
</style>