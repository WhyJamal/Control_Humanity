<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-700 via-indigo-800 to-purple-900 p-4"
       :style="{ backgroundImage: `url(${photoLogin})`, backgroundSize: 'cover', backgroundPosition: 'center' }">
    <div class="w-full max-w-7xl bg-white/10 backdrop-blur-lg rounded-2xl shadow-2xl p-8 border border-white/20">
      <h2 class="text-3xl font-bold text-white text-center mb-8 tracking-wide">
        Регистрация организации
      </h2>
      <form @submit.prevent="createOrganization" class="space-y-6">

        <!-- Organization Fields -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label for="orgName" class="block text-gray-200 font-medium mb-1">Полное название</label>
            <input v-model="form.organization.name" id="orgName" type="text" placeholder="ООО Пример"
                   class="w-full p-3 rounded-lg bg-gray-800 text-gray-100" />
          </div>
          <div>
            <label for="shortName" class="block text-gray-200 font-medium mb-1">Краткое название</label>
            <input v-model="form.organization.short_name" id="shortName" type="text" placeholder="Пример"
                   class="w-full p-3 rounded-lg bg-gray-800 text-gray-100" />
          </div>
          <div>
            <label for="inn" class="block text-gray-200 font-medium mb-1">ИНН</label>
            <input v-model="form.organization.inn" id="inn" type="text" maxlength="12" placeholder="123456789012"
                   class="w-full p-3 rounded-lg bg-gray-800 text-gray-100" />
          </div>
          <div>
            <label for="pnfl" class="block text-gray-200 font-medium mb-1">ПНФЛ</label>
            <input v-model="form.organization.pnfl" id="pnfl" type="text" maxlength="14" placeholder="12345678901234"
                   class="w-full p-3 rounded-lg bg-gray-800 text-gray-100" />
          </div>
          <div>
            <label for="address" class="block text-gray-200 font-medium mb-1">Адрес</label>
            <input v-model="form.organization.address" id="address" type="text" placeholder="Tashkent city"
                   class="w-full p-3 rounded-lg bg-gray-800 text-gray-100" />
          </div>
          <div>
            <label for="orgEmail" class="block text-gray-200 font-medium mb-1">Email организации</label>
            <input v-model="form.organization.email" id="orgEmail" type="email" placeholder="info@example.com"
                   class="w-full p-3 rounded-lg bg-gray-800 text-gray-100" />
          </div>
          <div>
            <label for="orgPhone" class="block text-gray-200 font-medium mb-1">Телефон организации</label>
            <input v-model="form.organization.phone" id="orgPhone" type="text" placeholder="+998901234567"
                   class="w-full p-3 rounded-lg bg-gray-800 text-gray-100" />
          </div>
          <div>
            <label for="bankName" class="block text-gray-200 font-medium mb-1">Наименование банка</label>
            <input v-model="form.organization.bank_name" id="bankName" type="text" placeholder="НБУ"
                   class="w-full p-3 rounded-lg bg-gray-800 text-gray-100" />
          </div>
          <div class="block text-gray-200 font-medium mb-1">
            <label for="bankAccount" class="block text-gray-200 font-medium mb-1">Расчётный счёт</label>
            <input v-model="form.organization.bank_account" id="bankAccount" type="text" placeholder="UZ123..."
                   class="w-full p-3 rounded-lg bg-gray-800 text-gray-100" />
          </div>
        </div>

        <hr class="border-gray-600" />

        <!-- User Fields -->
        <div @click="toggleUserFields" class="flex items-center cursor-pointer gap-2">
          <h2 class="text-xl font-bold tracking-wide">Юридическое лицо</h2>
          <svg
            class="mt-1 w-3 h-3 text-gray-600 transition-transform duration-200 dark:text-gray-400"
            :class="{ 'rotate-180': showUserFields }"
            fill="none"
            viewBox="0 0 10 6"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            >
            <path d="m1 1 4 4 4-4" />
          </svg>
        </div>
        <div v-if="showUserFields" class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label for="firstName" class="block text-gray-200 font-medium mb-1">Имя</label>
            <input v-model="form.user.first_name" id="firstName" type="text" placeholder="Имя"
                   class="w-full p-3 rounded-lg bg-gray-800 text-gray-100" />
          </div>
          <div>
            <label for="userEmail" class="block text-gray-200 font-medium mb-1">Email пользователя</label>
            <input v-model="form.user.email" id="userEmail" type="email" placeholder="admin@example.com"
                   class="w-full p-3 rounded-lg bg-gray-800 text-gray-100" />
          </div>
          <div>
            <label for="username" class="block text-gray-200 font-medium mb-1">Имя для входа</label>
            <input v-model="form.user.username" id="username" type="text" placeholder="user123"
                   class="w-full p-3 rounded-lg bg-gray-800 text-gray-100" />
          </div>
          <div>
            <label for="lastName" class="block text-gray-200 font-medium mb-1">Фамилия</label>
            <input v-model="form.user.last_name" id="lastName" type="text" placeholder="Фамилия"
                   class="w-full p-3 rounded-lg bg-gray-800 text-gray-100" />
          </div>
          <div>
            <label for="userPhone" class="block text-gray-200 font-medium mb-1">Телефон пользователя</label>
            <input v-model="form.user.phone" id="userPhone" type="text" placeholder="+998901234567"
                   class="w-full p-3 rounded-lg bg-gray-800 text-gray-100" />
          </div>
          <div>
            <label for="password" class="block text-gray-200 font-medium mb-1">Пароль</label>
            <input v-model="form.user.password" id="password" type="password" placeholder="••••••••"
                   class="w-full p-3 rounded-lg bg-gray-800 text-gray-100" />
          </div>
          <div>
            <label for="password2" class="block text-gray-200 font-medium mb-1">Подтвердите пароль</label>
            <input v-model="form.user.password2" id="password2" type="password" placeholder="••••••••"
                   class="w-full p-3 rounded-lg bg-gray-800 text-gray-100" />
          </div>
        </div>

        <div v-if="errorMessage" class="text-red-400 text-sm">{{ errorMessage }}</div>
        <div class="flex justify-center gap-6">
        <button @click="backToLogin"
                class="w-64 py-3 mt-4 bg-transparent border border-pink-400 text-pink-400 font-semibold py-3 rounded-xl hover:bg-pink-500 hover:text-white transition">
        Логин
        </button> 
        <button type="submit"
                class="w-64 py-3 mt-4 bg-gradient-to-r from-purple-500 to-pink-500 text-white font-semibold rounded-xl shadow-lg hover:from-purple-600 hover:to-pink-600 transition duration-300">
          Зарегистрировать
        </button> 
      </div>
      </form>
    </div>
  </div>
