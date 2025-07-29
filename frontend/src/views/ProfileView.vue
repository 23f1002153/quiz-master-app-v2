<template>
  <div class="user-profile-light-page">
    <div class="container py-5" v-if="profile">

      <TopSection :level="level" :profile="profile" :levelXP="levelXP"/>

      <div class="row g-4 text-center mb-5">
        <ProfileStatCards :daysSince="daysSince" :totalXP="totalXP" :quizzesCompleted="quizzesCompleted"/>
      </div>

      <div class="row g-4">

        <div class="col-lg-8">
          <AboutMe :editingProfile="editingProfile" @toggle="toggleEdit" />
        </div>

        <div class="col-lg-4 h-50">
          <SettingsCard @switch="editingProfile = !editingProfile" :editingProfile="editingProfile" />
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>

import { onMounted, ref } from 'vue';
import { useProfileStore } from '@/stores/profileStore';
import { storeToRefs } from 'pinia';
import AboutMe from '@/components/profile/AboutMe.vue';
import TopSection from '@/components/profile/TopSection.vue';
import ProfileStatCards from '@/components/profile/ProfileStatCards.vue';
import SettingsCard from '@/components/profile/SettingsCard.vue';

const profileStore = useProfileStore();
const { profile, quizzesCompleted,  daysSince, totalXP, level, levelXP } = storeToRefs(profileStore);

const editingProfile = ref(false);

const toggleEdit = () => {
  editingProfile.value = !editingProfile.value;
}

onMounted(() => {
  profileStore.fetchProfile();
});

</script>

<style scoped>
.user-profile-light-page {
  background-color: #f8f9fa; /* Light grey background */
  color: #212529; /* Standard dark text */
  min-height: 100vh;
  font-family: 'null, 'Roboto', sans-serif';
}
</style>
