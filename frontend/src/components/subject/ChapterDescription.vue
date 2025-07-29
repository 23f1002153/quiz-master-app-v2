<template>
  <div v-if="selectedChapter" class="w-100 p-4">
    <div class="d-flex justify-content-center align-items-center mb-4">
      <h1 class="fw-bold mb-0">{{ selectedChapter.name }}</h1>
    </div>

    <div class="mx-5 mb-5">
      <strong class="fs-3"> About the chapter: </strong>
      <p class="fw-normal fs-5"> {{ selectedChapter.description }}</p>
    </div>

    <div class="mx-5">

      <h2 class="fw-bold">Quizzes:</h2>

      <div class="quiz-filter-bar d-flex align-items-center p-3 bg-light rounded-2 border my-2">
        <div class="input-group me-3 flex-grow-1">
          <span class="input-group-text bg-white"><i class="bi bi-search"></i></span>
          <input v-model="name" type="search" class="form-control" placeholder="Search quizzes by name...">
        </div>

        <div class="me-3">
          <select v-model="type" class="form-select" aria-label="Filter by completion status">
            <option selected>All</option>
            <option value="upcoming">Upcoming</option>
            <option value="completed">Completed</option>
            <option value="not_done">Not Done</option>
            <option value="ongoing">Ongoing</option>
          </select>
        </div>

        <div class="filter-group d-flex align-items-center me-3">
          <label for="min-score" class="form-label me-2 mb-0 fw-bold">Score:</label>
          <input v-model="score_min" type="number" id="min-score" class="form-control range-input" placeholder="Min">
          <span class="mx-1">-</span>
          <input v-model="score_max" type="number" id="max-score" class="form-control range-input" placeholder="Max">
        </div>

        <div class="filter-group d-flex align-items-center">
          <label for="min-duration" class="form-label me-2 mb-0 fw-bold">Length:</label>
          <input v-model="length_min" type="number" id="min-duration" class="form-control range-input" placeholder="Mins">
          <span class="mx-1">-</span>
          <input v-model="length_max" type="number" id="max-duration" class="form-control range-input" placeholder="Mins">
        </div>
      </div>

      <div v-if="!loadingQuizzes">
        <div style="max-height: 60vh; overflow-y: auto">
          <div v-if="filteredQuizzes.length > 0">
            <div v-for="quiz in filteredQuizzes" :key="quiz.id">
              <QuizCard :quiz=quiz />
            </div>
          </div>
          <div v-else>
            No Quizzes
          </div>
        </div>
      </div>
      <div v-else>
        Loading Quizzes
      </div>
    </div>
  </div>

  <div v-else class="text-center text-muted py-4 w-100">
    <h1>Select a chapter to check out the Quizzes</h1>
  </div>
</template>

<script setup>
import { useChapterStore } from '@/stores/chapterStore';
import { storeToRefs } from 'pinia';
import QuizCard from '@/components/subject/QuizCard.vue';
import { ref, computed } from 'vue';

const chapterStore = useChapterStore();
const { selectedChapter, quizzes, loadingQuizzes } = storeToRefs(chapterStore);

const name = ref('');
const score_min = ref(0);
const score_max = ref(100);
const length_min = ref(0);
const length_max = ref(10000000);
const type = ref('All');

const filteredQuizzes = computed(() => {
  return quizzes.value.filter(
    quiz => {
      // A quiz must satisfy ALL of the following conditions to be returned.

      // 1. Name Filter: Check if the quiz name contains the search string (case-insensitive).
      const nameMatch = quiz.name.toLowerCase().includes(name.value.toLowerCase());

      // 2. Criteria Filter: Check the quiz status. If 'All' is selected, this condition passes.
      const criteriaMatch = (type.value === 'All' || quiz.status === 'criteria');

      // 3. Score Filter: Check if the quiz score is within the min/max range.
      // This assumes quizzes have a 'score' property (e.g., 0 or null for un-attempted quizzes).
      // const scoreMatch = quiz.score >= score_min.value && quiz.score <= score_max.value;
      const scoreMatch = 1;

      // 4. Length Filter: Check if the quiz length (duration in mins) is within the min/max range.
      const lengthMatch = quiz.duration >= length_min.value && quiz.duration <= length_max.value;

      return nameMatch && criteriaMatch && scoreMatch && lengthMatch;
  });
})

</script>
