import { defineStore } from "pinia";
import apiClient from "@/components/api/axios";


export const useQuizStore = defineStore('quizStore', {
  state: () => ({
    selectedQuiz: localStorage.getItem('quiz') ? JSON.parse(localStorage.getItem('quiz')) : null,
    errorType: null,
    remainingTime: null,
    isStarted: false,
    questions: [],
    quizAnswers: null,
  }),

  actions: {
    selectQuiz(quiz) {
      this.selectedQuiz = quiz;
      localStorage.setItem('quiz', JSON.stringify(quiz));
      console.log(this.selectedQuiz);
      return;
    },

    deselectQuiz() {
      this.selectedQuiz = null;
      // console.log(this.selectedQuiz);
      return;
    },

    async quizStarted(){
      try{
        console.log(this.selectedQuiz.id);
        const response = await apiClient.get(`/quiz/${this.selectedQuiz.id}/start`);
        const data = response.data;
        const message = data.message;
        if(message === "Quiz time ongoing"){
          console.log([true, data.remaining_time]);
          this.remainingTime = data.remaining_time;
          this.isStarted = true;
          return true
        }
        else{
          // console.log([false, this.selectedQuiz.duration]);
          this.remainingTime = this.selectedQuiz.duration;
          return false
        }
      }
      catch(error){
        if([400, 404].includes(error.response.status)){
          this.errorType = error.response.message;
        }
        else{
          return this.errorType = "Something went wrong";
        }
      }
    },

    async getQuestions(){
      try{
        const response = await apiClient.get(`/quiz/${this.selectedQuiz.id}/questions`)
        this.questions = response.data;
        console.log(this.questions);
      }
      catch{
        this.errorType = "Something went wrong";
      }
    },

    async startQuiz(){
      try{
        const quizStatus = await this.quizStarted();
        if(quizStatus === false){
          await apiClient.post(`/quiz/${this.selectedQuiz.id}/start`);
          this.getQuestions();
          this.isStarted = true;
        }
        else{
          await this.getQuestions();
          console.log(this.questions);
        }
      }
      catch(error){
        if([400, 404].includes(error.response.status)){
          this.errorType = error.response.message;
        }
        else{
          return this.errorType = "Something went wrong";
        }
      }
    },

    async submitQuiz(userAnswers){
      try{
        await apiClient.post(`quiz/${this.selectedQuiz.id}/submit`, userAnswers);
      }
      catch(error){
        if([400, 404, 422].includes(error.response.status)){
          this.errorType = error.response.message;
        }
        else{
          this.errorType = "Something went wrong";
        }
      }
    },

    async getAnswers(){
      try{
        const response = await apiClient.get(`quiz/${this.selectedQuiz.id}/submit`);
        this.quizAnswers = response.data;
      }
      catch(error){
        this.errorType = error.response.message;
      }
      finally{
        console.log(this.quizAnswers);
        console.log(this.selectedQuiz);
      }
    }

  }
})
