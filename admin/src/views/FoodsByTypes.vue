<template>
  <div>
    <Progress />
    <v-card>
      <v-card-title>
        {{title}}
        <v-spacer></v-spacer>
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="Поиск по базе"
          single-line
          hide-details
        ></v-text-field>
      </v-card-title>
      <v-data-table
        :headers="headers"
        :items="foods"
        :search="search"
        :footer-props="{
        'items-per-page-options': [15, 30, 40, 50]
      }"
      ></v-data-table>
    </v-card>
  </div>
</template>
<script>
import { mapGetters } from "vuex";

import Progress from "@/components/Progress.vue";

export default {
  components: { Progress },
  data() {
    return {
      title: "",
      foods: [],
      search: "",
      headers: [
        {
          text: "Наименование (на 100г. продукта)",
          align: "start",
          sortable: false,
          value: "title",
        },
        { text: "Калории", value: "calories" },
        { text: "Жиры (g)", value: "fats" },
        { text: "Углеводы (g)", value: "carbohydrates" },
        { text: "Белки (g)", value: "proteins" },
      ],
    };
  },
  computed: {
    ...mapGetters(["foodByTypeId", "foodTypesById"]),
  },
  mounted() {
    this.$store.dispatch("changeOverlayStatus", true);
    this.$store.dispatch("getFoodTypes");
    this.$store.dispatch("getFoodById", this.$route.params.id).then(() => {
      this.$store.dispatch("changeOverlayStatus", false);
      this.foods = this.foodByTypeId(this.$route.params.id);
      this.title = this.foodTypesById(this.$route.params.id).title;
    });
  },
};
</script>
