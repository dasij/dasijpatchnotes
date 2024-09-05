<template>
    <div v-if="ability" class="ability-tooltip">
        <p class="text-sm font-semibold" :class="abilityType === 'modified' ? 'modified-text' : 'vanilla-text'">
            {{ abilityType === 'modified' ? 'Modified Version' : 'Vanilla Version' }}
        </p>
        <div class="flex items-center mb-2">
            <img :src="ability.imagePath" alt="ability image" class="tooltip-image">
            <h3 class="text-xl font-semibold ml-2" style="color: #0099ff;">{{ ability.name }}</h3>
        </div>
        <div class="flex items-center text-xs mb-2">
            <div v-if="ability.cooldown" class="mr-2">
                <span class="font-semibold">Cooldown:</span> <span v-html="formatText(ability.cooldown)"></span>
            </div>
            <div v-if="ability.manaCost">
                <span class="font-semibold">Mana Cost:</span> <span v-html="formatText(ability.manaCost)"></span>
            </div>
        </div>
        <p class="text-sm" v-html="formatText(ability.description)"></p>
        <div v-if="ability.questText" class="mt-2">
            <p class="text-sm font-semibold quest-text">❢ Quest:</p>
            <p class="text-sm" v-html="ability.questText"></p>
        </div>
        <div v-if="ability.rewardsText && ability.rewardsText.length > 0" class="mt-2">
            <p class="text-sm font-semibold reward-text">❢ Rewards:</p>
            <ul>
                <li v-for="(reward, index) in ability.rewardsText" :key="index" class="text-sm" v-html="reward"></li>
            </ul>
        </div>
        <div v-if="ability.passivesText && ability.passivesText.length > 0" class="mt-2">
            <p class="text-sm font-semibold passive-text">Passive:</p>
            <ul>
                <li v-for="(passive, index) in ability.passivesText" :key="index" class="text-sm" v-html="passive"></li>
            </ul>
        </div>
    </div>
</template>

<script>
export default {
    name: 'AbilityTooltip',
    props: {
        ability: {
            type: Object,
            required: true
        },
        abilityType: {
            type: String,
            required: true
        }
    },
    methods: {
        formatText(text) {
            if (!text) return '';
            return text.replace(/{highlight}(.*?){\/highlight}/g, '<span style="color: red;">$1</span>');
        }
    }
};
</script>

<style scoped>
.tooltip {
    position: fixed;
    z-index: 1000;
    background-color: black;
    color: white;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid purple;
    max-width: 300px;
    width: auto;
    display: none;
}

.tooltip-image {
    width: 32px;
    height: 32px;
    object-fit: cover;
    border-radius: 4px;
}

.modified-text {
    color: #ff6b6b;
}

.vanilla-text {
    color: #4ecdc4;
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
</style>
