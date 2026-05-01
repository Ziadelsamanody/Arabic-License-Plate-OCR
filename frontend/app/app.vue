<template>
  <div id="app-root">
    <AppHeader />
    <main class="main-content">
      <NuxtPage />
    </main>
    <AppFooter />
  </div>
</template>

<style>
.main-content {
  min-height: calc(100vh - 64px);
}
</style>
