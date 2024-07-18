<template>
  <div class="bg-heroes-page-container bg-cover bg-no-repeat min-h-screen">
    <div class="container mx-auto py-8">
      <h1 class="text-3xl font-bold mb-4 text-white">Heroes</h1>
      <div class="mb-4">
        <button v-for="role in roles" :key="role.id" @click="filterHeroes(role.name)" class="role-button"
          :class="{ 'active': selectedRole === role.name }">
          <img :src="require(`@/assets/roles/${role.image}`)" :alt="role.name" />
          <span>{{ role.name }}</span>
        </button>
      </div>
      <div class="heroes-grid">
        <div v-for="hero in filteredHeroes" :key="hero.id" class="text-center hero-item">
          <router-link :to="'/hero/' + hero.name.toLowerCase()" class="block relative">
            <div class="hero-image-container">
              <img :src="require(`@/assets/${hero.image}`)" :alt="hero.name"
                class="w-38 h-38 object-contain mx-auto mb-2 rounded-full transition duration-300 ease-in-out transform hover:scale-110" />
            </div>
            <div
              class="hero-border rounded-full border-4 border-[#2E60A3] transition duration-300 ease-in-out hover:border-[#4a8fd9]">
            </div>
            <span class="text-lg font-bold text-[#CCE5FA] mt-6">{{ formatHeroName(hero.name) }}</span>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.hero-image-container {
  overflow: hidden;
  border-radius: 50%;
}

.hero-image-container img {
  transition: transform 0.3s ease-in-out;
}

.hero-image-container:hover img {
  transform: scale(1.1);
}

.hero-border {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 115px;
  height: 115px;
  pointer-events: none;
  transition: width 0.3s ease-in-out, height 0.3s ease-in-out;
}

.hero-image-container:hover+.hero-border {
  width: 120px;
  height: 120px;
  box-shadow: inset 0 0 7px rgba(74, 143, 217, 0.8), inset 0 0 3px rgba(74, 143, 217, 0.5);
}

.role-button {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem;
  margin-right: 0.5rem;
  margin-bottom: 0.5rem;
  border-radius: 0.375rem;
  background-color: transparent;
  transition: background-color 0.3s ease-in-out;
  border: 0px;


}

.role-button img {
  width: 2rem;
  height: 2rem;
  object-fit: contain;
  filter: brightness(0.6);
  transition: filter 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
  border-radius: 50%;
}

.role-button:hover img {
  filter: brightness(1);
  box-shadow: 0 0 8px rgba(74, 143, 217, 0.8);
}

.role-button:hover {
  filter: brightness(1);
  box-shadow: 0 0 0px rgba(74, 143, 217, 0.8);
}

.role-button span {
  margin-left: 0.5rem;
  color: white;
  font-weight: 600;
}

.role-button.active {
  background-color: rgba(59, 130, 246, 0.5);
}

.heroes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 1rem;
}

.hero-item {
  width: 113px;
  margin: 0 auto;
}

@media (min-width: 1024px) {
  .heroes-grid {
    grid-template-columns: repeat(6, 1fr);
    max-width: calc(150px * 6 + 5rem);
    /* 6 items + 5 gaps */
    margin-right: auto;
  }
}
</style>

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
      return this.heroes.filter(hero => {
        return hero.show !== "false" && (this.selectedRole === 'All' || hero.role === this.selectedRole);
      });
    },
  },
  methods: {
    filterHeroes(role) {
      this.selectedRole = role;
    },
    formatHeroName(name) {
      return name.split('-').map(part => part.charAt(0).toUpperCase() + part.slice(1).toLowerCase()).join(' ');
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
          show: heroData.show,
        };
      })
    );
    this.heroes = heroes;

    const roleData = require('@/data/roles.json');
    this.roles = roleData;
  },
};
</script>
