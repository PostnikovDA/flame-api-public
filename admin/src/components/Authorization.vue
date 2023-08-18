<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card class="elevation-12">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>Авторизация в FLAME ADMIN</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form ref="form" v-model="valid" lazy-validation>
              <v-text-field
                v-model="email"
                :rules="emailRules"
                label="Email"
                name="email"
                prepend-icon="mdi-account"
                required
                type="text"
              ></v-text-field>

              <v-text-field
                v-model="password"
                :append-icon="show ? 'mdi-eye' : 'mdi-eye-off-outline'"
                :rules="passwordRules"
                :type="show ? 'text' : 'password'"
                @click:append="show = !show"
                hint="Минимум 8 символов"
                id="password"
                label="Пароль"
                name="password"
                prepend-icon="mdi-lock"
                v-on:keyup.enter="submit"
              ></v-text-field>
            </v-form>
          </v-card-text>
          <div v-if=error align="center">{{ error_message }}</div>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" :disabled="!valid" @click="submit">Войти</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "Authorization",
  data: () => ({
    valid: true,
    email: "",
    emailRules: [
      (v) => !!v || "E-mail обязателен",
      (v) => /.+@.+\..+/.test(v) || "Невалидный email",
    ],
    show: false,
    password: "",
    passwordRules: [
      (v) => !!v || "Пароль обязателен",
      (v) => (v && v.length >= 8) || "Минимальное кол-во символов 8",
    ],
    token: "",
    error: false,
    error_message: "",
  }),
  methods: {
    submit() {
      if (this.$refs.form.validate()) {
        this.axios
          .post("auth/login_via_email", {
            user: {
              email: this.email,
              password: this.password,
            },
          })
          .then((response) => {
            let token = response.data.access_token
            localStorage.token = token
            this.$store.dispatch('login', {token: token})
          })
          .catch((error) => {
            this.error = true;
            this.error_message = error.response.data.detail;
          });
      }
    },
  },
};
</script>