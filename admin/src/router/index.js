import Vue from 'vue'
import VueRouter from 'vue-router'
// import Home from '../views/Home.vue'
import EditorMain from '../views/editor/EditorMain.vue'
import DishMain from '../views/editor/dishes/DishMain.vue'
import Foods from '../views/Foods.vue'
import FoodsByTypes from '../views/FoodsByTypes.vue'

Vue.use(VueRouter)

const routes = [
  // {
  //   path: '/',
  //   component: Home
  // },
  {
    path: '/editor',
    component: EditorMain,
  },
  {
    path: '/editor/dishes',
    component: DishMain
  },

  {
    path: '/foods',
    component: Foods
  },
  {
    path: '/foods_by_types/:id',
    component: FoodsByTypes
  },

]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
