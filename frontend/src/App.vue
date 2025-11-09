<template>
  <Header v-if="route.name === 'Landing'" />
  <router-view />
</template>

<script setup>
import { useRoute } from 'vue-router'
import Header from '@/components/Header.vue'

const route = useRoute()
</script>

<style>
/* nada aquí por ahora */
</style>
