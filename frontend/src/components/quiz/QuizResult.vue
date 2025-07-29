<template>

  <div class="quiz-results-page" v-if="quizAnswers">
    <div class="container">
      <!-- 1. Results Header & Summary -->
      <header class="results-header">
        <div class="summary-card">
          <h1 class="quiz-title">{{ quizAnswers[0]?.question.quiz_name || 'Quiz Results' }}</h1>
          <div class="summary-stats">
            <div class="stat-item score">
              <span class="stat-label">Final Score</span>
              <span class="stat-value">{{ userScore }} / {{ totalMarks }} </span>
            </div>

            <div class="stat-item correct">
              <span class="stat-label">Correct Answers</span>
              <span class="stat-value">{{ correctAnswersCount }}</span>
            </div>
            <div class="stat-item incorrect">
              <span class="stat-label">Incorrect Answers</span>
              <span class="stat-value">{{ quizAnswers.length - correctAnswersCount }}</span>
            </div>
          </div>
        </div>
      </header>



      <!-- 2. List of Questions and Answers -->
      <main class="results-list">
        <div v-for="(result, index) in quizAnswers" :key="result.question.id" class="question-result-card">
          <div class="question-header">
            <span class="question-number">Question {{ index + 1 }}</span>
            <span class="question-marks">{{ result.question.marks }} Marks</span>
          </div>
          <p class="question-statement">{{ result.question.statement }}</p>

          <div class="options-container">
            <div
              v-for="option in result.question.options"
              :key="option.id"
              class="option-item"
              :class="getOptionClass(option, result.selected_option)"
            >
              <i class="bi option-icon"></i>
              <span class="option-text">{{ option.text }}</span>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
  <div v-else>
    Loadng
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue';
import { useQuizStore } from '@/stores/quizStore';
import { storeToRefs } from 'pinia';

const quizStore = useQuizStore();

const getAns = async () => {
  await quizStore.getAnswers();
  console.log(quizStore.quizAnswers);
}

const { quizAnswers } = storeToRefs(quizStore);



onMounted(() => getAns());

// --- Computed Properties for Summary ---
const totalMarks = computed(() => {
  return quizAnswers.value.reduce((total, result) => total + result.question.marks, 0);
});

const userScore = computed(() => {
  return quizAnswers.value.reduce((score, result) => {
    const correctOption = result.question.options.find(opt => opt.is_correct);
    if (result.selected_option.id === correctOption.id) {
      return score + result.question.marks;
    }
    return score;
  }, 0);
});

const correctAnswersCount = computed(() => {
  return quizAnswers.value.filter(result => {
    const correctOption = result.question.options.find(opt => opt.is_correct);
    return result.selected_option.id === correctOption.id;
  }).length;
});

// --- Styling Logic ---
const getOptionClass = (option, selectedOption) => {
  const isSelected = option.id === selectedOption.id;

  if (option.is_correct) {
    return 'correct'; // Always highlight the correct answer in green
  }
  if (isSelected && !option.is_correct) {
    return 'incorrect'; // If this incorrect option was selected, highlight it in red
  }
  return 'neutral'; // All other non-selected, incorrect options
};
</script>

<style scoped>
.quiz-results-page {
  background-color: #f4f7f9;
  min-height: 100vh;
  padding: 2rem 0;
  font-family: 'Segoe UI', 'Roboto', sans-serif;
}

.container {
  max-width: 800px;
  margin: 0 auto;
}

/* Header & Summary */
.results-header {
  margin-bottom: 2rem;
}
.summary-card {
  background-color: #fff;
  border-radius: 1rem;
  padding: 2rem;
  text-align: center;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}
.quiz-title {
  font-weight: 700;
  margin-bottom: 1.5rem;
}
.summary-stats {
  display: flex;
  justify-content: space-around;
  gap: 1rem;
}
.stat-item {
  display: flex;
  flex-direction: column;
}
.stat-label {
  font-size: 0.9rem;
  color: #6c757d;
  margin-bottom: 0.25rem;
}
.stat-value {
  font-size: 1.75rem;
  font-weight: 700;
}
.stat-item.score .stat-value { color: #0d6efd; }
.stat-item.correct .stat-value { color: #198754; }
.stat-item.incorrect .stat-value { color: #dc3545; }

/* Question Cards */
.results-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
.question-result-card {
  background-color: #fff;
  border-radius: 0.75rem;
  padding: 1.5rem 2rem;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}
.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e9ecef;
}
.question-number {
  font-weight: 600;
  color: #0d6efd;
}
.question-marks {
  font-size: 0.9rem;
  background-color: #e9ecef;
  padding: 0.25rem 0.6rem;
  border-radius: 5px;
}
.question-statement {
  font-size: 1.1rem;
  font-weight: 500;
  margin-bottom: 1.5rem;
}

/* Options Styling */
.options-container {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.option-item {
  display: flex;
  align-items: center;
  padding: 0.9rem 1.25rem;
  border: 1px solid #dee2e6;
  border-radius: 0.5rem;
  transition: all 0.2s ease;
}
.option-icon {
  margin-right: 1rem;
  font-size: 1.2rem;
}

/* Correct (Green) */
.option-item.correct {
  background-color: lightgreen;
  border-color: #b2dfc8;
  color: #0f5132;
  font-weight: 600;
}
.option-item.correct .option-icon::before {
  content: '\F26E'; /* Bootstrap Icons: check-circle-fill */
}

/* Incorrect (Red) */
.option-item.incorrect {
  background-color: lightpink;
  border-color: #f5c2c7;
  color: #842029;
}
.option-item.incorrect .option-icon::before {
  content: '\F623'; /* Bootstrap Icons: x-circle-fill */
}

/* Neutral (Gray) */
.option-item.neutral {
  background-color: #f8f9fa;
  color: #6c757d;
}
.option-item.neutral .option-icon::before {
  content: '\F28A'; /* Bootstrap Icons: circle */
}
</style>
