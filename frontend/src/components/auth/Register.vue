<template>
  <div
    class="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-400 via-purple-500 to-indigo-700 p-4"
  >
    <div
      class="w-full max-w-xl bg-white/10 backdrop-blur-xl rounded-2xl shadow-2xl p-8 border border-white/20"
    >
      <h2 class="text-3xl font-bold text-white text-center mb-8 tracking-wide">
        Создать аккаунт
      </h2>

      <form @submit.prevent="handleRegister" class="space-y-5">
        <div>
          <label for="username" class="block text-white font-medium mb-1"
            >Имя пользователя</label
          >
          <input
            v-model="form.username"
            id="username"
            type="text"
            placeholder="Введите имя пользователя"
            class="w-full p-3 rounded-lg bg-white/10 text-white placeholder-white/70 border border-white/30 focus:outline-none focus:ring-2 focus:ring-white"
          />
        </div>

        <div>
          <label for="email" class="block text-white font-medium mb-1"
            >Электронная почта</label
          >
          <input
            v-model="form.email"
            id="email"
            type="email"
            placeholder="Введите эл. почту"
            class="w-full p-3 rounded-lg bg-white/10 text-white placeholder-white/70 border border-white/30 focus:outline-none focus:ring-2 focus:ring-white"
          />
        </div>

        <div>
          <label for="phone" class="block text-white font-medium mb-1">Телефон</label>
          <input
            v-model="form.phone"
            id="phone"
            type="text"
            placeholder="Введите номер телефона"
            class="w-full p-3 rounded-lg bg-white/10 text-white placeholder-white/70 border border-white/30 focus:outline-none focus:ring-2 focus:ring-white"
          />
        </div>


        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label for="first_name" class="block text-white font-medium mb-1"
              >Имя</label
            >
            <input
              v-model="form.first_name"
              id="first_name"
              type="text"
              placeholder="Ваше имя"
              class="w-full p-3 rounded-lg bg-white/10 text-white placeholder-white/70 border border-white/30 focus:outline-none focus:ring-2 focus:ring-white"
            />
          </div>
          <div>
            <label for="last_name" class="block text-white font-medium mb-1"
              >Фамилия</label
            >
            <input
              v-model="form.last_name"
              id="last_name"
              type="text"
              placeholder="Ваша фамилия"
              class="w-full p-3 rounded-lg bg-white/10 text-white placeholder-white/70 border border-white/30 focus:outline-none focus:ring-2 focus:ring-white"
            />
          </div>
        </div>

        <div class="mb-5">
          <label for="role" class="block text-sm font-semibold text-white mb-2"
            >Роль</label
          >
          <div class="relative">
            <select
              v-model="form.role"
              id="role"
              class="appearance-none w-full h-12 px-4 pr-10 bg-gradient-to-br rounded-lg from-indigo-600 via-purple-600 to-indigo-700 text-white rounded-2xl border-2 border-indigo-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition duration-200"
            >
              <option
                disabled
                value=""
                class="text-gray-400 rounded-lg bg-gray-800"
              >
                Выберите роль
              </option>
              <option value="admin" class="text-white bg-gray-800 rounded-2xl">
                Админ
              </option>
              <option
                value="director"
                class="text-white bg-gray-800 rounded-2xl"
              >
                Директор
              </option>
              <option value="manager" class="text-white bg-gray-800">
                Менеджер
              </option>
              <option value="employee" class="text-white bg-gray-800">
                Сотрудник
              </option>
            </select>
            <!-- Custom arrow -->
            <svg
              class="pointer-events-none absolute inset-y-3 right-4 w-5 h-5 text-white opacity-80"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 20 20"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M7 7l3-3 3 3m0 6l-3 3-3-3"
              />
            </svg>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label for="password" class="block text-white font-medium mb-1"
              >Пароль</label
            >
            <input
              v-model="form.password"
              id="password"
              type="password"
              placeholder="Введите пароль"
              class="w-full p-3 rounded-lg bg-white/10 text-white placeholder-white/70 border border-white/30 focus:outline-none focus:ring-2 focus:ring-white"
            />
          </div>
          <div>
            <label for="password2" class="block text-white font-medium mb-1"
              >Подтверждение пароля</label
            >
            <input
              v-model="form.password2"
              id="password2"
              type="password"
              placeholder="Повторите пароль"
              class="w-full p-3 rounded-lg bg-white/10 text-white placeholder-white/70 border border-white/30 focus:outline-none focus:ring-2 focus:ring-white"
            />
          </div>
        </div>

        <div v-if="errorMessage" class="text-red-300 text-sm mt-2">
          {{ errorMessage }}
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="w-full mt-4 bg-white text-indigo-700 font-semibold py-3 rounded-xl shadow-xl hover:bg-indigo-100 transition duration-300"
        >
          <span v-if="loading">Регистрация...</span>
          <span v-else>Зарегистрироваться</span>
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import api from "@/utils/axios";

export default {
  name: "Register",
  data() {
    return {
      form: {
        username: "",
        email: "",
        phone: "",
        first_name: "",
        last_name: "",
        role: "",
        password: "",
        password2: "",
      },
      loading: false,
      errorMessage: "",
    };
  },
  methods: {
    async handleRegister() {
      this.errorMessage = "";

      if (
        !this.form.username ||
        !this.form.email ||
        !this.form.phone ||
        !this.form.first_name ||
        !this.form.last_name ||
        !this.form.role ||
        !this.form.password ||
        !this.form.password2
      ) {
        this.errorMessage = "Пожалуйста, заполните все поля.";
        return;
      }
      if (this.form.password !== this.form.password2) {
        this.errorMessage = "Пароли не совпадают.";
        return;
      }

      try {
        this.loading = true;
        await api.post("/auth/register/", {
          user: {
            username: this.form.username,
            email: this.form.email,
            phone: this.form.phone,
            first_name: this.form.first_name,
            last_name: this.form.last_name,
            role: this.form.role,
            password: this.form.password,
            password2: this.form.password2,
          },
        });

        this.$router.push("/users");
      } catch (err) {
        if (err.response && err.response.data) {
          const data = err.response.data;
          if (typeof data === "object") {
            this.errorMessage = Object.values(data).flat().join(" ");
          } else {
            this.errorMessage = data || "Не удалось зарегистрироваться.";
          }
        } else {
          this.errorMessage =
            "Ошибка при регистрации. Пожалуйста, проверьте введённые данные.";
        }
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>
