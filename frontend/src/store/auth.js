import api from '@/utils/axios'
import router from '@/router'

let refreshTimeoutId

const state = () => ({
  token: localStorage.getItem('token') || '',
  refreshToken: localStorage.getItem('refresh_token') || '',
  user: null,
})

const getters = {
  isAuthenticated: state => !!state.token,
  getUser: state => state.user,
}

const mutations = {
  setToken(state, token) { state.token = token },
  setRefreshToken(state, refresh) { state.refreshToken = refresh },
  setUser(state, user) { state.user = user },
  logoutUser(state) { state.token = ''; state.refreshToken = ''; state.user = null },
}

// Simple JWT parser without external libs
function parseJwt(token) {
  try {
    const base64Url = token.split('.')[1]
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    )
    return JSON.parse(jsonPayload)
  } catch {
    return {}
  }
}

// Schedule token refresh before expiry
function scheduleRefresh(dispatch, token) {
  const { exp } = parseJwt(token)
  if (!exp) return
  const delay = exp * 1000 - Date.now() - 30000 // 30s before exp
  clearTimeout(refreshTimeoutId)
  if (delay <= 0) {
    dispatch('refreshToken')
  } else {
    refreshTimeoutId = setTimeout(() => dispatch('refreshToken'), delay)
  }
}

const actions = {
  async login({ commit, dispatch }, creds) {
    const { data } = await api.post('/auth/token/', creds)
    commit('setToken', data.access)
    commit('setRefreshToken', data.refresh)
    localStorage.setItem('token', data.access)
    localStorage.setItem('refresh_token', data.refresh)
    api.defaults.headers.common['Authorization'] = `Bearer ${data.access}`
    const profile = await api.get('/auth/users/me/')
    commit('setUser', profile.data)

    if (profile.data.language) {
      localStorage.setItem('lang', profile.data.language)
    }
    // localStorage.setItem('userRole', profile.data.role)
    // localStorage.setItem('userId', profile.data.id)

    scheduleRefresh(dispatch, data.access)

    return profile.data.role
  },

  async checkAuth({ commit, dispatch, state }) {
    if (!state.token) return
    api.defaults.headers.common['Authorization'] = `Bearer ${state.token}`
    const profile = await api.get('/auth/users/me/')
    commit('setUser', profile.data)

    // localStorage.setItem('userRole', profile.data.role)
    // localStorage.setItem('userId', profile.data.id)

    scheduleRefresh(dispatch, state.token)
  },

  async refreshToken({ commit, state, dispatch }) {
    const { data } = await api.post('/auth/token/refresh/', { refresh: state.refreshToken })
    commit('setToken', data.access)
    localStorage.setItem('token', data.access)
    api.defaults.headers.common['Authorization'] = `Bearer ${data.access}`
    scheduleRefresh(dispatch, data.access)
  },

  logout({ commit }) {
    commit('logoutUser')
    localStorage.removeItem('token')
    localStorage.removeItem('refresh_token')
    delete api.defaults.headers.common['Authorization']
    clearTimeout(refreshTimeoutId)
    router.push({ name: 'Login' })
  },

  async register({ dispatch }, userData) {
    await api.post('/auth/users/', userData)
    await dispatch('login', { username: userData.username, password: userData.password })
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
}

