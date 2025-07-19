<template>
  <div class="w-full max-w-3xl mx-auto">
    <h3 class="text-2xl font-bold mb-6 text-white">Новый проект</h3>

    <form
      @submit.prevent="handleSubmit"
      enctype="multipart/form-data"
      class="bg-gradient-to-br from-[#2a2c31] to-[#1e1f22] border border-neutral-700 text-white p-8 rounded-2xl shadow-xl space-y-6"
    >
      <!-- Grid контейнер для полей -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Название проекта -->
        <div>
          <label
            class="block mb-2 font-semibold text-base text-gray-300"
            for="name"
            >Название проекта *</label
          >
          <input
            v-model="form.name"
            id="name"
            type="text"
            placeholder="Введите название проекта"
            class="w-full px-4 py-3 rounded-lg border border-neutral-600 bg-neutral-900 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-purple-500"
            required
          />
        </div>

        <div>
          <label
            class="block mb-2 font-semibold text-base text-gray-300"
            for="end_date"
            >Дата окончания</label
          >
          <flat-pickr
            v-model="form.end_date"
            id="end_date"
            :config="datePickerConfig"
            class="w-full px-4 py-3 rounded-lg border border-neutral-600 bg-neutral-900 text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
          />
        </div>

        <!-- Менеджер -->
        <div class="md:col-span-2">
          <label
            class="block mb-2 font-semibold text-base text-gray-300"
            for="manager"
            >Назначить менеджера</label
          >
          <div class="relative">
            <Listbox v-model="form.manager_id">
              <div class="relative">
                <ListboxButton
                  class="w-full px-4 py-3 rounded-lg bg-neutral-900 border border-neutral-600 text-white flex justify-between items-center focus:outline-none focus:ring-2 focus:ring-purple-500"
                >
                  <span>
                    {{
                      managers.find((m) => m.id === form.manager_id)
                        ?.username || "Выберите менеджера"
                    }}
                  </span>
                  <ChevronUpDownIcon class="w-5 h-5 text-gray-400" />
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
                    class="absolute mt-2 w-full bg-neutral-800 rounded-lg shadow-lg z-50 ring-1 ring-black/20 focus:outline-none"
                  >
                    <ListboxOption
                      v-for="mgr in managers"
                      :key="mgr.id"
                      :value="mgr.id"
                      class="cursor-pointer select-none relative py-2 pl-10 pr-4 hover:bg-neutral-700 rounded-lg"
                      v-slot="{ selected }"
                    >
                      <span
                        :class="[
                          selected
                            ? 'font-semibold text-white'
                            : 'text-gray-300',
                        ]"
                      >
                        {{ mgr.username }}
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
      </div>

      <!-- Описание -->
      <div>
        <label
          class="block mb-2 font-semibold text-base text-gray-300"
          for="description"
          >Описание</label
        >
        <textarea
          v-model="form.description"
          id="description"
          rows="3"
          placeholder="Введите описание проекта"
          class="w-full px-4 py-3 rounded-lg border border-neutral-600 bg-neutral-900 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-purple-500"
        ></textarea>
      </div>

      <!-- Изображение проекта -->
      <div>
        <label
          class="block mb-2 font-semibold text-base text-gray-300"
          for="image"
          >Изображение проекта</label
        >
        <input
          @change="handleImageChange"
          id="image"
          type="file"
          accept="image/*"
          class="w-full p-2 rounded-lg border border-neutral-600 bg-neutral-900 text-white file:mr-4 file:py-2 file:px-3 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-purple-600 file:text-white hover:file:bg-purple-700"
        />
      </div>

      <!-- Ошибка -->
      <div v-if="errorMessage" class="text-red-400 text-sm">
        {{ errorMessage }}
      </div>

      <!-- Кнопки -->
      <div class="flex justify-end space-x-4 pt-4">
        <button
          type="button"
          @click="$emit('cancel')"
          class="px-6 py-3 border border-gray-500 text-white rounded-lg hover:bg-neutral-800 transition duration-200"
        >
          Отменить
        </button>
        <button
          type="submit"
          class="px-6 py-3 bg-purple-600 hover:bg-purple-700 text-white font-medium text-base rounded-lg transition duration-200 flex items-center justify-center"
          :disabled="loading"
        >
          <svg
            v-if="loading"
            class="animate-spin -ml-1 mr-2 h-5 w-5 text-white"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              class="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              stroke-width="4"
            ></circle>
            <path
              class="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8v8z"
            ></path>
          </svg>
          <span>{{ loading ? "Добавление..." : "Добавить" }}</span>
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import api from "@/utils/axios";
import { CheckIcon, ChevronUpDownIcon } from "@heroicons/vue/24/solid";
import { Transition } from "vue";

export default {
  name: "ProjectForm",
  components: {
    ChevronUpDownIcon,
    CheckIcon,
  },
  data() {
    return {
      form: {
        name: "",
        description: "",
        manager_id: "",
        end_date: "",
        image: null,
        datePickerConfig: {
          dateFormat: "d.m.Y",
          altInput: true,
          altFormat: "j F, Y",
          minDate: "today",
        },
      },
      managers: [],
      loading: false,
      errorMessage: "",
    };
  },
  methods: {
    async fetchManagers() {
      try {
        const response = await api.get("/auth/users/managers/");
        this.managers = response.data;
      } catch (err) {
        console.error("Failed to fetch managers:", err);
      }
    },
    handleImageChange(event) {
      this.form.image = event.target.files[0];
    },
    async handleSubmit() {
      this.errorMessage = "";
      if (!this.form.name) {
        this.errorMessage = "Название проекта обязательно.";
        return;
      }

      const payload = new FormData();
      payload.append("name", this.form.name);
      payload.append("description", this.form.description);
      // payload.append('manager', this.form.manager)
      payload.append("manager_id", this.form.manager_id);
      if (this.form.end_date) payload.append("end_date", this.form.end_date);
      if (this.form.image) payload.append("image", this.form.image);

      try {
        this.loading = true;
        await api.post("/projects/", payload, {
          headers: { "Content-Type": "multipart/form-data" },
        });
        this.$emit("saved");
      } catch (err) {
        console.error(err);
        this.errorMessage = "Не удалось создать проект.";
      } finally {
        this.loading = false;
      }
    },
  },
  created() {
    this.fetchManagers();
  },
};
</script>
