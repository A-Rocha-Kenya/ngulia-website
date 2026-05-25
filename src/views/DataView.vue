<template><InfoPage :content="scienceSections.data" /></template>

<script setup>
import InfoPage from '../components/InfoPage.vue'
import { scienceSections } from '../data/siteContent.js'
</script>
