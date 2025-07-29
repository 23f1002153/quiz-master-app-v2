<template>
  <div class="col-md-4">
    <div class="stat-card">
      <i class="bi bi-joystick stat-icon"></i>
      <span class="stat-value"><slot name="stat"></slot></span>
      <span class="stat-label"><slot name="content"></slot></span>
    </div>
  </div>
</template>

<style scoped>
/* Stat Cards */
.stat-card {
  background-color: #ffffff;
  padding: 1.5rem;
  border-radius: 0.75rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  border: 1px solid #e9ecef;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}
.stat-icon { font-size: 2.5rem; color: var(--bs-primary); }
.stat-value { font-size: 2.25rem; font-weight: 700; }
.stat-label { font-size: 1rem; color: #6c757d; }

</style>
