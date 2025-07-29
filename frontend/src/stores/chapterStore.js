// stores/chapterStore.js
import { defineStore } from 'pinia';
import apiClient from '@/components/api/axios';

export const useChapterStore = defineStore('chapterStore', {
  state: () => ({
    chaptersBySubject: {},        // subject_id -> [chapters]
    selectedChapter: null,
    loadingSubjectIds: new Set(), // track which subject chapters are loading
    quizzes: [],
    loadingQuizzes: false
  }),

  actions: {
    async fetchChapters(subjectId) {
      if (this.chaptersBySubject[subjectId] || this.loadingSubjectIds.has(subjectId)) return;

      this.loadingSubjectIds.add(subjectId);
      try {
        const response = await apiClient.get(`/chapters/${subjectId}`);
        this.chaptersBySubject[subjectId] = response.data;
      } catch (err) {
        console.error(err);
      } finally {
        this.loadingSubjectIds.delete(subjectId);
      }
    },

    selectChapter(subjectId, chapterId){
      this.quizzes = []
      this.selectedChapter = this.chaptersBySubject[subjectId].find(chapter => chapter.id === chapterId);
      this.fetchQuizzes();
      return;
    },

    async fetchQuizzes(){
      if(this.quizzes.length > 0 || this.loadingQuizzes) return;

      this.loadingQuizzes = true;
      try{
        const response = await apiClient.get(`quizzes/${this.selectedChapter.id}`);
        this.quizzes = response.data;
      }
      catch(error){
        console.log(error);
      }
      finally{
        this.loadingQuizzes = false;
        console.log(this.quizzes);
        // console.log(this.quizzes[0]);
      }
    },
  }
});
