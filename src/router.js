import { createRouter, createWebHashHistory } from 'vue-router';
import HeroPatchNotesPage from './components/HeroPatchNotesPage.vue';
import UnifiedPatchNotesPage from './components/UnifiedPatchNotesPage.vue';

const routes = [
  { path: '/', component: UnifiedPatchNotesPage },
  { path: '/heroes', component: HeroPatchNotesPage },
  { path: '/hero/:name', component: HeroPatchNotesPage },
  { path: '/maps', component: UnifiedPatchNotesPage },
  { path: '/map/:name', component: UnifiedPatchNotesPage },
  { path: '/general', component: UnifiedPatchNotesPage },
  { path: '/general/:name', component: UnifiedPatchNotesPage },
  { path: '/gamemodes', component: UnifiedPatchNotesPage },
  { path: '/gamemode/:name', component: UnifiedPatchNotesPage },
];

const router = createRouter({
  history: createWebHashHistory('/dasijpatchnotes/'),
  routes,
});

export default router;
