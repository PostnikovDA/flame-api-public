import Vue from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify';
import axios from 'axios'
import VueAxios from 'vue-axios'

axios.defaults.baseURL = 'http://localhost:8000/api/';
axios.defaults.headers.common['Authorization'] = `Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmaXJlYmFzZV9pZCI6IkF4WWlpV2FzYjhTS2pYR09xSzYwbUVtVnc2RTIiLCJleHAiOjE2MjYxMDA3NTUsInN1YiI6ImFjY2VzcyJ9.25NiKaHMZ5BoSaBU9VoI1cbZ3hcKYyRBZhC68NhJhZE`;

Vue.use(VueAxios, axios)
Vue.config.productionTip = false

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
