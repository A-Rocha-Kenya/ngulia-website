<template>
  <footer class="site-footer">
    <div class="site-footer__inner">
      <p class="site-footer__text">
        © Ngulia Bird Migration Project. Scientific material for research and outreach purposes.
        <span v-if="siteMeta.footerEmail"> Contact: {{ siteMeta.footerEmail }}</span>
      </p>
    </div>
  </footer>
</template>

<script setup>
import { siteMeta } from '../data/siteContent.js'
</script>

<style scoped>
.site-footer {
  position: relative;
  z-index: 2;
  border-top: 1px solid rgba(243, 239, 230, 0.08);
  background: rgba(5, 10, 15, 0.6);
}

.site-footer__inner {
  width: min(var(--content-width), calc(100% - 2rem));
  margin: 0 auto;
  padding: 1rem 0 1.4rem;
}

.site-footer__text {
  margin: 0;
  color: var(--text-soft);
  font-size: 0.82rem;
  line-height: 1.5;
}
</style>
