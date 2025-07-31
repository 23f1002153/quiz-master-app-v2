<template>
  <div class="edit-quiz-page">
    <div class="container">
      <!-- 1. Page Header -->
      <header class="page-header">
        <h1>Edit Quiz</h1>
        <h2 class="chapter-context">
          For Chapter: <strong>{{ chapterName }}</strong>
        </h2>
      </header>

      <!-- 2. Main Quiz Details Form -->
      <div class="card quiz-details-card">
        <div class="card-body">
          <div class="mb-3">
            <label for="quizName" class="form-label fw-bold">Quiz Name</label>
            <input type="text" class="form-control" id="quizName" v-model="quiz.name" placeholder="e.g., Assessment 1">
          </div>
          <div class="mb-3">
            <label for="quizDescription" class="form-label fw-bold">Description</label>
            <textarea class="form-control" id="quizDescription" rows="3" v-model="quiz.description" placeholder="A brief summary of what this quiz covers."></textarea>
          </div>
          <div class="row">
            <div class="col-md-6 mb-3">
              <label for="quizDate" class="form-label fw-bold">Date</label>
              <input type="date" class="form-control" id="quizDate" v-model="quiz.date">
            </div>
            <div class="col-md-6 mb-3">
              <label for="quizTime" class="form-label fw-bold">Time</label>
              <input type="time" class="form-control" id="quizTime" v-model="quiz.time">
            </div>
          </div>
          <div class="row">
            <div class="col-md-6 mb-3">
              <label for="quizDuration" class="form-label fw-bold">Duration (in minutes)</label>
              <input type="number" class="form-control" id="quizDuration" v-model.number="quiz.duration" min="1">
            </div>
            <div class="col-md-6 mb-3">
              <label for="quizPassing" class="form-label fw-bold">Passing Score (%)</label>
              <input type="number" class="form-control" id="quizPassing" v-model.number="quiz.passing" min="0" max="100">
            </div>
          </div>
          <div class="mb-3">
            <label for="quizRemarks" class="form-label fw-bold">Remarks (Optional)</label>
            <input type="text" class="form-control" id="quizRemarks" v-model="quiz.remarks" placeholder="Any additional notes or remarks for this quiz.">
          </div>
        </div>
      </div>

      <!-- 3. Dynamic Questions List -->
      <div class="questions-section">
        <h2 class="section-title">Questions</h2>
        <div v-for="(question, qIndex) in quiz.questions" :key="question.id" class="card question-card">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h5 class="mb-0">Question {{ qIndex + 1 }}</h5>
            <button class="btn btn-sm btn-outline-danger" @click="removeQuestion(qIndex)">
              <i class="bi bi-trash-fill"></i> Remove Question
            </button>
          </div>
          <div class="card-body">
            <div class="mb-3">
              <label class="form-label">Question Statement</label>
              <textarea class="form-control" rows="2" v-model="question.statement" placeholder="Enter the question text..."></textarea>
            </div>
            <div class="mb-3">
              <label class="form-label">Marks</label>
              <input type="number" class="form-control" v-model.number="question.marks" min="1">
            </div>
            <div class="options-list">
              <label class="form-label">Options (Select the correct answer)</label>
              <div v-for="(option, oIndex) in question.options" :key="option.id" class="input-group mb-2">
                <div class="input-group-text">
                  <input
                    class="form-check-input mt-0"
                    type="radio"
                    :name="'correct-option-' + question.id"
                    :value="option.id"
                    v-model="question.correct_option_id"
                  >
                </div>
                <input type="text" class="form-control" v-model="option.text" placeholder="Enter option text...">
                <button class="btn btn-outline-secondary" @click="removeOption(qIndex, oIndex)" :disabled="question.options.length <= 2">
                  <i class="bi bi-x"></i>
                </button>
              </div>
            </div>
            <button class="btn btn-sm btn-secondary mt-2" @click="addOption(qIndex)" :disabled="question.options.length >= 4">
              <i class="bi bi-plus"></i> Add Option
            </button>
          </div>
        </div>
        <button class="btn btn-primary w-100" @click="addQuestion">
          <i class="bi bi-plus-circle-fill me-2"></i>Add Another Question
        </button>
      </div>

      <!-- 4. Final Save Button -->
      <div class="form-actions">
        <button class="btn btn-success btn-lg w-100" @click="updateQuiz">
          Update Quiz
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useAdminQuizStore } from '@/stores/admin/adminQuizStore';
import { storeToRefs } from 'pinia';
import { useRouter } from 'vue-router';

const router = useRouter();

const adminQuizStore = useAdminQuizStore();
const { selectedQuiz, selectedQuestions } = storeToRefs(adminQuizStore);


// --- Assumed data from your store ---
const chapterName = ref('Introduction to Calculus');

const quiz = ref({});

const fetchQuizData = async () => {
  await adminQuizStore.fetchQuestions();
  quiz.value = JSON.parse(JSON.stringify(selectedQuiz.value));
  quiz.value.questions = JSON.parse(JSON.stringify(selectedQuestions.value));
  for(let question of quiz.value.questions){
    question.correct_option_id = question.options.find(opt => opt.is_correct).id;
  }
};

onMounted(() => {
  fetchQuizData();
});

// --- Functions to Manage the Form ---
const addQuestion = () => {
  const newQuestionId = Date.now();
  quiz.value.questions.push({
    id: newQuestionId,
    statement: '',
    marks: 10,
    options: [
      { id: newQuestionId + 1, text: '' },
      { id: newQuestionId + 2, text: '' },
    ],
    correct_option_id: null,
  });
};

const removeQuestion = (index) => {
  quiz.value.questions.splice(index, 1);
};

const addOption = (questionIndex) => {
  const question = quiz.value.questions[questionIndex];
  if (question.options.length < 4) {
    question.options.push({ id: Date.now(), text: '' });
  }
};

const removeOption = (questionIndex, optionIndex) => {
  const question = quiz.value.questions[questionIndex];
  if (question.options.length > 2) {
    question.options.splice(optionIndex, 1);
  }
};

const updateQuiz = () => {
  // You will handle the API call to PATCH/PUT the updated quiz data here.
  adminQuizStore.updateQuiz(quiz.value);
  alert('Quiz updated.');
  router.push('/admin/subjects');
};


</script>

<style scoped>
.edit-quiz-page {
  background-color: #f8f9fa;
  min-height: 100vh;
  padding: 2rem 0;
  font-family: 'Segoe UI', 'Roboto', sans-serif;
}
.container {
  max-width: 800px;
  margin: 0 auto;
}
.page-header {
  text-align: center;
  margin-bottom: 2rem;
}
.page-header h1 {
  font-weight: 700;
}
.chapter-context {
  font-size: 1.25rem;
  font-weight: 400;
  color: #6c757d;
}
.quiz-details-card, .question-card {
  background-color: #fff;
  border: 1px solid #dee2e6;
  border-radius: 0.75rem;
  margin-bottom: 1.5rem;
}
.questions-section {
  margin-top: 2.5rem;
}
.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1rem;
}
.question-card .card-header {
  background-color: #f8f9fa;
}
.options-list .input-group-text {
  background-color: #e9ecef;
}
.form-actions {
  margin-top: 2.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #dee2e6;
}
</style>
