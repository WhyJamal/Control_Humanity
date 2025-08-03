<template>
  <transition name="fade">
    <div
      class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50"
    >
      <!-- Confirm Modal -->
      <div
        v-if="showConfirmModal"
        tabindex="-1"
        class="fixed inset-0 z-50 flex items-center justify-center w-full h-full"
      >
        <div class="relative p-4 w-full max-w-md max-h-full">
          <div class="relative bg-white rounded-lg shadow-sm dark:bg-gray-700">
            <div class="p-4 md:p-5 text-center">
              <svg
                v-if="isSuccess"
                class="mx-auto mb-4 text-green-500 w-12 h-12 dark:text-green-400"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 20 20"
                stroke="currentColor"
              >
                <circle
                  cx="10" cy="10" r="9"
                  stroke-width="2"
                />
                <path
                  d="M6 10.5l2.5 2.5L14 7"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>
              <svg
                v-else
                class="mx-auto mb-4 text-red-500 w-12 h-12 dark:text-gray-200"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 20 20"
                stroke="currentColor"
              >
                <path
                  stroke-width="2"
                  d="M10 11V6m0 8h.01M19 10a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
                />
              </svg>
              <h3 class="mb-5 text-lg font-normal text-gray-500 dark:text-gray-400">
                {{ confirmMessage }}
              </h3>
              <button
                type="button"
                @click="closeModal"
                class="text-white bg-red-600 hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 dark:focus:ring-red-800 font-medium rounded-lg text-sm inline-flex items-center px-5 py-2.5"
              >
                OK ({{ countdown }})
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Change Password Form -->
      <div
        v-else
        class="bg-white dark:bg-[#1e293b] p-6 rounded-lg shadow-md w-full max-w-md space-y-4"
      >
        <h2 class="text-gray-900 dark:text-white text-lg font-semibold">
          Change Password
        </h2>

        <div>
          <label class="block text-gray-700 dark:text-white text-sm mb-1">
            Current Password
          </label>
          <input
            type="password"
            v-model="current"
            class="w-full bg-gray-100 dark:bg-[#334155] border border-gray-300 dark:border-gray-600 rounded-md p-2 text-gray-900 dark:text-white focus:outline-none"
          />
        </div>

        <div>
          <label class="block text-gray-700 dark:text-white text-sm mb-1">
            New Password
          </label>
          <input
            type="password"
            v-model="newPass"
            class="w-full bg-gray-100 dark:bg-[#334155] border border-gray-300 dark:border-gray-600 rounded-md p-2 text-gray-900 dark:text-white focus:outline-none"
          />
        </div>

        <div>
          <label class="block text-gray-700 dark:text-white text-sm mb-1">
            Confirm New Password
          </label>
          <input
            type="password"
            v-model="confirm"
            class="w-full bg-gray-100 dark:bg-[#334155] border border-gray-300 dark:border-gray-600 rounded-md p-2 text-gray-900 dark:text-white focus:outline-none"
          />
        </div>

        <div class="flex justify-end space-x-3 pt-2">
          <button
            @click="$emit('close')"
            class="bg-gray-200 dark:bg-gray-700 px-4 py-2 rounded-md text-gray-700 dark:text-white hover:bg-gray-300 dark:hover:bg-gray-600 transition"
          >
            Cancel
          </button>
          <button
            @click="submit"
            :disabled="loading"
            class="bg-green-600 dark:bg-[#420275] px-4 py-2 rounded-md text-white hover:bg-green-700 dark:hover:bg-[#6a04b8] transition disabled:opacity-50"
          >
            <span v-if="loading">Updating...</span>
            <span v-else>Update</span>
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
import api from "@/utils/axios";

export default {
  props: {
    show: { type: Boolean, default: true }
  },
  data() {
    return {
      current: "",
      newPass: "",
      confirm: "",
      loading: false,
      isSuccess: false,
      confirmMessage: "",
      showConfirmModal: false,
      countdown: 10,
      countdownTimer: null,
    };
  },
  methods: {
    async submit() {
      if (this.newPass !== this.confirm) {
        alert("Passwords do not match");
        return;
      }
      this.loading = true;
      try {
        const token = localStorage.getItem("token");
        await api.post(
          "v1/auth/users/set_password/",
          { current_password: this.current, new_password: this.newPass },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        this.isSuccess = true;
        this.confirmMessage = "Password updated successfully";
      } catch {
        this.isSuccess = false;
        this.confirmMessage = "Failed to update password.";
      } finally {
        this.loading = false;
        this.showConfirmModal = true;
      }
    },
    closeModal() {
      this.showConfirmModal = false;
      this.$emit("close");
    },
  },
  watch: {
    showConfirmModal(newVal) {
      if (newVal) {
        this.countdown = 10;
        this.countdownTimer = setInterval(() => {
          if (this.countdown > 0) {
            this.countdown--;   
          } else {
            clearInterval(this.countdownTimer);
            this.closeModal();
          }
        }, 1000);
      } else {
        clearInterval(this.countdownTimer);
      }
    },
  },
};
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
