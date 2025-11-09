import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import auth from './stores/auth';

import './assets/global.css'; 

const app = createApp(App)
app.use(router)

// no bloqueamos el montaje; cargamos la sesión en background
auth.loadSession()

app.mount('#app');
