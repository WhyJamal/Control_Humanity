<template>
  <router-view />
</template>

<script>
export default {
  name: 'App',
}
</script>

<style>
  @tailwind base;
  @tailwind components;
  @tailwind utilities;

  .rotate-ghost {
  transform: rotate(10deg) scale(1.05) !important;
  opacity: 0.8 !important;
  transition: transform 0.2s ease;
}

@keyframes spin {
  from { transform: rotate(0deg) scale(1.05); }
  to   { transform: rotate(360deg) scale(1.05); }
}
.rotate-ghost.spin {
  animation: spin 1s linear infinite;
  opacity: 0.8;
}
</style>
