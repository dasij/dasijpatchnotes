<template>
    <div class="abilities-container mt-8">
        <h2 class="text-2xl font-bold text-white mb-4">Basic Abilities</h2>
        <div class="flex justify-start">
            <div v-for="ability in abilities.basic" :key="ability.name" class="ability"
                @mouseover="showTooltipAbility(ability, 'basic', $event)" @mouseleave="hideTooltipAbility">
                <div class="hexagon-border" :class="{ 'ability-changed': ability.abilityChanged }">
                    <img :src="require(`@/assets/talents/${heroName}/${ability.image}`)" alt="ability image"
                        class="ability-image">
                </div>
            </div>
        </div>

        <h2 class="text-2xl font-bold text-white mb-4 mt-8">Heroic Abilities</h2>
        <div class="flex justify-start">
            <div v-for="ability in abilities.heroic" :key="ability.name" class="ability"
                @mouseover="showTooltipAbility(ability, 'heroic', $event)" @mouseleave="hideTooltipAbility">
                <div class="hexagon-border" :class="{ 'ability-changed': ability.abilityChanged }">
                    <img :src="require(`@/assets/talents/${heroName}/${ability.image}`)" alt="ability image"
                        class="ability-image">
                </div>
            </div>
        </div>

        <h2 class="text-2xl font-bold text-white mb-4 mt-8">Trait</h2>
        <div class="flex justify-start">
            <div class="ability" @mouseover="showTooltipAbility(abilities.trait, 'trait', $event)"
                @mouseleave="hideTooltipAbility">
                <div class="hexagon-border" :class="{ 'ability-changed': abilities.trait.abilityChanged }">
                    <img :src="require(`@/assets/talents/${heroName}/${abilities.trait.image}`)" alt="trait image"
                        class="ability-image">
                </div>
            </div>
        </div>

        <AbilityTooltip :ability="tooltipAbility" :abilityType="tooltipAbilityType" v-if="tooltipAbility"
            :style="tooltipStyle" />
    </div>
</template>

<script>
import AbilityTooltip from './AbilityTooltip.vue';

export default {
    name: 'HeroAbilities',
    components: {
        AbilityTooltip
    },
    props: {
        abilities: {
            type: Object,
            required: true
        },
        heroName: {
            type: String,
            required: true
        }
    },
    data() {
        return {
            tooltipAbility: null,
            tooltipAbilityType: '',
            tooltipStyle: {
                top: '0px',
                left: '0px'
            }
        };
    },
    methods: {
        showTooltip(talent, event) {
            this.tooltipTalent = talent;

            this.$nextTick(() => {
                const tooltipElement = this.$refs.tooltipTalentElement;
                if (tooltipElement && event && this.tooltipTalent) {
                    const targetElement = event.target;
                    const rect = targetElement.getBoundingClientRect();
                    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
                    const scrollLeft = window.pageXOffset || document.documentElement.scrollLeft;

                    tooltipElement.style.position = 'fixed';
                    tooltipElement.style.top = `${rect.top + scrollTop}px`;
                    tooltipElement.style.left = `${rect.right + scrollLeft + 10}px`;
                    tooltipElement.style.display = 'block';

                    // Ensure the tooltip doesn't go off-screen
                    const tooltipRect = tooltipElement.getBoundingClientRect();
                    if (tooltipRect.right > window.innerWidth) {
                        tooltipElement.style.left = `${rect.left + scrollLeft - tooltipRect.width - 10}px`;
                    }
                }
            });
        },
        hideTooltipAbility() {
            this.tooltipAbility = null;
            this.tooltipAbilityType = '';
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
.ability {
    margin: 10px;
    position: relative;
    display: inline-block;
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
    opacity: 0;
    transition: opacity 0.3s ease-in-out;
}

.hexagon-border.ability-changed {
    filter: drop-shadow(0 0 20px rgba(255, 0, 0, 1));
}

.hexagon-border:hover::before {
    opacity: 0.6;
}

.hexagon-border:hover {
    filter: drop-shadow(0 0 20px rgba(90, 188, 227, 0.8));
}

.ability-image {
    width: 64px;
    height: 64px;
    object-fit: cover;
    clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}
</style>
