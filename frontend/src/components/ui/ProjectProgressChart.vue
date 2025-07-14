<template>
  <div class="p-4 h-[400px] grid grid-cols-1 md:grid-cols-3 gap-4">
    <div
      v-for="card in cards"
      :key="card.id"
      class="bg-white dark:bg-gray-800 rounded-xl shadow-md border border-gray-200 dark:border-gray-700 p-4 flex flex-col"
    >
      <div class="flex justify-between items-center mb-2">
        <h3 class="text-lg font-semibold text-gray-800 dark:text-white">
          {{ card.title }}
        </h3>
        <button
          v-if="card.refreshable"
          @click="updateData()"
          class="text-sm text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
        >
          Refresh
        </button>
      </div>
      <div :class="card.chartContainerClass">
        <component
          :is="card.component"
          :data="card.data"
          :options="card.options"
        />
      </div>
      <ul v-if="card.legend" class="text-sm space-y-1 mt-2">
        <li
          v-for="(item, idx) in card.legend"
          :key="idx"
          class="flex items-center"
        >
          <span
            class="block w-3 h-3 rounded-full mr-2"
            :class="item.colorClass"
          ></span>
          {{ item.label }}: {{ item.value }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { reactive, onMounted } from 'vue'
import api from '@/utils/axios'
import { Doughnut, Bar, Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  BarElement,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
} from 'chart.js'

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  ArcElement,
  BarElement,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement
)

// Dashboard kartalari konfiguratsiyasi
const cards = reactive([
  {
    id: 'status',
    title: 'Vazifalar holati',
    component: Doughnut,
    refreshable: true,
    chartContainerClass: 'h-48',
    data: {
      labels: [],
      datasets: [{ data: [], backgroundColor: [], borderWidth: 0 }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      cutout: '70%',
    },
    legend: [],
  },
  {
    id: 'yearly',
    title: 'Yillik vazifalar soni',
    component: Bar,
    refreshable: false,
    chartContainerClass: 'h-48',
    data: {
      labels: [],
      datasets: [{ label: 'Vazifalar', data: [], backgroundColor: '#3B82F6' }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: { x: { grid: { display: false } }, y: { beginAtZero: true } },
      plugins: { legend: { display: false } },
    },
    legend: null,
  },
  {
    id: 'monthly',
    title: 'Oyma-oy vazifalar',
    component: Line,
    refreshable: false,
    chartContainerClass: 'h-48',
    data: {
      labels: [],
      datasets: [
        {
          label: 'Yaratilgan',
          data: [],
          fill: false,
          tension: 0.4,
          borderWidth: 2,
          pointRadius: 0,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: { x: { grid: { display: false } }, y: { beginAtZero: true } },
      plugins: { legend: { position: 'top' } },
    },
    legend: null,
  },
])

async function updateData() {
  try {
    const [tasksRes, projectsRes] = await Promise.all([
      api.get('/tasks/'),
      api.get('/projects/'),
    ])

    // DRF paginatsiya bo‘lsa results
    const tasks = Array.isArray(tasksRes.data)
      ? tasksRes.data
      : tasksRes.data.results || []
    const projects = Array.isArray(projectsRes.data)
      ? projectsRes.data
      : projectsRes.data.results || []

    // 1) Donut: status bo‘yicha
    const statusCount = { done: 0, in_progress: 0, todo: 0 }
    tasks.forEach(t => {
      const key = t.status.name
      if (statusCount[key] !== undefined) statusCount[key]++
    })
    const donut = cards.find(c => c.id === 'status')
    const labels = ['Zавершен', 'В процессе', 'Не начат']
    const keys = ['done', 'in_progress', 'todo']
    const colors = ['#10B981', '#FBBF24', '#EF4444']
    donut.data.labels = labels
    donut.data.datasets[0].data = keys.map(k => statusCount[k])
    donut.data.datasets[0].backgroundColor = colors
    donut.legend = labels.map((lbl, idx) => ({
      label: lbl,
      value: statusCount[keys[idx]],
      colorClass: ['bg-green-500', 'bg-yellow-500', 'bg-red-500'][idx],
    }))

    // 2) Bar: yillik vazifalar
    const yearMap = {}
    tasks.forEach(t => {
      const y = new Date(t.created_at).getFullYear()
      yearMap[y] = (yearMap[y] || 0) + 1
    })
    const bar = cards.find(c => c.id === 'yearly')
    const sortedYears = Object.keys(yearMap).sort()
    bar.data.labels = sortedYears
    bar.data.datasets[0].data = sortedYears.map(y => yearMap[y])

    // 3) Line: oyma-oy (joriy yil)
    const currentYear = new Date().getFullYear()
    const monthlyCounts = Array(12).fill(0)
    tasks.forEach(t => {
      const d = new Date(t.created_at)
      if (d.getFullYear() === currentYear) {
        monthlyCounts[d.getMonth()]++
      }
    })
    const line = cards.find(c => c.id === 'monthly')
    line.data.labels = ['Yan','Fev','Mar','Apr','May','Iyun','Iyul','Avg','Sen','Okt','Noy','Dek']
    line.data.datasets[0].data = monthlyCounts

  } catch (err) {
    console.error('Dashboard data yuklashda xato:', err)
  }
}

onMounted(updateData)
</script>

<style scoped>

</style>
