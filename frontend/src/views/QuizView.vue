<template>
  <div v-if="selectedQuiz.is_ended">
    <QuizResult/>
  </div>
  <div v-else>
    <QuizFront v-if="!startedQuiz" @startQuiz="startedQuiz = true"/>
    <QuizPage v-else />
  </div>

</template>

<script setup>
import QuizFront from '@/components/quiz/QuizFront.vue';
import QuizPage from '@/components/quiz/QuizPage.vue';
import { ref } from 'vue';
import { useQuizStore } from '@/stores/quizStore';
import { storeToRefs } from 'pinia';
import QuizResult from '@/components/quiz/QuizResult.vue';

const quizStore = useQuizStore();
const { selectedQuiz } = storeToRefs(quizStore);

const startedQuiz = ref(false);


</script>
