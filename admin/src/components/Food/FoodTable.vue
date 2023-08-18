<template>
  <v-data-table
    :headers="headers"
    :items="foods"
    sort-by="calories"
    class="elevation-1 mt-4"
    :search="search"
  >
    <template v-slot:top>
      <v-toolbar flat color="white">
        <v-autocomplete
          v-model="food.type"
          :items="food_types"
          :filter="searchFilter"
          label="Категория поиска*"
          item-text="title"
          @input="refreshFoodByTypeId"
          return-object
          hide-details
        ></v-autocomplete>
        <v-divider class="mx-4" inset vertical></v-divider>
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="Поиск по базе"
          single-line
          hide-details
        ></v-text-field>
        <v-spacer></v-spacer>
        <v-dialog v-model="dialog" max-width="500px">
          <template v-slot:activator="{ on, attrs }">
            <v-btn color="primary" dark class="mb-2" v-bind="attrs" v-on="on">New Item</v-btn>
          </template>
          <v-card>
            <v-card-title>
              <span class="headline">{{ formTitle }}</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field v-model="editedItem.name" label="Dessert name"></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field v-model="editedItem.calories" label="Calories"></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field v-model="editedItem.fat" label="Fat (g)"></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field v-model="editedItem.carbs" label="Carbs (g)"></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field v-model="editedItem.protein" label="Protein (g)"></v-text-field>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="close">Cancel</v-btn>
              <v-btn color="blue darken-1" text @click="save">Save</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-toolbar>
    </template>
    <template v-slot:item.actions="{ item }">
      <v-icon small class="mr-2" @click="editItem(item)">mdi-pencil</v-icon>
      <v-icon small @click="deleteItem(item)">mdi-delete</v-icon>
    </template>
  </v-data-table>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "FoodTable",
  data: () => ({
    dialog: false,
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
      { text: "Actions", value: "actions", sortable: false },
    ],
    search: "",
    food: {},
    foods: [],
    food_types: [],
    editedIndex: -1,
    editedItem: {
      name: "",
      calories: 0,
      fat: 0,
      carbs: 0,
      protein: 0,
    },
    defaultItem: {
      name: "",
      calories: 0,
      fat: 0,
      carbs: 0,
      protein: 0,
    },
  }),

  computed: {
    ...mapGetters(["foodByTypeId", "foodTypes"]),
    formTitle() {
      return this.editedIndex === -1 ? "New Item" : "Edit Item";
    },
  },

  watch: {
    dialog(val) {
      val || this.close();
    },
  },

  created() {
    this.initialize();
  },

  methods: {
    initialize() {
      this.$store.dispatch("getFoodTypes").then(() => {
        this.food_types = this.foodTypes;
        this.food_types.push({
          group_id: 0,
          title: "Всё",
        });
      });
    },

    refreshFoodByTypeId(product_type) {
      const id = product_type.group_id;
      if (id === 0) {
        this.$store.dispatch("changeOverlayStatus", true);
        this.food_types.forEach((item) => {
          this.$store
            .dispatch("getFoodById", item.group_id)
            .then(() => {
              this.foods.push(...this.foodByTypeId(item.group_id));
            })
            .then(() => {
              this.$store.dispatch("changeOverlayStatus", false);
            });
        });
      } else {
        this.$store.dispatch("getFoodById", id).then(() => {
          this.foods = this.foodByTypeId(id);
        });
      }
    },

    searchFilter(item, query) {
      const text = item.title.toLowerCase();
      const searchText = query.toLowerCase();
      return text.indexOf(searchText) > -1;
    },

    editItem(item) {
      this.editedIndex = this.desserts.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },

    deleteItem(item) {
      const index = this.desserts.indexOf(item);
      confirm("Are you sure you want to delete this item?") &&
        this.desserts.splice(index, 1);
    },

    close() {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    save() {
      if (this.editedIndex > -1) {
        Object.assign(this.desserts[this.editedIndex], this.editedItem);
      } else {
        this.desserts.push(this.editedItem);
      }
      this.close();
    },
  },
};
</script>