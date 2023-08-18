<template>
  <!-- <v-container>
    <v-row no-gutters>
      <v-col v-for="food_type in food_types" :key="food_type.group_id" lg="3">
        <v-card class="mx-auto" max-width="344" outlined>
          <v-list-item two-line>
            <v-list-item-content>
              <v-list-item-title class="headline mb-1">{{food_type.title}}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn text v-on:click="moveToFood(food_type.group_id)">Открыть</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>-->
  <FoodTable />
</template>

<script>
import FoodTable from "@/components/Food/FoodTable.vue";

export default {
  components: { FoodTable },
  
};
</script>