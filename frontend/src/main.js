import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import api, { setupInterceptors } from '@/utils/axios'
import './assets/tailwind.css'
import i18n from './i18n'
import HeadlessUI from './plugins/headlessui'
import FlatPickr from 'vue-flatpickr-component';
import 'flatpickr/dist/flatpickr.css';

const app = createApp(App)
app.use(store)
app.use(router)
app.use(i18n)
app.use(HeadlessUI)

app.component('FlatPickr', FlatPickr)

app.mount('#app')

setupInterceptors(store)

store.dispatch('auth/checkAuth')

// // v-click-outside direktiva
// app.directive('click-outside', {
//     beforeMount(el, binding) {
//       el.__clickOutsideHandler__ = event => {
//         // Agar click element ichida bo‘lmasa, funksiyani chaqir
//         if (!(el === event.target || el.contains(event.target))) {
//           binding.value(event)
//         }
//       }
//       document.addEventListener('click', el.__clickOutsideHandler__)
//     },
//     unmounted(el) {
//       document.removeEventListener('click', el.__clickOutsideHandler__)
//       el.__clickOutsideHandler__ = null
//     }
//   })
