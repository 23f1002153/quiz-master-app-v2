<template>
  <div class="quiz-page">
    <header class="quiz-header">
      <div class="container">
        <h1 class="quiz-name">{{ selectedQuiz.name }}</h1>
        <div class="timer">
          <i class="bi bi-stopwatch-fill"></i>
          <span>Time Left: <strong>{{ minutes }} : {{ seconds }} minutes</strong></span>
        </div>
      </div>
    </header>

    <div class="container quiz-layout">
      <main class="question-area">
        <div v-for="(question, index) in questions" :key="question.id">
          <div v-show="index === currentQuestionIndex" class="question-card">
            <div class="question-header">
              <span class="question-number">Question {{ index + 1 }}</span>
              <span class="question-marks">{{ question.marks }} Marks</span>
            </div>
            <p class="question-statement">{{ question.statement }}</p>

            <div class="options-container">
              <label
                v-for="option in question.options"
                :key="option.id"
                class="option-label"
                :class="{ 'selected': userAnswers[question.id] === option.id }"
              >
                <input
                  type="radio"
                  :name="'question-' + question.id"
                  :value="option.id"
                  v-model="userAnswers[question.id]"
                  class="option-radio"
                >
                <span class="option-text">{{ option.text }}</span>
              </label>
            </div>
          </div>
        </div>
        <div class="question-nav-buttons">
          <button @click="prevQuestion" :disabled="currentQuestionIndex === 0" class="btn-nav">
            <i class="bi bi-arrow-left"></i> Previous
          </button>
          <button @click="nextQuestion" :disabled="currentQuestionIndex === questions.length - 1" class="btn-nav">
            Next <i class="bi bi-arrow-right"></i>
          </button>
        </div>
      </main>

      <aside class="navigation-panel">
        <div class="navigation-card">
          <h3 class="panel-title">Question Palette</h3>
          <div class="question-grid">
            <button
              v-for="(question, index) in questions"
              :key="question.id"
              class="question-grid-item"
              :class="{
                'current': index === currentQuestionIndex,
                'answered': userAnswers[question.id] !== undefined
              }"
              @click="goToQuestion(index)"
            >
              {{ index + 1 }}
            </button>
          </div>
          <button class="submit-btn" @click="submit()">Submit Quiz</button>
        </div>
      </aside>
    </div>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue';
import { useQuizStore } from '@/stores/quizStore';
import { storeToRefs } from 'pinia';
import { useRouter } from 'vue-router';

const router = useRouter();
const quizStore = useQuizStore();

const { questions, selectedQuiz, remainingTime } = storeToRefs(quizStore);

const currentQuestionIndex = ref(0);

// Helper function to safely get and parse answers from localStorage
const getInitialAnswers = () => {
  const savedAnswers = localStorage.getItem('quizAnswers');
  if (savedAnswers) {
    try {
      // Parse the stored JSON string back into a JavaScript object
      return JSON.parse(savedAnswers);
    } catch (e) {
      console.error("Error parsing saved answers:", e);
      // If data is corrupted, start with an empty object
      return {};
    }
  }
  // If nothing is in storage, start with an empty object
  return {};
};

// Initialize the ref with the data from localStorage
const userAnswers = ref(getInitialAnswers());

// The watcher to save subsequent changes remains the same
watch(userAnswers, (newAnswers) => {
  localStorage.setItem('quizAnswers', JSON.stringify(newAnswers));
}, {
  deep: true
});

const parseAnswers = (answers) => {
  let parsedAns = []
  for (let [q_id, o_id] of Object.entries(answers)){
    const ans = {
      "question_id": Number(q_id),
      "option_id": o_id
    }
    parsedAns.push(ans);
  };
  return {"responses": parsedAns};
}

const submit = async () => {
  const parsedAns = parseAnswers(userAnswers.value);
  await quizStore.submitQuiz(parsedAns);
  localStorage.removeItem('quizAnswers');
  router.push('/quizzeria');
}

const totalSeconds = ref(remainingTime.value * 60);
let timer = null;

