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
          <NavItem :to="{ name: 'guest_home' }">Home</NavItem>
          <NavItem :to="{ name: 'login' }">Login</NavItem>
          <NavItem :to="{ name: 'signup' }">Register</NavItem>
        </ul>
      </div>

      <!-- Right: Profile -->
      <div class="ms-auto">
      </div>

    </div>
  </nav>
</template>

<script setup>
import NavItem from '@/components/nav/NavItem.vue';
</script>
