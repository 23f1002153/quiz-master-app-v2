<template>
  <!--
    This is a definition list that displays the user's profile information.
    The 'profile-details-list' class is used to apply our custom responsive styles.
  -->
  <dl class="profile-details-list">
    <dt>Email</dt>
    <dd>{{ profile.email }}</dd>

    <dt>Phone No.</dt>
    <dd>{{ profile.phone }}</dd>

    <dt>Gender</dt>
    <dd>{{ profile.gender }}</dd>

    <dt>Date of Birth</dt>
    <dd>{{ profile.dob }}</dd>

    <dt>Qualification</dt>
    <dd>{{ profile.qualification }}</dd>

    <dt>College</dt>
    <dd>{{ profile.college }}</dd>
  </dl>
</template>

<script setup>
// We're using Pinia for state management.
import { useProfileStore } from '@/stores/profileStore';
import { storeToRefs } from 'pinia';

// This creates an instance of our profile store.
const profileStore = useProfileStore();

// 'storeToRefs' makes the state properties (like 'profile') reactive,
// so the component will automatically update if the data in the store changes.
const { profile } = storeToRefs(profileStore);
</script>

<style scoped>
/* These styles are "scoped", meaning they only apply to this component.
*/

/* By default (for desktop screens), we use a CSS grid to create a clean,
  two-column layout. The first column is for the labels (dt) and the
  second is for the data (dd).
*/
.profile-details-list {
  display: grid;
  grid-template-columns: 150px 1fr; /* First column is 150px wide, second takes the rest. */
  gap: 1rem 0.75rem; /* Adds some space between rows and columns. */
  margin-top: 1.5rem; /* Adds some space below the card title. */
}

/* Styles for the term/label (e.g., "Email"). */
.profile-details-list dt {
  font-weight: 500;
  color: #6c757d;
}

/* Styles for the definition/data (e.g., "user@example.com"). */
.profile-details-list dd {
  font-weight: 600;
  color: #212529;
  margin: 0;
}

/* This is a media query for responsiveness.
  These styles will ONLY apply on screens that are 768px wide or smaller (like mobile phones).
*/
@media (max-width: 768px) {
  .profile-details-list {
    /* We switch the grid to a single column for a better vertical layout on small screens. */
    grid-template-columns: 1fr;
    gap: 0.25rem; /* Reduce the gap between items for a more compact look. */
  }

  /* On mobile, we make the label bold and add some space below it to clearly separate it
     from the data that now appears on the next line.
  */
  .profile-details-list dt {
    font-weight: 700;
    margin-top: 0.75rem;
  }
}
</style>