const minutes = computed(() => Math.floor(totalSeconds.value / 60));
const seconds = computed(() => totalSeconds.value % 60);

const startCountdown = () => {
  timer = setInterval(() => {
    totalSeconds.value--;
    if(totalSeconds.value < 30){
      submit();
      clearInterval(timer);
    }
  }, 1000)
}

onMounted(() => {
  startCountdown();
});

onBeforeUnmount(() => {
  clearInterval(timer);
})

// --- Question Navigation ---
const nextQuestion = () => { if (currentQuestionIndex.value < questions.value.length - 1) currentQuestionIndex.value++; };
const prevQuestion = () => { if (currentQuestionIndex.value > 0) currentQuestionIndex.value--; };
const goToQuestion = (index) => { currentQuestionIndex.value = index; };
</script>

<style scoped>
.quiz-page { background-color: #f0f2f5; min-height: 100vh; font-family: 'Segoe UI', 'Roboto', sans-serif; }
.container { width: 100%; max-width: 1200px; margin: 0 auto; padding: 0 1rem; }

/* Sticky Header */
.quiz-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background-color: #fff;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  padding: 1rem 0;
  border-bottom: 1px solid #dee2e6;
}
.quiz-header .container { display: flex; justify-content: space-between; align-items: center; }
.quiz-name { font-size: 1.5rem; font-weight: 600; margin: 0; }
.timer { font-size: 1.25rem; display: flex; align-items: center; gap: 0.5rem; background-color: #ffeeda; color: #d9534f; padding: 0.5rem 1rem; border-radius: 0.5rem; }

/* Main Layout */
.quiz-layout { display: flex; gap: 2rem; padding-top: 2rem; }
.question-area { flex: 1; }
.navigation-panel { width: 300px; }

/* Question Card */
.question-card { background-color: #fff; border-radius: 0.75rem; padding: 2rem; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
.question-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; border-bottom: 1px solid #e9ecef; padding-bottom: 1rem; }
.question-number { font-size: 1.1rem; font-weight: 600; color: #0d6efd; }
.question-marks { font-size: 0.9rem; font-weight: 500; background-color: #e9ecef; padding: 0.25rem 0.5rem; border-radius: 4px; }
.question-statement { font-size: 1.25rem; margin-bottom: 2rem; line-height: 1.6; }
.options-container { display: flex; flex-direction: column; gap: 0.75rem; }
.option-label {
  display: flex;
  align-items: center;
  padding: 1rem;
  border: 1px solid #ced4da;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
}
.option-label:hover { background-color: #f8f9fa; }
.option-label.selected { border-color: #0d6efd; background-color: #e7f1ff; font-weight: 600; }
.option-radio { display: none; }
.option-text { margin-left: 0.75rem; }
.question-nav-buttons { display: flex; justify-content: space-between; margin-top: 2rem; }
.btn-nav { background: none; border: 1px solid #ced4da; padding: 0.75rem 1.5rem; border-radius: 0.5rem; cursor: pointer; font-weight: 600; display: flex; align-items: center; gap: 0.5rem; }
.btn-nav:disabled { opacity: 0.5; cursor: not-allowed; }

/* Navigation Panel */
.navigation-card { background-color: #fff; border-radius: 0.75rem; padding: 1.5rem; position: sticky; top: 110px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
.panel-title { font-size: 1.2rem; font-weight: 600; margin-bottom: 1rem; }
.question-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(40px, 1fr)); gap: 0.75rem; margin-bottom: 1.5rem; }
.question-grid-item {
  width: 40px;
  height: 40px;
  border: 1px solid #ced4da;
  background-color: #fff;
  border-radius: 0.5rem;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s ease;
}
.question-grid-item:hover { background-color: #f8f9fa; }
.question-grid-item.answered { background-color: #198754; color: white; border-color: #198754; }
.question-grid-item.current { background-color: #0d6efd; color: white; border-color: #0d6efd; transform: scale(1.1); }
.submit-btn { width: 100%; padding: 0.75rem; font-size: 1rem; font-weight: 600; color: white; background-color: #dc3545; border: none; border-radius: 0.5rem; cursor: pointer; }
</style>
