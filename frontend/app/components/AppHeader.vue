<template>
  <header class="app-header" :class="{ scrolled }">
    <div class="container header-inner">
      <!-- Logo -->
      <NuxtLink to="/" class="logo" id="app-logo">
        <div class="logo-icon">
          <svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="2" y="8" width="28" height="16" rx="3" stroke="currentColor" stroke-width="2"/>
            <line x1="16" y1="8" x2="16" y2="24" stroke="currentColor" stroke-width="1.5" opacity="0.4"/>
            <circle cx="9" cy="16" r="2" fill="currentColor"/>
            <circle cx="23" cy="16" r="2" fill="currentColor"/>
          </svg>
        </div>
        <span class="logo-text">لوحتك</span>
      </NuxtLink>

      <!-- Navigation -->
      <nav class="nav-links hide-mobile" id="main-nav">
        <NuxtLink v-for="link in links" :key="link.to" :to="link.to" class="nav-link" :id="link.id">
          <span class="nav-icon" v-html="link.icon"></span>
          {{ link.label }}
        </NuxtLink>
      </nav>

      <!-- Right side -->
      <div class="header-right">
        <StatusBadge />
        <button class="btn btn-ghost mobile-menu-btn hide-desktop" @click="mobileOpen = !mobileOpen" id="mobile-menu-btn">
          <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
            <rect x="2" y="4" width="16" height="2" rx="1"/>
            <rect x="2" y="9" width="16" height="2" rx="1"/>
            <rect x="2" y="14" width="16" height="2" rx="1"/>
          </svg>
        </button>
      </div>
    </div>

    <!-- Mobile menu -->
    <Transition name="slide-down">
      <div v-if="mobileOpen" class="mobile-menu hide-desktop" id="mobile-menu">
        <NuxtLink
          v-for="link in links"
          :key="link.to"
          :to="link.to"
          class="mobile-link"
          @click="mobileOpen = false"
        >
          <span class="nav-icon" v-html="link.icon"></span>
          {{ link.label }}
        </NuxtLink>
      </div>
    </Transition>
  </header>
</template>

<script setup lang="ts">
const links = [
  {
    to: '/',
    label: 'Home',
    id: 'nav-home',
    icon: '<svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M8 1.3l6.5 5.2V14a1 1 0 01-1 1h-3.5V10H6v5H2.5a1 1 0 01-1-1V6.5L8 1.3z"/></svg>',
  },
  {
    to: '/detect',
    label: 'Detect',
    id: 'nav-detect',
    icon: '<svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M1 1h4v4H1V1zm0 10h4v4H1v-4zm10-10h4v4h-4V1zm0 10h4v4h-4v-4zM6 6h4v4H6V6z"/></svg>',
  },
  {
    to: '/history',
    label: 'History',
    id: 'nav-history',
    icon: '<svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M8 1a7 7 0 100 14A7 7 0 008 1zm0 2a5 5 0 110 10A5 5 0 018 3zm-.5 2v3.5l2.5 1.5.5-.87-2-1.2V5h-1z"/></svg>',
  },
  {
    to: '/about',
    label: 'About',
    id: 'nav-about',
    icon: '<svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><circle cx="8" cy="4" r="2"/><path d="M8 7c-2.2 0-4 1.3-4 3v2h8v-2c0-1.7-1.8-3-4-3z"/></svg>',
  },
]

const mobileOpen = ref(false)
const scrolled = ref(false)

function onScroll() {
  scrolled.value = window.scrollY > 20
}

onMounted(() => {
  window.addEventListener('scroll', onScroll, { passive: true })
})

onUnmounted(() => {
  window.removeEventListener('scroll', onScroll)
})
</script>

<style scoped>
.app-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  transition: all var(--transition-normal);
  border-bottom: 1px solid transparent;
}

.app-header.scrolled {
  background: var(--bg-glass);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom-color: var(--bg-card-border);
}

.header-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
}

/* Logo */
.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--text-primary);
  text-decoration: none;
  transition: all var(--transition-fast);
}

.logo:hover {
  color: var(--accent);
}

.logo-icon {
  width: 32px;
  height: 32px;
  color: var(--accent);
}

.logo-text {
  font-family: var(--font-heading);
  font-weight: 900;
  font-size: 1.4rem;
  background: var(--accent-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Nav */
.nav-links {
  display: flex;
  align-items: center;
  gap: 4px;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
  font-size: 0.875rem;
  font-weight: 500;
  text-decoration: none;
  transition: all var(--transition-fast);
}

.nav-link:hover {
  color: var(--text-primary);
  background: var(--bg-card);
}

.nav-link.router-link-active {
  color: var(--accent);
  background: var(--accent-dim);
}

.nav-icon {
  display: flex;
  align-items: center;
  opacity: 0.7;
}

/* Right */
.header-right {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

/* Mobile */
.mobile-menu-btn {
  display: flex;
}

.mobile-menu {
  padding: var(--space-md) var(--space-lg);
  background: var(--bg-glass);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--bg-card-border);
}

.mobile-link {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
  font-weight: 500;
  text-decoration: none;
  transition: all var(--transition-fast);
}

.mobile-link:hover,
.mobile-link.router-link-active {
  color: var(--accent);
  background: var(--accent-dim);
}

/* Transitions */
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s var(--ease-out);
}

.slide-down-enter-from,
.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
