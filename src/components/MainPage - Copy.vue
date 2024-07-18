<template>
  <div class="main-page">
    <div class="content-wrapper">
      <div v-if="isMainRoute" class="welcome-title-container">
        <h1 class="welcome-title">WELCOME TO DASIJ'S PATCH NOTES</h1>
      </div>
      <div v-if="isMainRoute" class="explanation-section px-4 sm:px-6 lg:px-8">
        <p class="text-lg sm:text-xl lg:text-2xl max-w-3xl mx-auto">Here you will find patch notes based on my
          philosophy, so every change I propose will be based on things I believe are correct for the Heroes of the
          Storm I envision. I myself can't recreate the feeling that the original developers wanted, and I don't want to
          either, because I can't and I don't pretend to. My main focus on the changes I propose is based on further
          diving into the established concept of how the heroes' roles, both in lore and gameplay, prioritize fun rather
          than full gameplay balance.</p>
      </div>

      <div class="links-container">
        <div v-if="isMainRoute" class="link-section">
          <router-link to="/heroes">
            <div class="image-wrapper">
              <img class="rounded-full" src="@/assets/mainpage/heroes.webp" alt="Heroes">
            </div>
            <span>Heroes</span>
          </router-link>
        </div>

        <div v-if="isMainRoute" class="link-section">
          <router-link to="/maps">
            <div class="image-wrapper">
              <img class="rounded-full" src="@/assets/mainpage/maps.webp" alt="Maps">
            </div>
            <span>Maps</span>
          </router-link>
        </div>

        <div v-if="isMainRoute" class="link-section">
          <router-link to="/general">
            <div class="image-wrapper">
              <img class="rounded-full" src="@/assets/mainpage/general.webp" alt="General">
            </div>
            <span>General</span>
          </router-link>
        </div>

        <div v-if="isMainRoute" class="link-section">
          <router-link to="/gamemodes">
            <div class="image-wrapper">
              <img class="rounded-full" src="@/assets/mainpage/gamemodes.webp" alt="Game Modes">
            </div>
            <span>Game Modes</span>
          </router-link>
        </div>
      </div>

      <router-view></router-view>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MainPage',
  computed: {
    isMainRoute() {
      return this.$route.path === '/';
    }
  }
}
</script>

<style scoped>
.main-page {
  background-image: url('@/assets/background-main-website.jpg');
  background-size: cover;
  background-position: center;
  min-height: 100vh;
}

.content-wrapper {
  background-color: rgba(0, 0, 0, 0.9);
  min-height: calc(100vh);
}

.welcome-title-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
  /* Adjust the height as needed */
}

.welcome-title {
  font-family: "Blizzard", sans-serif;
  font-size: 48px;
  font-weight: 700;
  color: #fff;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
  text-align: center;
}

.explanation-section {
  text-align: center;
  margin-bottom: 40px;
}

.explanation-section p {
  font-family: "Blizzard", sans-serif;
  font-size: 20px;
  color: #fff;
}

.links-container {
  display: flex;
  justify-content: center;
  /* Center the links horizontally */
  flex-wrap: wrap;
  /* Allows wrapping if the screen is too small */
}

.link-section {
  margin: 0 20px;
  /* Adds spacing between the links */
}

.link-section a {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-decoration: none;
  position: relative;
}

.link-section .image-wrapper {
  position: relative;
  z-index: 1;
}

.link-section img {
  width: 152px;
  height: auto;
  margin-bottom: 10px;
  transition: transform 0.3s ease-in-out;
  border-radius: 50%;
}

.link-section a:hover img {
  transform: scale(1.1) translateY(-5px);
}

.link-section a::before {
  content: '';
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 157px;
  height: 157px;
  border-radius: 50%;
  border: 6px solid #2E60A3;
  pointer-events: none;
  transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
  z-index: 2;
}

.link-section a:hover::before {
  transform: translateX(-50%) scale(1.1) translateY(-5px);
  box-shadow: inset 0 0 7px rgba(74, 143, 217, 0.8), inset 0 0 3px rgba(74, 143, 217, 0.5);
}

.link-section span {
  margin-top: 20px;
  font-family: "Blizzard", sans-serif;
  font-size: 18px;
  color: #fff;
}
</style>
