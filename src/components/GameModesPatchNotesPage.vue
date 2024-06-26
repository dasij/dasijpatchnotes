<template>
  <div class="bg-hots-repeat min-h-screen">
    <div class="container mx-auto py-8">
      <nav class="mb-8">
        <button @click="selectTab('patchNotes')"
          :class="['px-14 py-8 text-white font-semibold rounded mr-4 nav-tabs', { 'selected': selectedTab === 'patchNotes' }]">
          Patch Notes
        </button>
      </nav>

      <div v-if="selectedTab === 'patchNotes'" class="mt-8">
        <h1 class="text-4xl font-bold text-white mb-4">{{ gameModeItem.name }} PATCH NOTES</h1>
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
            <h3 class="text-xl font-semibold" style="color: #9900ff;">General Changes</h3>
            <ul class="list-disc list-inside space-y-4" style="color: #ccc8d3;">
              <li v-for="(item, index) in patchNote.general" :key="index">
                <span class="text-lg font-medium" style="color: #0099ff;">{{ item.change }}</span>
                <ul class="list-disc list-inside ml-4">
                  <li v-for="(textItem, textIndex) in item.texts" :key="textIndex">
                    <span style="color: #ccc8d3;">{{ textItem.text }}</span>
                    <div v-if="textItem.image" class="mt-2">
                      <img :src="require(`@/assets/${textItem.image}`)" alt="Patch Note Image"
                        class="max-w-[400px] rounded-[10%] border-4 border-purple-500 mb-7">
                    </div>
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
                <button @click="likeChange(patchNote.id, item.change_id)"
                  :class="['like-button', { 'loading': isLoading, 'liked': item.likedBy && item.likedBy[userId] }]">
                  👍 {{ item.likes || 0 }}
                </button>
              </li>
            </ul>
          </div>
        </div>
      </div>

      <div v-if="selectedTab === 'details'" class="mt-8">
        <div class="general-details-container mt-8">
          <h2 class="text-2xl font-bold text-white mb-4">General Details</h2>
          <p class="text-white">{{ gameModeItem.details }}</p>
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
  name: 'GameModesPatchNotesPage',
  setup(props, { emit }) {
    const route = useRoute();
    const gameModeItem = ref({});
    const patchNotes = ref([]);
    const selectedTab = ref('patchNotes');
    const isUserLoggedIn = ref(false);
    const isLoading = ref(false);
    const likesData = ref({});

    const loadGameModeData = async (gameModeName) => {
      try {
        const gameModeData = await import(`../data/gamemodes/${gameModeName}.json`);
        gameModeItem.value = gameModeData.default;
        patchNotes.value = gameModeData.default.patchNotes;
        loadLikes(gameModeName);
      } catch (error) {
        console.error('Failed to load game mode data', error);
      }
    };

    const loadLikes = async (gameModeName) => {
      const likesRef = dbRef(database, `gamemodes/${gameModeName}/likes`);
      const snapshot = await get(likesRef);
      if (snapshot.exists()) {
        likesData.value = snapshot.val();
        applyLikes();
      }
    };

    const applyLikes = () => {
      patchNotes.value.forEach(patchNote => {
        patchNote.general.forEach(change => {
          const likeInfo = likesData.value[change.change_id];
          if (likeInfo) {
            change.likes = likeInfo.likes;
            change.likedBy = likeInfo.likedBy;
          }
        });
      });
    };

    watch(
      () => route.params.name,
      (newName) => {
        const gameModeName = newName.toLowerCase().replace(/ /g, '_');
        loadGameModeData(gameModeName);
      },
      { immediate: true }
    );

    const selectTab = (tab) => {
      selectedTab.value = tab;
    };

    const likeChange = (patchNoteId, changeId) => {
      if (!isUserLoggedIn.value) {
        emit('open-login-modal');
        return;
      }

      const patchNote = patchNotes.value.find(note => note.id === patchNoteId);
      const change = patchNote.general.find(item => item.change_id === changeId);

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
      const gameModeName = gameModeItem.value.name.toLowerCase().replace(/ /g, '_');
      const likesRef = dbRef(database, `gamemodes/${gameModeName}/likes`);
      const likesToSave = {};

      patchNotes.value.forEach(patchNote => {
        patchNote.general.forEach(change => {
          likesToSave[change.change_id] = {
            likes: change.likes,
            likedBy: change.likedBy
          };
        });
      });

      set(likesRef, likesToSave);
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
      gameModeItem,
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
      if (!this.gameModeItem.name) {
        console.error('Game mode item name is not defined');
        return;
      }
      const changesRef = dbRef(database, `gamemodes/${this.gameModeItem.name.toLowerCase().replace(/ /g, '_')}/patchNotes`);
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

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  z-index: 1;
}

.container {
  position: relative;
  z-index: 2;
}

.nav-tabs {
  background-color: #4a148c;
  /* Darker purple */
  transition: background-color 0.3s ease-in-out;
}

.nav-tabs.selected {
  background-color: #6a1b9a;
  /* Slightly lighter purple */
}

.general-details-container {
  background-color: rgba(0, 0, 0, 0.7);
  padding: 20px;
  border-radius: 10px;
}
</style>