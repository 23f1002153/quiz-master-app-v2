<template>
  <!--
    This form is used to edit the user's profile details.
    The '@submit.prevent' modifier stops the default browser behavior of reloading the page
    when the form is submitted, allowing our 'save_and_reload' function to handle it instead.
  -->
  <form @submit.prevent="save_and_reload">
    <!--
      We use Bootstrap's grid system ('row' and 'col-md-6') to make the layout responsive.
      On medium screens (md) and larger, the fields will appear in two columns.
      On smaller screens (like mobile), they will automatically stack into a single column.
    -->
    <div class="row mt-3">
      <div class="col-md-6">
        <div class="mb-3">
          <label for="edit-email" class="form-label fw-bold">Email</label>
          <input type="email" class="form-control" id="edit-email" v-model="newProfile.email">
        </div>
      </div>
      <div class="col-md-6">
        <div class="mb-3">
          <label for="edit-phone" class="form-label fw-bold">Phone No.</label>
          <input
            type="tel"
            class="form-control"
            id="edit-phone"
            v-model="newProfile.phone"
            inputmode="numeric"
            @input="newProfile.phone = newProfile.phone.replace(/[^0-9]/g, '')"
          >
          <!-- This validation message only appears if the phone number is not 10 digits -->
          <small v-if="!validPhone" class="text-danger">Please enter a valid 10-digit phone number</small>
        </div>
      </div>
    </div>

    <div class="row">
      <div class="col-md-6">
        <div class="mb-3">
          <label for="edit-gender" class="form-label fw-bold">Gender</label>
          <select class="form-select" id="edit-gender" v-model="newProfile.gender">
            <option>Male</option>
            <option>Female</option>
            <option>Other</option>
          </select>
        </div>
      </div>
      <div class="col-md-6">
        <div class="mb-3">
          <label for="edit-dob" class="form-label fw-bold">Date of Birth</label>
          <!-- The 'max' attribute prevents users from selecting a future date -->
          <input type="date" class="form-control" id="edit-dob" v-model="newProfile.dob" :max="today">
        </div>
      </div>
    </div>

    <div class="row">
      <div class="col-md-6">
        <div class="mb-3">
          <label for="edit-qualification" class="form-label fw-bold">Qualification</label>
          <input type="text" class="form-control" id="edit-qualification" v-model="newProfile.qualification">
        </div>
      </div>
      <div class="col-md-6">
        <div class="mb-3">
          <label for="edit-college" class="form-label fw-bold">College</label>
          <input type="text" class="form-control" id="edit-college" v-model="newProfile.college">
        </div>
      </div>
    </div>

    <!-- Form Action Buttons -->
    <div class="mt-4">
      <button type="submit" class="btn btn-primary btn-lg">
        Save Changes
      </button>
      <!--
        When the user clicks "Cancel", we don't submit the form.
        Instead, we just emit the 'toggle' event to tell the parent component
        to switch back to the display view.
      -->
      <button type="button" class="btn btn-secondary btn-lg mx-3" @click="emit('toggle')">
        Cancel
      </button>
    </div>

    <!-- This div is used to display any error messages from the store -->
    <div v-if="errorType" class="text-center mb-0 mt-4">
      <p class="text-danger fs-6">{{ errorType }}</p>
    </div>
  </form>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useProfileStore } from '@/stores/profileStore';
import { storeToRefs } from 'pinia';

// This defines the 'toggle' event that this component can send to its parent.
const emit = defineEmits(['toggle']);

// Initialize the Pinia store.
const profileStore = useProfileStore();

// Make the 'profile' and 'errorType' state from the store reactive.
const { profile, errorType } = storeToRefs(profileStore);

// This computed property validates the phone number in real-time.
const validPhone = computed(() => /^\d{10}$/.test(newProfile.value.phone) || !newProfile.value.phone);

// This computed property gets today's date in YYYY-MM-DD format for the date picker.
const today = computed(() => new Date().toISOString().split('T')[0]);

// This 'ref' will hold a copy of the profile data for editing,
// so we don't modify the original data in the store directly.
const newProfile = ref({});

// The 'onMounted' hook runs when the component is first created.
// We use it to pre-fill the form with the user's current profile data.
onMounted(() => {
  newProfile.value = { ...profile.value };
});

// This function is called when the form is submitted.
const save_and_reload = async () => {
  try {
    // Call the 'editProfile' action in our Pinia store.
    await profileStore.editProfile(newProfile.value);
    // If the save is successful, emit the 'toggle' event to switch the view.
    emit('toggle');
    alert("Profile Edited Successfully!");
  } catch (error) {
    // If the store action throws an error, it will be caught here.
    // The 'errorType' from the store will be displayed in the template.
    console.log(error);
  }
};
</script>

<style scoped>
/* No custom styles are needed for this component as Bootstrap handles the layout and styling. */
</style>
