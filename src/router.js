import { createRouter, createWebHistory } from 'vue-router';
import HeroesPage from './components/HeroesPage.vue';
import HeroPatchNotesPage from './components/HeroPatchNotesPage.vue';
import MainPage from './components/MainPage.vue'; // Add this import
import MapsPage from '@/components/MapsPage.vue';
import MapPatchNotesPage from '@/components/MapPatchNotesPage.vue'; // Add this import

const routes = [
  { path: '/', component: MainPage }, // Set the main page as the root path
  { path: '/heroes', component: HeroesPage },
  { path: '/hero/:name', component: HeroPatchNotesPage },
  { path: '/maps', name: 'Maps', component: MapsPage },
  { path: '/map/:name', component: MapPatchNotesPage }, // Add this route
];

const router = createRouter({
  history: createWebHistory('/dasijpatchnotes/'), // Keep the base URL
  routes,
});

export default router;
