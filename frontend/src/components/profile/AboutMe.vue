<template>
  <!--
    This is the main container for the "About Me" section.
    We use Bootstrap's grid system here. The 'row' class sets up the grid,
    and 'col-12' ensures this component takes up the full width of its parent
    on all screen sizes, from mobile to desktop.
  -->
  <div class="row g-4">
    <div class="col-12">
      <div class="details-card card h-100">
        <div class="card-body p-4">

          <!-- Card Title -->
          <h3 class="card-title-alt">
            <i class="bi bi-person-circle me-2"></i>About Me
          </h3>

          <!--
            This is where the magic happens.
            The v-if directive checks the 'editingProfile' prop passed down from the parent.
            If it's false, it shows the DefaultAbout component.
            If it's true, it shows the EditingAbout component instead.
          -->

          <!-- Display Mode -->
          <div v-if="!props.editingProfile">
            <DefaultAbout />
          </div>

          <!-- Editing Mode -->
          <div v-else>
            <!--
              When the user finishes editing and clicks "Save" or "Cancel"
              inside the EditingAbout component, it will emit a 'toggle' event.
              We listen for that event here and pass it up to the parent component
              to tell it to switch back to the display mode.
            -->
            <EditingAbout @toggle="emit('toggle')" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// We're importing the two child components that this component will switch between.
import DefaultAbout from '@/components/profile/DefaultAbout.vue';
import EditingAbout from '@/components/profile/EditingAbout.vue';

// This defines the properties (props) that this component accepts from its parent.
// 'editingProfile' is a boolean that tells us whether to show the display view or the edit form.
const props = defineProps(['editingProfile']);

// This defines the custom events that this component can send (emit) up to its parent.
// We use 'toggle' to signal that the view should be switched.
const emit = defineEmits(['toggle']);
</script>

<style scoped>
/* These styles are "scoped", meaning they will only apply to this component
  and won't interfere with the styling of other parts of your application.
*/

/* Styles for the main card that holds the profile information. */
.details-card {
  background-color: #ffffff;
  border: 1px solid #e9ecef;
  border-radius: 0.75rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
}

/* Styles for the title inside the card. */
.card-title-alt {
  font-weight: 600;
  color: #212529;
}

/* This creates a two-column layout for the definition list (dl) used in the DefaultAbout component.
  The first column (dt) is sized to fit its content, and the second column (dd) takes the rest of the space.
*/
.details-card dl {
  display: grid;
  grid-template-columns: 150px 1fr;
  gap: 0.75rem;
}

/* Styles for the term (e.g., "Email") in the definition list. */
.details-card dt {
  color: #6c757d;
}

/* Styles for the definition (e.g., "user@example.com") in the list. */
.details-card dd {
  color: #212529;
  font-weight: 600;
}
</style>
