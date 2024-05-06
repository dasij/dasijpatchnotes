<!-- MainPage.vue -->
<template>
    <div>
      <h1>Main Page</h1>
      <nav>
        <router-link to="/heroes">Heroes CLICK HERE TO START</router-link>
      </nav>
      <router-view></router-view>
    </div>
  </template>
  
  <script>
  export default {
    name: 'MainPage',
  }
  </script>