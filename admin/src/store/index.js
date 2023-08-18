import Vue from 'vue'
import Vuex from 'vuex'
import users from './modules/users'
import foods from './modules/foods'
import common from './modules/common'
import dishes from './modules/dishes'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    users,
    foods,
    common,
    dishes,
  }
})
