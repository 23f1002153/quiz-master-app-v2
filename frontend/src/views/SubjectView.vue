<template>
  <div class="container-fluid">
    <div class="row min-vh-100">
      <!-- Left Sidebar -->
      <div class="col-2 border border-black p-2 d-flex flex-column">
        <SubjectListing/>
      </div>

      <div class="col-10">

        <!-- Bottom Row -->
        <div class="row" style="height: 100vh;">
          <!-- Main Content -->
          <div class="col-12 border border-black d-flex">
            <ChapterDescription/>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import ChapterDescription from '@/components/subject/ChapterDescription.vue';
import SubjectListing from '@/components/subject/SubjectListing.vue';

</script>
