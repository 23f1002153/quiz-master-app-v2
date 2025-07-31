<template>
  <nav class="navbar navbar-expand-lg bg-dark-subtle px-4 py-0">
    <div class="container-fluid d-flex justify-content-between align-items-center">
      <!-- Left: Logo -->
      <div class="me-auto">
        <span class="fw-bold">QUIZMASTER</span>
      </div>

      <!-- Center: Nav Items -->
      <div class="d-none d-lg-flex mx-auto" id="navbarNav">
        <ul class="navbar-nav">
          <NavItem :to="{ name: 'admin_dashboard' }">Dashboard</NavItem>
          <NavItem :to="{ name: 'admin_subjects' }">Classroom</NavItem>
          <NavItem :to="{ name: 'admin_users' }">Users</NavItem>
          <NavItem :to="{ name: 'admin_stats' }">Results</NavItem>
        </ul>
      </div>

      <!-- Right: Profile -->
      <div class="ms-auto">
        <button class="btn btn-dark" @click="logout">Logout</button>
      </div>

    </div>
  </nav>
</template>

<script setup>
import NavItem from '@/components/nav/NavItem.vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const logout = () => {
  if (window.confirm("Are you sure you want to logout?")) {
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    router.push('/login');
  }
};


</script>
