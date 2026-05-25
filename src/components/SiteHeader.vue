<template>
  <header class="site-header">
    <div class="site-header__inner">
      <RouterLink class="brand" to="/">
        <span class="brand__glow"></span>
        <span class="brand__text">
          <strong>Ngulia</strong>
          <span>Bird Migration Project</span>
        </span>
      </RouterLink>

      <nav class="desktop-nav" aria-label="Primary">
        <div v-for="group in navigation" :key="group.label" class="nav-group">
          <button class="nav-group__button" type="button">
            {{ group.label }}
          </button>
          <div class="nav-group__menu">
            <RouterLink v-for="item in group.items" :key="item.to" :to="item.to" class="nav-group__link">
              {{ item.label }}
            </RouterLink>
          </div>
        </div>
      </nav>

      <details class="mobile-nav">
        <summary>Menu</summary>
        <div class="mobile-nav__panel">
          <div v-for="group in navigation" :key="group.label" class="mobile-nav__group">
            <div class="mobile-nav__label">{{ group.label }}</div>
            <RouterLink v-for="item in group.items" :key="item.to" :to="item.to" class="mobile-nav__link">
              {{ item.label }}
            </RouterLink>
          </div>
        </div>
      </details>
    </div>
  </header>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { navigation } from '../data/siteContent.js'
</script>

<style scoped>
.site-header {
  position: sticky;
  top: 0;
  z-index: 30;
  backdrop-filter: blur(16px);
  background: linear-gradient(180deg, rgba(5, 10, 15, 0.88), rgba(5, 10, 15, 0.55));
  border-bottom: 1px solid rgba(243, 239, 230, 0.08);
}

.site-header__inner {
  width: min(var(--content-width), calc(100% - 2rem));
  margin: 0 auto;
  min-height: 76px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 0.85rem;
}

.brand__glow {
  width: 1.35rem;
  height: 1.35rem;
  border-radius: 999px;
  background: radial-gradient(circle, rgba(255, 217, 120, 1), rgba(242, 193, 78, 0.5) 42%, rgba(242, 193, 78, 0) 74%);
  box-shadow: 0 0 24px rgba(255, 217, 120, 0.42);
}

.brand__text {
  display: grid;
  gap: 0.08rem;
  line-height: 1;
}

.brand__text strong {
  font-size: 1rem;
  letter-spacing: 0.03em;
}

.brand__text span {
  color: var(--text-soft);
  font-size: 0.78rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.desktop-nav {
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.nav-group {
  position: relative;
}

.nav-group__button {
  border: 0;
  color: var(--text);
  background: transparent;
  padding: 0.9rem 0.9rem;
  cursor: pointer;
}

.nav-group__menu {
  position: absolute;
  top: calc(100% - 0.15rem);
  left: 0;
  min-width: 13rem;
  display: grid;
  gap: 0.25rem;
  padding: 0.5rem;
  border-radius: 1rem;
  border: 1px solid var(--border);
  background: rgba(10, 18, 28, 0.96);
  box-shadow: var(--shadow);
  opacity: 0;
  pointer-events: none;
  transform: translateY(4px);
  transition: opacity 160ms ease, transform 160ms ease;
}

.nav-group:hover .nav-group__menu,
.nav-group:focus-within .nav-group__menu {
  opacity: 1;
  pointer-events: auto;
  transform: translateY(0);
}

.nav-group__link {
  padding: 0.75rem 0.8rem;
  border-radius: 0.8rem;
  color: var(--text-soft);
}

.nav-group__link:hover,
.nav-group__link.router-link-active {
  color: var(--text);
  background: rgba(255, 217, 120, 0.08);
}

.mobile-nav {
  display: none;
}

@media (max-width: 900px) {
  .desktop-nav {
    display: none;
  }

  .mobile-nav {
    display: block;
  }

  .mobile-nav summary {
    list-style: none;
    cursor: pointer;
    padding: 0.8rem 0.9rem;
    border-radius: 999px;
    border: 1px solid var(--border);
    background: rgba(255, 255, 255, 0.03);
  }

  .mobile-nav__panel {
    position: absolute;
    right: 1rem;
    top: 66px;
    width: min(22rem, calc(100% - 2rem));
    border: 1px solid var(--border);
    border-radius: 1rem;
    background: rgba(8, 14, 21, 0.97);
    box-shadow: var(--shadow);
    padding: 0.8rem;
  }

  .mobile-nav__group + .mobile-nav__group {
    margin-top: 0.8rem;
  }

  .mobile-nav__label {
    color: var(--accent-soft);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-size: 0.74rem;
    margin-bottom: 0.4rem;
  }

  .mobile-nav__link {
    display: block;
    padding: 0.6rem 0;
    color: var(--text-soft);
  }
}
</style>
