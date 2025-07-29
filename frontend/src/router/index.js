import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import AboutView from '@/views/AboutView.vue'
import SubjectView from '@/views/SubjectView.vue'
import QuizView from '@/views/QuizView.vue'
import ResultsView from '@/views/ResultView.vue'
import ProfileView from '@/views/ProfileView.vue'
import LoginView from '@/views/LoginView.vue'
import SignupView from '@/views/SignupView.vue'
import QuizzeriaView from '@/views/QuizzeriaView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: true }
    },
    {
      path: '/about',
      name: 'about',
      component: AboutView,
      meta: { requiresAuth: true }
    },
    {
      path: '/subject',
      name: 'subject',
      component: SubjectView,
      meta: { requiresAuth: true }
    },
    {
      path: '/quizzeria',
      name: 'quizzeria',
      component: QuizzeriaView,
      meta: { requiresAuth: true }
    },

    // To be added later
    {
      path: '/quiz/:id',
      name: 'quiz_details',
      component: QuizView
    },

    {
      path: '/result',
      name: 'result',
      component: ResultsView,
      meta: { requiresAuth: true }
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView,
      meta: { requiresAuth: true }
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
    },
  ],
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');

  if (to.meta.requiresAuth && !token) {
    next('/login'); // redirect to login if no token
  } else {
    next();
  }
});

export default router
