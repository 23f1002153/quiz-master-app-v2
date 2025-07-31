<template>
  <!--
    This 'row' class is from Bootstrap. It creates a flexbox container
    that allows the 'col-md-4' classes inside your ProfileCard component
    to work correctly, placing them side-by-side on larger screens.
  -->
  <div class="row g-4">
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
  </div>
</template>

<script setup>
import ProfileCard from '@/components/profile/ProfileCard.vue'

const props = defineProps(['quizzesCompleted', 'daysSince', 'totalXP'])
</script>
