<template>
  <div class="quiz-start-page-container">
    <div class="quiz-card">
      <header class="quiz-header">
        <div class="quiz-icon">
          <i class="bi bi-file-earmark-text-fill"></i>
        </div>
        <h1 class="quiz-title">{{ selectedQuiz.name }}</h1>
        <span class="quiz-id-badge">ID: {{ selectedQuiz.id }}</span>
      </header>

      <div class="quiz-body">
        <section class="quiz-section">
          <h2 class="section-title">About this Quiz</h2>
          <p class="quiz-description">{{ selectedQuiz.description }}</p>
        </section>

        <hr class="section-divider">

        <section class="quiz-section">
          <h2 class="section-title">Instructions</h2>
          <ul class="instructions-list">
            <li>This quiz consists of <strong> only multiple-choice questions</strong>.</li>
            <li>You will have <strong>{{ selectedQuiz.duration }} minutes</strong> to complete the quiz once you begin.</li>
            <li>The quiz can only be attempted <strong>once</strong>.</li>
            <li>Do not close the browser window or navigate away from the quiz page.</li>
          </ul>
        </section>
      </div>

      <footer class="quiz-footer">
        <button class="btn btn-primary start-quiz-btn" @click="beginQuiz">
          Start/Resume Quiz
        </button>
        {{ errorType }}
      </footer>
    </div>
  </div>
</template>

<script setup>

import { useQuizStore } from '@/stores/quizStore';
import { storeToRefs } from 'pinia';

const emits = defineEmits(['startQuiz'])

const quizStore = useQuizStore();

const { selectedQuiz, errorType } = storeToRefs(quizStore);

const beginQuiz = async () => {
  try{
    await quizStore.startQuiz();
    emits('startQuiz');
  }
  catch(error){
    console.log(error);
  }
}


</script>

<style scoped>
/* Define color palette for easy customization */
:root {
  --primary-color: #0d6efd;
  --light-gray-color: #f8f9fa;
  --medium-gray-color: #e9ecef;
  --dark-gray-color: #6c757d;
  --text-color: #212529;
}

/* Full Page Container */
.quiz-start-page-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-color: var(--light-gray-color);
  font-family: 'Segoe UI', 'Roboto', sans-serif;
  padding: 2rem;
}

/* Main Card Styling */
.quiz-card {
  width: 100%;
  max-width: 700px;
  background-color: #ffffff;
  border-radius: 1rem;
  box-shadow: 0 10px 35px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

/* Card Header */
.quiz-header {
  text-align: center;
  padding: 2.5rem 2rem;
  background-color: var(--primary-color);
  position: relative;
}
.quiz-icon {
  font-size: 3rem;
  margin-bottom: 0.5rem;
  opacity: 0.8;
}
.quiz-title {
  font-size: 3rem;
  font-weight: 700;
  margin: 0;
}
.quiz-id-badge {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background-color: rgba(255, 255, 255, 0.2);
  padding: 0.3rem 0.7rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
}

/* Card Body */
.quiz-body {
  padding: 2rem 2.5rem;
}
.section-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-color);
  margin-bottom: 1rem;
}
.quiz-description {
  font-size: 1.1rem;
  line-height: 1.6;
  color: var(--dark-gray-color);
}
.section-divider {
  border: 0;
  height: 1px;
  background-color: var(--medium-gray-color);
  margin: 2rem 0;
}

/* Instructions List */
.instructions-list {
  list-style-type: none;
  padding-left: 0;
  font-size: 1.05rem;
  color: #495057;
}
.instructions-list li {
  padding-left: 2rem;
  position: relative;
  margin-bottom: 0.75rem;
}
.instructions-list li::before {
  content: '✓';
  color: var(--primary-color);
  position: absolute;
  left: 0;
  font-weight: 700;
  font-size: 1.2rem;
}

/* Card Footer */
.quiz-footer {
  padding: 1.5rem 2.5rem;
  background-color: var(--light-gray-color);
  text-align: center;
  border-top: 1px solid var(--medium-gray-color);
}
.start-quiz-btn {
  width: 100%;
  padding: 1rem;
  font-size: 1.5rem;
  font-weight: 700;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
}
.start-quiz-btn:hover {
  opacity: 0.9;
  box-shadow: 0 5px 15px rgba(13, 110, 253, 0.4);
}
</style>
