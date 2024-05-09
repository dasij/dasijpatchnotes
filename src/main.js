import { createApp } from 'vue'
import App from './App.vue' // Import the root component
import router from './router.js'
import './index.css'

const app = createApp(App) // Pass the root component to createApp
app.use(router)
app.mount('#app')