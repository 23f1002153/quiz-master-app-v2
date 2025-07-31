// stores/subject.js
import { defineStore } from 'pinia'
import apiClient from '@/components/api/axios'

export const useAdminSubjectStore = defineStore('adminSubjectStore', {
  state: () => ({
    subjects: [],
    loading: false,
  }),
  actions: {
    async fetchSubjects() {
      if (this.subjects.length > 0) return;
      try {
        this.loading = true
        const response = await apiClient.get('/subjects');
        this.subjects = response.data
        console.log(this.subjects);
      } catch (err) {
        console.error(err)
      } finally {
        this.loading = false
      }
    },
    
    getSubject(subject_id) {
      return this.subjects.find(subject => subject.id === subject_id);
    },

    async createSubject(data){
      try{
        const response = await apiClient.post(`/subjects`, data);
        const new_id = response.data.id;
        const newSub = await apiClient.get(`/subject/${new_id}`)
        this.subjects.push(newSub.data);
      }
      catch(error){
        console.log(error);
      }
    },

    async updateSubject(data){
      try{
        await apiClient.patch(`/subject/${data.id}`, data);
        const updatedSub = await apiClient.get(`/subject/${data.id}`);
        const index = this.subjects.findIndex(s => s.id === data.id);
        if (index !== -1) {
          this.subjects[index] = updatedSub.data;
        }
        console.log("UPDATE");
        console.log(data)
      }
      catch(error){
        console.log(error);
      }
    },

    async deleteSubject(data){
      try{
        await apiClient.delete(`/subject/${data.id}`);
        this.subjects = this.subjects.filter(s => s.id !== data.id);
        console.log("DELETE");
        console.log(data);
      }
      catch(error){
        console.log(error)
      }
    }



  }
})
