<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-700 via-indigo-800 to-purple-900 p-4"
        :style="{ backgroundImage: `url(${photoLogin})`, backgroundSize: 'cover', backgroundPosition: 'center' }">
    <div class="w-full max-w-md bg-white/10 backdrop-blur-lg rounded-2xl shadow-2xl p-8 border border-white/20">
      <h2 class="text-3xl font-bold text-white text-center mb-8 tracking-wide">Добро пожаловать!</h2>

      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label for="username" class="block text-gray-200 font-medium mb-1">Имя пользователя</label>
          <input
            v-model="credentials.username"
            id="username"
            type="text"
            placeholder="Введите имя пользователя"
            class="w-full p-3 rounded-lg bg-gray-800 text-gray-100 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
        </div>

        <div>
          <label for="password" class="block text-gray-200 font-medium mb-1">Пароль</label>
          <input
            v-model="credentials.password"
            id="password"
            type="password"
            placeholder="Введите свой пароль"
            class="w-full p-3 rounded-lg bg-gray-800 text-gray-100 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
        </div>

        <div v-if="errorMessage" class="text-red-400 text-sm mt-2">
          {{ errorMessage }}
        </div>

        <button
          type="submit"
          class="w-full mt-2 bg-gradient-to-r from-purple-500 to-pink-500 text-white font-semibold py-3 rounded-xl shadow-lg hover:from-purple-600 hover:to-pink-600 transition duration-300"
          :disabled="loading"
        >
          <span v-if="loading">
            <div role="status">
              <svg aria-hidden="true" class="inline w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-gray-600 dark:fill-gray-300" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>
                  <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>
              </svg>
              <span class="sr-only">Loading...</span>
            </div>          
          </span>
          <span v-else>Войти</span>
        </button>

        <button
          type="button"
          class="w-full bg-transparent border border-pink-400 text-pink-400 font-semibold py-3 rounded-xl hover:bg-pink-500 hover:text-white transition mt-3"
          @click="handleSignup"
        >
          Создать организацию
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import photoLogin from '@/assets/photo_login_page.png'

export default {
  name: 'Login',
  data() {
    return {
      credentials: {
        username: '',
        password: ''
      },
      loading: false,
      errorMessage: '',
      photoLogin
    }
  },
  methods: {
    async handleLogin() {
      this.errorMessage = ''
      if (!this.credentials.username || !this.credentials.password) {
        this.errorMessage = 'Please enter both username and password.'
        return
      }

      try {
        this.loading = true
        //await this.$store.dispatch('auth/login', {
        //  username: this.credentials.username,
        //  password: this.credentials.password
        //})
        //this.$router.push('/projects')
        const role = await this.$store.dispatch("auth/login", {
          username: this.credentials.username,
          password: this.credentials.password,
        });
        if (role === "employee") {
          this.$router.push("/taskstable");
        } else {
          this.$router.push("/projects");
        }
      } catch (err) {
        if (err.response && err.response.data) {
          this.errorMessage = err.response.data.detail || 'Login failed.'
        } else {
          this.errorMessage = 'Login failed. Please try again.'
        }
      } finally {
        this.loading = false
      }
    },
    handleSignup() {
      this.$router.push('/organization')
    }
  }
}
</script>
