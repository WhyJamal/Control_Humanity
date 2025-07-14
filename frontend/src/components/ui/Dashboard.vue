<template>
  <div class="p-6 space-y-8 bg-gradient-to-br rounded-lg from-gray-50 to-white dark:from-gray-900 dark:to-gray-800 min-h-screen">
    <h1 class="text-4xl font-extrabold text-gray-800 dark:text-gray-100">
      Umumiy Dashboard
    </h1>

    <!-- Statistika kartochkalari -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-6">
      <div
        class="bg-gradient-to-tr from-blue-500 to-indigo-600 text-white p-6 rounded-2xl shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition"
      >
        <h2 class="text-xl font-semibold">Jami loyihalar</h2>
        <p class="text-5xl mt-4">{{ stats.projects }}</p>
      </div>
      <div
        class="bg-gradient-to-tr from-green-400 to-emerald-500 text-white p-6 rounded-2xl shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition"
      >
        <h2 class="text-xl font-semibold">Jami modullar</h2>
        <p class="text-5xl mt-4">{{ stats.modules }}</p>
      </div>
      <div
        class="bg-gradient-to-tr from-pink-400 to-rose-500 text-white p-6 rounded-2xl shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition"
      >
        <h2 class="text-xl font-semibold">Jami vazifalar</h2>
        <p class="text-5xl mt-4">{{ stats.tasks }}</p>
      </div>
    </div>

    <!-- Loyihalar progress diagrammasi -->
    <div
      class="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-md"
    >
      <h2 class="text-2xl font-semibold mb-4 text-gray-700 dark:text-gray-200">
        Loyihalar progressi
      </h2>
      <ProjectProgressChart :all-projects="projects" />
    </div>

    <!-- Oxirgi 5 ta vazifa -->
    <div
      class="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-md"
    >
      <h2 class="text-2xl font-semibold mb-4 text-gray-700 dark:text-gray-200">
        So‘nggi vazifalar
      </h2>
      <ul class="divide-y divide-gray-200 dark:divide-gray-700">
        <li
          v-for="task in recentTasks"
          :key="task.id"
          class="py-3 flex justify-between items-center"
        >
          <span class="text-gray-800 dark:text-gray-100">{{ task.title }}</span>
          <span
            :class="[
              'px-3 py-1 rounded-full text-sm font-medium',
              statusClass(task.status.name)
            ]"
          >
            {{ statusLabel(task.status.name) }}
          </span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import api from '@/utils/axios'
import ProjectProgressChart from '@/components/ui/ProjectProgressChart.vue'

export default {
  name: 'Dashboard',
  components: { ProjectProgressChart },
  data() {
    return {
      projects: [],
      tasks: [],
      stats: { projects: 0, modules: 0, tasks: 0 },
    }
  },
  computed: {
    recentTasks() {
      return this.tasks
        .slice()
        .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
        .slice(0, 5)
    },
  },
  methods: {
    statusLabel(name) {
      const map = {
        done: 'Завершен',
        in_progress: 'В процессе',
        todo: 'Не начат',
      }
      return map[name] || name
    },
    statusClass(name) {
      return {
        done: 'bg-green-100 text-green-800',
        in_progress: 'bg-yellow-100 text-yellow-800',
        todo: 'bg-red-100 text-red-800',
      }[name] || ''
    },

    async fetchDashboardData() {
      try {
        const [prRes, tRes] = await Promise.all([
          api.get('/projects/'),
          api.get('/tasks/'),
        ])

        const projectsData = Array.isArray(prRes.data)
          ? prRes.data
          : prRes.data.results || []
        const tasksData = Array.isArray(tRes.data)
          ? tRes.data
          : tRes.data.results || []

        this.projects = projectsData
        this.tasks = tasksData

        const modulesCount = projectsData.reduce((sum, p) => {
          return sum + (Array.isArray(p.modules) ? p.modules.length : 0)
        }, 0)

        this.stats = {
          projects: projectsData.length,
          modules: modulesCount,
          tasks: tasksData.length,
        }
      } catch (err) {
        console.error('Dashboard maʼlumot yuklashda xato:', err)
      }
    },
  },
  async created() {
    await this.fetchDashboardData()
  },
}
</script>

<style scoped>
/* Dizayn o'zgarishlari uchun qo'shimcha uslublar */
</style>
