<template>
  <div class="row g-4">
    <div class="details-card card h-100">
      <div class="card-body p-4">

        <h3 class="card-title-alt"><i class="bi bi-person-circle me-2"></i>About Me</h3>

        <!-- Default Mode -->
        <div v-if="!props.editingProfile">
          <DefaultAbout/>
        </div>

        <!-- Editing Mode -->
        <div v-else>
          <EditingAbout @toggle="emit('toggle')"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import DefaultAbout from '@/components/profile/DefaultAbout.vue';
import EditingAbout from '@/components/profile/EditingAbout.vue';

const props = defineProps(['editingProfile'])
const emit = defineEmits(['toggle'])

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
