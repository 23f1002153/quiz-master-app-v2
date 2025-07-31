
<template>
    <div class="wrapper">
      <component :is="navbarComponent" v-if="navbarComponent"/>
    </div>

  <RouterView :key="$route.fullPath" />
</template>

<script setup>
import UserNavBar from '@/components/nav/UserNavBar.vue';
import AdminNavBar from '@/components/nav/AdminNavBar.vue';
import GuestNavBar from '@/components/nav/GuestNavBar.vue';

import { onMounted, ref, computed } from 'vue';

const role = ref(null);

onMounted(() => {
  role.value = localStorage.getItem('role');
})

const navbarComponent = computed(() => {
  if (role.value === 'admin') return AdminNavBar;
  if (role.value === 'user') return UserNavBar;
  return GuestNavBar; // fallback
});


</script>
