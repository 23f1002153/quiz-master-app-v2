<template>
  <!--
    This is the main container for the chapter details view.
    It uses a v-if to check if a chapter has been selected. If not, it shows a placeholder message.
  -->
  <div v-if="selectedChapter" class="chapter-details-container p-4">
    <!-- Chapter Title and Description -->
    <div class="text-center mb-4">
      <h1 class="fw-bold mb-0">{{ selectedChapter.name }}</h1>
    </div>
    <div class="mb-5">
      <strong class="fs-4">About the chapter:</strong>
      <p class="fs-5 text-muted">{{ selectedChapter.description }}</p>
    </div>

    <div>
      <h2 class="fw-bold">Quizzes:</h2>

      <!--
        This filter bar is now responsive.
        - 'flex-column': On mobile, the filter items will stack vertically.
        - 'flex-lg-row': On large screens (desktops), they will switch back to a horizontal row.
        - 'align-items-stretch': Ensures all items stretch to the same height in the column layout.
        - 'align-items-lg-center': Vertically centers items when in the row layout.
      -->
      <div class="quiz-filter-bar d-flex flex-column flex-lg-row align-items-stretch align-items-lg-center p-3 bg-light rounded-2 border my-3">
        <!-- Search Bar -->
        <div class="input-group me-lg-3 mb-2 mb-lg-0 flex-grow-1">
          <span class="input-group-text bg-white"><i class="bi bi-search"></i></span>
          <input v-model="name" type="search" class="form-control" placeholder="Search quizzes by name...">
        </div>

        <!-- Status Dropdown -->
        <div class="me-lg-3 mb-2 mb-lg-0">
          <select v-model="type" class="form-select" aria-label="Filter by completion status">
            <option value="All">All Statuses</option>
            <option value="upcoming">Upcoming</option>
            <option value="completed">Completed</option>
            <option value="not_done">Not Done</option>
            <option value="ongoing">Ongoing</option>
          </select>
        </div>

        <!-- Score Range Filter -->
        <div class="filter-group d-flex align-items-center me-lg-3 mb-2 mb-lg-0">
          <label for="min-score" class="form-label me-2 mb-0 fw-bold">Score:</label>
          <input v-model="score_min" type="number" id="min-score" class="form-control range-input" placeholder="Min">
          <span class="mx-1">-</span>
          <input v-model="score_max" type="number" id="max-score" class="form-control range-input" placeholder="Max">
        </div>

        <!-- Duration Range Filter -->
        <div class="filter-group d-flex align-items-center">
          <label for="min-duration" class="form-label me-2 mb-0 fw-bold">Length:</label>
          <input v-model="length_min" type="number" id="min-duration" class="form-control range-input" placeholder="Mins">
          <span class="mx-1">-</span>
          <input v-model="length_max" type="number" id="max-duration" class="form-control range-input" placeholder="Mins">
        </div>
      </div>

      <!-- Quiz List -->
      <div v-if="!loadingQuizzes">
        <!-- This container makes the list of quizzes scrollable if it gets too long. -->
        <div class="quiz-list-wrapper">
          <div v-if="filteredQuizzes.length > 0">
            <div v-for="quiz in filteredQuizzes" :key="quiz.id">
              <QuizCard :quiz="quiz" />
            </div>
          </div>
          <!-- This message is shown if the filters result in no matching quizzes. -->
          <div v-else class="text-center text-muted p-5">
            <h4>No Quizzes Found</h4>
            <p>Try adjusting your filter criteria.</p>
          </div>
        </div>
      </div>
      <!-- This message is shown while the quizzes are being loaded from the API. -->
      <div v-else class="text-center text-muted p-5">
        <div class="spinner-border" role="status"></div>
        <p class="mt-2">Loading Quizzes...</p>
      </div>
    </div>
  </div>

  <!-- This placeholder is shown if no chapter has been selected yet. -->
  <div v-else class="canvas-placeholder">
    <h1>Select a chapter to check out the Quizzes</h1>
  </div>
</template>

<script setup>
import { useChapterStore } from '@/stores/chapterStore';
import { storeToRefs } from 'pinia';
import QuizCard from '@/components/subject/QuizCard.vue';
import { ref, computed } from 'vue';

// Initialize the Pinia store for chapters.
const chapterStore = useChapterStore();

// Make state properties from the store reactive.
const { selectedChapter, quizzes, loadingQuizzes } = storeToRefs(chapterStore);

// Refs to hold the current values from the filter inputs.
const name = ref('');
const score_min = ref(null); // Use null for empty number inputs
const score_max = ref(null);
const length_min = ref(null);
const length_max = ref(null);
const type = ref('All');

// This computed property filters the list of quizzes in real-time based on the filter inputs.
const filteredQuizzes = computed(() => {
  return quizzes.value.filter(quiz => {
    // Name Filter: Checks if the quiz name includes the search text.
    const nameMatch = quiz.name.toLowerCase().includes(name.value.toLowerCase());

    // Status Filter: Checks if the quiz status matches the selected type.
    // Corrected this line to use the 'type.value' from the filter.
    const criteriaMatch = (type.value === 'All' || quiz.status === type.value);

    // Score Filter: Checks if the quiz score is within the min/max range.
    // It safely handles cases where min/max are not set.
    const scoreMatch =
      (score_min.value === null || quiz.score >= score_min.value) &&
      (score_max.value === null || quiz.score <= score_max.value);

    // Length Filter: Checks if the quiz duration is within the min/max range.
    const lengthMatch =
      (length_min.value === null || quiz.duration >= length_min.value) &&
      (length_max.value === null || quiz.duration <= length_max.value);

    // A quiz is only included if it matches ALL the filter conditions.
    return nameMatch && criteriaMatch && scoreMatch && lengthMatch;
  });
});
</script>

<style scoped>
/* Styles for the main container of this view. */
.chapter-details-container {
  width: 100%;
}

/* Styles for the placeholder message shown when no chapter is selected. */
.canvas-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: #6c757d;
  width: 100%;
  height: 100%;
}

/* Styles for the filter bar. */
.quiz-filter-bar .form-label {
  white-space: nowrap; /* Prevents labels like "Score:" from wrapping */
}
.quiz-filter-bar .range-input {
  width: 85px; /* Keeps the min/max input fields compact */
}

/* Hides the arrows on number inputs for a cleaner look in some browsers. */
.quiz-filter-bar input[type=number]::-webkit-inner-spin-button,
.quiz-filter-bar input[type=number]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

/* Styles for the scrollable list of quizzes. */
.quiz-list-wrapper {
  max-height: 60vh;
  overflow-y: auto;
  padding-right: 10px; /* Adds some space for the scrollbar */
}
</style>
