<template>
  <ProfileCard>
    <template #stat>{{ props.quizzesCompleted }}</template>
    <template #content>Quizzes Completed</template>
  </ProfileCard>
  <ProfileCard>
    <template #stat>{{ props.daysSince }}</template>
    <template #content>Days Active</template>
  </ProfileCard>
  <ProfileCard>
    <template #stat>{{ props.totalXP }}</template>
    <template #content>Total XP Earned</template>
  </ProfileCard>
</template>

<script setup>
import ProfileCard from '@/components/profile/ProfileCard.vue'

const props = defineProps(['quizzesCompleted', 'daysSince', 'totalXP'])
</script>


