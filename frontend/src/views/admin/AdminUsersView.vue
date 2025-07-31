<template>
  <div class="admin-users-page">
    <div class="container">
      <!-- 1. Page Header -->
      <header class="page-header">
        <h1>User Management</h1>
        <p class="text-muted">View, search, and manage all users on the platform.</p>
      </header>

      <!-- 2. High-Level KPI Cards -->
      <div class="row g-4 mb-4">
        <div class="col-md-6 col-lg-3">
          <div class="kpi-card">
            <div class="kpi-icon icon-total"><i class="bi bi-people-fill"></i></div>
            <div class="kpi-content">
              <span class="kpi-value">{{ summary.total_users }}</span>
              <span class="kpi-label">Total Users</span>
            </div>
          </div>
        </div>
        <div class="col-md-6 col-lg-3">
          <div class="kpi-card">
            <div class="kpi-icon icon-active"><i class="bi bi-person-check-fill"></i></div>
            <div class="kpi-content">
              <span class="kpi-value">{{ summary.active_today }}</span>
              <span class="kpi-label">Users Active Today</span>
            </div>
          </div>
        </div>
        <div class="col-md-6 col-lg-3">
          <div class="kpi-card">
            <div class="kpi-icon icon-new"><i class="bi bi-person-plus-fill"></i></div>
            <div class="kpi-content">
              <span class="kpi-value">{{ summary.last_30days_newUsers }}</span>
              <span class="kpi-label">New Users (30d)</span>
            </div>
          </div>
        </div>
        <div class="col-md-6 col-lg-3">
          <div class="kpi-card">
            <div class="kpi-icon icon-suspended"><i class="bi bi-person-x-fill"></i></div>
            <div class="kpi-content">
              <span class="kpi-value">{{ summary.suspended_accounts }}</span>
              <span class="kpi-label">Suspended Accounts</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 3. Filter & Search Bar -->
      <div class="card filter-card">
        <div class="card-body d-flex gap-3">
          <div class="input-group">
            <span class="input-group-text"><i class="bi bi-search"></i></span>
            <input type="text" class="form-control" placeholder="Search by name or email..." v-model="searchQuery">
          </div>
          <select class="form-select" v-model="statusFilter">
            <option value="All">All Statuses</option>
            <option value="Active">Active</option>
            <option value="Suspended">Suspended</option>
          </select>
        </div>
      </div>

      <!-- 4. Users Table -->
      <div class="card users-table-card">
        <div class="table-responsive table-scroll-wrapper">
          <table class="table table-hover align-middle mb-0">
            <thead>
              <tr>
                <th>User</th>
                <th>Quizzes Attempted</th>
                <th>Average Score</th>
                <th>Last Active</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in filteredUsers" :key="user.id">
                <td>
                  <div class="user-info">
                    <!-- <img :src="user.avatar" class="user-avatar" alt="Avatar"> -->
                    <div>
                      <div class="user-name">{{ user.username }}</div>
                      <div class="user-email">{{ user.email }}</div>
                    </div>
                  </div>
                </td>
                <td>{{ user.attempts.length }}</td>
                <td>{{ getAverage(user) }}%</td>
                <td>{{ formatDate(user.last_login) }}</td>
                <td>
                  <span class="badge" :class="user.status === 'Active' ? 'bg-success-light text-success' : 'bg-danger-light text-danger'">
                    {{ user.status }}
                  </span>
                </td>
                <td>
                  <div class="action-buttons">
                    <button class="btn btn-sm btn-outline-secondary" @click="openProfileModal(user)">View Profile</button>
                    <button class="btn btn-sm btn-outline-danger ms-2">Suspend</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- MODIFIED: User Profile Modal with full details -->
    <div v-if="showProfileModal && selectedUser" class="modal-backdrop" @click.self="closeProfileModal">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">User Profile: {{ selectedUser.name }}</h5>
            <button type="button" class="btn-close" @click="closeProfileModal"></button>
          </div>
          <div class="modal-body">
            <div class="row">
              <!-- Left Side: Avatar & Personal Info -->
              <div class="col-md-5">
                <!-- <div class="text-center mb-4">
                  <img :src="selectedUser.avatar.replace('40x40', '120x120')" class="profile-modal-avatar" alt="Avatar">
                </div> -->
                <h5>Personal Details</h5>
                <dl class="details-list">
                  <dt>Username</dt><dd>{{ selectedUser.name }}</dd>
                  <dt>Email</dt><dd>{{ selectedUser.email }}</dd>
                  <dt>Phone</dt><dd>{{ selectedUser.phone }}</dd>
                  <dt>Gender</dt><dd>{{ selectedUser.gender }}</dd>
                  <dt>Date of Birth</dt><dd>{{ formatDate(selectedUser.dob) }}</dd>
                </dl>
              </div>
              <!-- Right Side: Academic & Account Info -->
              <div class="col-md-7">
                <h5>Academic Background</h5>
                <dl class="details-list">
                  <dt>Qualification</dt><dd>{{ selectedUser.qualification }}</dd>
                  <dt>College</dt><dd>{{ selectedUser.college }}</dd>
                </dl>
                <hr class="my-4">
                <h5>Account Activity</h5>
                <dl class="details-list">
                  <dt>User ID</dt><dd>{{ selectedUser.id }}</dd>
                  <dt>Joining Date</dt><dd>{{ formatDate(selectedUser.joiningDate) }}</dd>
                  <dt>Last Login</dt><dd>{{ formatDate(selectedUser.last_login) }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import apiClient from '@/components/api/axios';
import { formatDate } from '@/composables/useDateFormat';
import { ref, computed, onMounted } from 'vue';


// --- State for Profile Modal ---
const showProfileModal = ref(false);
const selectedUser = ref(null);

const users = ref([]);

const fetchUsers = async () => {
  const response = await apiClient.get('/users/all')
  users.value = response.data.users;
}

const today = new Date();
const daysAgo = (days) => {
  const d = new Date();
  d.setDate(d.getDate() - days);
  return d;
};

const summary = computed(() => ({
  total_users: users.value.length,
  active_today: users.value.reduce(
    (count, user) =>
      count + (formatDate(user.last_login) === formatDate(today) ? 1 : 0),
    0
  ),
  last_30days_newUsers: users.value.reduce(
    (count, user) =>
      count + (new Date(user.joiningDate) >= daysAgo(30) ? 1 : 0),
    0
  ),
  suspended_accounts: users.value.reduce(
    (count, user) => count + (user.status === 'Suspended' ? 1 : 0),
    0
  )
}));

const getAverage = (user) => {
  const total = user.attempts.reduce((sum, attempt) => sum + attempt.percentage, 0);
  return Math.round(total / user.attempts.length);
};

// --- State for Filters ---
const searchQuery = ref('');
const statusFilter = ref('All');

// --- Filtering Logic ---
const filteredUsers = computed(() => {
  let userList = [...users.value];
  if (statusFilter.value !== 'All') {
    userList = userList.filter(user => user.status === statusFilter.value);
  }
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    userList = userList.filter(user =>
      user.username.toLowerCase().includes(query) ||
      user.email.toLowerCase().includes(query)
    );
  }
  return userList;
});

