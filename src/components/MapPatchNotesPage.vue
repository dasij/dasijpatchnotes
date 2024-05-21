<template>
    <div class="bg-hots-repeat min-h-screen">
        <div class="container mx-auto py-8">
            <nav class="mb-8">
                <button @click="selectTab('patchNotes')" :class="{ 'selected': selectedTab === 'patchNotes' }"
                    class="px-14 py-8 text-white font-semibold rounded mr-4 nav-tabs">
                    Patch Notes
                </button>
            </nav>

            <div v-if="selectedTab === 'patchNotes'" class="mt-8">
                <div class="bg-hots-repeat min-h-screen">
                    <div class="container mx-auto py-8">
                        <h1 class="text-4xl font-bold text-white mb-4">{{ map.name }} PATCH NOTES</h1>
                        <div v-for="patchNote in patchNotes" :key="patchNote.id" class="mb-12">
                            <h2 class="text-2xl font-bold text-white mb-2">{{ patchNote.title }}</h2>
                            <p class="text-gray-400 text-sm mb-6">{{ patchNote.date }}</p>
                            <div v-if="patchNote.developerCommentary"
                                class="mt-4 bg-[#742aff] bg-opacity-5 border-l-4 border-[#742aff] p-4 text-white italic">
                                <p class="font-semibold mb-2">Developer Comment:</p>
                                <p v-for="(paragraph, index) in patchNote.developerCommentary.split('\n\n')"
                                    :key="index">
                                    {{ paragraph }}
                                </p>
                            </div>
                            <div v-if="patchNote.general && patchNote.general.length > 0" class="mt-8">
                                <h3 class="text-xl font-semibold" style="color: #9900ff;">General Changes</h3>
                                <ul class="list-disc list-inside space-y-4" style="color: #ccc8d3;">
                                    <li v-for="(item, index) in patchNote.general" :key="index">
                                        <span class="text-lg font-medium" style="color: #0099ff;">{{ item.change
                                            }}</span>
                                        <ul class="list-disc list-inside ml-4">
                                            <li v-for="(textItem, textIndex) in item.texts" :key="textIndex">
                                                <span style="color: #ccc8d3;">{{ textItem.text }}</span>
                                                <div v-if="textItem.image" class="mt-2">
                                                    <img :src="require(`@/assets/${textItem.image}`)"
                                                        alt="Patch Note Image"
                                                        class="max-w-[400px] rounded-[10%] border-4 border-purple-500 mb-7">
                                                </div>
                                                <ul v-if="textItem.subtexts" class="list-disc list-inside ml-8">
                                                    <li v-for="(subtext, subtextIndex) in textItem.subtexts"
                                                        :key="subtextIndex" class="text-sm" style="color: #ccc8d3;">
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
                                        <button @click="likeChange(patchNote.id, index)"
                                            :class="['like-button', { 'loading': isLoading, 'liked': item.likedBy && item.likedBy[userId] }]">
                                            👍 {{ item.likes || 0 }}
                                        </button>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div v-if="selectedTab === 'details'" class="mt-8">
                <div class="map-details-container mt-8">
                    <h2 class="text-2xl font-bold text-white mb-4">Map Details</h2>
                    <p class="text-white">{{ map.details }}</p>
                </div>
            </div>
        </div>
    </div>
</template>


<script>
import { database, ref as dbRef, auth, googleProvider, facebookProvider } from '../firebase';
import { set, get } from 'firebase/database';
import { signInWithPopup } from 'firebase/auth';
import { watch, ref } from 'vue';
import { useRoute } from 'vue-router';

export default {
    name: 'MapPatchNotesPage',
    setup(props, { emit }) {
        const route = useRoute();
        const map = ref({});
        const patchNotes = ref([]);
        const selectedTab = ref('patchNotes');
        const isUserLoggedIn = ref(false);
        const isLoading = ref(false);

        const loadMapData = async (mapName) => {
            try {
                const mapData = await import(`../data/maps/${mapName}.json`);
                map.value = mapData.default;
                patchNotes.value = mapData.default.patchNotes;
            } catch (error) {
                console.error('Failed to load map data', error);
            }
        };

        watch(
            () => route.params.name,
            (newName) => {
                const mapName = newName.toLowerCase().replace(/ /g, '_');
                loadMapData(mapName);
            },
            { immediate: true }
        );

        const selectTab = (tab) => {
            selectedTab.value = tab;
        };

        const likeChange = (patchNoteId, generalIndex, changeIndex = null) => {
            if (!isUserLoggedIn.value) {
                emit('open-login-modal');
                return;
            }

            const patchNote = patchNotes.value.find(note => note.id === patchNoteId);
            let change;
            if (changeIndex !== null) {
                const section = patchNote.sections[generalIndex];
                change = section.changes[changeIndex];
            } else {
                change = patchNote.general[generalIndex];
            }

            if (!change.likedBy) {
                change.likedBy = {};
            }

            const userId = getUserId();
            if (userId) {
                if (change.likedBy[userId]) {
                    change.likes = (change.likes || 0) - 1;
                    delete change.likedBy[userId];
                } else {
                    change.likes = (change.likes || 0) + 1;
                    change.likedBy[userId] = true;
                }
                saveChanges();
            }
        };

        const saveChanges = () => {
            const changesRef = dbRef(database, `maps/${map.value.name.toLowerCase().replace(/ /g, '_')}/patchNotes`);
            set(changesRef, patchNotes.value);
        };

        const getUserId = () => {
            let userId = localStorage.getItem('userId');
            if (!userId) {
                userId = 'user-' + Math.random().toString(36).substr(2, 9);
                localStorage.setItem('userId', userId);
            }
            return userId;
        };

        auth.onAuthStateChanged(user => {
            isUserLoggedIn.value = !!user;
        });

        return {
            map,
            patchNotes,
            selectedTab,
            selectTab,
            likeChange,
            isUserLoggedIn,
            isLoading,
        };
    },
    methods: {
        authenticateUser() {
            auth.onAuthStateChanged(user => {
                this.isUserLoggedIn = !!user;
                if (user) {
                    this.userId = user.uid;
                }
            });
        },
        handleLogin() {
            const provider = Math.random() > 0.5 ? googleProvider : facebookProvider;
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
        loadChanges() {
            if (!this.map.name) {
                console.error('Map name is not defined');
                return;
            }
            const changesRef = dbRef(database, `maps/${this.map.name.toLowerCase().replace(/ /g, '_')}/patchNotes`);
            get(changesRef).then(snapshot => {
                if (snapshot.exists()) {
                    this.patchNotes = snapshot.val();
                }
                this.isLoading = false; // Atualizar o estado de carregamento
            });
        }
    },
    mounted() {
        this.checkUserLogin();
        this.authenticateUser();
        this.loadChanges();
    },
};
</script>


<style scoped>
@import '@/assets/css/common.css';
</style>
