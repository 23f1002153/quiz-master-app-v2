<template>
  <div class="quiz-history-page">
    <div class="container">
      <header class="page-header">
        <h1>My Quiz History</h1>
        <p class="text-muted">Review your performance and revisit past quizzes.</p>
      </header>

      <div class="filter-bar">
        <div class="input-group">
          <span class="input-group-text"><i class="bi bi-search"></i></span>
          <input type="text" class="form-control" placeholder="Search by quiz name..." v-model="searchQuery">
        </div>
        <div class="input-group">
          <label class="input-group-text" for="subject-filter">Subject</label>
          <select class="form-select" id="subject-filter" v-model="selectedSubject">
            <option value="All">All Subjects</option>
            <option v-for="subject in subjects" :key="subject.id" :value="subject.name">{{ capitalize(subject.name )}}</option>
          </select>
        </div>
        <div class="input-group">
          <label class="input-group-text" for="sort-filter">Sort By</label>
          <select class="form-select" id="sort-filter" v-model="sortBy">
            <option value="date_desc">Date (Newest)</option>
            <option value="date_asc">Date (Oldest)</option>
            <option value="score_desc">Score (High-Low)</option>
            <option value="score_asc">Score (Low-High)</option>
          </select>
        </div>
      </div>

      <div v-if="filteredQuizzes.length > 0" class="row g-4">
        <div v-for="quiz in filteredQuizzes" :key="quiz.id" class="col-md-6 col-lg-4">
          <QuizzeriaCard :quiz="quiz"/>
        </div>
      </div>

      <div v-else class="empty-state">
        <i class="bi bi-journal-x"></i>
        <h4>No Quizzes Found</h4>
        <p>Your completed quizzes will appear here once you finish them.</p>
      </div>

    </div>
  </div>
</template>

<script setup>
import apiClient from '@/components/api/axios';
import QuizzeriaCard from '@/components/quizzeria/QuizzeriaCard.vue';
import { ref, computed, onMounted, capitalize } from 'vue';

// --- State for Filters ---
const searchQuery = ref('');
const selectedSubject = ref('All');
const sortBy = ref('date_desc');

const completedQuizzes = ref([]);
const subjects = ref(null);

const findQuizzes = async () => {
  try{
    const response = await apiClient.get('/user/quizzes');
    completedQuizzes.value = response.data;
    console.log(response.data)
  }
  catch(error){
    console.log(error);
  }
}


const allSubjects = async () => {
  try{
    const response = await apiClient.get('/subjects');
    subjects.value = response.data;
    // console.log(sub)
  }
  catch(error){
    console.log(error);
  }
}

onMounted(() => {
  findQuizzes();
  allSubjects();
});

// --- Filtering and Sorting Logic ---
const filteredQuizzes = computed(() => {
  let quizzes = [...completedQuizzes.value];

  // 1. Filter by search query
  if (searchQuery.value) {
    quizzes = quizzes.filter(q => q.quiz_name.toLowerCase().includes(searchQuery.value.toLowerCase()));
  }

  // 2. Filter by subject
  if (selectedSubject.value !== 'All') {
    quizzes = quizzes.filter(q => q.subject_name === selectedSubject.value);
  }

  // 3. Sort the results
  quizzes.sort((a, b) => {
    switch (sortBy.value) {
      case 'score_desc': return (b.percentage) - (a.percentage);
      case 'score_asc': return (a.percentage) - (b.percentage);
      case 'date_asc': return new Date(a.attempted_at) - new Date(b.attempted_at);
      case 'date_desc':
      default:
        return new Date(b.attempted_at) - new Date(a.attempted_at);
    }
  });

  return quizzes;
});
</script>

<style scoped>
.quiz-history-page {
  background-color: #f8f9fa;
  min-height: 100vh;
  padding: 2rem 0;
  font-family: 'Segoe UI', 'Roboto', sans-serif;
}

.page-header {
  text-align: center;
  margin-bottom: 2rem;
}

.page-header h1 {
  font-weight: 700;
}

.filter-bar {
  display: grid;
  grid-template-columns: 1fr auto auto;
  gap: 1rem;
  background-color: #fff;
  padding: 1rem;
  border-radius: 0.75rem;
  margin-bottom: 2.5rem;
  border: 1px solid #dee2e6;
}

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
