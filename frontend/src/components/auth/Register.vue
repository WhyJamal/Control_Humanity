<template>
  <Transition appear>
    <div v-if="show" class="fixed inset-0 z-40 flex items-center justify-center bg-black/50 dark:bg-black/60">
      <div class="bg-white dark:bg-[#1e1f22] text-gray-800 dark:text-gray-200 rounded-2xl shadow-xl w-full max-w-2xl p-6 relative">
        <!-- Close Button -->
        <button
          @click="$emit('close')"
          class="absolute top-4 right-4 text-gray-500 dark:text-gray-300 hover:text-gray-700 dark:hover:text-gray-100"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

        <h2 class="text-2xl font-bold text-center mb-6">Создать пользователя</h2>

        <form @submit.prevent="handleRegister" class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Left Column -->
          <div class="space-y-4">
            <div>
              <label for="username" class="block font-medium mb-1">Имя пользователя</label>
              <input v-model="form.username" id="username" type="text" placeholder="Введите имя пользователя"
                class="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-[#242629] text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500" />
            </div>

            <div>
              <label for="email" class="block font-medium mb-1">Электронная почта</label>
              <input v-model="form.email" id="email" type="email" placeholder="Введите эл. почту"
                class="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-[#242629] text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500" />
            </div>

            <div>
              <label for="phone" class="block font-medium mb-1">Телефон</label>
              <input v-model="form.phone" id="phone" type="text" placeholder="Введите номер телефона"
                class="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-[#242629] text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500" />
            </div>

            <div>
              <label for="role" class="block font-medium mb-1">Роль</label>
              <Listbox v-model="form.role">
                <div class="relative">
                  <ListboxButton
                    class="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-[#242629] text-gray-900 dark:text-white flex justify-between items-center focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  >
                    <span>{{ roleLabels[form.role] || 'Выберите роль' }}</span>
                    <ChevronUpDownIcon class="w-5 h-5 text-gray-500 dark:text-gray-300" />
                  </ListboxButton>

                  <Transition
                    enter="transition ease-out duration-100"
                    enter-from="opacity-0 scale-95"
                    enter-to="opacity-100 scale-100"
                    leave="transition ease-in duration-75"
                    leave-from="opacity-100 scale-100"
                    leave-to="opacity-0 scale-95"
                  >
                    <ListboxOptions class="absolute mt-2 w-full bg-white dark:bg-[#242629] border border-gray-200 dark:border-gray-600 rounded-lg shadow-lg z-50">
                      <ListboxOption
                        v-for="role in roles"
                        :key="role"
                        :value="role"
                        class="cursor-pointer select-none relative py-2 pl-10 pr-4 hover:bg-gray-100 dark:hover:bg-gray-700"
                        v-slot="{ selected }"
                      >
                        <span :class="[selected ? 'font-semibold text-gray-900 dark:text-white' : 'text-gray-700 dark:text-gray-300']">
                          {{ roleLabels[role] }}
                        </span>
                        <span
                          v-if="selected"
                          class="absolute inset-y-0 left-0 flex items-center pl-3 text-indigo-500"
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

          <!-- Right Column -->
          <div class="space-y-4">
            <div>
              <label for="first_name" class="block font-medium mb-1">Имя</label>
              <input v-model="form.first_name" id="first_name" type="text" placeholder="Ваше имя"
                class="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-[#242629] text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500" />
            </div>

            <div>
              <label for="last_name" class="block font-medium mb-1">Фамилия</label>
              <input v-model="form.last_name" id="last_name" type="text" placeholder="Ваша фамилия"
                class="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-[#242629] text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500" />
            </div>

            <div>
              <label for="password" class="block font-medium mb-1">Пароль</label>
              <input v-model="form.password" id="password" type="password" placeholder="Введите пароль"
                class="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-[#242629] text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500" />
            </div>

            <div>
              <label for="password2" class="block font-medium mb-1">Подтверждение пароля</label>
              <input v-model="form.password2" id="password2" type="password" placeholder="Повторите пароль"
                class="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-[#242629] text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500" />
            </div>
          </div>

          <!-- Submit -->
          <div class="col-span-1 md:col-span-2 text-center mt-4">
            <div v-if="errorMessage" class="text-red-600 text-sm mb-2">
              {{ errorMessage }}
            </div>
            <button type="submit" :disabled="loading"
              class="w-full bg-green-500 hover:bg-green-700 dark:bg-indigo-950 dark:hover:bg-indigo-900 text-white font-semibold py-2 rounded-lg transition"
            >
              <span v-if="loading">Регистрация...</span>
              <span v-else>Зарегистрироваться</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref } from 'vue';
import api from '@/utils/axios';
import { ChevronUpDownIcon, CheckIcon } from '@heroicons/vue/24/solid';

const props = defineProps({
  show: Boolean
});
const emit = defineEmits(['close', 'registered']);

const form = ref({ username: '', email: '', phone: '', first_name: '', last_name: '', role: '', password: '', password2: '' });
const roles = ['admin', 'director', 'manager', 'employee'];
const roleLabels = { admin: 'Админ', director: 'Директор', manager: 'Менеджер', employee: 'Сотрудник' };
const loading = ref(false);
const errorMessage = ref('');

async function handleRegister() {
  errorMessage.value = '';
  const f = form.value;
  if (!f.username || !f.email || !f.phone || !f.first_name || !f.last_name || !f.role || !f.password || !f.password2) {
    errorMessage.value = 'Пожалуйста, заполните все поля.';
    return;
  }
  if (f.password !== f.password2) {
    errorMessage.value = 'Пароли не совпадают.';
    return;
  }

  try {
    loading.value = true;
    await api.post('/auth/register/', f);
    emit('registered');
    emit('close');
  } catch (err) {
    const data = err.response?.data;
    errorMessage.value = data
      ? (typeof data === 'object' ? Object.values(data).flat().join(' ') : data)
      : 'Ошибка при регистрации.';
  } finally {
    loading.value = false;
  }
}
</script>