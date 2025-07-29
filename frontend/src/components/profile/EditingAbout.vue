<template>
  <form @submit.prevent = "save_and_reload">
    <div class="mb-3">
      <label for="edit-email" class="form-label fw-bold">Email</label>
      <input type="email" class="form-control" id="edit-email" v-model="newProfile.email" :placeholder="profile.email">
    </div>
    <div class="mb-3">
      <label for="edit-phone" class="form-label fw-bold">Phone No.</label>
      <input
        type="tel"
        class="form-control"
        id="edit-phone"
        v-model="newProfile.phone"
        inputmode="numeric"
        @input="newProfile.phone = newProfile.phone.replace(/[^0-9]/g, '')"
        :placeholder="profile.phone"
      >
      <small v-if="!validPhone" class="text-danger">Please enter a valid phone number</small>
    </div>
    <div class="mb-3">
      <label for="edit-gender" class="form-label fw-bold">Gender</label>
      <select class="form-select" id="edit-gender" v-model="newProfile.gender" :placeholder="profile.gender">
        <option>Male</option>
        <option>Female</option>
        <option>Other</option>
      </select>
    </div>
    <div class="mb-3">
      <label for="edit-dob" class="form-label fw-bold">Date of Birth</label>
      <input type="date" class="form-control" id="edit-dob" v-model="newProfile.dob" :max="today">
    </div>
    <div class="mb-3">
      <label for="edit-qualification" class="form-label fw-bold">Qualification</label>
      <input type="text" class="form-control" id="edit-qualification" v-model="newProfile.qualification" :placeholder="profile.qualification">
    </div>
    <div class="mb-3">
      <label for="edit-college" class="form-label fw-bold">College</label>
      <input type="text" class="form-control" id="edit-college" v-model="newProfile.college" :placeholder="profile.college">
    </div>
    <button class="btn btn-primary btn-lg">
      Edit Profile
    </button>
    <button class="btn btn-success btn-lg mx-4" @click="emit('toggle')">
      Cancel
    </button>
  </form>
  <div class="text-center mb-0 mt-4">
    <p class="text-danger fs-6">{{ errorType }}</p>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useProfileStore } from '@/stores/profileStore';
import { storeToRefs } from 'pinia';
import { defineEmits } from 'vue';

const emit = defineEmits(['toggle']);

const profileStore = useProfileStore();
const { profile, errorType } = storeToRefs(profileStore);

const validPhone = computed(() => /^\d{10}$/.test(newProfile.value.phone) || !newProfile.value.phone);
const today = new Date().toISOString().split('T')[0];

const newProfile = ref({
  'email': null,
  'phone': null,
  'gender': null,
  'dob': null,
  'qualification': null,
  'college': null
});

const save_and_reload = async () => {
  try{
    await profileStore.editProfile(newProfile.value);
    emit('toggle');
    alert("Profile Edited Successfully!");
  }
  catch (error) {
    console.log(error);
  }
}



</script>
