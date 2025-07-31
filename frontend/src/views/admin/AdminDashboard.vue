<template>
  <div class="home-page">

    <!-- Hero Section -->
    <section class="hero-section admin-hero">
        <div class="container">
            <h1 class="display-4">Platform Management Hub</h1>
            <p class="lead my-4">Oversee all platform activity, manage content, and analyze user performance from one central location.</p>
            <a href="/admin/subjects" class="btn btn-light btn-lg fw-bold px-5 py-3">Go to Classroom</a>
        </div>
    </section>

    <!-- Features Section -->
    <section class="section">
        <div class="container">
            <h2 class="section-title">Core Admin Functions</h2>
            <div class="row g-4">
                <div class="col-md-4">
                    <div class="feature-card">
                        <div class="feature-icon admin-icon"><i class="bi bi-folder-symlink-fill"></i></div>
                        <h4 class="fw-bold">Content Management</h4>
                        <p>Create, edit, and organize subjects, chapters, and quizzes with a powerful and intuitive interface.</p>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="feature-card">
                        <div class="feature-icon admin-icon"><i class="bi bi-people-fill"></i></div>
                        <h4 class="fw-bold">User Oversight</h4>
                        <p>View detailed profiles, track individual progress, and manage user accounts and permissions.</p>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="feature-card">
                        <div class="feature-icon admin-icon"><i class="bi bi-bar-chart-line-fill"></i></div>
                        <h4 class="fw-bold">Performance Analytics</h4>
                        <p>Access a comprehensive dashboard with insights on content effectiveness and user engagement.</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
        <div class="container text-center">
            <p>&copy; 2025 QuizMaster Admin Panel. All Rights Reserved.</p>
        </div>
    </footer>
  </div>
</template>

<script setup>
// No script logic needed for this static page
</script>

<style scoped>
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
.admin-hero {
    background: linear-gradient(45deg, #2d3748, #4a5568);
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
.admin-icon {
    color: #6f42c1;
}
.footer {
    background-color: #343a40;
    color: #adb5bd;
    padding: 40px 0;
}
</style>