// --- Modal Functions ---
const openProfileModal = (user) => {
  selectedUser.value = user;
  showProfileModal.value = true;
};
const closeProfileModal = () => {
  showProfileModal.value = false;
  selectedUser.value = null;
};

onMounted(() => fetchUsers());

</script>

<style scoped>
.admin-users-page { background-color: #f8f9fa; min-height: 100vh; padding: 2rem 0; font-family: 'Segoe UI', 'Roboto', sans-serif; }
.page-header { text-align: center; margin-bottom: 2rem; }
.page-header h1 { font-weight: 700; }

/* KPI Cards */
.kpi-card { background-color: #fff; border: 1px solid #dee2e6; border-radius: 0.75rem; padding: 1.5rem; display: flex; align-items: center; }
.kpi-icon { font-size: 1.75rem; width: 60px; height: 60px; border-radius: 50%; margin-right: 1rem; color: white; display: flex; align-items: center; justify-content: center; }
.icon-total { background-color: #0d6efd; }
.icon-active { background-color: #198754; }
.icon-new { background-color: #6f42c1; }
.icon-suspended { background-color: #dc3545; }
.kpi-content { display: flex; flex-direction: column; }
.kpi-value { font-size: 1.75rem; font-weight: 700; }
.kpi-label { font-size: 0.9rem; color: #6c757d; }

/* Filter Card */
.filter-card { margin-bottom: 1.5rem; border: 1px solid #dee2e6; }
.filter-card .form-select { max-width: 200px; }

/* Users Table */
.users-table-card { border: 1px solid #dee2e6; border-radius: 0.75rem; overflow: hidden; }
.table-scroll-wrapper { max-height: 60vh; overflow-y: auto; }
.table thead th { background-color: #f8f9fa; font-weight: 600; color: #495057; position: sticky; top: 0; z-index: 1; }
.table td, .table th { vertical-align: middle; }
.user-info { display: flex; align-items: center; gap: 1rem; }
.user-avatar { width: 40px; height: 40px; border-radius: 50%; }
.user-name { font-weight: 600; }
.user-email { font-size: 0.9rem; color: #6c757d; }
.badge { padding: 0.4rem 0.75rem; font-weight: 600; font-size: 0.8rem; }
.bg-success-light { background-color: #d1e7dd; }
.bg-danger-light { background-color: #f8d7da; }

/* Profile Modal Styles */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1050;
  padding: 1rem;
  box-sizing: border-box;
}

.modal-dialog {
  max-width: 1200px;
  background-color: #fff8e1; /* softened orange tone */
  border-radius: 12px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
  padding: 2rem;
  width: 100%;
}

.profile-modal-avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  border: 4px solid #fff;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  margin: 0 auto 1rem;
  display: block;
}

.details-list {
  display: grid;
  grid-template-columns: 120px 1fr;
  gap: 1rem 1.5rem;
  margin-top: 1.5rem;
}

.details-list dt {
  font-weight: 600;
  color: #555;
  text-align: right;
}

.details-list dd {
  margin: 0;
  font-weight: 500;
  color: #222;
  word-break: break-word;
}

@media (max-width: 600px) {
  .details-list {
    grid-template-columns: 1fr;
    text-align: left;
  }

  .details-list dt {
    text-align: left;
  }
}

</style>
