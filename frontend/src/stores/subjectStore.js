// stores/subject.js
import { defineStore } from 'pinia'
import apiClient from '@/components/api/axios'

export const useSubjectStore = defineStore('subjectStore', {
  state: () => ({
    subjects: [],
    loading: false,
  }),
  actions: {
    async fetchSubjects() {
      if (this.subjects.length > 0) return;
      try {
        this.loading = true
        const response = await apiClient.get('/subjects')
        this.subjects = response.data
      } catch (err) {
        console.error(err)
      } finally {
        this.loading = false
      }
    },
    getSubject(subject_id) {
      return this.subjects.find(subject => subject.id === subject_id);
    }
  }
})
