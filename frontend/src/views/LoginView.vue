<template>
  <div class="d-flex justify-content-center align-items-center vh-100 bg-light">
    <div class="card shadow-lg p-4" style="width: 100%; max-width: 400px; border-radius: 1rem;">
      <!-- Logo -->
      <div class="text-center mb-4">
        <img src="@/assets/logo.png" alt="QuizMaster Pro" class="rounded-circle" style="width: 120px; height: 120px;" />
        <h2 class="mt-2 fw-bold">QuizMaster Pro</h2>
      </div>

      <div class="text-center mt-2">
        <p class="text-danger fs-6">{{ errorType }}</p>
      </div>

      <!-- Login Form -->
      <form @submit.prevent="login">
        <div class="mb-3 fs-5">
          <label class="form-label">Username</label>
          <input type="text" class="form-control" v-model="username" required />
        </div>

        <div class="mb-3 fs-5">
          <label class="form-label">Password</label>
          <input type="password" class="form-control" v-model="password" required />
        </div>

        <button type="submit" class="btn btn-primary w-100 fs-5">Login</button>
      </form>
      <div class="text-center mt-2">
        <a href="/signup" class="text-decoration-none">New user? Signup</a>
      </div>
    </div>
  </div>
</template>

<script setup>
import apiClient from '@/components/api/axios';
import { useRouter } from 'vue-router';
import { ref } from 'vue';

const errorType = ref('');
const router = useRouter();

const username = ref('');
const password = ref('');

const login = async () => {
  // Handle login logic
  const data = {
    'username': username.value,
    'password': password.value
  }

  try{
    const response = await apiClient.post('/auth/login', data);
    const token = response.data.access_token;
    localStorage.setItem('token', token);
    router.push('/');
    alert("Login Successful")
  }
  catch(error){
    if (error.response){
      errorType.value = error.response.data.message;
    }
    console.log(error);
  }
}
</script>