</template>

<script>
import photoLogin from '@/assets/photo_login_page.png';
import api from '@/utils/axios';

export default {
  name: 'RegisterOrganization',
  data() {
    return {
      photoLogin,
      showUserFields: false,
      form: {
        organization: {
          name: '',
          short_name: '',
          inn: '',
          pnfl: '',
          address: '',
          email: '',
          phone: '',
          bank_name: '',
          bank_account: ''
        },
        user: {
          username: '',
          email: '',
          first_name: '',
          last_name: '',
          role: 'director',
          phone: '',
          password: '',
          password2: ''
        }
      },
      errorMessage: ''
    };
  },
  methods: {
    backToLogin() {
      this.$router.push({ name: 'Login' });
    },
    toggleUserFields() {
      this.showUserFields = !this.showUserFields;
    },
    async createOrganization() {
      this.errorMessage = '';
      const { organization: org, user } = this.form;
      if (!org.name || !org.inn || !user.username || !user.password || !user.password2) {
        this.errorMessage = 'Пожалуйста, заполните все обязательные поля.';
        return;
      }
      if (user.password !== user.password2) {
        this.errorMessage = 'Пароли не совпадают.';
        return;
      }
      try {
        const payload = { organization: org, user };
        const response = await api.post('/auth/register-organization/', payload);
        console.log('Успешно зарегистрировано:', response.data);
        this.$router.push({ name: 'Projects' });
      } catch (err) {
        console.error('Ошибка:', err.response?.data || err.message);
        this.errorMessage = err.response?.data.detail || 'Ошибка при регистрации.';
      }
    }
  }
};
</script>
