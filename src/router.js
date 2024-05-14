import { createRouter, createWebHistory } from 'vue-router';
import HeroesPage from './components/HeroesPage.vue';
import HeroPatchNotesPage from './components/HeroPatchNotesPage.vue';
import MainPage from './components/MainPage.vue';
import MapsPage from '@/components/MapsPage.vue';
import MapPatchNotesPage from '@/components/MapPatchNotesPage.vue';
import GeneralPage from '@/components/GeneralPage.vue';
import GeneralPatchNotesPage from '@/components/GeneralPatchNotesPage.vue';
import GameModesPage from '@/components/GameModesPage.vue';
import GameModesPatchNotesPage from '@/components/GameModesPatchNotesPage.vue'; // Add this import

const routes = [
  { path: '/', component: MainPage },
  { path: '/heroes', component: HeroesPage },
  { path: '/hero/:name', component: HeroPatchNotesPage },
  { path: '/maps', name: 'Maps', component: MapsPage },
  { path: '/map/:name', component: MapPatchNotesPage },
  { path: '/general', component: GeneralPage },
  { path: '/general/:name', component: GeneralPatchNotesPage },
  { path: '/gamemodes', component: GameModesPage },
  { path: '/gamemode/:name', component: GameModesPatchNotesPage }, // Add this route
];

const router = createRouter({
  history: createWebHistory('/dasijpatchnotes/'), // Keep the base URL
  routes,
});

export default router;
