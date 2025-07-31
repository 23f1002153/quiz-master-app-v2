<template>
  <div class="admin-dashboard-page">
    <div class="container">
      <!-- 1. Page Header -->
      <header class="page-header">
        <h1>Admin Dashboard</h1>
        <p class="text-muted">A high-level overview of platform activity and content performance.</p>
      </header>

      <!-- 2. Platform-Wide KPIs -->
      <div class="row g-4 mb-5">
        <div class="col-md-6 col-lg-3">
          <div class="kpi-card">
            <div class="kpi-icon icon-subjects"><i class="bi bi-stack"></i></div>
            <div class="kpi-content">
              <span class="kpi-value">{{ kpis.totalSubjects }}</span>
              <span class="kpi-label">Total Subjects</span>
            </div>
          </div>
        </div>
        <div class="col-md-6 col-lg-3">
          <div class="kpi-card">
            <div class="kpi-icon icon-quizzes"><i class="bi bi-collection-fill"></i></div>
            <div class="kpi-content">
              <span class="kpi-value">{{ kpis.totalQuizzes }}</span>
              <span class="kpi-label">Total Quizzes</span>
            </div>
          </div>
        </div>
        <div class="col-md-6 col-lg-3">
          <div class="kpi-card">
            <div class="kpi-icon icon-attempts"><i class="bi bi-journal-check"></i></div>
            <div class="kpi-content">
              <span class="kpi-value">{{ kpis.totalAttempts }}</span>
              <span class="kpi-label">Total Quiz Attempts</span>
            </div>
          </div>
        </div>
        <div class="col-md-6 col-lg-3">
          <div class="kpi-card">
            <div class="kpi-icon icon-score"><i class="bi bi-star-fill"></i></div>
            <div class="kpi-content">
              <span class="kpi-value">{{ kpis.averageScore }}%</span>
              <span class="kpi-label">Platform Avg. Score</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 3. Subject Performance & Visualization -->
      <div class="row g-4 mb-5">
        <div class="col-lg-7">
          <div class="dashboard-card">
            <div class="card-header"><h3>Performance by Subject</h3></div>
            <div class="card-body table-responsive">
              <table class="table table-hover">
                <thead>
                  <tr>
                    <th>Subject</th>
                    <th>Quizzes</th>
                    <th>Total Attempts</th>
                    <th>Avg. Score</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="subject in performanceBySubject" :key="subject.name">
                    <td><strong>{{ subject.name }}</strong></td>
                    <td>{{ subject.quizCount }}</td>
                    <td>{{ subject.totalAttempts }}</td>
                    <td>{{ subject.avgScore }}%</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
        <div class="col-lg-5">
          <div class="dashboard-card">
            <div class="card-header"><h3>Average Score by Subject</h3></div>
            <div class="card-body chart-wrapper">
              <div class="y-axis-labels"><span>100%</span><span>50%</span><span>0%</span></div>
              <div class="chart-container">
                <div v-for="subject in performanceBySubject" :key="subject.name" class="chart-element">
                  <div class="chart-bar-wrapper">
                    <div class="chart-bar" :style="{ height: subject.avgScore + '%' }">
                      <span class="bar-label-inside">{{ subject.avgScore }}%</span>
                    </div>
                  </div>
                  <span class="chart-x-axis-label">{{ subject.name }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- NEW: Quiz Performance Analysis -->
      <div class="row g-4 mb-5">
        <div class="col-lg-6">
          <div class="dashboard-card">
            <div class="card-header"><h3>Problematic Quizzes (Lowest Scores)</h3></div>
            <div class="card-body table-responsive">
              <table class="table">
                <thead><tr><th>Quiz Name</th><th>Attempts</th><th>Avg. Score</th></tr></thead>
                <tbody>
                  <tr v-for="quiz in problematicQuizzes" :key="quiz.id">
                    <td><strong>{{ quiz.name }}</strong><br><small class="text-muted">{{ quiz.subject }}</small></td>
                    <td>{{ quiz.attempts }}</td>
                    <td><span class="badge bg-danger-light text-danger">{{ quiz.avgScore }}%</span></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
        <div class="col-lg-6">
          <div class="dashboard-card">
            <div class="card-header"><h3>Top Quizzes (Highest Scores)</h3></div>
            <div class="card-body table-responsive">
              <table class="table">
                <thead><tr><th>Quiz Name</th><th>Attempts</th><th>Avg. Score</th></tr></thead>
                <tbody>
                  <tr v-for="quiz in topQuizzes" :key="quiz.id">
                    <td><strong>{{ quiz.name }}</strong><br><small class="text-muted">{{ quiz.subject }}</small></td>
                    <td>{{ quiz.attempts }}</td>
                    <td><span class="badge bg-success-light text-success">{{ quiz.avgScore }}%</span></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- 4. Trend Charts Section -->
      <div class="dashboard-card">
        <div class="card-header filter-header">
          <h3>Performance Trends</h3>

          <div class="d-flex gap-2">
            <select class="form-select form-select-sm" v-model="trendChartSubject">
              <option value="All">All Subjects</option>
              <option v-for="sub in performanceBySubject" :key="sub.name" :value="sub.name">{{ sub.name }}</option>
            </select>
            <select class="form-select form-select-sm" v-model.number="trendChartCount">
              <option value="10">Last 10 Attempts</option>
              <option value="20">Last 20 Attempts</option>
              <option value="50">Last 50 Attempts</option>
              <option value="0">All Attempts</option>
            </select>
          </div>
          <button class="btn btn-outline-secondary btn-sm" @click="download"><i class="bi bi-file-earmark-spreadsheet-fill me-2"></i>Download</button>
        </div>

        <div class="card-body border-bottom">
            <h6 class="chart-title">Scores Over Last {{ trendChartCount > 0 ? trendChartCount : 'All' }} Attempts</h6>
            <div class="chart-wrapper">
              <div class="y-axis-labels"><span>100%</span><span>50%</span><span>0%</span></div>
              <div class="line-chart-container">
                <svg class="line-chart-svg" viewBox="0 0 500 200">
                  <path :d="latestAttemptsPath" class="chart-path attempts-path" />
                </svg>
              </div>
            </div>
        </div>

        <div class="card-body">
            <h6 class="chart-title">Moving Average Over Last {{ trendChartCount > 0 ? trendChartCount : 'All' }} Attempts</h6>
            <div class="chart-wrapper">
              <div class="y-axis-labels"><span>100%</span><span>50%</span><span>0%</span></div>
              <div class="line-chart-container">
                <svg class="line-chart-svg" viewBox="0 0 500 200">
                  <path :d="averageAttemptsPath" class="chart-path avg-path" />
                </svg>
              </div>
            </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import apiClient from '@/components/api/axios';
import { ref, computed, onMounted } from 'vue';

const subjects = ref([]);
const quizzes = ref([]);
const attempts = ref([])

const fetchSubjects = async () => {
  const response = await apiClient.get('/subjects');
  subjects.value = response.data;
}

const fetchQuizzes = async () => {
  const response = await apiClient.get('/quizzes/all');
  quizzes.value = response.data;
}

const fetchAttempts = async () => {
  const response = await apiClient.get('/attempts/all');
  attempts.value = response.data;
}

const download = async () => {
  try{
    const response = await apiClient.post('/jobs/export/all-users');
    alert(`${response.data.message}`);
  }
  catch(error){
    console.log(error);
  }
}

onMounted(() => {
  fetchSubjects();
  fetchQuizzes();
  fetchAttempts();
  allSubjectPerformance();
  allQuizPerformance();
})


// --- Dummy Data ---
const kpis = computed(() => ({
  totalSubjects: subjects.value.length,
  totalQuizzes: quizzes.value.length,
  totalAttempts: attempts.value.length,
  averageScore:
    attempts.value.length > 0
      ? Math.round(attempts.value.reduce((total, attempt) => total + attempt.percentage, 0) / attempts.value.length)
      : 0
}));

const performanceBySubject = ref([])

const performanceSub = (sub) => {
  const name = sub.name;
  const quizCount = quizzes.value.reduce((count, quiz) => count + (quiz.subject_name === sub.name ? 1 : 0), 0);
  const totalAttempts = attempts.value.reduce((count, attempt) => count + (attempt.subject_name === sub.name ? 1 : 0), 0);
  const avgScore = totalAttempts > 0 ? Math.round(attempts.value.reduce((total, attempt) => total + (attempt.subject_name === sub.name ? attempt.percentage : 0), 0) / totalAttempts) : 0;
  const per = {
    name: name,
    quizCount: quizCount,
    totalAttempts: totalAttempts,
    avgScore: avgScore
  }
  performanceBySubject.value.push(per);
}

const allSubjectPerformance = async () => {
  await fetchSubjects();
  await fetchQuizzes();
  await fetchAttempts();
  performanceBySubject.value = [];
  for(let subject of subjects.value){
    performanceSub(subject);
  }
}

const performanceByQuiz = ref([]);

const performanceQuiz = (quiz) => {
  const id = quiz.id
  const name = quiz.name;
  const subject = quiz.subject_name
  const totalAttempts = attempts.value.reduce((count, attempt) => count + (attempt.quiz_name === quiz.name ? 1 : 0), 0);
  const avgScore = totalAttempts > 0 ? Math.round(attempts.value.reduce((total, attempt) => total + (attempt.quiz_name === quiz.name ? attempt.percentage : 0), 0) / totalAttempts) : 0;
  const per = {
    id: id,
    name: name,
    subject: subject,
    attempts: totalAttempts,
    avgScore: avgScore
  }
  performanceByQuiz.value.push(per);
}

const allQuizPerformance = async () => {
  await fetchQuizzes();
  await fetchAttempts();
  performanceByQuiz.value = [];
  for(let quiz of quizzes.value){
    performanceQuiz(quiz);
  }
  performanceByQuiz.value.sort((a, b) => b.avgScore - a.avgScore);
}

const problematicQuizzes = computed(() => performanceByQuiz.value.slice().reverse().slice(0, 3));
const topQuizzes = computed(() => performanceByQuiz.value.slice(0, 3));


// --- State for Filters ---
const trendChartCount = ref(10);
const trendChartSubject = ref('All');

// --- Computed Properties for Charts ---
const filteredAttempts = computed(() => {
    let quizzes = attempts.value;
    if (trendChartSubject.value !== 'All') {
        quizzes = quizzes.filter(a => a.subject_name === trendChartSubject.value);
    }
    if (trendChartCount.value > 0) {
        return quizzes.slice(-trendChartCount.value);
    }
    return quizzes;
});

const latestAttemptsPath = computed(() => {
    const data = filteredAttempts.value.map(a => a.percentage);
    if (data.length < 2) return '';
    const maxVal = 100;
    let path = `M 0 ${200 - (data[0] / maxVal) * 200}`;
    data.forEach((p, i) => {
        if (i > 0) {
            const x = (500 / (data.length - 1)) * i;
            const y = 200 - (p / maxVal) * 200;
            path += ` L ${x} ${y}`;
        }
    });
    return path;
});

const averageAttemptsPath = computed(() => {
    const data = filteredAttempts.value.map(a => a.percentage);
    if (data.length < 2) return '';
    const maxVal = 100;
    let runningTotal = 0;
    const averages = data.map((score, index) => {
        runningTotal += score;
        return runningTotal / (index + 1);
    });
    let path = `M 0 ${200 - (averages[0] / maxVal) * 200}`;
    averages.forEach((p, i) => {
        if (i > 0) {
            const x = (500 / (averages.length - 1)) * i;
            const y = 200 - (p / maxVal) * 200;
            path += ` L ${x} ${y}`;
        }
    });
    return path;
});
</script>

<style scoped>
.admin-dashboard-page { background-color: #f8f9fa; min-height: 100vh; padding: 2rem 0; font-family: 'Segoe UI', 'Roboto', sans-serif; }
.page-header { text-align: center; margin-bottom: 2rem; }
.page-header h1 { font-weight: 700; }

/* KPI Cards */
.kpi-card { background-color: #fff; border: 1px solid #dee2e6; border-radius: 0.75rem; padding: 1.5rem; display: flex; align-items: center; }
.kpi-icon { font-size: 1.75rem; width: 60px; height: 60px; border-radius: 50%; margin-right: 1rem; color: white; display: flex; align-items: center; justify-content: center; }
.icon-subjects { background-color: #6f42c1; }
.icon-quizzes { background-color: #0d6efd; }
.icon-attempts { background-color: #fd7e14; }
.icon-score { background-color: #198754; }
.kpi-content { display: flex; flex-direction: column; }
.kpi-value { font-size: 1.75rem; font-weight: 700; }
.kpi-label { font-size: 0.9rem; color: #6c757d; }

/* Dashboard Cards */
.dashboard-card { background-color: #fff; border: 1px solid #dee2e6; border-radius: 0.75rem; height: 100%; }
.card-header { display: flex; justify-content: space-between; align-items: center; padding: 1rem 1.5rem; border-bottom: 1px solid #dee2e6; font-size: 1.2rem; font-weight: 600; }
.card-header.filter-header h3 { font-size: 1.2rem; }
.card-body { padding: 1.5rem; }
.border-bottom { border-bottom: 1px solid #dee2e6; }

/* Tables */
.table { margin-bottom: 0; }
.table thead th { border-bottom-width: 2px; }
.badge { font-weight: 600; }
.bg-danger-light { background-color: #f8d7da; }
.bg-success-light { background-color: #d1e7dd; }


/* Chart Styles */
.chart-title { font-weight: 600; color: #495057; margin-bottom: 1rem; }
.chart-wrapper { position: relative; padding-left: 35px; }
.y-axis-labels { position: absolute; left: 0; top: 0; bottom: 0; width: 30px; display: flex; flex-direction: column; justify-content: space-between; text-align: right; font-size: 0.8rem; color: #6c757d; }
.chart-container { height: 250px; display: flex; justify-content: space-around; align-items: flex-end; width: 100%; }
.chart-element { display: flex; flex-direction: column; align-items: center; height: 100%; }
.chart-bar-wrapper { display: flex; flex-direction: column; justify-content: flex-end; align-items: center; height: 100%; width: 60px; }
.chart-bar { width: 50px; background-color: #0d6efd; border-radius: 5px 5px 0 0; transition: height 0.5s ease-out; display: flex; justify-content: center; align-items: center; }
.bar-label-inside { color: white; font-size: 0.8rem; font-weight: 600; }
.chart-x-axis-label { margin-top: 0.75rem; font-weight: 600; font-size: 0.9rem; color: #495057; }
.line-chart-container { height: 250px; }
.line-chart-svg { width: 100%; height: 100%; }
.chart-path { stroke-linecap: round; stroke-linejoin: round; fill: none; stroke-width: 3; }
.attempts-path { stroke: #fd7e14; }
.avg-path { stroke: #198754; }

.mb-5 { margin-bottom: 3rem !important; }
</style>
