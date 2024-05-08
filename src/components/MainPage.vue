<!-- MainPage.vue -->
<template>
  <div class="main-page">
    <div class="navbar-overlay"></div>
    <nav class="navbar">
      <div class="navbar-content">
        <div class="navbar-background"></div>
        <div class="navbar-logo">
          <img src="@\assets\nav\logo_hots.png" alt="Logo">
        </div>
        <ul class="navbar-menu">
          <li><router-link to="/">Home</router-link></li>
          <li><router-link to="/heroes">Heroes</router-link></li>
        </ul>
      </div>
    </nav>

    <div class="content-wrapper">
      <div v-if="isMainRoute" class="welcome-title-container">
        <h1 class="welcome-title">WELCOME TO DASIJ PATCH NOTES</h1>
      </div>
      <div v-if="isMainRoute" class="explanation-section px-4 sm:px-6 lg:px-8">
        <p class="text-lg sm:text-xl lg:text-2xl max-w-3xl mx-auto">Here you will find a patch notes based on my
          philosophy so every change i propose will be base on things i
          believe are correct for the Heroes of the Storm crave. I my self can't recreate the feeling that the original
          developers wanted and neither i want to and that's because i can't and i don't pretend to. My main focus on
          the changes i propose are based on further diving into the estabilished concept of how the heroes role both in
          lore and gameplay prioritizing the fun rather than full gameplay</p>
      </div>
      <div v-if="isMainRoute" class="link-section">
        <router-link to="/heroes">
          <div class="image-wrapper">
            <img class="rounded-full" src="@/assets/mainpage/Nexus_Recruit_Portrait.webp" alt="Heroes">
          </div>
          <span>Heroes</span>
        </router-link>
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

.navbar-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 150px;
  /* Adjust the height to match the navbar height */
  background-color: rgba(0, 0, 0, 0.4);
  z-index: 0;
}

.navbar {
  display: flex;
  justify-content: center;
  padding: 0;
  background-color: transparent;
  position: relative;
  z-index: 1;
  padding-top: 50px;
  padding-bottom: 50px;
}

.navbar-content {
  display: flex;
  align-items: center;
  max-width: 1200px;
  width: 100%;
  position: relative;
  height: 50px;
  padding-left: 280px;
  /* Adjust the padding to create space for the logo */
}

.navbar-background {
  position: absolute;
  top: 0;
  left: 200px;
  width: calc(100% - 200px);
  height: 100%;
  background: linear-gradient(to right, #04459F, #2D0699);
  z-index: -1;
  border-radius: 10px;
}

.navbar-logo {
  position: absolute;
  top: 50%;
  left: 0;
  transform: translateY(-50%);

  z-index: 2;
  margin-left: 1rem;
  /* Add margin to the logo */
}

.navbar-logo img {
  height: auto;
  width: auto;
  margin-left: 1rem;
  max-width: none;

}

.navbar-menu {
  margin-left: 1rem;
  display: flex;
  align-items: center;
  color: #fff;
  text-decoration: none;
  font-family: "Blizzard", sans-serif;
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
  transition: color 0.2s ease;
  height: 100%;
}

.navbar-menu li {
  margin-left: 1rem;
  display: flex;
  align-items: center;
  color: #fff;
  text-decoration: none;
  font-family: "Blizzard", sans-serif;
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
  transition: background-color 0.3s ease;
  padding: 0 5px;
  height: 100%;
}

.navbar-menu li a {
  color: #CCCCFF;
  text-decoration: none;
  display: flex;
  align-items: center;
  height: 100%;
  padding: 0 10px;

}

.navbar-menu li a:hover {
  color: #fff;
}

.navbar-menu li:hover {
  background: linear-gradient(to bottom, #1238A2, #00AAFF);
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

.link-section {
  display: flex;
  justify-content: center;
  margin-bottom: 40px;
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
  width: 200px;
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
  width: 205px;
  height: 205px;
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