<template>
  <nav class="flex" aria-label="BreadcrumbHistory">
    <ol class="inline-flex items-center space-x-1 md:space-x-2 rtl:space-x-reverse">
      <li
        v-for="(crumb, idx) in visitedRoutes"
        :key="crumb.path"
        class="relative inline-flex items-center bg-gray-100 dark:bg-gray-800 rounded-md px-2 py-1"
      >
        <router-link
          :to="crumb.path"
          class="inline-flex items-center text-sm font-medium text-gray-700 hover:text-blue-600 dark:text-gray-200 dark:hover:text-white pr-4"
        >
          {{ crumb.name }}
        </router-link>
        <button
          @click="removeCrumb(idx)"
          class="absolute right-1 top-0 opacity-0 hover:opacity-100 text-gray-500 hover:text-red-600 transition-opacity"
        >
          ×
        </button>
        <span
          v-if="idx < visitedRoutes.length - 1"
          class="mx-1 text-gray-400 select-none"
        ></span>
      </li>
    </ol>
  </nav>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const LOCAL_KEY = 'visited_routes'
const visitedRoutes = ref([])

const route  = useRoute()
const router = useRouter()

const formatName = (path) => {
  const seg = path.split('/').filter(Boolean).pop() || 'Home'
  return seg
    .replace(/-/g, ' ')
    .replace(/\b\w/g, l => l.toUpperCase())
}

onMounted(() => {
  const saved = localStorage.getItem(LOCAL_KEY)
  if (saved) visitedRoutes.value = JSON.parse(saved)
})

watch(
  () => route.fullPath,
  (newPath) => {
    if (!visitedRoutes.value.find(c => c.path === newPath)) {
      visitedRoutes.value.push({
        path: newPath,
        name: formatName(newPath)
      })
      localStorage.setItem(LOCAL_KEY, JSON.stringify(visitedRoutes.value))
    }
  },
  { immediate: true }
)

const removeCrumb = (idx) => {
  let targetPath = '/dashboard'
  if (visitedRoutes.value.length > 1) {
    targetPath = idx > 0
      ? visitedRoutes.value[idx - 1].path
      : visitedRoutes.value[1].path
  }

  visitedRoutes.value.splice(idx, 1)
  localStorage.setItem(LOCAL_KEY, JSON.stringify(visitedRoutes.value))

  router.push(targetPath)
}
</script>

<style scoped>
li.relative:hover button {
  opacity: 1;
}
</style>
