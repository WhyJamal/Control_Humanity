<template>
  <div
    class="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-400 via-purple-500 to-indigo-700 p-4"
    :style="{ backgroundImage: `url(${photoLogin})`, backgroundSize: 'cover', backgroundPosition: 'center' }"
  >
    <div class="w-full max-w-4xl bg-white/10 backdrop-blur-xl rounded-2xl shadow-2xl p-8 border border-white/20">
      <h2 class="text-3xl font-bold text-white text-center mb-6 tracking-wide">
        Создать пользователя
      </h2>

      <form @submit.prevent="handleRegister" class="grid grid-cols-1 md:grid-cols-2 gap-5">
        <!-- Left column -->
        <div class="space-y-5">
          <div>
            <label for="username" class="block text-white font-medium mb-1">Имя пользователя</label>
            <input v-model="form.username" id="username" type="text" placeholder="Введите имя пользователя"
              class="w-full p-3 rounded-lg bg-white/10 text-white placeholder-white/70 border border-white/30 focus:outline-none focus:ring-2 focus:ring-white" />
          </div>

          <div>
            <label for="email" class="block text-white font-medium mb-1">Электронная почта</label>
            <input v-model="form.email" id="email" type="email" placeholder="Введите эл. почту"
              class="w-full p-3 rounded-lg bg-white/10 text-white placeholder-white/70 border border-white/30 focus:outline-none focus:ring-2 focus:ring-white" />
          </div>

          <div>
            <label for="phone" class="block text-white font-medium mb-1">Телефон</label>
            <input v-model="form.phone" id="phone" type="text" placeholder="Введите номер телефона"
              class="w-full p-3 rounded-lg bg-white/10 text-white placeholder-white/70 border border-white/30 focus:outline-none focus:ring-2 focus:ring-white" />
          </div>

          <!-- Role select -->
          <div class="w-full max-w-sm">
            <label for="role" class="block text-white font-medium mb-1">Роль</label>
              <Listbox v-model="form.role">
                <div class="relative">
                  <ListboxButton
                    class="w-full p-3 rounded-lg bg-white/10 text-white border border-white/30 focus:outline-none focus:ring-2 focus:ring-white flex justify-between items-center"
                  >
                    <span>{{ roleLabels[form.role] || 'Выберите роль' }}</span>
                    <ChevronUpDownIcon class="w-5 h-5 text-white/70" />
                  </ListboxButton>

                  <Transition
                    enter="transition ease-out duration-100"
                    enter-from="opacity-0 scale-95"
                    enter-to="opacity-100 scale-100"
                    leave="transition ease-in duration-75"
                    leave-from="opacity-100 scale-100"
                    leave-to="opacity-0 scale-95"
                  >
                    <ListboxOptions
                      class="absolute mt-2 w-full bg-black/60 backdrop-blur-lg rounded-lg shadow-lg z-50 ring-1 ring-black/20 focus:outline-none"
                    >
                      <ListboxOption
                        v-for="role in roles"
                        :key="role"
                        :value="role"
                        class="cursor-pointer select-none relative py-2 pl-10 pr-4 hover:bg-white/20"
                        v-slot="{ selected }"
                      >
                        <span :class="[selected ? 'font-semibold text-black' : 'text-white']">
                          {{ roleLabels[role] }}
                        </span>
                        <span
                          v-if="selected"
                          class="absolute inset-y-0 left-0 flex items-center pl-3 text-white"
                        >
                          <CheckIcon class="w-5 h-5" />
                        </span>
                      </ListboxOption>
                    </ListboxOptions>
                  </Transition>
                </div>
              </Listbox>
            </div>
          </div>

        <!-- Right column -->
        <div class="space-y-5">
          <div>
            <label for="first_name" class="block text-white font-medium mb-1">Имя</label>
            <input v-model="form.first_name" id="first_name" type="text" placeholder="Ваше имя"
              class="w-full p-3 rounded-lg bg-white/10 text-white placeholder-white/70 border border-white/30 focus:outline-none focus:ring-2 focus:ring-white" />
          </div>

          <div>
            <label for="last_name" class="block text-white font-medium mb-1">Фамилия</label>
            <input v-model="form.last_name" id="last_name" type="text" placeholder="Ваша фамилия"
              class="w-full p-3 rounded-lg bg-white/10 text-white placeholder-white/70 border border-white/30 focus:outline-none focus:ring-2 focus:ring-white" />
          </div>

          <div>
            <label for="password" class="block text-white font-medium mb-1">Пароль</label>
            <input v-model="form.password" id="password" type="password" placeholder="Введите пароль"
              class="w-full p-3 rounded-lg bg-white/10 text-white placeholder-white/70 border border-white/30 focus:outline-none focus:ring-2 focus:ring-white" />
          </div>

          <div>
            <label for="password2" class="block text-white font-medium mb-1">Подтверждение пароля</label>
            <input v-model="form.password2" id="password2" type="password" placeholder="Повторите пароль"
              class="w-full p-3 rounded-lg bg-white/10 text-white placeholder-white/70 border border-white/30 focus:outline-none focus:ring-2 focus:ring-white" />
          </div>
        </div>

        <!-- Full-width row -->
        <div class="col-span-1 md:col-span-2">
          <div v-if="errorMessage" class="text-red-300 text-sm mb-3">
            {{ errorMessage }}
          </div>
          <button type="submit" :disabled="loading"
            class="w-full bg-white text-indigo-700 font-semibold py-3 rounded-xl shadow-xl hover:bg-indigo-100 transition duration-300">
            <span v-if="loading">Регистрация...</span>
            <span v-else>Зарегистрироваться</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>


<script>
import api from "@/utils/axios";
import photoLogin from '@/assets/photo_login_page.png';
import { ChevronUpDownIcon, CheckIcon } from '@heroicons/vue/24/solid';
import { Transition } from 'vue';

export default {
  name: "Register",
  components: {
    ChevronUpDownIcon,
    CheckIcon,
  },
  data() {
    return {
      photoLogin,
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
      roles: ['admin', 'director', 'manager', 'employee'],
      roleLabels: {
        admin: 'Админ',
        director: 'Директор',
        manager: 'Менеджер',
        employee: 'Сотрудник',
      },
      loading: false,
      errorMessage: "",
    };
  },
  methods: {
    async handleRegister() {
      this.errorMessage = "";

      const f = this.form;
      if (
        !f.username || !f.email || !f.phone ||
        !f.first_name || !f.last_name ||
        !f.role || !f.password || !f.password2
      ) {
        this.errorMessage = "Пожалуйста, заполните все поля.";
        return;
      }
      if (f.password !== f.password2) {
        this.errorMessage = "Пароли не совпадают.";
        return;
      }

      try {
        this.loading = true;
        await api.post("/auth/register/", {
                        username:   f.username,
                        email:      f.email,
                        phone:      f.phone,
                        first_name: f.first_name,
                        last_name:  f.last_name,
                        role:       f.role,
                        password:   f.password,
                        password2:  f.password2,
                      });
        this.$router.push("/users");
      } catch (err) {
        if (err.response?.data) {
          const data = err.response.data;
          this.errorMessage = typeof data === "object"
            ? Object.values(data).flat().join(" ")
            : data;
        } else {
          this.errorMessage = "Ошибка при регистрации. Пожалуйста, проверьте введённые данные.";
        }
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>