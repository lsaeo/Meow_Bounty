import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'

import '@fontsource/cinzel/400.css'
import '@fontsource/cinzel/700.css'
import '@fontsource/cinzel/900.css'
import '@fontsource/cormorant-garamond/400.css'
import '@fontsource/cormorant-garamond/700.css'
import '@fontsource/noto-serif-sc/400.css'
import '@fontsource/noto-serif-sc/700.css'

const app = createApp(App)
app.use(createPinia())
app.mount('#app')
