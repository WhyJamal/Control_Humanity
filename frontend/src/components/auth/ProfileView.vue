<template>
  <div
    class="w-full min-h-screen bg-[#1e293b] rounded-lg shadow-md p-6 space-y-6 border border-gray-700 relative"
  >
    <!-- <button
      @click="closeModal"
      class="absolute top-4 right-4 text-white hover:text-gray-400 text-xl"
    >
      &times;
    </button> -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div
        class="dark:bg-neutral-900/90 dark:border-neutral-700 dark:text-gray-200 rounded-lg shadow-md p-6"
      >
        <div class="flex items-center space-x-4">
          <img
            :src="profile.profile_picture || defaultAvatar"
            class="w-20 h-20 rounded-xl"
          />
          <div>
            <span class="text-xs bg-blue-600 px-2 py-0.5 rounded-lg text-white"
              >PRO</span
            >
            <h3 class="text-xl font-bold mt-1">
              {{ profile.first_name }} {{ profile.last_name }}
            </h3>
            <p class="text-gray-400">{{ profile.role }}</p>
          </div>
        </div>
        <hr class="my-6 border-gray-700" />
        <button
          v-if="user && user.id === profile.id"
          @click="editProfilePicture = true"
          class="text-base font-semibold bg-blue-600 px-4 py-2 rounded-md"
        >
          Edit
        </button>
      </div>

      <div
        class="dark:bg-neutral-900/90 dark:border-neutral-700 dark:text-gray-200 rounded-lg shadow-md p-6 space-y-4"
      >
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <strong class="text-gray-300 block text-sm mb-1">Timezone</strong>
            <select
              class="w-full bg-[#334155] border rounded-md p-2 text-white"
            >
              <option>UTC-08:00 (PST)</option>
            </select>
          </div>
          <div>
            <strong class="text-gray-300 block text-sm mb-1">Language</strong>
            <div
              class="w-full bg-[#334155] border border-gray-300 rounded-md p-2 text-white"
            >
              {{ profile.language }}
            </div>
          </div>
          <div>
            <strong class="text-gray-300 block text-sm mb-1"
              >Date of birth</strong
            >
            <input
              type="date"
              v-model="profile.date_of_birth"
              class="w-full bg-[#334155] border border-gray-300 rounded-md p-2 text-white"
            />
          </div>
          <div>
            <strong class="text-gray-300 block text-sm mb-1">Gender</strong>
            <div
              class="w-full bg-[#334155] border border-gray-100 rounded-md p-2 text-white"
            >
              {{ profile.gender }}
            </div>
          </div>
        </div>
        <hr class="border-gray-700" />
        <button
          v-if="user && user.id === profile.id"
          class="text-base font-semibold bg-blue-600 px-4 py-2 rounded-md"
          @click="saveProfile"
        >
          Save
        </button>
      </div>
    </div>

    <div
      class="dark:bg-neutral-900/90 dark:border-neutral-700 dark:text-gray-200 rounded-lg shadow-md p-6"
    >
      <h2 class="text-gray-200 text-lg font-semibold mb-4">
        Personal information
      </h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="space-y-4">
          <div>
            <strong class="text-gray-300">Full name</strong>
            <p class="text-gray-400">
              {{ profile.first_name }} {{ profile.last_name }}
            </p>
          </div>
          <div>
            <strong class="text-gray-300">Biography</strong>
            <p class="text-gray-400">
              I am {{ profile.first_name }}, {{ profile.bio }}
            </p>
          </div>
          <div>
            <strong class="text-gray-300">Social</strong>
            <div class="flex mt-2 space-x-3 text-gray-400 text-xl">
              <a
                v-for="(handle, key) in profile.social_links"
                :key="key"
                :href="
                  handle.startsWith('http')
                    ? handle
                    : (platformMap[key.replace(/_\d+$/, '')]?.prefix || '') +
                      handle.replace(/^@/, '')
                "
                target="_blank"
                rel="noopener noreferrer"
                class="hover:text-white transition"
              >
              <img
                :src="`/icons/${key.replace(/_\d+$/, '')}.png`"
                :alt="key"
                class="w-6 h-6"
              />
              </a>
            </div>
          </div>
          <div>
            <strong class="text-gray-300">Location</strong>
            <p class="text-gray-400">{{ profile.location }}</p>
          </div>
          <!-- <div>
            <strong>Job Title</strong>
            <p>💼 Frontend Developer</p>
          </div> -->
        </div>
        <div class="space-y-4">
          <div>
            <strong class="text-gray-300">Email Address</strong>
            <p class="text-gray-400">{{ profile.email }}</p>
          </div>
          <div>
            <strong class="text-gray-300">Home Address</strong>
            <p class="text-gray-400">{{ profile.address }}</p>
          </div>
          <div>
            <strong class="text-gray-300">Phone Number</strong>
            <p class="text-gray-400">{{ profile.phone }}</p>
          </div>
          <div>
            <strong class="text-gray-300">Software Skills</strong>
            <div class="flex space-x-2 text-lg">
              <!-- Skills -->
            </div>
          </div>
          <!-- <div>
            <strong>Languages</strong>
            <p>English, French, Spanish</p>
          </div> -->
        </div>
      </div>
      <hr class="my-4 border-gray-700" />
      <div class="flex space-x-4" v-if="user && user.id === profile.id">
        <router-link
          class="text-base font-semibold bg-blue-700 px-4 py-2 rounded-md hover:bg-[#6874fc]"
          :to="{ name: 'ProfileSettings', params: { userId: user.id } }"
        >
          Edit
        </router-link>
        <button
          @click="showChangePassword = true"
          class="text-base font-semibold bg-[#420275] px-4 py-2 rounded-md text-white hover:bg-[#6a04b8]"
        >
          Change Password
        </button>
      </div>

      <!-- Modal -->
      <ChangePasswordModal
        v-if="showChangePassword"
        @close="showChangePassword = false"
      />
    </div>

    <!-- Edit rasm modal -->
    <UpdateProfilePictureModal
      :edit-profile-picture.sync="editProfilePicture"
      :profile="profile"
      @saved="handleSaved"
      @deleted="handleDeleted"
      @close="editProfilePicture = false"
    />
  </div>
