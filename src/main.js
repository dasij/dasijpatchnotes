import { createApp } from 'vue'
import App from './App.vue' // Import the root component
import router from './router.js'
import { createMetaManager } from 'vue-meta'
import './index.css'
import './assets/css/common.css';

const app = createApp(App) // Pass the root component to createApp
app.use(router)
app.use(createMetaManager())
app.mount('#app')