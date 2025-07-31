// stores/chapterStore.js
import { defineStore } from 'pinia';
import apiClient from '@/components/api/axios';

export const useAdminChapterStore = defineStore('adminChapterStore', {
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

    async createChapter(data){
      try{
        await apiClient.post(`/chapters/${data.subject_id}`, data)
      }
      catch(error){
        console.log(error);
      }
    },

    async updateChapter(data){
      try{
        await apiClient.patch(`/chapter/${data.id}`, data);
      }
      catch(error){
        console.log(error);
      }
    },

    async deleteChapter(data){
      try{
        await apiClient.delete(`/chapter/${data.id}`);
      }
      catch(error){
        console.log(error);
      }
    }
  }
})
