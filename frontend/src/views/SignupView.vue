<template>
  <div class="d-flex justify-content-center align-items-center vh-100 bg-light">
    <div class="card shadow-lg p-4" style="width: 100%; max-width: 500px; border-radius: 1rem;">
      <!-- Logo -->
      <div class="text-center mb-1">
        <img src="@/assets/logo.png" alt="QuizMaster Pro" class="rounded-circle" style="width: 100px; height: 100px;" />
        <h2 class="mt-2 fw-bold">Create Account</h2>
      </div>

        <div class="text-center mb-0">
          <p class="text-danger fs-6">{{ errorType }}</p>
        </div>

      <!-- Signup Form -->
      <form @submit.prevent="signup">
        <div class="mb-1">
          <label class="form-label mb-0 fs-5">Username</label>
          <input type="text" class="form-control" v-model="username" required />
        </div>

        <div class="mb-2">
          <label class="form-label mb-0 fs-5">Email</label>
          <input type="email" class="form-control" v-model="email" required />
        </div>

        <div class="mb-2">
          <label class="form-label mb-0 fs-5">Gender</label>
          <select class="form-select" v-model="gender" required>
            <option value="" disabled>Select Gender</option>
            <option>Male</option>
            <option>Female</option>
            <option>Other</option>
          </select>
        </div>

        <div class="mb-2">
          <label class="form-label mb-0 fs-5">Date of Birth</label>
          <input type="date" class="form-control" v-model="dob" :max="today" required />
        </div>

        <div class="mb-2">
          <label class="form-label mb-0 fs-5">Qualification</label>
          <input type="text" class="form-control" v-model="qualification" required />
        </div>

        <div class="mb-2">
          <label class="form-label mb-0 fs-5">College</label>
          <input type="text" class="form-control" v-model="college" required />
        </div>

        <div class="mb-2">
          <label class="form-label mb-0 fs-5">Phone</label>
          <input type="tel" class="form-control" v-model="phone" required />
          <small v-if="!validPhone" class="text-danger">Please enter a valid phone number</small>
        </div>

        <div class="mb-2">
          <label class="form-label mb-0 fs-5">Password</label>
          <input type="password" class="form-control" v-model="password" required minlength="6" />
          <small v-if="!validPassword" class="text-danger">Password must be atleast 6 characters</small>
        </div>

        <div class="mb-2">
          <label class="form-label mb-0 fs-5">Confirm Password</label>
          <input type="password" class="form-control" v-model="confirmPassword" required />
          <small v-if="passwordsMismatch" class="text-danger">Passwords do not match</small>
        </div>

        <button type="submit" class="btn btn-success w-100" :disabled="passwordsMismatch">Sign Up</button>
        <div class="text-center mt-2">
          <a href="/login" class="text-decoration-none">Already have an account? Login</a>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import apiClient from '@/components/api/axios';
import { useRouter } from 'vue-router';

const username = ref('');
const email = ref('');
const gender = ref('');
const dob = ref('');
const qualification = ref('');
const college = ref('');
const phone = ref('');
const password = ref('');
const confirmPassword = ref('');

const passwordsMismatch = computed(() => password.value !== confirmPassword.value);
const validPassword = computed(() => password.value.length >= 6 || password.value.length === 0);
const validPhone = computed(() => /^\d{10}$/.test(phone.value) || phone.value.length === 0);
const today = new Date().toISOString().split('T')[0];
const router = useRouter();
const errorType = ref('');

const signup = async () => {
  if (passwordsMismatch.value) return;

  const payload = {
    username: username.value,
    email: email.value,
    gender: gender.value,
    dob: dob.value,
    qualification: qualification.value,
    college: college.value,
    phone: Number(phone.value),
    password: password.value,
  };

  try {
    await apiClient.post('/auth/register', payload);
    alert('Signup successful!');
    router.push('/login');
    return
  } catch (error) {
    if(error.response.status === 409){
      let message = error.response.data.message;
      console.log(message);
      errorType.value = message;
      console.log(errorType.value);
    }
    else{
      console.log("Something went wrong");
    }
  }
};
</script>
