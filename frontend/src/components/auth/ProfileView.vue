<template>
<!-- Bosh konteyner: butun sahifa bo‘ylab padding va fon -->
<div class="bg-[#1e293b] rounded-lg shadow-md p-6 space-y-6 border border-gray-700">
<button
  @click="closeModal"
  class="absolute top-4 right-4 text-white hover:text-gray-400 text-xl"
>
  &times;
</button>
  <!-- 1. Yuqori qator (2 ustun: Chap – profil, O‘ng – sozlamalar) -->
  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
    
    <!-- 1.1 Chap ustun: Profil rasim va ism -->
    <div class="bg-[#1e293b] rounded-lg shadow-md p-6">
      <!-- Sarlavha -->
      <h2 class="text-lg font-semibold mb-4">
        Profile picture <span class="text-gray-400 text-sm">❓</span>
      </h2>
      <!-- Rasm + ism qatori -->
      <div class="flex items-center space-x-4">
        <img :src="profile.avatar || defaultAvatar" class="w-20 h-20 rounded-xl" />
        <div>
          <span class="text-xs bg-blue-600 px-2 py-0.5 rounded-lg text-white">PRO</span>
          <h3 class="text-xl font-bold mt-1">Joseph McFall</h3>
          <p class="text-gray-400">Web Developer</p>
        </div>
      </div>
      <hr class="my-6 border-gray-700" />
      <!-- Edit tugma -->
      <button @click="editProfilePicture = true" class="bg-blue-600 px-4 py-2 rounded-md">Edit</button>
    </div>

    <!-- 1.2 O‘ng ustun: Form sozlamalari -->
    <div class="bg-[#1e293b] rounded-lg shadow-md p-6 space-y-4">
      <!-- Ichkarida yana 2 ustunli grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <!-- Timezone -->
        <div>
          <label class="block text-sm mb-1">Timezone ❓</label>
          <select class="w-full bg-[#334155] border rounded-md p-2 text-white">
            <option>UTC-08:00 (PST)</option>
          </select>
        </div>
        <!-- Language -->
        <div>
          <label class="block text-sm mb-1">Language</label>
          <select class="w-full bg-[#334155] border rounded-md p-2 text-white">
            <option>Choose your account type</option>
          </select>
        </div>
        <!-- Date of birth -->
        <div>
          <label class="block text-sm mb-1">Date of birth</label>
          <input type="date" class="w-full bg-[#334155] border rounded-md p-2 text-white" />
        </div>
        <!-- Gender -->
        <div>
          <label class="block text-sm mb-1">Gender</label>
          <select class="w-full bg-[#334155] border rounded-md p-2 text-white">
            <option>Choose your gender</option>
          </select>
        </div>
      </div>
      <hr class="border-gray-700" />
      <!-- Save tugma -->
      <button class="bg-blue-600 px-4 py-2 rounded-md">Save</button>
    </div>

  </div>

  <!-- 2. Pastki bo‘lim: Personal information -->
  <div class="bg-[#1e2900] rounded-lg shadow-md p-6">
    <!-- Sarlavha -->
    <h2 class="text-lg font-semibold mb-4">Personal information ❓</h2>
    <!-- Pastki bo‘lim ichida 2 ustun -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      
      <!-- 2.1 Chap ustun: Biography va social -->
      <div class="space-y-4">
        <div>
          <strong>Full name</strong>
          <p>Joseph McFall</p>
        </div>
        <div>
          <strong>Biography</strong>
          <p>I am Joseph McFall, a fervent explorer…</p>
        </div>
        <div>
          <strong>Social</strong>
          <div class="flex space-x-3 text-gray-400 text-xl">
            <!-- ikonalar -->
          </div>
        </div>
        <div>
          <strong>Location</strong>
          <p>📍 California, USA</p>
        </div>
        <div>
          <strong>Job Title</strong>
          <p>💼 Frontend Developer</p>
        </div>
      </div>

      <!-- 2.2 O‘ng ustun: Contact va skills -->
      <div class="space-y-4">
        <div>
          <strong>Email Address</strong>
          <p>helene@company.com</p>
        </div>
        <div>
          <strong>Home Address</strong>
          <p>92 Miles Drive, Newark, NJ 07103</p>
        </div>
        <div>
          <strong>Phone Number</strong>
          <p>+1234 567 890 / +12 345 678</p>
        </div>
        <div>
          <strong>Software Skills</strong>
          <div class="flex space-x-2 text-lg">
            <!-- skill ikonalar -->
          </div>
        </div>
        <div>
          <strong>Languages</strong>
          <p>English, French, Spanish</p>
        </div>
      </div>

    </div>
    <hr class="my-4 border-gray-700" />
    <!-- Oxirgi Edit tugma -->
    <button class="bg-blue-600 px-4 py-2 rounded-md">Edit</button>
  </div>
<update-profile-picture-modal
    :edit-profile-picture.sync="editProfilePicture"
    :profile="profile"
    @saved="handleSaved"
    @deleted="handleDeleted"
  />
</div>

</template>

<script>
import api from "@/utils/axios";
import { mapState } from "vuex";
import defaultAvatar from "../../assets/Default.png";
import UpdateProfilePictureModal from '@/components/ui/UpdateProfilePictureModal.vue';

export default {
  name: "ProfileView",
  components: { UpdateProfilePictureModal }, 
  props: {
    profile: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      error: "",
      success: "",
      defaultAvatar,
      editProfilePicture: false,
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
      this.$emit("close");
    },
  },
};
</script>
