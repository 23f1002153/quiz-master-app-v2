<template>
  <!--
    This is the main header for the user's profile page.
    It uses Bootstrap's flexbox utilities ('d-flex', 'align-items-center', 'justify-content-between')
    to create a responsive layout. On small screens, the elements will stack gracefully if needed,
    and on larger screens, they will sit side-by-side.
  -->
  <header class="player-header">
    <div class="d-flex align-items-center">
      <img src="https://placehold.co/120x120/333/FFF?text=AVATAR" alt="User Avatar" class="player-avatar"/>
      <div class="player-info ms-4">
        <h1 class="player-name">{{ props.profile.username }}</h1>
        <p class="player-joined text-muted">Member Since: {{ props.profile.joiningDate }}</p>
      </div>
    </div>
    <div class="player-level-info">
      <div class="level-badge">
        <span class="level-text">LEVEL</span>
        <span class="level-number">{{ props.level + 1 }}</span>
      </div>
    </div>
  </header>

  <!-- This wrapper contains the XP bar and its labels. -->
  <div class="xp-bar-wrapper my-4">
    <div class="d-flex justify-content-between mb-1 text-secondary">
      <span class="fw-bold">XP Progress</span>
      <span class="fw-bold">{{ props.levelXP }}/100 XP</span>
    </div>
    <!-- The progress bar component from Bootstrap, used to visually represent the user's XP. -->
    <div class="progress" role="progressbar" :aria-valuenow="props.levelXP" aria-valuemin="0" aria-valuemax="100">
      <div class="progress-bar xp-bar" :style="{ width: props.levelXP + '%' }"></div>
    </div>
  </div>
</template>

<script setup>
// This defines the properties (props) that this component receives from its parent.
// It expects to get the user's level, XP, and their full profile object.
const props = defineProps(['level', 'levelXP', 'profile']);
</script>

<style scoped>
/* These styles are "scoped", meaning they only apply to this component.
*/

/* Styles for the main header container. */
.player-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* Styles for the user's circular avatar image. */
.player-avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  border: 4px solid #ffffff;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

/* Styles for the user's name. */
.player-name {
  font-size: 2.5rem;
  font-weight: 700;
}

/* Styles for the circular level badge. */
.level-badge {
  background: linear-gradient(145deg, #0d6efd, #0b5ed7);
  color: white;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 4px solid #fff;
  box-shadow: 0 0 15px rgba(0, 123, 255, 0.4);
}

/* Styles for the "LEVEL" text inside the badge. */
.level-text {
  font-size: 0.8rem;
  font-weight: 600;
}

/* Styles for the large level number inside the badge. */
.level-number {
  font-size: 2.5rem;
  font-weight: 700;
  line-height: 1; /* Improves vertical alignment. */
}

/* Styles for the outer container of the progress bar. */
.xp-bar-wrapper .progress {
  height: 20px;
  background-color: #e9ecef;
  border-radius: 10px;
  padding: 3px;
}

/* Styles for the inner, colored part of the XP bar. */
.xp-bar {
  background: linear-gradient(90deg, #0d6efd, #3c8ffb);
  border-radius: 7px;
}
</style>
