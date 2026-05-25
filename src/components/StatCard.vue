<template>
  <div class="panel stat-card">
    <div class="panel-inner">
      <div class="eyebrow">{{ label }}</div>
      <div class="stat-card__value">{{ value }}</div>
      <div class="muted">{{ description }}</div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  label: String,
  value: String,
  description: String
})
</script>

<style scoped>
.stat-card__value {
  font-size: clamp(2rem, 4vw, 3rem);
  line-height: 0.95;
  margin-bottom: 0.45rem;
  color: var(--accent-soft);
}
</style>
