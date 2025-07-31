import { defineStore } from "pinia";
import apiClient from "@/components/api/axios";
import { formatDate, getDateDifference } from "@/composables/useDateFormat";

export const useProfileStore = defineStore('profileStore', {
  state: () => ({
    profile: null,
    loadingProfile: false,
    quizzesCompleted: 0,
    daysSince: 0,
    totalXP: 0,
    level: 0,
    levelXP: 0,
    errorType: "",
  }),
  actions: {

    findDays() {
      const today = formatDate(new Date())
      this.daysSince =  getDateDifference(this.profile.joiningDate, today);
      return;
    },

    findXP() {
      this.totalXP =  this.daysSince * 1 + this.quizzesCompleted * 10;
      this.level = Math.floor(this.totalXP / 100);
      this.levelXP = this.totalXP - (this.level * 200);
    },

    async fetchProfile() {
      // if (this.profile || this.loadingProfile) return;
      try{
        this.loadingProfile = true;
        const response = await apiClient.get('/users/me');
        this.profile = response.data;
        this.profile.joiningDate = formatDate(this.profile.joiningDate);
        this.quizzesCompleted = this.profile.attempts.length;
        this.findDays();
        this.findXP();
      }
      catch(error){
        console.log(error);
      }
      finally{
        this.loadingProfile = false;
      }
    },

    async editProfile(newProfile) {
      try{
        await apiClient.patch('/users/update-profile', newProfile);
        // this.profile = null;
        await this.fetchProfile();
      } catch (error) {
        if([409, 422].includes(error.response.status) ){
          this.errorType = error.response.data.message;
        }
        else{
          this.errorType = "Something went wrong";
        }
        throw error
      }
    },

    async editPassword(oldPassword, newPassword){
      try{
        const data = {
          'oldPassword': oldPassword,
          'newPassword': newPassword
        }
        await apiClient.patch('/users/update-password', data);
      }
      catch(error){
        if([400, 401, 422].includes(error.response.status)){
          this.errorType = error.response.data.message;
        }
        else{
          this.errorType = "Something went wrong";
          console.log("Something went wrong");
        }
        throw error
      }
    }
  }
})
