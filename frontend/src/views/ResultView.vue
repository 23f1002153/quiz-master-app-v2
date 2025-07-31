<template>
  <div class="results-dashboard" v-if="completedQuizzes">
    <div class="container">
      <!-- Page Header -->
      <header class="page-header">
        <h1>Performance Dashboard</h1>
        <p class="text-muted">A summary of your quiz activity and performance metrics.</p>
      </header>

      <!-- KPI Row -->
      <div class="row g-4 mb-4">
        <div class="col-md-6 col-lg-3">
          <div class="kpi-card">
            <div class="kpi-icon icon-quizzes"><i class="bi bi-journal-check"></i></div>
            <div class="kpi-content">
              <span class="kpi-value">{{ summary.quizzesAttempted }}</span>
              <span class="kpi-label">Quizzes Attempted</span>
            </div>
          </div>
        </div>
        <div class="col-md-6 col-lg-3">
          <div class="kpi-card">
            <div class="kpi-icon icon-score"><i class="bi bi-star-fill"></i></div>
            <div class="kpi-content">
              <span class="kpi-value">{{ summary.averageScore }}%</span>
              <span class="kpi-label">Average Score</span>
            </div>
          </div>
        </div>
        <div class="col-md-6 col-lg-3">
          <div class="kpi-card">
            <div class="kpi-icon icon-passrate"><i class="bi bi-check2-circle"></i></div>
            <div class="kpi-content">
              <span class="kpi-value">{{ summary.passRate }}%</span>
              <span class="kpi-label">Pass Rate</span>
            </div>
          </div>
        </div>
        <div class="col-md-6 col-lg-3">
          <div class="kpi-card">
            <div class="kpi-icon icon-time"><i class="bi bi-stopwatch-fill"></i></div>
            <div class="kpi-content">
              <span class="kpi-value">{{ summary.hours }}h {{ summary.minutes }}m</span>
              <span class="kpi-label">Total Time Spent</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Subject Performance & Score Distribution Row -->
      <div class="row g-4">
        <div class="col-lg-6">
          <div class="dashboard-card">
            <div class="card-header">
              <h3>Performance by Subject</h3>
            </div>
            <div class="card-body">
              <div class="row">
                <div class="col-md-6 mb-3">
                  <div class="subject-stat-card best">
                    <span class="label">Best Subject</span>
                    <span class="subject-name">{{ summary.bestSubject }}</span>
                  </div>
                </div>
                <div class="col-md-6 mb-3">
                  <div class="subject-stat-card weakest">
                    <span class="label">Weakest Subject</span>
                    <span class="subject-name">{{ summary.weakestSubject }}</span>
                  </div>
                </div>
              </div>
              <table class="table table-hover">
                <thead>
                  <tr>
                    <th>Subject</th>
                    <th>Quizzes Taken</th>
                    <th>Avg. Score</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="subject in performanceBySubject" :key="subject.name">
                    <td><strong>{{ subject.name }}</strong></td>
                    <td>{{ subject.quizzesTaken }}</td>
                    <td>{{ subject.avgScore }}%</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
        <div class="col-lg-6">
          <div class="dashboard-card">
            <div class="card-header">
              <h3>Score Distribution</h3>
            </div>
            <div class="card-body chart-wrapper">
              <div class="y-axis-labels"><span>100%</span><span>50%</span><span>0%</span></div>
              <div class="chart-container">
                <div v-for="subject in performanceBySubject" :key="subject.name" class="chart-element">
                  <div class="chart-bar-wrapper">
                    <span v-if="subject.avgScore < 15" class="bar-label-outside">{{ subject.avgScore }}%</span>
                    <div class="chart-bar" :style="{ height: subject.avgScore + '%' }">
                      <span v-if="subject.avgScore >= 15" class="bar-label-inside">{{ subject.avgScore }}%</span>
                    </div>
                  </div>
                  <span class="chart-x-axis-label">{{ subject.name }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Performance Over Time -->
      <div class="row g-4">
        <div class="col-12">
          <div class="dashboard-card">
            <div class="card-header">
              <h3>Performance Over Time</h3>
              <div class="d-flex gap-2">
                <select class="form-select form-select-sm" v-model="trendChartSubject">
                  <option value="All">All Subjects</option>
                  <option v-for="sub in subjects" :key="sub.id" :value="sub.name">{{ sub.name }}</option>
                </select>
                <select class="form-select form-select-sm" v-model.number="trendChartCount">
                  <option value="3">Last 3</option>
                  <option value="5">Last 5</option>
                  <option value="10">Last 10</option>
                  <option value="0">All</option>
                </select>
              </div>
            </div>
            <div class="card-body chart-wrapper">
              <div class="y-axis-labels"><span>100%</span><span>50%</span><span>0%</span></div>
              <div class="line-chart-container">
                <svg class="line-chart-svg" viewBox="0 0 500 200">
                  <line x1="0" y1="0" x2="500" y2="0" stroke="#e9ecef" />
                  <line x1="0" y1="100" x2="500" y2="100" stroke="#e9ecef" />
                  <line x1="0" y1="200" x2="500" y2="200" stroke="#dee2e6" />
                  <path :d="performancePath" class="chart-path" />
                  <g v-for="(point, index) in performancePoints" :key="index">
                    <circle :cx="point.x" :cy="point.y" r="4" class="chart-point" />
                    <!-- NEW: Text label for the score -->
                    <text :x="point.x" :y="point.y - 10" class="chart-point-label">{{ point.score }}%</text>
                    <title>{{point.score}}% on {{point.date}}</title>
                  </g>
                </svg>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Average Performance Trend -->
      <div class="row g-4">
        <div class="col-12">
          <div class="dashboard-card">
            <div class="card-header">
              <h3>Average Performance Trend</h3>
            </div>
            <div class="card-body chart-wrapper">
              <div class="y-axis-labels"><span>100%</span><span>50%</span><span>0%</span></div>
              <div class="line-chart-container">
                <svg class="line-chart-svg" viewBox="0 0 500 200">
                  <line x1="0" y1="0" x2="500" y2="0" stroke="#e9ecef" />
                  <line x1="0" y1="100" x2="500" y2="100" stroke="#e9ecef" />
                  <line x1="0" y1="200" x2="500" y2="200" stroke="#dee2e6" />
                  <path :d="averagePerformancePath" class="chart-path avg-path" />
                  <g v-for="(point, index) in averagePerformancePoints" :key="index">
                    <circle :cx="point.x" :cy="point.y" r="4" class="chart-point avg-point" />
                     <!-- NEW: Text label for the score -->
                    <text :x="point.x" :y="point.y - 10" class="chart-point-label avg-label">{{ point.score }}%</text>
                    <title>Avg. {{point.score}}%</title>
                  </g>
                </svg>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Attempts & Personal Best -->
      <div class="row g-4">
        <div class="col-lg-7">
          <div class="dashboard-card">
            <div class="card-header">
              <h3>Recent Quiz Attempts</h3>
              <button class="btn btn-outline-secondary btn-sm" @click="download"><i class="bi bi-file-earmark-spreadsheet-fill me-2"></i>Download</button>
            </div>
            <div class="card-body table-responsive">
              <table class="table table-borderless">
                <thead>
                  <tr>
                    <th>Quiz Name</th>
                    <th>Score</th>
                    <th>Percentage</th>
                    <th>Date Completed</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="quiz in recentAttempts" :key="quiz.id">
                    <td><strong>{{ quiz.name }}</strong><br><small class="text-muted">{{ quiz.subject }}</small></td>
                    <td><span class="score-badge">{{ quiz.score }}/{{ quiz.totalMarks }}</span></td>
                    <td><strong>{{ quiz.percentage }}%</strong></td>
                    <td>{{ quiz.dateCompleted }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
        <div class="col-lg-5">
          <div class="dashboard-card personal-best-card">
            <div class="card-body">
              <div class="best-icon"><i class="bi bi-trophy-fill"></i></div>
              <div class="best-content">
                  <h4>Personal Best</h4>
                  <p class="best-quiz-name">{{ highestScoringQuiz.name }}</p>
                  <small class="text-muted">Completed on {{ highestScoringQuiz.dateCompleted }}</small>
              </div>
              <div class="best-score">{{ highestScoringQuiz.percentage }}%</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue';
import apiClient from '@/components/api/axios';
import { formatDate } from '@/composables/useDateFormat';

const completedQuizzes = ref([]);
const subjects = ref([]);

// --- Chart Filters State ---
const trendChartCount = ref(10);
const trendChartSubject = ref('All');

// --- Computed Properties ---
const quizzesAttempted = computed(() => completedQuizzes.value.length);
const averageScore = computed(() => completedQuizzes.value.length === 0 ? 0 : Math.round(completedQuizzes.value.reduce((sum, quiz) => sum + quiz.percentage, 0) / completedQuizzes.value.length));
const timeSpent = computed(() => completedQuizzes.value.reduce((sum, quiz) => sum + quiz.duration, 0));

const performanceBySubjectMap = computed(() => {
    const subjectMap = {};
    subjects.value.forEach(sub => { subjectMap[sub.name] = { name: sub.name, quizzesTaken: 0, totalPercentage: 0 }; });
    completedQuizzes.value.forEach(quiz => {
        if (subjectMap[quiz.subject_name]) {
            subjectMap[quiz.subject_name].quizzesTaken++;
            subjectMap[quiz.subject_name].totalPercentage += quiz.percentage;
        }
    });
    return Object.values(subjectMap).map(sub => ({ ...sub, avgScore: sub.quizzesTaken > 0 ? Math.round(sub.totalPercentage / sub.quizzesTaken) : 0 }));
});

const download = async () => {
  try{
    const response = await apiClient.post('/jobs/export/my-history');
    alert(`${response.data.message}`)
  }
  catch(error){
    console.log(error)
  }
}

const bestSubject = computed(() => {
    if (performanceBySubjectMap.value.length === 0) return 'N/A';
    return [...performanceBySubjectMap.value].sort((a, b) => b.avgScore - a.avgScore)[0].name;
});
const weakestSubject = computed(() => {
    if (performanceBySubjectMap.value.length === 0) return 'N/A';
    return [...performanceBySubjectMap.value].sort((a, b) => a.avgScore - b.avgScore)[0].name;
});
const passRate = computed(() => {
    if (completedQuizzes.value.length === 0) return 0;
    const passedQuizzes = completedQuizzes.value.filter(q => q.percentage >= (q.passing_percentage || 50)).length;
    return Math.round((passedQuizzes / completedQuizzes.value.length) * 100);
});
const highestScoringQuiz = computed(() => {
    if (completedQuizzes.value.length === 0) return { name: 'N/A', percentage: 0, dateCompleted: '' };
    const best = completedQuizzes.value.reduce((b, c) => c.percentage > b.percentage ? c : b, {percentage: 0});
    return { ...best, name: best.quiz_name, dateCompleted: formatDate(best.attempted_at) };
});

const summary = computed(() => ({
  quizzesAttempted: quizzesAttempted.value, averageScore: averageScore.value, bestSubject: bestSubject.value,
  weakestSubject: weakestSubject.value, passRate: passRate.value,
  hours: Math.floor(timeSpent.value / 60), minutes: timeSpent.value % 60
}));

const performanceBySubject = computed(() => performanceBySubjectMap.value);

const recentAttempts = computed(() => {
    return completedQuizzes.value.slice(-3).reverse().map(attempt => ({
        id: attempt.id, name: attempt.quiz_name, subject: attempt.subject_name,
        score: attempt.total_score, totalMarks: attempt.total_marks,
        percentage: attempt.percentage, dateCompleted: formatDate(attempt.attempted_at)
    }));
});

// --- Line Chart Logic ---
const filteredTrendQuizzes = computed(() => {
    let quizzes = [...completedQuizzes.value].sort((a, b) => new Date(a.attempted_at) - new Date(b.attempted_at));
    if (trendChartSubject.value !== 'All') {
        quizzes = quizzes.filter(q => q.subject_name === trendChartSubject.value);
    }
    if (trendChartCount.value > 0) {
        return quizzes.slice(-trendChartCount.value);
    }
    return quizzes;
});

const performancePoints = computed(() => {
    const quizzes = filteredTrendQuizzes.value;
    if (quizzes.length === 0) return [];
    if (quizzes.length === 1) {
        return [{ x: 250, y: 200 - (quizzes[0].percentage * 2), score: quizzes[0].percentage, date: formatDate(quizzes[0].attempted_at) }];
    }
    return quizzes.map((quiz, index) => ({
        x: (500 / (quizzes.length - 1)) * index,
        y: 200 - (quiz.percentage * 2),
        score: quiz.percentage,
        date: formatDate(quiz.attempted_at)
    }));
});
const performancePath = computed(() => {
    if (performancePoints.value.length < 2) return '';
    return performancePoints.value.map((p, i) => (i === 0 ? 'M' : 'L') + `${p.x} ${p.y}`).join(' ');
});

const averagePerformancePoints = computed(() => {
    const quizzes = filteredTrendQuizzes.value;
    if (quizzes.length === 0) return [];
    let runningTotal = 0;
    const points = quizzes.map((quiz, index) => {
        runningTotal += quiz.percentage;
        return { avg: Math.round(runningTotal / (index + 1)), index: index };
    });

    if (quizzes.length === 1) {
        return [{ x: 250, y: 200 - (points[0].avg * 2), score: points[0].avg }];
    }

    return points.map((point) => ({
        x: (500 / (quizzes.length - 1)) * point.index,
        y: 200 - (point.avg * 2),
        score: point.avg
    }));
});
const averagePerformancePath = computed(() => {
    if (averagePerformancePoints.value.length < 2) return '';
    return averagePerformancePoints.value.map((p, i) => (i === 0 ? 'M' : 'L') + `${p.x} ${p.y}`).join(' ');
});

// --- API Calls ---
const findQuizzes = async () => { try { const r = await apiClient.get('/user/quizzes'); completedQuizzes.value = r.data.map(q => ({...q, passing_percentage: 50})); } catch(e) { console.log(e); } }
const allSubjects = async () => { try { const r = await apiClient.get('/subjects'); subjects.value = r.data; } catch(e) { console.log(e); } }
onMounted(async () => { await allSubjects(); await findQuizzes(); });
</script>

<style scoped>
.results-dashboard { background-color: #f8f9fa; min-height: 100vh; padding: 2rem 0; font-family: 'Segoe UI', 'Roboto', sans-serif; }
.page-header { text-align: center; margin-bottom: 2rem; }
.page-header h1 { font-weight: 700; }
.kpi-card { background-color: #fff; border: 1px solid #dee2e6; border-radius: 0.75rem; padding: 1.5rem; display: flex; align-items: center; height: 100%; }
.kpi-icon { font-size: 2rem; padding: 1rem; border-radius: 50%; margin-right: 1rem; color: white; }
.icon-quizzes { background-color: #0d6efd; }
.icon-score { background-color: #198754; }
.icon-passrate { background-color: #0dcaf0; }
.icon-time { background-color: #fd7e14; }
.kpi-content { display: flex; flex-direction: column; }
.kpi-value { font-size: 1.75rem; font-weight: 700; }
.kpi-label { font-size: 0.9rem; color: #6c757d; }
.dashboard-card { background-color: #fff; border: 1px solid #dee2e6; border-radius: 0.75rem; height: 100%; }
.card-header { display: flex; justify-content: space-between; align-items: center; padding: 1rem 1.5rem; border-bottom: 1px solid #dee2e6; }
.card-header h3 { font-size: 1.2rem; font-weight: 600; margin: 0; }
.card-body { padding: 1.5rem; }
.table { margin-bottom: 0; }
.table thead th { border-bottom-width: 2px; }
.score-badge { background-color: #e7f1ff; color: #0d6efd; padding: 0.3rem 0.6rem; border-radius: 5px; font-weight: 600; }

/* Subject Stat Cards */
.subject-stat-card { border-radius: 0.5rem; padding: 1rem; text-align: center; }
.subject-stat-card .label { font-size: 0.9rem; font-weight: 500; }
.subject-stat-card .subject-name { font-size: 1.2rem; font-weight: 700; display: block; }
.subject-stat-card.best { background-color: #d1e7dd; color: #0f5132; }
.subject-stat-card.weakest { background-color: #f8d7da; color: #842029; }

/* Chart Wrapper with Axes */
.chart-wrapper { position: relative; padding-left: 35px; padding-bottom: 20px; }
.y-axis-labels { position: absolute; left: 0; top: 0; bottom: 20px; width: 30px; display: flex; flex-direction: column; justify-content: space-between; text-align: right; font-size: 0.8rem; color: #6c757d; }
.chart-container { height: 250px; }

/* Bar Chart */
.chart-container { display: flex; justify-content: space-around; align-items: flex-end; width: 100%; }
.chart-element { display: flex; flex-direction: column; align-items: center; height: 100%; }
.chart-bar-wrapper { display: flex; flex-direction: column; justify-content: flex-end; align-items: center; height: 100%; width: 60px; }
.chart-bar { width: 50px; background-color: #0d6efd; border-radius: 5px 5px 0 0; transition: height 0.5s ease-out; display: flex; justify-content: center; align-items: center; }
.bar-label-inside { color: white; font-size: 0.8rem; font-weight: 600; }
.bar-label-outside { color: #212529; font-size: 0.8rem; font-weight: 600; margin-bottom: 4px; }
.chart-x-axis-label { margin-top: 0.75rem; font-weight: 600; font-size: 0.9rem; color: #495057; }

/* Line Chart */
.line-chart-svg { width: 100%; height: 100%; overflow: visible; }
.chart-path { stroke-linecap: round; stroke-linejoin: round; fill: none; stroke-width: 3; stroke: #0d6efd;}
.chart-path.avg-path { stroke: #198754; }
.chart-point { fill: #0d6efd; stroke: white; stroke-width: 2; cursor: pointer; }
.chart-point.avg-point { fill: #198754; }
.chart-point:hover { r: 6; }
.chart-point-label {
  text-anchor: middle;
  font-size: 6px;
  font-weight: 600;
  fill: #212529;
}
.chart-point-label.avg-label {
  fill: #198754;
}

/* Personal Best Card */
.personal-best-card { display: flex; align-items: center; padding: 1.5rem; text-align: center; }
.best-icon { font-size: 3rem; color: #ffc107; }
.best-content { flex-grow: 1; padding: 0 1rem; }
.best-content h4 { font-size: 1.1rem; font-weight: 600; }
.best-quiz-name { font-size: 1rem; margin: 0; color: #6c757d; }
.best-score { font-size: 2.5rem; font-weight: 700; color: #198754; }

.g-4 { margin-top: 0 !important; }
</style>
