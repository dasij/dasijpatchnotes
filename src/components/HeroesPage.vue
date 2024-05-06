<template>
  <div class="bg-heroes-page-container bg-cover bg-no-repeat  min-h-screen">
    <div class="container mx-auto py-8">
      <h1 class="text-3xl font-bold mb-4 text-white">Heroes</h1>
      <div class="mb-4">
        <button
          v-for="role in roles"
          :key="role.id"
          @click="filterHeroes(role.name)"
          class="px-4 py-2 mr-2 rounded bg-blue-500 text-white"
        >
          {{ role.name }}
        </button>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        <div v-for="hero in filteredHeroes" :key="hero.id" class="bg-white bg-opacity-75 p-4 rounded shadow">
          <router-link :to="'/hero/' + hero.name.toLowerCase()">
            <img :src="require(`@/assets/${hero.image}`)" :alt="hero.name" class="w-full h-auto mb-2" />
            <span class="text-lg font-bold text-gray-800">{{ hero.name }}</span>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HeroesPage',
  data() {
    return {
      heroes: [],
      roles: [],
      selectedRole: 'All',
    };
  },
  computed: {
    filteredHeroes() {
      if (this.selectedRole === 'All') {
        return this.heroes;
      } else {
        return this.heroes.filter(hero => hero.role === this.selectedRole);
      }
    },
  },
  methods: {
    filterHeroes(role) {
      this.selectedRole = role;
    },
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
          role: heroData.role,
        };
      })
    );
    this.heroes = heroes;

    const uniqueRoles = [...new Set(heroes.map(hero => hero.role))];
    this.roles = [
      { id: 'all', name: 'All' },
      ...uniqueRoles.map(role => ({ id: role.toLowerCase(), name: role })),
    ];
  },
};
</script>