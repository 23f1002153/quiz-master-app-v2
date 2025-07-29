<template>
  <div class="container-fluid py-4 d-grid">
    <!-- Top Canvas -->
     <TopCanvas/>

    <!-- Middle Canvas -->
     <MiddleCanvas/>

    <!-- Bottom Canvas -->
    <BottomCanvas/>
  </div>
</template>

<script setup>
import BottomCanvas from '@/components/home/BottomCanvas.vue';
import MiddleCanvas from '@/components/home/MiddleCanvas.vue';
import TopCanvas from '@/components/home/TopCanvas.vue';

</script>
