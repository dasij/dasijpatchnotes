<!-- HeroesPage.vue -->
<template>
  <div>
    <h1>Heroes</h1>
    <div v-for="hero in heroes" :key="hero.id">
      <router-link :to="'/heroes/' + hero.id">
        <img :src="hero.image" :alt="hero.name" />
        <span>{{ hero.name }}</span>
      </router-link>
    </div>
  </div>
</template>

<script>
import { heroes } from '../heroData.js'

export default {
  name: 'HeroesPage',
  data() {
    return {
      heroes: heroes,
    }
  },
}
</script>
