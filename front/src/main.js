// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import '@mdi/font/css/materialdesignicons.css'
import Vue from 'vue'
import App from './App'
import router from './router'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'
import VueHighlightJS from 'vue-highlight.js'
import 'vue-highlight.js/lib/allLanguages'
import 'highlight.js/styles/atom-one-dark-reasonable.css'

Vue.use(VueHighlightJS)
Vue.use(Vuetify, {
  iconfont: 'mdi'
})
Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
