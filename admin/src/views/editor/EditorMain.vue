<template>
  <v-container>
    <v-row no-gutters>
      <v-col v-for="card in cards" :key="card.id" lg="3">
        <v-card class="mx-auto" max-width="344" outlined>
          <v-list-item two-line>
            <v-list-item-content>
              <v-list-item-title class="headline mb-1">{{card.title}}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn text v-on:click="moveToDish()">Открыть</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data: () => ({
    cards: [{ title: "Блюда", id: 1 }],
  }),
  methods: {
    moveToDish() {
      this.$router.replace({ path: `/editor/dishes` });
    },
  },
};
</script>