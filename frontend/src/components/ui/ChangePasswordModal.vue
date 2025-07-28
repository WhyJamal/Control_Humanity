<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
    <div class="bg-[#1e293b] p-6 rounded-lg shadow-md w-full max-w-md space-y-4">
      <h2 class="text-white text-lg font-semibold">Change Password</h2>

      <div>
        <label class="block text-white text-sm mb-1">Current Password</label>
        <input type="password" v-model="current" class="w-full bg-[#334155] border rounded-md p-2 text-white" />
      </div>

      <div>
        <label class="block text-white text-sm mb-1">New Password</label>
        <input type="password" v-model="newPass" class="w-full bg-[#334155] border rounded-md p-2 text-white" />
      </div>

      <div>
        <label class="block text-white text-sm mb-1">Confirm New Password</label>
        <input type="password" v-model="confirm" class="w-full bg-[#334155] border rounded-md p-2 text-white" />
      </div>

      <div class="flex justify-end space-x-3 pt-2">
        <button @click="$emit('close')" class="bg-gray-600 px-4 py-2 rounded-md text-white">Cancel</button>
        <button @click="submit" class="bg-blue-600 px-4 py-2 rounded-md text-white" :disabled="loading">
          <span v-if="loading">Updating...</span>
          <span v-else>Update</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/utils/axios'

export default {
  data() {
    return {
      current: '',
      newPass: '',
      confirm: '',
      loading: false,
    }
  },
  methods: {
    async submit() {
      if (this.newPass !== this.confirm) {
        alert("Passwords do not match");
        return;
      }

      try {
        this.loading = true;
        const token = localStorage.getItem('token');

        await api.post('v1/auth/users/set_password/', {
          current_password: this.current,
          new_password: this.newPass
        }, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });

        alert("Password updated successfully!");
        this.$emit('close');

      } catch (err) {
        console.error(err);
        const detail = err.response?.data?.current_password?.[0]
          || err.response?.data?.new_password?.[0]
          || err.response?.data?.detail
          || "Failed to update password.";
        alert(detail);
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>
