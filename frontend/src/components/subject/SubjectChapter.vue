<template>
  <div class="card subject-accordion my-3">
    <div v-if="subject">
      <div
        class="subject-header card-header d-flex justify-content-between align-items-center"
        @click="showChapters = !showChapters"
      >
        <h2 class="mb-0 fs-5 fw-bold">{{ subject.name }}</h2>
        <span class="toggle-icon" :class="{ 'expanded': showChapters }">
          <i class="bi bi-chevron-down"></i>
        </span>
      </div>

      <transition name="slide-fade">
        <div v-show="showChapters">
          <div v-if="loadingChapters" class="state-message">
            <div class="spinner-border spinner-border-sm" role="status"></div>
            <span class="ms-2">Loading Chapters...</span>
          </div>

          <div v-else>
            <ul v-if="chapters.length > 0" class="list-group list-group-flush">
              <li
                class="chapter-item list-group-item"
                v-for="chapter in chapters"
                :key="chapter.id"
                @click="chapterStore.selectChapter(props.subject_id, chapter.id)"
              >
                {{ chapter.name }}
              </li>
            </ul>
            <div v-else class="state-message">
              No chapters found for this subject.
            </div>
          </div>
        </div>
      </transition>
    </div>

    <div v-else class="card-body state-message">
      No subject selected.
    </div>
  </div>
</template>

<script setup>

import { onMounted, ref, computed } from 'vue'
import { useChapterStore } from '@/stores/chapterStore';
import { useSubjectStore } from '@/stores/subjectStore';
import { storeToRefs } from 'pinia';

const props = defineProps(['subject_id']);
const showChapters = ref(false);

const chapterStore = useChapterStore();
const subjectStore = useSubjectStore();

const { chaptersBySubject, loadingSubjectIds } = storeToRefs(chapterStore);

const chapters = computed(() => chaptersBySubject.value[props.subject_id] || []);
const loadingChapters = computed(() => loadingSubjectIds.value.has(props.subject_id));

const subject = ref(null);

onMounted(() => {
  chapterStore.fetchChapters(props.subject_id),
  subject.value = subjectStore.getSubject(props.subject_id)
})

</script>

<style scoped>
/* Main Accordion Card */
.subject-accordion {
  border: 1px solid #dee2e6;
  border-radius: 0.5rem;
  overflow: hidden; /* Important for containing the sliding list */
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

/* Clickable Header Styling */
.subject-header {
  cursor: pointer;
  background-color: var(--bs-primary);
  color: white;
  padding: 1rem 1.25rem;
  user-select: none; /* Prevents text selection on click */
}

/* Toggle Icon Animation */
.toggle-icon {
  font-size: 1.2rem;
  transition: transform 0.3s ease-in-out;
}
.toggle-icon.expanded {
  transform: rotate(180deg);
}

/* Chapter Item Styling & Hover Effect */
.chapter-item {
  cursor: pointer;
  padding: 0.9rem 1.25rem;
  border-bottom: 1px solid #f1f1f1;
  transition: background-color 0.2s ease, color 0.2s ease;
}
.chapter-item:last-child {
  border-bottom: none;
}
.chapter-item:hover {
  background-color: #f8f9fa; /* A light grey */
  color: var(--bs-primary);
}

/* Message Styling for "Loading" or "No Chapters" */
.state-message {
  padding: 1.5rem;
  text-align: center;
  color: #6c757d; /* Bootstrap's secondary text color */
  background-color: #fafafa;
}

/* Vue Transition for the slide-down/up effect */
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.35s ease-out;
}
.slide-fade-enter-from,
.slide-fade-leave-to {
  max-height: 0;
  opacity: 0;
  transform: translateY(-10px);
}
.slide-fade-enter-to,
.slide-fade-leave-from {
  max-height: 500px; /* Set a max-height larger than your content */
  opacity: 1;
  transform: translateY(0);
}
</style>

