<!-- NavItem.vue -->
<template>
  <RouterLink
    :to="to"
    class="nav-link"
    active-class="active"
  >
    <slot />
  </RouterLink>
</template>

<script setup>

import { RouterLink } from 'vue-router';

defineProps({
  to: { type: Object, required: true }
});
</script>

<style scoped>
.nav-link {
  padding: 0.5rem 1rem;
  color: #333;
  text-decoration: none;
  font-size: 1.2rem;
  margin-left: 1rem;
  /* transition: all 0.1s ease-in-out; */
}

.nav-link:hover {
  color: #0056b3;
  background-color: #e7f1ff;
  border-radius: 0.25rem;
}

.nav-link.active {
  font-size: 1.4rem;
  font-weight: bold;
  color: #0d6efd;           /* Bootstrap primary */
  border-bottom: 5px solid #0d6efd;
}

</style>
