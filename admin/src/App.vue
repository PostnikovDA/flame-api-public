<template>
  <v-app v-if=token>
    <v-navigation-drawer v-model="drawer" app>
      <v-list dense>
        <!-- <v-list-item link to="/">
          <v-list-item-action>
            <v-icon>mdi-home</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Главная</v-list-item-title>
          </v-list-item-content>
        </v-list-item> -->
        <v-list-item link to="/editor">
          <v-list-item-action>
            <v-icon>mdi-email</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title >Редактор</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item link to="/foods">
          <v-list-item-action>
            <v-icon>mdi-apple</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title >База продуктов</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    
    <v-app-bar app color="primary" dark>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>FLAME ADMIN</v-toolbar-title>
      <v-spacer></v-spacer>

      <v-btn text @click="clearToken" link to="/">
        <span class="mr-2">Выйти</span>
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main>
      <router-view></router-view>
    </v-main>
  </v-app>
  <v-app v-else>
    <v-main>
      <Authorization/>
    </v-main>
  </v-app>
</template>

<script>
import Authorization from '@/components/Authorization.vue'

export default {
  name: "App",

  components: {
    Authorization
  },
  data: () => ({
    drawer: null,
  }),
  computed: {
    token () {
      if(localStorage.token) {
        return localStorage.token
      }
      return this.$store.state.users.token
    }
  },
  methods: {
    clearToken() {
      localStorage.token = ""
      this.$store.dispatch('logout')
      this.$router.go()
    },
  },
};
</script>
