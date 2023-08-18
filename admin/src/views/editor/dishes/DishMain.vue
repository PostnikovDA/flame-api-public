<template>
  <div>
    <AddDishForm/>
    <!-- <DishesTable/> -->
    <DishTable/>
  </div>
</template>

<script>
import AddDishForm from "@/components/Dish/AddDishForm.vue";
import DishTable from "@/components/Dish/DishTable.vue";
// import FoodsTable from "@/components/Dish/FoodsTable.vue";
// import { mapGetters } from "vuex";

export default {
  components: { 
    AddDishForm, 
    DishTable, 
    // FoodsTable 
  },
  data: () => ({}),
  computed: {},
  methods: {},
  mounted() {},
};
</script>
