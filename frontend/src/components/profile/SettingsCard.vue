<template>
  <div class="details-card card h-100">
    <div class="card-body p-4 d-flex flex-column">
      <h3 class="card-title-alt"><i class="bi bi-gear-wide-connected me-2"></i>Settings</h3>
      <p class="text-muted">Manage your profile information and account security.</p>
      <div class="mt-auto">
        <div class="d-grid mb-2">
          <button class="btn btn-primary btn-lg" @click="$emit('switch')" v-if="!props.editingProfile">
            Edit Profile
          </button>
        </div>
        <div class="text-center">
          <a href="#" class="text-secondary small">Change Password</a>
        </div>
      </div>
    </div>
  </div>

</template>

<script setup>

defineEmits(['switch'])
const props = defineProps(['editingProfile'])

</script>

<style scoped>
/* Details & Settings Cards */
.details-card {
  background-color: #ffffff;
  border: 1px solid #e9ecef;
  border-radius: 0.75rem;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}
.card-title-alt { font-weight: 600; color: #212529; }
.details-card dl { display: grid; grid-template-columns: 150px 1fr; gap: 0.75rem; }
.details-card dt { color: #6c757d; }
.details-card dd { color: #212529; font-weight: 600; }

</style>
