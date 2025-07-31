<template>
  <div class="home-page">

    <!-- Hero Section -->
    <section class="hero-section user-hero">
        <div class="container">
            <h1 class="display-4">Test Your Knowledge, Master Your Subjects</h1>
            <p class="lead my-4">Engage with interactive quizzes across a wide range of subjects and track your learning journey like never before.</p>
            <button class="btn btn-light btn-lg fw-bold px-5 py-3">Get Started Now</button>
        </div>
    </section>

    <!-- Features Section -->
    <section class="section">
        <div class="container">
            <h2 class="section-title">Why Choose QuizMaster?</h2>
            <div class="row g-4">
                <div class="col-md-4">
                    <div class="feature-card">
                        <div class="feature-icon user-icon"><i class="bi bi-bookshelf"></i></div>
                        <h4 class="fw-bold">Diverse Subjects</h4>
                        <p>From Mathematics to History, explore a vast library of quizzes designed to challenge and educate.</p>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="feature-card">
                        <div class="feature-icon user-icon"><i class="bi bi-graph-up-arrow"></i></div>
                        <h4 class="fw-bold">Track Your Progress</h4>
                        <p>Our detailed performance dashboard helps you visualize your strengths and weaknesses over time.</p>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="feature-card">
                        <div class="feature-icon user-icon"><i class="bi bi-controller"></i></div>
                        <h4 class="fw-bold">Interactive Experience</h4>
                        <p>Engage with a modern, user-friendly interface that makes learning and testing your knowledge fun.</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- How It Works Section -->
    <section class="section bg-white">
        <div class="container">
            <h2 class="section-title">Get Started in 3 Easy Steps</h2>
            <div class="row g-5">
                <div class="col-md-4">
                    <div class="how-it-works-step">
                        <div class="step-number">1</div>
                        <h4 class="fw-bold">Choose a Subject</h4>
                        <p class="text-muted">Browse our extensive collection of subjects and pick a chapter you want to master.</p>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="how-it-works-step">
                        <div class="step-number">2</div>
                        <h4 class="fw-bold">Take the Quiz</h4>
                        <p class="text-muted">Answer multiple-choice questions within the time limit in our distraction-free quiz interface.</p>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="how-it-works-step">
                        <div class="step-number">3</div>
                        <h4 class="fw-bold">Review Your Results</h4>
                        <p class="text-muted">Get instant feedback on your performance, see the correct answers, and track your scores.</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
        <div class="container text-center">
            <p>&copy; 2025 QuizMaster. All Rights Reserved.</p>
        </div>
    </footer>
  </div>
</template>

<script setup>
// No script logic needed for this static page
</script>

<style scoped>
/* Scoped styles ensure they don't leak to other components */
.home-page {
    font-family: 'Poppins', sans-serif;
    background-color: #f8f9fa;
}
.navbar {
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}
.hero-section {
    color: white;
    padding: 100px 0;
    text-align: center;
}
.user-hero {
    background: linear-gradient(45deg, #0d6efd, #6f42c1);
}
.hero-section h1 {
    font-weight: 700;
    font-size: 3.5rem;
}
.hero-section p {
    font-size: 1.25rem;
    opacity: 0.9;
}
.section {
    padding: 80px 0;
}
.section-title {
    text-align: center;
    margin-bottom: 50px;
    font-weight: 600;
    font-size: 2.5rem;
}
.feature-card {
    background-color: #fff;
    border: 1px solid #dee2e6;
    border-radius: 0.75rem;
    padding: 2rem;
    text-align: center;
    transition: all 0.3s ease;
    height: 100%;
}
.feature-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}
.feature-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
}
.user-icon {
    color: #0d6efd;
}
.how-it-works-step {
    text-align: center;
}
.step-number {
    width: 60px;
    height: 60px;
    background-color: #e7f1ff;
    color: #0d6efd;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    font-weight: 700;
    margin: 0 auto 1rem;
}
.footer {
    background-color: #343a40;
    color: #adb5bd;
    padding: 40px 0;
}
</style>

