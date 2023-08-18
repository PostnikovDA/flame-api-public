<template>
    <v-progress-linear v-if="overlay" indeterminate color="blue" :height="6"></v-progress-linear>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "Progress",
  computed: {
    ...mapGetters({
      overlay: "overlayStatus",
    }),
  },
};
</script>

<style>
</style>