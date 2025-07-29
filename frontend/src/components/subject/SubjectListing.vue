
<template>
  <h1 class="text-center border-bottom border-black fw-bold">
    Subjects
  </h1>
  <div v-if="!subjectStore.loading">
    <div v-if="subjectStore.subjects.length > 0">
      <div v-for="subject in subjectStore.subjects" :key="subject.id">
        <SubjectChapter :subject_id="subject.id"/>
      </div>
    </div>
    <div v-else>
      No subjects
    </div>
  </div>
  <div v-else>
    LOADING
  </div>
</template>

<script setup>
import SubjectChapter from '@/components/subject/SubjectChapter.vue';
import { useSubjectStore } from '@/stores/subjectStore';
import { onMounted} from 'vue';

const subjectStore = useSubjectStore();

onMounted(() => {
  subjectStore.fetchSubjects();
})

</script>
