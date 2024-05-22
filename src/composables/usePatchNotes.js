// src/composables/usePatchNotes.js
import { ref, watch } from 'vue';
import { database, ref as dbRef, auth, googleProvider, facebookProvider } from '../firebase';
import { set, get } from 'firebase/database';
import { signInWithPopup } from 'firebase/auth';
import { useRoute } from 'vue-router';

export default function usePatchNotes() {
    const route = useRoute();
    const item = ref({});
    const patchNotes = ref([]);
    const selectedTab = ref('patchNotes');
    const isUserLoggedIn = ref(false);
    const isLoading = ref(false);

    const loadData = async (type, name) => {
        try {
            const data = await import(`../data/${type}/${name}.json`);
            item.value = data.default;
            patchNotes.value = data.default.patchNotes;
            console.log(`Loaded ${type} data:`, data.default);
        } catch (error) {
            console.error(`Failed to load ${type} data`, error);
        }
    };

    const loadGameModeData = (gameModeName) => loadData('gamemodes', gameModeName);
    const loadMapData = (mapName) => loadData('maps', mapName);
    const loadGeneralData = (generalName) => loadData('general', generalName);
    const loadHeroData = (heroName) => loadData('heroes', heroName);

    watch(
        () => route.params.name,
        (newName) => {
            const name = newName.toLowerCase().replace(/ /g, '_');
            if (route.path.includes('gamemodes')) loadGameModeData(name);
            else if (route.path.includes('maps')) loadMapData(name);
            else if (route.path.includes('general')) loadGeneralData(name);
            else if (route.path.includes('heroes')) loadHeroData(name);
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
        const changesRef = dbRef(database, `${route.path.split('/')[1]}/${item.value.name.toLowerCase().replace(/ /g, '_')}/patchNotes`);
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

    const authenticateUser = () => {
        auth.onAuthStateChanged(user => {
            isUserLoggedIn.value = !!user;
        });
    };

    const handleLogin = () => {
        const provider = Math.random() > 0.5 ? googleProvider : facebookProvider;
        signInWithPopup(auth, provider)
            .then(result => {
                console.log('User logged in:', result.user);
            })
            .catch(error => {
                console.error('Error during authentication:', error);
            });
    };

    const checkUserLogin = () => {
        auth.onAuthStateChanged(user => {
            isUserLoggedIn.value = !!user;
        });
    };

    const loadChanges = () => {
        if (!item.value.name) {
            console.error('Item name is not defined');
            return;
        }
        const changesRef = dbRef(database, `${route.path.split('/')[1]}/${item.value.name.toLowerCase().replace(/ /g, '_')}/patchNotes`);
        get(changesRef).then(snapshot => {
            if (snapshot.exists()) {
                patchNotes.value = snapshot.val();
            }
            isLoading.value = false;
        });
    };

    return {
        item,
        patchNotes,
        selectedTab,
        selectTab,
        likeChange,
        isUserLoggedIn,
        isLoading,
        loadChanges,
        authenticateUser,
        handleLogin,
        checkUserLogin,
    };
}