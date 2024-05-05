<template>
  <div>
    <h1>Heroes</h1>
    <div v-for="hero in heroes" :key="hero.id">
      <router-link :to="'/hero/' + hero.name.toLowerCase()">
        <img :src="require(`@/assets/${hero.image}`)" :alt="hero.name" />
        <span>{{ hero.name }}</span>
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HeroesPage',
  data() {
    return {
      heroes: [],
    };
  },
  async created() {
    const heroFiles = require.context('@/data/heroes', false, /\.json$/);
    const heroes = await Promise.all(
      heroFiles.keys().map(async (key) => {
        const heroData = await heroFiles(key);
        return {
          id: heroData.id,
          name: heroData.name,
          image: heroData.image,
        };
      })
    );
    this.heroes = heroes;
  },
};
</script>