</template>

<script>
import api from "@/utils/axios";
import { mapState } from "vuex";
import UpdateProfilePictureModal from "@/components/ui/UpdateProfilePictureModal.vue";
import ChangePasswordModal from "@/components/ui/ChangePasswordModal.vue";

export default {
  name: "ProfileView",
  components: { UpdateProfilePictureModal, ChangePasswordModal },
  data() {
    return {
      profile: {},
      error: "",
      success: "",
      defaultAvatar: '/avatar.png',
      editProfilePicture: false,
      showChangePassword: false,
    };
  },
  computed: {
    ...mapState("auth", ["user"]),
    isSelf() {
      return this.user.id === this.profile.id;
    },
    isDirector() {
      return this.user.role === "director";
    },
    canEditOwn() {
      return this.isSelf;
    },
    canEditRole() {
      return this.isDirector && !this.isSelf;
    },
    platformMap() {
      return {
        telegram: { prefix: "https://t.me/" },
        twitter: { prefix: "https://twitter.com/" },
        github: { prefix: "https://github.com/" },
        linkedin: { prefix: "https://linkedin.com/in/" },
        facebook: { prefix: "https://facebook.com/" },
        instagram: { prefix: "https://instagram.com/" },
      };
    },
  },
  async created() {
    try {
      const id = this.$route.params.userId;
      const response = await api.get(`/auth/users/${id}/`);
      this.profile = response.data;
    } catch (e) {
      this.error = "Failed to load profile.";
    }
  },
  methods: {
    async saveProfile() {
      this.error = "";
      this.success = "";
      try {
        await api.patch(`/auth/users/${this.profile.id}/`, {
          username: this.profile.username,
          email: this.profile.email,
          first_name: this.profile.first_name,
          last_name: this.profile.last_name,
        });
        this.success = "Profile updated successfully.";
      } catch (e) {
        this.error = "Failed to update profile.";
      }
    },
    async saveRole() {
      this.error = "";
      this.success = "";
      try {
        await api.patch(`/auth/users/${this.profile.id}/`, {
          role: this.profile.role,
        });
        this.success = "Role updated successfully.";
      } catch (e) {
        this.error = "Failed to update role.";
      }
    },
    closeModal() {
      this.$router.back();
    },
    handleSaved(updatedProfile) {
      this.profile = updatedProfile;
      this.editProfilePicture = false;
    },
    handleDeleted() {
      this.profile.avatar = null;
      this.editProfilePicture = false;
    },
  },
};
</script>

<style scoped>
/* Optional: stil o‘zgartirishlar */
</style>
