<template>
  <div>
    <v-btn color="red" bottom dark fab fixed right @click="dialog = !dialog">
      <v-icon>mdi-plus</v-icon>
    </v-btn>
    <v-dialog v-model="dialog" width="1400px">
      <v-card>
        <v-card-title dark>Новое блюдо</v-card-title>
        <v-container>
          <v-row class="mx-2">
            <v-col cols="6">
              <v-text-field label="Название блюда*" v-model="dish.title"></v-text-field>
            </v-col>
            <v-col cols="6">
              <v-select
                v-model="dish.meal_id"
                :items="meals"
                label="Приём пищи*"
                required
                item-text="title"
                item-value="meal_id"
              ></v-select>
            </v-col>
            <v-col cols="2">
              <v-autocomplete
                v-model="dish.type"
                :items="foodTypes"
                :filter="searchFilter"
                label="Категория поиска*"
                item-text="title"
                @input="refreshFoodByTypeId"
                return-object
              ></v-autocomplete>
            </v-col>
            <v-col cols="9">
              <v-autocomplete
                v-model="selected"
                :items="foods"
                :filter="searchFilter"
                item-text="title"
                label="Наименование продукта"
                prepend-icon="mdi-database-search"
                return-object
              ></v-autocomplete>
            </v-col>
            <v-col cols="1">
              <v-btn text color="primary" @click="addSearchFood()">добавить</v-btn>
            </v-col>
            <v-col cols="12">
              <v-data-table
                v-model="selected_foods_in_table"
                :headers="headers"
                :items="selected_foods"
                show-select
                hide-default-footer
                group-by="category"
              ></v-data-table>
              <v-btn
                v-if="selectedFoodsListIsNotEmpty"
                @click="removeSelectedFoods()"
                text
                color="red"
              >Удалить</v-btn>
            </v-col>
          </v-row>
        </v-container>
        <v-card-actions>
          <v-btn text color="red" @click="cleanup()">Сбросить</v-btn>
          <v-spacer></v-spacer>
          <v-btn text color="primary" @click="cleanup(); dialog = false;">Закрыть</v-btn>
          <v-btn text color="primary" @click="save(); dialog = false;">Создать</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "AddDishForm",
  data: () => ({
    dish: {},
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
    foods: [],
    selected: "",
    selected_foods: [],
    selected_foods_in_table: [],
    dialog: false,
    meals: [
      { title: "Завтрак", meal_id: 1 },
      { title: "Обед", meal_id: 2 },
      { title: "Перекус", meal_id: 3 },
      { title: "Ужин", meal_id: 4 },
    ],
  }),
  computed: {
    ...mapGetters(["foodTypes", "foodByTypeId"]),
    selectedFoodsListIsNotEmpty: function () {
      return this.selected_foods_in_table.length > 0;
    },
  },
  methods: {
    refreshFoodByTypeId(product_type) {
      const id = product_type.group_id;
      this.$store.dispatch("getFoodById", id).then(() => {
        this.foods = this.foodByTypeId(id);
      });
    },
    searchFilter(item, query) {
      const text = item.title.toLowerCase();
      const searchText = query.toLowerCase();
      return text.indexOf(searchText) > -1;
    },
    addSearchFood() {
      const food_in_selected = this.selected_foods.find(
        (food) => food.id === this.selected.id
      );
      if (food_in_selected) {
        this.selected = "";
      } else {
        this.selected["category"] = this.dish.type.title;
        this.selected_foods.push(this.selected);
        this.selected = "";
      }
    },
    cleanup() {
      this.selected = "";
      this.selected_foods = [];
      this.selected_foods_in_table = [];
      this.dish = {};
    },
    removeSelectedFoods() {
      this.selected_foods = this.selected_foods.filter(
        (element) =>
          !this.selected_foods_in_table.find(
            (to_remove) => to_remove.id === element.id
          )
      );
    },
    save() {
      let selected_foods_id = [];
      this.selected_foods.forEach((item) => {
        selected_foods_id.push(item.id);
      });
      this.$store.dispatch("saveDishIntoDB", {
        title: this.dish.title,
        meal_id: this.dish.meal_id,
        foods: selected_foods_id,
      });
      this.cleanup();
    },
  },
  mounted() {
    this.$store.dispatch("getFoodTypes");
  },
};
</script>
