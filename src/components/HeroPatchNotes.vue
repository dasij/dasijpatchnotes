<template>
    <div class="patch-notes-container">
        <h1 class="text-4xl font-bold text-white mb-4">{{ heroName.toUpperCase() }} PATCH NOTES</h1>
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
                                    <li v-for="(subtext, subtextIndex) in textItem.subtexts" :key="subtextIndex"
                                        class="text-sm" style="color: #ccc8d3;">
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
                                        <span style="color: #ccc8d3;"
                                            v-html="convertTextPlaceholders(textItem.text)"></span>
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
</template>

<script>
import { ref, onMounted } from 'vue';
import { database, auth } from '../firebase';
import { ref as dbRef, set, get } from 'firebase/database';

export default {
    name: 'HeroPatchNotes',
    props: {
        heroName: {
            type: String,
            required: true
        },
        patchNotes: {
            type: Array,
            required: true
        }
    },
    setup(props) {
        const userId = ref(null);
        const isLoading = ref(false);

        onMounted(() => {
            auth.onAuthStateChanged(user => {
                userId.value = user ? user.uid : null;
            });
        });

        const convertTextPlaceholders = (text) => {
            if (!text) return '';
            return text.replace(/<([^,]+),\s*([^,]+),\s*([^,]+),\s*(\d+)(?:,\s*([^>]+))?>/g, (match, type, section, category, index, heroName) => {
                const targetHero = heroName || props.heroName;
                // Implement the logic to find the correct ability or talent
                // This might need to be adjusted based on your data structure
                const item = findAbilityOrTalent(type, section, category, parseInt(index, 10), targetHero);
                if (item) {
                    const className = type === 'modified' ? 'modified-text' : 'vanilla-text';
                    const imagePath = require(`@/assets/talents/${targetHero}/${item.image}`);
                    let heroPrefix = '';
                    if (heroName && heroName !== props.heroName) {
                        const displayHeroName = heroName.replace(/-/g, ' ')
                            .split(' ')
                            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
                            .join(' ');
                        heroPrefix = `<span class="hero-prefix">${displayHeroName}'s </span>`;
                    }
                    return `${heroPrefix}<img src="${imagePath}" alt="${item.name}" class="inline-image" />
        <span class="ability-tooltip ${className}" 
          data-type="${type}" 
          data-section="${section}" 
          data-category="${category}" 
          data-index="${index}" 
          data-hero="${targetHero}"
          data-tooltip="${item.name}">
          <span class="tooltip-content">${item.name}</span>
        </span>`;
                }
                return match;
            });
        };

        const findAbilityOrTalent = (type, section, category, index, heroName) => {
            const targetHero = heroName || props.heroName;
            const talentsFileName = type === 'modified' ? `${targetHero}_talents.json` : `${targetHero}_talents_vanilla.json`;
            const talentsData = require(`@/data/heroes/talents/${talentsFileName}`);

            if (section === 'abilities') {
                if (category === 'trait') {
                    return talentsData.abilities.trait;
                } else {
                    return talentsData.abilities[category][index];
                }
            } else {
                return talentsData[category][index];
            }
        };


        const likeChange = async (patchNoteId, changeId) => {
            if (!userId.value) {
                // Handle user not logged in
                return;
            }

            isLoading.value = true;
            const likesRef = dbRef(database, `heroes/${props.heroName}/likes/${changeId}`);

            try {
                const snapshot = await get(likesRef);
                const currentLikes = snapshot.val() || { likes: 0, likedBy: {} };

                if (currentLikes.likedBy[userId.value]) {
                    currentLikes.likes--;
                    delete currentLikes.likedBy[userId.value];
                } else {
                    currentLikes.likes++;
                    currentLikes.likedBy[userId.value] = true;
                }

                await set(likesRef, currentLikes);

                // Update local state
                const patchNote = props.patchNotes.find(note => note.id === patchNoteId);
                const change = patchNote.general.find(item => item.change_id === changeId) ||
                    patchNote.sections.flatMap(section => section.changes).find(item => item.change_id === changeId);

                if (change) {
                    change.likes = currentLikes.likes;
                    change.likedBy = currentLikes.likedBy;
                }
            } catch (error) {
                console.error('Error updating likes:', error);
            } finally {
                isLoading.value = false;
            }
        };

        return {
            userId,
            isLoading,
            convertTextPlaceholders,
            likeChange
        };
    }
};
</script>

<style scoped>
.patch-notes-container {
    color: #ffffff;
}

.like-button {
    background-color: #4a5568;
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 0.25rem;
    margin-top: 0.5rem;
    cursor: pointer;
    transition: background-color 0.3s;
}

.like-button:hover {
    background-color: #2d3748;
}

.like-button.liked {
    background-color: #48bb78;
}

.like-button.loading {
    opacity: 0.5;
    cursor: not-allowed;
}

.inline-image {
    width: 24px;
    height: 24px;
    vertical-align: middle;
    margin-right: 4px;
}

.ability-tooltip {
    position: relative;
    cursor: pointer;
}

.ability-tooltip .tooltip-content {
    visibility: hidden;
    width: 120px;
    background-color: black;
    color: #fff;
    text-align: center;
    border-radius: 6px;
    padding: 5px 0;
    position: absolute;
    z-index: 1;
    bottom: 125%;
    left: 50%;
    margin-left: -60px;
    opacity: 0;
    transition: opacity 0.3s;
}

.ability-tooltip:hover .tooltip-content {
    visibility: visible;
    opacity: 1;
}

.modified-text {
    color: #ff6b6b;
}

.vanilla-text {
    color: #4ecdc4;
}

.hero-prefix {
    font-weight: bold;
    color: #f6e58d;
}
</style>
