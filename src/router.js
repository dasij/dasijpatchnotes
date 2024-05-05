import { createRouter, createWebHistory } from 'vue-router'
import HeroesPage from './components/HeroesPage.vue'
import HeroPatchNotesPage from './components/HeroPatchNotesPage.vue'

const routes = [
  { path: '/heroes', component: HeroesPage },
  { path: '/hero/:name', component: HeroPatchNotesPage },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router