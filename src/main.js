import { createApp } from 'vue'
import MainPage from './components/MainPage.vue'
import router from './router.js'
import './index.css'

const app = createApp(MainPage)
app.use(router)
app.mount('#app')