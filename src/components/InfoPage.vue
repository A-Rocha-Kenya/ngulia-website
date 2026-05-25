<template>
  <section class="page">
    <div class="section-label">{{ content.eyebrow }}</div>
    <h1 class="page-title">{{ content.title }}</h1>
    <p class="page-intro">{{ content.intro }}</p>

    <div class="grid" style="grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); margin-top: 2rem;">
      <article v-for="section in content.sections" :key="section.title" class="panel">
        <div class="panel-inner">
          <h2 class="panel-title">{{ section.title }}</h2>
          <ul class="bullets">
            <li v-for="bullet in section.bullets" :key="bullet">{{ bullet }}</li>
          </ul>
        </div>
      </article>
    </div>
  </section>
</template>

<script setup>
defineProps({
  content: {
    type: Object,
    required: true
  }
})
</script>
