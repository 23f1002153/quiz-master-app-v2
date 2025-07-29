<template>
  <div class="quiz-result-card">
    <div class="card-body">
      <span class="quiz-subject-badge">{{ props.quiz.subject_name }}</span> ---- <span class="quiz-chapter-badge">{{ props.quiz.chapter_name }}</span>
      <h3 class="quiz-name">{{ props.quiz.quiz_name }}</h3>
      <div class="quiz-stats">
        <div class="stat-item">
          <i class="bi bi-bar-chart-line-fill"></i>
          <span>Score: <strong>{{ props.quiz.total_score }} / {{ props.quiz.total_marks }} ({{ props.quiz.percentage }}%)</strong></span>
        </div>
        <div class="stat-item">
          <i class="bi bi-calendar-check-fill"></i>
          <span>Completed: <strong>{{ formatDate(props.quiz.attempted_at) }}</strong></span>
        </div>
      </div>
    </div>
    <div class="card-footer">
      <button class="btn btn-primary w-100" :disabled="!props.quiz.is_ended" @click="viewResults">{{ props.quiz.is_ended ? "View Answers" : "Quiz time Ongoing" }}</button>
    </div>
  </div>
</template>

<script setup>
import { formatDate } from '@/composables/useDateFormat';
import { useQuizStore } from '@/stores/quizStore';
import { storeToRefs } from 'pinia';
import { useRouter } from 'vue-router';

const quizStore = useQuizStore();
const { selectedQuiz } = storeToRefs(quizStore);

const props = defineProps(['quiz']);

const router = useRouter();

const viewResults = async () => {
  quizStore.selectQuiz(props.quiz);
  await quizStore.getAnswers();
  router.push(`/quiz/${selectedQuiz.value.id}`);
}


</script>

<style scoped>
.quiz-result-card {
  background-color: #fff;
  border: 1px solid #e9ecef;
  border-radius: 0.75rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.quiz-result-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.card-body {
  padding: 1.5rem;
  flex-grow: 1;
}

.quiz-subject-badge {
  display: inline-block;
  background-color: #e7f1ff;
  color: #0d6efd;
  padding: 0.3rem 0.7rem;
  border-radius: 20px;
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
}

.quiz-chapter-badge {
  display: inline-block;
  background-color: #e7f1ff;
  color: red;
  padding: 0.3rem 0.7rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
}

.quiz-name {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

.quiz-stats {
  font-size: 0.95rem;
  color: #6c757d;
}

.stat-item {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
}

.stat-item .bi {
  margin-right: 0.75rem;
  font-size: 1.2rem;
  color: #adb5bd;
}

.card-footer {
  background-color: transparent;
  border-top: 1px solid #e9ecef;
  padding: 1rem 1.5rem;
}

.empty-state {
  text-align: center;
  padding: 4rem;
  background-color: #fff;
  border-radius: 0.75rem;
  border: 1px solid #dee2e6;
  color: #6c757d;
}

.empty-state .bi {
  font-size: 4rem;
  color: #adb5bd;
  margin-bottom: 1rem;
}
</style>
