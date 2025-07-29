<template>
  <dl>
    <dt>Email</dt><dd>{{ profile.email }}</dd>
    <dt>Phone No.</dt><dd>{{ profile.phone }}</dd>
    <dt>Gender</dt><dd>{{ profile.gender }}</dd>
    <dt>Date of Birth</dt><dd>{{ profile.dob }}</dd>
    <dt>Qualification</dt><dd>{{ profile.qualification }}</dd>
    <dt>College</dt><dd>{{ profile.college }}</dd>
  </dl>
</template>

<script setup>

import { useProfileStore } from '@/stores/profileStore';
import { storeToRefs } from 'pinia';

const profileStore = useProfileStore();
const { profile } = storeToRefs(profileStore);

</script>
