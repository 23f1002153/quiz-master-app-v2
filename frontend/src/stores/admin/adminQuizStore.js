import { defineStore } from "pinia";
import apiClient from "@/components/api/axios";


export const useAdminQuizStore = defineStore('adminQuizStore', {
  state: () => ({
    chapter_id: null,
    selectedQuiz: null,
    selectedQuestions: null,
    quizzes: [],
  }),

  actions: {

    selectChapter(chapter){
      this.chapter_id = chapter.id;
    },


    selectQuiz(quiz) {
      this.selectedQuiz = quiz;
    },

    async fetchQuizzes () {
      try{
        const response = await apiClient.get(`/quizzes/${this.chapter_id}`);
        this.quizzes = response.data;
      }
      catch(error){
        console.log(error)
      }
    },

    async fetchQuestions() {
      try{
        const response = await apiClient.get(`/quiz/${this.selectedQuiz.id}/questions`);
        this.selectedQuestions = response.data;
      }
      catch(error){
        console.log(error);
      }
    },

    async createQuiz(data) {
      try {
        const { name, description, duration, date, time, remarks, questions, passing } = data;
        const quizData = { name, description, duration, date, time, remarks, passing, chapter_id: this.chapter_id };

        // 1. Create Quiz
        const response = await apiClient.post(`/quizzes/${this.chapter_id}`, quizData);
        const quiz_id = response.data.id;

        // 2. Create Questions
        for (let question of questions) {
          const { options, correct_option_id } = question;
          const fin_question = {
            statement: question.statement,
            marks: question.marks,
            quiz_id: quiz_id
          };

          const ques_response = await apiClient.post(`/questions/${quiz_id}`, fin_question);
          const question_id = ques_response.data.id;

          // 3. Create Options
          for (let option of options) {
            const fin_option = {
              text: option.text,
              is_correct: option.id === correct_option_id,
              question_id: question_id
            };

            await apiClient.post(`/options/${question_id}`, fin_option);
          }
        }

        const new_quiz = await apiClient.get(`/quiz/${quiz_id}`);
        this.quizzes.push(new_quiz.data);
      } catch (error) {
        console.error("Error while creating quiz:", error);
      }
    },

    async updateQuiz(data) {
      try {
        const { name, description, duration, date, time, remarks, questions, passing } = data;
        const quizData = { name, description, duration, date, time, remarks, passing, chapter_id: this.chapter_id };

        // 1. Create Quiz
        await apiClient.patch(`/quiz/${this.selectedQuiz.id}`, quizData);

        // 2. Delete all questions and options
        for(let question of questions){
          try{
            await apiClient.delete(`/question/${question.id}`);
          }
          catch{
            continue;
          }
        }

        // 3. Create Questions
        for (let question of questions) {
          const { options, correct_option_id } = question;
          const fin_question = {
            statement: question.statement,
            marks: question.marks,
            quiz_id: this.selectedQuiz.id
          };

          const ques_response = await apiClient.post(`/questions/${this.selectedQuiz.id}`, fin_question);
          const question_id = ques_response.data.id;

          // 4. Create Options
          for (let option of options) {
            const fin_option = {
              text: option.text,
              is_correct: option.id === correct_option_id,
              question_id: question_id
            };

            await apiClient.post(`/options/${question_id}`, fin_option);
          }
        }
      }
      catch (error) {
        console.error("Error while creating quiz:", error);
      }
    },


    async deleteQuiz(quiz) {
      try{
        await apiClient.delete(`/quiz/${quiz.id}`);
      }
      catch(error){
        console.log(error);
      }
    }
  }
})
