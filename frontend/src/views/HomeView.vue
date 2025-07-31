<template>
  <div class="user-home-page">
    <!-- 2. Main Content Area -->
    <main class="container py-5">
      <!-- Welcome Header -->
      <header class="welcome-header mb-5">
        <h1>Welcome back, Alex!</h1>
        <p class="lead text-muted">Ready to continue your learning journey?</p>
      </header>

      <!-- Action Cards -->
      <div class="row g-4">
        <div class="col-lg-8">
          <div class="action-card primary-card">
            <div class="action-content">
              <i class="bi bi-easel2-fill action-icon"></i>
              <h2>Go to Classroom</h2>
              <p>Dive back into your subjects, review chapters, and take new quizzes.</p>
              <a href="/subject" class="btn btn-light stretched-link">Start Learning <i class="bi bi-arrow-right-short"></i></a>
            </div>
          </div>
        </div>
        <div class="col-lg-4">
          <div class="action-card secondary-card">
            <div class="action-content">
              <i class="bi bi-bar-chart-line-fill action-icon"></i>
              <h2>View My Results</h2>
              <p>Analyze your performance and track your progress.</p>
              <a href="/result" class="btn btn-dark stretched-link">Check Dashboard</a>
            </div>
          </div>
        </div>
        <div class="col-lg-4">
          <div class="action-card secondary-card">
            <div class="action-content">
              <i class="bi bi-person-fill-gear action-icon"></i>
              <h2>My Profile</h2>
              <p>Update your personal details and account settings.</p>
              <a href="/profile" class="btn btn-dark stretched-link">Edit Profile</a>
            </div>
          </div>
        </div>
        <div class="col-lg-8">
            <div class="action-card secondary-card">
            <div class="action-content">
              <i class="bi bi-trophy-fill action-icon"></i>
              <h2>View Completed Quizzes</h2>
              <p>Review your past attempts and see detailed results for each quiz.</p>
              <a href="/result" class="btn btn-dark stretched-link">See History</a>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
// No script logic is needed for this static page.
</script>

<style scoped>
.user-home-page {
  background-color: #f8f9fa;
  min-height: 100vh;
  font-family: 'Poppins', sans-serif;
}
.navbar {
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}
.welcome-header {
  text-align: center;
}
.welcome-header h1 {
  font-weight: 700;
  font-size: 2.5rem;
}

/* Action Cards */
.action-card {
  border-radius: 1rem;
  padding: 2.5rem;
  color: white;
  position: relative;
  overflow: hidden;
  height: 100%;
  transition: transform 0.3s ease;
}
.action-card:hover {
    transform: translateY(-5px);
}
.primary-card {
  background: linear-gradient(45deg, #0d6efd, #3c8ffb);
}
.secondary-card {
  background-color: #ffffff;
  color: #212529;
  border: 1px solid #dee2e6;
}
.action-content h2 {
  font-weight: 600;
  margin-bottom: 0.5rem;
}
.action-content p {
  opacity: 0.9;
  margin-bottom: 1.5rem;
}
.action-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  display: block;
}
.stretched-link::after {
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    z-index: 1;
    content: "";
}
</style>
