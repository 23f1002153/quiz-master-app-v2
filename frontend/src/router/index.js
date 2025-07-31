import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '@/views/HomeView.vue'
import SubjectView from '@/views/SubjectView.vue'
import QuizView from '@/views/QuizView.vue'
import ResultsView from '@/views/ResultView.vue'
import ProfileView from '@/views/ProfileView.vue'
import LoginView from '@/views/LoginView.vue'
import SignupView from '@/views/SignupView.vue'
import QuizzeriaView from '@/views/QuizzeriaView.vue'

// Admin views
import AdminDashboard from '@/views/admin/AdminDashboard.vue'
import AdminSubjects from '@/views/admin/AdminSubjects.vue'
import AdminCreateQuiz from '@/views/admin/AdminCreateQuiz.vue'
import AdminEditQuiz from '@/views/admin/AdminEditQuiz.vue'
import AdminUsersView from '@/views/admin/AdminUsersView.vue'
import AdminStatsView from '@/views/admin/AdminStatsView.vue'
import GuestHomeView from '@/views/GuestHomeView.vue'

// Guest views
// import WelcomeView from '@/views/guest/WelcomeView.vue'
// import HelpView from '@/views/guest/HelpView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [

    // AUTH ROUTES (USER)
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: true, role: 'user' }
    },
    {
      path: '/subject',
      name: 'subject',
      component: SubjectView,
      meta: { requiresAuth: true, role: 'user' }
    },
    {
      path: '/quizzeria',
      name: 'quizzeria',
      component: QuizzeriaView,
      meta: { requiresAuth: true, role: 'user' }
    },
    {
      path: '/quiz/:id',
      name: 'quiz_details',
      component: QuizView,
      meta: { requiresAuth: true, role: 'user' }
    },
    {
      path: '/result',
      name: 'result',
      component: ResultsView,
      meta: { requiresAuth: true, role: 'user' }
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView,
      meta: { requiresAuth: true, role: 'user' }
    },

    // ADMIN ROUTES
    {
      path: '/admin',
      name: 'admin_dashboard',
      component: AdminDashboard,
      meta: { requiresAuth: true, role: 'admin' }
    },
    {
      path: '/admin/subjects',
      name: 'admin_subjects',
      component: AdminSubjects,
      meta: { requiresAuth: true, role: 'admin' }
    },

    {
      path: '/admin/quiz/create',
      name: 'admin_quiz_create',
      component: AdminCreateQuiz,
      meta: { requiresAuth: true, role: 'admin' }
    },
    {
      path: '/admin/quiz/edit/:id',
      name: 'admin_quiz_edit',
      component: AdminEditQuiz,
      meta: { requiresAuth: true, role: 'admin' }
    },
    {
      path: '/admin/users',
      name: 'admin_users',
      component:AdminUsersView,
      meta: { requiresAuth: true, role: 'admin' }
    },
    {
      path: '/admin/stats',
      name: 'admin_stats',
      component:AdminStatsView,
      meta: { requiresAuth: true, role: 'admin' }
    },

    // PUBLIC ROUTES
    {
      path: '/guest/home',
      name: 'guest_home',
      component: GuestHomeView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView
    }
  ]
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');
  const role = localStorage.getItem('role');

  if (to.meta.requiresAuth && !token) {
    console.log("No token");
    return next('/login');
  }

  if (to.meta.role && role !== to.meta.role) {
    console.log("No role");
    return next('/login');
  }

  // Force reload when navigating to the same path
  if (to.path === from.path && JSON.stringify(to.query) === JSON.stringify(from.query)) {
    console.log("HI");
    return next({
      path: to.path,
      query: { ...to.query, reload: Date.now() }
    });
  }

  next();
});


export default router
