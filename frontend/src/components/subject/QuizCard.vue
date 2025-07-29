<template>
  <div class="quiz-card card mb-4">
    <div class="card-body p-4">
      <div class="d-flex justify-content-between align-items-start mb-3">
        <h2 class="quiz-title mb-0">{{ props.quiz.name }}</h2>
        <span class="quiz-id-badge">#{{ props.quiz.id }}</span>
      </div>

      <div class="quiz-meta row g-3 text-secondary mb-4">
        <div class="col-md-4 d-flex align-items-center">
          <i class="bi bi-calendar-event me-2"></i>
          <span><strong>Date:</strong> {{ formattedDate }}</span>
        </div>
        <div class="col-md-4 d-flex align-items-center">
          <i class="bi bi-clock me-2"></i>
          <span><strong>Time:</strong> {{ props.quiz.time }}</span>
        </div>
        <div class="col-md-4 d-flex align-items-center">
          <i class="bi bi-hourglass-split me-2"></i>
          <span><strong>Duration:</strong> {{ props.quiz.duration }} mins</span>
        </div>
      </div>

      <div class="quiz-description">
        <p class="mb-0">{{ props.quiz.description }}</p>
      </div>
    </div>

    <div class="quiz-actions card-footer bg-white text-end p-3">
      <div v-if="quiz.is_started">
          <div v-if="quiz.is_ended">
            <div v-if="hasSubmitted">
              <button class="btn btn-success btn-lg" @click="review_quiz(quiz)">
                Review Quiz <i class="bi bi-arrow-right-short"></i>
              </button>
            </div>
            <div v-else>
              <button class="btn btn-success btn-lg disabled">
                Not Submitted <i class="bi bi-arrow-right-short"></i>
              </button>
            </div>
          </div>

          <div v-else>
            <div v-if="hasSubmitted">
              <button class="btn btn-primary btn-lg disabled" @click="start_redirect(quiz)">
                Already Submitted <i class="bi bi-play-fill"></i>
              </button>
            </div>
            <div v-else>
              <button class="btn btn-primary btn-lg" @click="start_redirect(quiz)">
                Start Quiz <i class="bi bi-play-fill"></i>
              </button>
            </div>
          </div>
        </div>
      <div v-else class="quiz-locked">
        <i class="bi bi-lock-fill me-2"></i>
        <span>LOCKED</span>
      </div>
    </div>
  </div>
</template>


<script setup>
import { formatDate } from '@/composables/useDateFormat';
import { useRouter } from 'vue-router';
import { useQuizStore } from '@/stores/quizStore';
import apiClient from '../api/axios';
import { ref, onMounted } from 'vue';

const router = useRouter();
const quizStore = useQuizStore();

const props = defineProps(['quiz'])

const formattedDate = formatDate(props.quiz.date);

const hasSubmitted = ref(false);

const checkSubmission = async () => {
  console.log(props.quiz)
  const response = await apiClient.get('/user/attempts');
  const attempts = response.data;
  hasSubmitted.value = attempts.some(attempt => attempt.quiz_id === props.quiz.id);
}

const start_redirect = (quiz) => {
  quizStore.selectQuiz(quiz);
  router.push(`/quiz/${quiz.id}`);
  return;
}

const review_quiz = (quiz) => {
  quizStore.selectQuiz(quiz);
  router.push(`/quiz/${quiz.id}`);
}

onMounted(() => checkSubmission());

</script>

<style scoped>
/* Main Card Styling & Hover Effect */
.quiz-card {
  border: 1px solid #e9ecef;
  border-radius: 0.75rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease-in-out;
}
.quiz-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

/* Header Elements */
.quiz-title {
  color: #212529;
  font-weight: 700;
}
.quiz-id-badge {
  background-color: #e9ecef;
  color: #6c757d;
  font-weight: 600;
  padding: 0.25rem 0.6rem;
  border-radius: 20px;
  font-size: 0.8rem;
}

/* Meta Info Styling */
.quiz-meta {
  font-size: 0.95rem;
}
.quiz-meta .bi {
  color: var(--bs-primary);
  font-size: 1.4rem;
}

/* Description Blockquote Style */
.quiz-description {
  background-color: #f8f9fa;
  border-left: 4px solid var(--bs-primary);
  padding: 1rem 1.25rem;
  border-radius: 0.25rem;
  color: #495057;
}

/* Actions Footer */
.quiz-actions {
  border-top: 1px solid #e9ecef;
}

/* Locked State Styling */
.quiz-locked {
  display: inline-flex;
  align-items: center;
  font-size: 1rem;
  font-weight: 600;
  color: #6c757d;
  opacity: 0.8;
}
.quiz-locked .bi {
  font-size: 1.2rem;
}

/* Button Styling */
.btn {
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}
.btn .bi {
  font-size: 1.5em; /* Make icon slightly larger than button text */
  line-height: 1; /* Helps with vertical alignment */
}
</style>
