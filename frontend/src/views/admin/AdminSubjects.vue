<template>
  <div class="admin-dashboard">
    <div class="row g-0">
      <!-- Left Panel: Subject & Chapter List -->
      <div class="col-lg-4">
        <div class="left-panel">
          <header class="panel-header">
            <h3>Subject Management</h3>
            <button class="btn btn-primary btn-sm" @click="openSubjectCreateModal">
              <i class="bi bi-plus-circle-fill me-1"></i> New Subject
            </button>
          </header>

          <div class="subjects-list">
            <div v-for="subject in subjects" :key="subject.id" class="subject-card">
              <div class="subject-header">
                <div class="subject-title d-flex justify-content-between w-100">
                  <span>{{ subject.name }}</span>
                  <div class="d-flex justify-content-between gap-3">
                    <button type="button" class="btn btn-warning btn-sm" @click="openSubjectEditModal(subject)">Edit</button>
                    <button type="button" class="btn btn-danger btn-sm" @click="openSubjectDeleteModal(subject)">Delete</button>
                  </div>
                </div>
              </div>

              <div class="chapters-list">
                <div v-if="subject.chapters.length > 0">
                  <div
                    v-for="chapter in subject.chapters"
                    :key="chapter.id"
                    class="chapter-item"
                    :class="{ 'active': selectedChapter?.id === chapter.id }"
                    @click="selectChapter(chapter)"
                  >
                    <span>{{ chapter.name }}</span>
                    <!-- NEW: Chapter Action Buttons -->
                    <div class="chapter-actions">
                        <button class="btn btn-sm btn-light" @click.stop="openChapterEditModal(chapter)">
                            Edit
                        </button>
                        <button class="btn btn-sm btn-light text-danger ms-1" @click.stop="openChapterDeleteModal(chapter)">
                            Delete
                        </button>
                    </div>
                  </div>
                </div>
                <div v-else class="empty-chapters-message">
                  <small>No chapters found.</small>
                </div>
              </div>

              <div class="card-footer">
                <!-- MODIFIED: Button now opens the chapter creation modal -->
                <button class="btn btn-outline-secondary btn-sm w-100" @click="openChapterCreateModal(subject)">
                  <i class="bi bi-plus"></i> Add Chapter
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Panel: Canvas for Chapter Details -->
      <div class="col-lg-8">
        <div class="right-panel-canvas">
          <div v-if="selectedChapter" class="canvas-content">
            <h2>{{ selectedChapter.name }}</h2>
            <p class="text-muted">{{ selectedChapter.description }}</p>
                      <div class="quiz-management-section">
              <div class="section-header">
                <h3>Quizzes in this Chapter</h3>
                <button class="btn btn-success btn-sm" @click="createQuiz()">
                  <i class="bi bi-plus-circle-fill me-1"></i> Create Quiz
                </button>
              </div>
              <div v-if="quizzes.length > 0" class="quiz-list">
                <div v-for="quiz in quizzes" :key="quiz.id" class="quiz-item">
                  <div class="quiz-info">
                    <i class="bi bi-file-earmark-text-fill"></i>
                    <span>{{ quiz.name }}</span>
                  </div>
                  <div class="quiz-actions">
                    <button class="btn btn-sm btn-outline-secondary" @click="editQuiz(quiz)" :disabled="quiz.is_ended">Edit</button>
                    <button class="btn btn-sm btn-outline-danger ms-2" @click="deleteQuiz(quiz)" :disabled="quiz.is_ended">Delete</button>
                  </div>
                </div>
              </div>
              <div v-else class="empty-quizzes-message">
                <p>No quizzes have been created for this chapter yet.</p>
              </div>
            </div>
          </div>
          <div v-else class="canvas-placeholder">
            <i class="bi bi-arrow-left-circle"></i>
            <h3>Select a chapter</h3>
            <p>Choose a chapter from the list on the left to view its details.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Subject Modal -->
    <div v-if="showSubjectModal" class="modal-backdrop" @click.self="closeSubjectModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ modalSubjectContent.title }}</h5>
            <button type="button" class="btn-close" @click="closeSubjectModal"></button>
          </div>
          <div class="modal-body">
            <form v-if="modalSubjectContent.mode === 'create' || modalSubjectContent.mode === 'edit'" @submit.prevent="handleSubjectFormSubmit">
              <div class="mb-3">
                <label for="subjectName" class="form-label">Subject Name</label>
                <input type="text" class="form-control" id="subjectName" v-model="formSubjectData.name" required>
              </div>
              <div class="mb-3">
                <label for="subjectDescription" class="form-label">Description</label>
                <textarea class="form-control" id="subjectDescription" rows="5" v-model="formSubjectData.description" required></textarea>
              </div>
            </form>
            <p v-if="modalSubjectContent.mode === 'delete'">
              Are you sure you want to delete the subject "<strong>{{ formSubjectData.name }}</strong>"? This action cannot be undone.
            </p>
          </div>
          <div class="modal-footer d-flex justify-content-between">
            <button type="button" class="btn btn-secondary" @click="closeSubjectModal">Cancel</button>
            <button type="button" class="btn" :class="modalSubjectContent.confirmClass" @click="handleSubjectFormSubmit">
              {{ modalSubjectContent.confirmText }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- NEW: Chapter Modal -->
    <div v-if="showChapterModal" class="modal-backdrop" @click.self="closeChapterModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ modalChapterContent.title }}</h5>
            <button type="button" class="btn-close" @click="closeChapterModal"></button>
          </div>
          <div class="modal-body">
            <form v-if="modalChapterContent.mode === 'create' || modalChapterContent.mode === 'edit'" @submit.prevent="handleChapterFormSubmit">
              <div class="mb-3">
                <label for="chapterName" class="form-label">Chapter Name</label>
                <input type="text" class="form-control" id="chapterName" v-model="formChapterData.name" required>
              </div>
              <div class="mb-3">
                <label for="chapterDescription" class="form-label">Description</label>
                <textarea class="form-control" id="chapterDescription" rows="5" v-model="formChapterData.description" required></textarea>
              </div>
            </form>
            <p v-if="modalChapterContent.mode === 'delete'">
              Are you sure you want to delete the chapter "<strong>{{ formChapterData.name }}</strong>"?
            </p>
          </div>
          <div class="modal-footer d-flex justify-content-between">
            <button type="button" class="btn btn-secondary" @click="closeChapterModal">Cancel</button>
            <button type="button" class="btn" :class="modalChapterContent.confirmClass" @click="handleChapterFormSubmit">
              {{ modalChapterContent.confirmText }}
            </button>
          </div>
        </div>
      </div>
    </div>
    <!-- Quiz Delete Modal -->
    <div v-if="showQuizModal" class="modal-backdrop" @click.self="closeQuizModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ modalQuizContent.title }}</h5>
            <button type="button" class="btn-close" @click="closeQuizModal"></button>
          </div>
          <div class="modal-body">
            <p>
              Are you sure you want to delete the quiz "<strong>{{ formQuizData.name }} {{ formQuizData.id }}</strong>"? This action cannot be undone.
            </p>
          </div>
          <div class="modal-footer d-flex justify-content-between">
            <button type="button" class="btn btn-secondary" @click="closeQuizModal">Cancel</button>
            <button type="button" class="btn" :class="modalQuizContent.confirmClass" @click="handleQuizFormSubmit">
              {{ modalQuizContent.confirmText }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>

import { ref, reactive, onMounted } from 'vue';
import { useAdminSubjectStore } from '@/stores/admin/adminSubjectStore';
import { useAdminChapterStore } from '@/stores/admin/adminChapterStore';
import { useAdminQuizStore } from '@/stores/admin/adminQuizStore';
import { storeToRefs } from 'pinia';
import { useRouter } from 'vue-router';


const adminSubjectStore = useAdminSubjectStore();
const adminChapterStore = useAdminChapterStore();
const adminQuizStore = useAdminQuizStore();

const { subjects } = storeToRefs(adminSubjectStore);

const router = useRouter();

// --- State Management ---
const selectedChapter = ref(null);

// Subject Modal State
const showSubjectModal = ref(false);
const modalSubjectContent = ref({});
const formSubjectData = reactive({ id: null, name: '', description: '' });
const quizzes = ref([])

// --- Functions ---
const selectChapter = (chapter) => {
  selectedChapter.value = chapter;
  adminQuizStore.selectChapter(chapter);
  quizzes.value = chapter.quizzes;
  console.log(quizzes.value);
};

// Subject Modal Functions
const openSubjectCreateModal = () => {
  modalSubjectContent.value = { mode: 'create', title: 'Create New Subject', confirmText: 'Create Subject', confirmClass: 'btn-primary' };
  formSubjectData.id = null;
  formSubjectData.name = '';
  formSubjectData.description = '';
  showSubjectModal.value = true;
};
const openSubjectEditModal = (subject) => {
  modalSubjectContent.value = { mode: 'edit', title: `Edit Subject: ${subject.name}`, confirmText: 'Save Changes', confirmClass: 'btn-success' };
  formSubjectData.id = subject.id;
  formSubjectData.name = subject.name;
  formSubjectData.description = subject.description;
  showSubjectModal.value = true;
};
const openSubjectDeleteModal = (subject) => {
  modalSubjectContent.value = { mode: 'delete', title: 'Confirm Deletion', confirmText: 'Delete Subject', confirmClass: 'btn-danger' };
  formSubjectData.id = subject.id;
  formSubjectData.name = subject.name;
  showSubjectModal.value = true;
};
const closeSubjectModal = () => {
  showSubjectModal.value = false;
};

const handleSubjectFormSubmit = async () => {
  // console.log('Form Submitted!', { mode: modalContent.value.mode, data: formData });

  switch (modalSubjectContent.value.mode) {
    case 'create':
      await adminSubjectStore.createSubject(formSubjectData);
      alert('Subject Created');
      break;
    case 'edit':
      await adminSubjectStore.updateSubject(formSubjectData);
      alert('Changes Saved');
      break;
    case 'delete':
      await adminSubjectStore.deleteSubject(formSubjectData);
      alert('Subject Deleted');
      break;
    default:
      break;
  }
  closeSubjectModal();
}

// NEW: Chapter Modal State
const showChapterModal = ref(false);
const modalChapterContent = ref({});
const formChapterData = reactive({ id: null, name: '', description: '', subject_id: null });

// NEW: Chapter Modal Functions
const openChapterCreateModal = (subject) => {
  modalChapterContent.value = { mode: 'create', title: `Create Chapter for ${subject.name}`, confirmText: 'Create Chapter', confirmClass: 'btn-primary' };
  formChapterData.id = null;
  formChapterData.name = '';
  formChapterData.description = '';
  formChapterData.subject_id = subject.id; // Important: associate with the correct subject
  showChapterModal.value = true;
};

const openChapterEditModal = (chapter) => {
  modalChapterContent.value = { mode: 'edit', title: `Edit Chapter: ${chapter.name}`, confirmText: 'Save Changes', confirmClass: 'btn-success' };
  formChapterData.id = chapter.id;
  formChapterData.name = chapter.name;
  formChapterData.description = chapter.description;
  showChapterModal.value = true;
};

const openChapterDeleteModal = (chapter) => {
  modalChapterContent.value = { mode: 'delete', title: 'Confirm Deletion', confirmText: 'Delete Chapter', confirmClass: 'btn-danger' };
  formChapterData.id = chapter.id;
  formChapterData.name = chapter.name;
  showChapterModal.value = true;
};

const closeChapterModal = () => {
  showChapterModal.value = false;
};

const handleChapterFormSubmit = async () => {
  // console.log('Form Submitted!', { mode: modalContent.value.mode, data: formData });

  switch (modalChapterContent.value.mode) {
    case 'create':
      await adminChapterStore.createChapter(formChapterData);
      alert('Chapter Created');
      router.push('/admin/subjects');
      break;
    case 'edit':
      await adminChapterStore.updateChapter(formChapterData);
      alert('Changes Saved');
      router.push('/admin/subjects');
      break;
    case 'delete':
      await adminChapterStore.deleteChapter(formChapterData);
      alert('Chapter Deleted');
      router.push('/admin/subjects');
      break;
    default:
      break;
  }
  closeChapterModal();
}


// --- Quiz Modal State ---
const showQuizModal = ref(false);
const modalQuizContent = ref({});
const formQuizData = reactive({ id: null, name: '' });

// --- Quiz Modal Functions ---
const openQuizDeleteModal = (quiz) => {
    modalQuizContent.value = {
        mode: 'delete',
        title: 'Confirm Quiz Deletion',
        confirmText: 'Delete Quiz',
        confirmClass: 'btn-danger'
    };
    formQuizData.id = quiz.id;
    formQuizData.name = quiz.name;
    showQuizModal.value = true;
};

const closeQuizModal = () => {
    showQuizModal.value = false;
};


const createQuiz = () => {
  router.push('/admin/quiz/create');
}

const editQuiz = (quiz) => {
  adminQuizStore.selectQuiz(quiz);
  router.push(`/admin/quiz/edit/${quiz.id}`);
}

const deleteQuiz = (quiz) => {
  openQuizDeleteModal(quiz);
};

const handleQuizFormSubmit = async () => {
    await adminQuizStore.deleteQuiz(formQuizData);
    alert('Quiz deleted successfully');
    closeQuizModal();
};

onMounted(() => {
  adminSubjectStore.fetchSubjects();
});

</script>

<style scoped>
/* UNCHANGED STYLES */
.admin-dashboard { display: flex; min-height: 100vh; font-family: 'Segoe UI', 'Roboto', sans-serif; }
.row { width: 100%; }
.left-panel { background-color: #f8f9fa; border-right: 1px solid #dee2e6; height: 100vh; display: flex; flex-direction: column; overflow-y: auto; }
.panel-header { display: flex; justify-content: space-between; align-items: center; padding: 1rem 1.25rem; border-bottom: 1px solid #dee2e6; background-color: #fff; position: sticky; top: 0; z-index: 10; }
.panel-header h3 { margin: 0; font-size: 1.25rem; font-weight: 600; }
.subjects-list { padding: 1rem; display: flex; flex-direction: column; gap: 1rem; }
.subject-card { background-color: #ffffff; border: 1px solid #dee2e6; border-radius: 0.5rem; }
.subject-header { display: flex; justify-content: space-between; align-items: center; padding: 0.75rem 1rem; border-bottom: 1px solid #e9ecef; }
.subject-title { display: flex; align-items: center; gap: 0.5rem; font-weight: 800; font-size: 1.5rem; }
.chapters-list { padding: 0.5rem; }
.chapter-item { display: flex; justify-content: space-between; align-items: center; padding: 0.75rem 1rem; border-radius: 0.375rem; cursor: pointer; font-weight: 500; transition: background-color 0.2s ease, color 0.2s ease; }
.chapter-item:hover { background-color: #e9ecef; }
.chapter-item.active { background-color: #0d6efd; color: white; font-weight: 600; }
.empty-chapters-message { text-align: center; padding: 1rem; color: #6c757d; }
.card-footer { background-color: transparent; border-top: 1px solid #e9ecef; padding: 0.75rem; }
.right-panel-canvas { height: 100vh; padding: 2.5rem; overflow-y: auto; }
.canvas-placeholder { display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; text-align: center; color: #adb5bd; }
.canvas-placeholder .bi { font-size: 4rem; margin-bottom: 1rem; }
.canvas-placeholder h3 { font-weight: 600; color: #6c757d; }
.canvas-content h2 { font-weight: 700; }

/* NEW: Chapter action buttons styling */
.chapter-actions { opacity: 0.5; transition: opacity 0.2s ease-in-out; }
.chapter-item:hover .chapter-actions { opacity: 1; }

/* MODAL STYLES */
.modal-backdrop { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0, 0, 0, 0.5); display: flex; justify-content: center; align-items: center; z-index: 1050; }
.modal-dialog { width: 100%; max-width: 500px; margin: 1.75rem auto; }
.modal-content { background-color: #fff; border-radius: 0.5rem; box-shadow: 0 5px 15px rgba(0, 0, 0, 0.5); }
.modal-header { padding: 1rem 1.5rem; border-bottom: 1px solid #dee2e6; }
.modal-body { padding: 1.5rem; }
.modal-footer { padding: 1rem 1.5rem; border-top: 1px solid #dee2e6; }

/* NEW STYLES FOR QUIZ LIST */
.quiz-management-section .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
}
.quiz-management-section .section-header h3 {
    margin: 0;
    font-size: 1.5rem;
    font-weight: 600;
}
.quiz-list {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}
.quiz-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #f8f9fa;
    padding: 1rem 1.25rem;
    border: 1px solid #dee2e6;
    border-radius: 0.5rem;
}
.quiz-info {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-weight: 500;
}
.quiz-info .bi {
    color: #0d6efd;
}
.empty-quizzes-message {
    text-align: center;
    padding: 2rem;
    background-color: #f8f9fa;
    border-radius: 0.5rem;
    border: 1px dashed #ced4da;
    color: #6c757d;
}
</style>
