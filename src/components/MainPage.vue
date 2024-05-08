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
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MainPage',
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
  background-color: rgba(0, 0, 0, 0.7);
  min-height: calc(100vh);

}
</style>