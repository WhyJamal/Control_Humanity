import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', name: 'Login', component: () => import('../components/auth/Login.vue') },
  { path: '/organization', component: () => import('../components/auth/Organization.vue') },
  { path: '/payments', component: () => import('@/components/pages/Payments.vue') },
  { 
    path: '/', 
    component: () => import('@/components/Layout.vue'),
    meta: { requiresAuth: true },
    redirect: '/projects',
    children: [
      { path: 'register', name: 'Register', component: () => import('@/components/auth/Register.vue') },
      { path: 'dashboard', component: () => import('@/components/pages/Dashboard.vue'), meta: { requiresAuth: true },},
      { path: 'projects', name: 'Projects', component: () => import('@/components/projects/ProjectsTable.vue'), meta: { requiresAuth: true }, },
      { path: 'archivedprojects', component: () => import('@/components/projects/ArchivedProjects.vue'), meta: { requiresAuth: true }, },
      { path: 'taskstable', component: () => import('@/components/tasks/TasksTable.vue'), meta: { requiresAuth: true }, },
      { path: 'archivedtasks', component: () => import('@/components/tasks/ArchivedTasks.vue'), meta: { requiresAuth: true }, },
      { path: 'projects/:id', component: () => import('@/components/projects/ProjectDetail.vue') },
      { path: 'chat', component: () => import('@/components/chat/ChatList.vue') },
      { path: 'chat/:id', component: () => import('@/components/chat/ChatWindow.vue') },
      { path: 'ratings', component: () => import('@/components/ratings/RatingForm.vue') },
      { path: 'tasks', component: () => import('@/components/tasks/KanbanBoard.vue') }, 
      { path: 'mytasks', component: () => import('@/components/tasks/MyTasks.vue') }, 
      { path: 'taskform/:taskId', component: () => import('@/components/tasks/TaskForm.vue') }, 
      { path: 'users', name: 'UserList', component: () => import('@/components/auth/AllUsers.vue')},
      { 
        path: 'profileview/:userId?', name: 'ProfileView', component: () => import('@/components/auth/ProfileView.vue'),
        meta: { requiresAuth: true }
      },    
      {
        path: 'settings/:userId?', name: 'ProfileSettings', component: () => import('@/components/auth/ProfileSettings.vue'),
      },
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const auth = store.state.auth

  // 1. General auth check
  if (to.meta.requiresAuth && !auth.token) {
    return next('/login')
  }

  // 2. Profile route guard
  if (to.path.startsWith('/profile')) {
    const targetId = to.params.userId ? Number(to.params.userId) : auth.user.id
    const isSelf = targetId === auth.user.id
    const canViewOther = ['director', 'manager'].includes(auth.user.role)

    if (isSelf || canViewOther) {
      return next()
    } else {
      return next('/forbidden')
    }
  }

  // 3. Default
  next()
})

export default router
