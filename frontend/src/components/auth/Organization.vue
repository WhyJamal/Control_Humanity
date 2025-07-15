<template>
  <div
    class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-700 via-indigo-800 to-purple-900 p-4"
    :style="{
      backgroundImage: `url(${photoLogin})`,
      backgroundSize: 'cover',
      backgroundPosition: 'center',
    }"
  >
    <div
      class="w-full max-w-md bg-white/10 backdrop-blur-lg rounded-2xl shadow-2xl p-8 border border-white/20"
    >
      <h2 class="text-3xl font-bold text-white text-center mb-6 tracking-wide">
        Создать организацию
      </h2>

      <form class="space-y-6">
        <div>
          <label for="name" class="block text-gray-200 font-medium mb-1"
            >Название организации</label
          >
          <input
            v-model="organization.name"
            type="text"
            id="name"
            placeholder="ООО Пример"
            class="w-full p-3 rounded-lg bg-gray-800 text-gray-100 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
        </div>

        <div>
          <label for="inn" class="block text-gray-200 font-medium mb-1"
            >ИНН</label
          >
          <input
            v-model="organization.inn"
            type="text"
            id="inn"
            placeholder="123456789012"
            maxlength="12"
            pattern="\d{1,12}"
            @input="validateInn"
            class="w-full p-2 rounded border"
          />
        </div>

        <div v-if="errorMessage" class="text-red-400 text-sm mt-2">
          {{ errorMessage }}
        </div>

        <button
          type="button"
          @click="createOrganization"
          class="w-full bg-gradient-to-r from-purple-500 to-pink-500 text-white font-semibold py-3 rounded-xl shadow-lg hover:from-purple-600 hover:to-pink-600 transition duration-300"
        >
          Сохранить
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import photoLogin from "@/assets/photo_login_page.png";
import api from "@/utils/axios";

export default {
  name: "Organization",
  data() {
    return {
      organization: {
        name: "",
        inn: "",
      },
      errorMessage: "",
      photoLogin,
    };
  },
  methods: {
    async createOrganization() {
      this.errorMessage = "";

      if (!this.organization.name || !this.organization.inn) {
        this.errorMessage = "Пожалуйста, заполните все поля.";
        return;
      }

      try {
        await this.submitOrganization(); 
        this.$router.push({ name: "Login" });
      } catch (err) {
        if (err.response?.data?.inn) {
          this.errorMessage = err.response.data.inn[0];
        } else if (err.response?.data?.detail) {
          this.errorMessage = err.response.data.detail;
        } else {
          this.errorMessage = "Ошибка при создании организации.";
        }
      }
    },
    async submitOrganization() {
      return await api.post("/organizations/", this.organization);
    },
  },
};
</script>
