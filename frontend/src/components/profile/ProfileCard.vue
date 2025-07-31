<template>
  <!--
    This component is designed to be a reusable "widget" within a Bootstrap grid.
    - 'col-12': On extra-small screens (like mobile phones), this card will take up the full 12-column width.
    - 'col-md-4': On medium screens (like tablets and desktops) and larger, it will take up 4 of the 12 columns,
      allowing three of these cards to fit side-by-side in a row.
  -->
  <div class="col-12 col-md-4">
    <div class="stat-card">
      <!-- The icon provides a visual cue for the type of statistic being displayed. -->
      <i class="bi bi-joystick stat-icon"></i>

      <!--
        This is a "named slot". It acts as a placeholder.
        When you use this component, you can inject any content you want into this specific spot.
        This slot is intended for the main statistic value (e.g., "85", "120").
      -->
      <span class="stat-value">
        <slot name="stat"></slot>
      </span>

      <!--
        This is another named slot, intended for the descriptive label
        that explains what the statistic represents (e.g., "Quizzes Completed").
      -->
      <span class="stat-label">
        <slot name="content"></slot>
      </span>
    </div>
  </div>
</template>

<script setup>
// This component is purely for presentation, so no JavaScript logic is needed.
// It receives all its content through slots from the parent component.
</script>

<style scoped>
/* These styles are "scoped", meaning they only apply to this StatCard component.
*/

/* Styles for the main card container. */
.stat-card {
  background-color: #ffffff;
  padding: 1.5rem;
  border-radius: 0.75rem;
  /* Flexbox is used to easily center the content vertically and horizontally. */
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem; /* Adds a small space between the icon, value, and label. */
  border: 1px solid #e9ecef;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  height: 100%; /* Ensures all cards in a row have the same height. */
}

/* Styles for the icon at the top of the card. */
.stat-icon {
  font-size: 2.5rem;
  color: var(--bs-primary);
}

/* Styles for the large number (the main statistic). */
.stat-value {
  font-size: 2.25rem;
  font-weight: 700;
}

/* Styles for the small descriptive text at the bottom. */
.stat-label {
  font-size: 1rem;
  color: #6c757d;
}
</style>
