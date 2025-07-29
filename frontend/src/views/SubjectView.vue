<template>
  <div class="container-fluid">
    <div class="row min-vh-100">
      <!-- Left Sidebar -->
      <div class="col-2 border border-black p-2 d-flex flex-column">
        <SubjectListing/>
      </div>

      <div class="col-10">
        <!-- Top Bar -->
        <div class="row">
          <div class="col border border-black d-flex justify-content-center align-items-center" style="height: 8vh;">
            <TopSection/>
          </div>
        </div>

        <!-- Bottom Row -->
        <div class="row" style="height: 92vh;">
          <!-- Main Content -->
          <div class="col-10 border border-black d-flex">
            <ChapterDescription/>
          </div>
          <!-- Right Sidebar -->
          <div class="col-2 border border-black d-flex justify-content-center align-items-center">
            4
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import ChapterDescription from '@/components/subject/ChapterDescription.vue';
import TopSection from '@/components/subject/TopSection.vue';
import SubjectListing from '@/components/subject/SubjectListing.vue';

</script>
