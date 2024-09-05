<template>
    <div v-if="talent" class="talent-tooltip">
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
        <div v-if="talent.quest" class="mt-2 quest-text">
            <p class="text-sm" v-html="formatText('❢ Quest: ' + talent.quest)"></p>
        </div>
        <div v-if="talent.rewards && talent.rewards.length > 0" class="mt-2">
            <ul>
                <li v-for="(reward, index) in talent.rewards" :key="index" class="text-sm reward-text"
                    v-html="formatText('❢ Reward: ' + reward)"></li>
            </ul>
        </div>
        <div v-if="talent.passives && talent.passives.length > 0" class="mt-2">
            <ul>
                <li v-for="(passive, index) in talent.passives" :key="index" class="text-sm"
                    v-html="formatText(passive)"></li>
            </ul>
        </div>
    </div>
</template>

<script>
export default {
    name: 'TalentTooltip',
    props: {
        talent: {
            type: Object,
            required: true
        }
    },
    methods: {
        formatText(text) {
            // Implement the formatText method as in your original component
            return text.replace(/{highlight}(.*?){\/highlight}/g, '<span style="color: red;">$1</span>');
        }
    }
}
</script>

<style scoped>
.talent-tooltip {
    position: absolute;
    z-index: 10;
    background-color: black;
    color: white;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid purple;
    max-width: 300px;
    width: auto;
}

.quest-text {
    color: #DFCB00 !important;
}

.reward-text {
    color: #DFCB00 !important;
}
</style>
