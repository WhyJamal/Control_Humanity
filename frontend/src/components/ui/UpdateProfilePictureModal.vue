<template>
  <div
    v-if="editProfilePicture"
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-2"
  >
    <!-- Modal box -->
    <div class="bg-[#1e293b] rounded-2xl shadow-xl w-full max-w-lg p-8 relative flex flex-col space-y-6">
      <!-- Header -->
      <div class="flex items-center justify-between">
        <h3 class="text-xl font-semibold text-white">Update Profile Picture</h3>
        <button
          @click="closeModal"
          class="text-gray-400 hover:text-white transition-colors"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <!-- Body: preview + file input -->
      <div class="flex flex-col md:flex-row items-center md:items-start gap-6">
        <!-- Image preview -->
        <div class="flex-shrink-0">
          <img
            :src="previewUrl || profile.avatar || defaultAvatar"
            alt="Profile preview"
            class="w-28 h-28 md:w-32 md:h-32 rounded-xl object-cover border-4 border-gray-700"
          />
        </div>

        <!-- File chooser -->
        <div class="flex-1 space-y-3">
          <label class="block text-sm font-medium text-gray-300">Choose new picture</label>
          <div class="flex items-center bg-[#334155] rounded-md overflow-hidden">
            <input
              type="file"
              accept=".svg,.png,.jpg,.jpeg,.gif"
              @change="onFileChange"
              class="flex-1 px-4 py-2 bg-transparent text-gray-200 focus:outline-none"
            />
            <span class="px-4 py-2 bg-gray-600 text-gray-300 text-sm whitespace-nowrap">
              {{ fileName }}
            </span>
          </div>
          <p class="text-xs text-gray-500">SVG, PNG, JPG or GIF (MAX. 800×400px).</p>
        </div>
      </div>

      <!-- Footer: action buttons -->
      <div class="flex flex-col sm:flex-row items-center sm:justify-between space-y-3 sm:space-y-0 sm:space-x-4">
        <div class="flex w-full sm:w-auto space-x-3">
          <button
            @click="upload"
            class="flex-1 bg-[#334155] hover:bg-[#3f4a5e] text-gray-200 px-5 py-2 rounded-lg transition-colors"
          >
            Upload
          </button>
          <button
            @click="deletePicture"
            class="flex-1 bg-transparent border border-gray-500 hover:bg-gray-700 text-gray-200 px-5 py-2 rounded-lg transition-colors"
          >
            Delete
          </button>
        </div>
        <button
          @click="save"
          class="w-full sm:w-auto bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg transition-colors"
        >
          Save Changes
        </button>
      </div>

      <!-- Success / Error messages -->
      <div class="space-y-2">
        <p v-if="success" class="text-center text-green-400">{{ success }}</p>
        <p v-if="error" class="text-center text-red-400">{{ error }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import defaultAvatar from "@/assets/defaultAvatar.png";

export default {
  name: "UpdateProfilePictureModal",
  props: {
    editProfilePicture: {
      type: Boolean,
      required: true,
    },
    profile: {
      type: Object,
      default: () => ({}),
    },
  },
  data() {
    return {
      defaultAvatar,
      file: null,
      fileName: "No file selected",
      previewUrl: "",
      error: "",
      success: "",
    };
  },
  methods: {
    closeModal() {
      this.$emit("update:editProfilePicture", false);
      this.reset();
      this.$emit('close');
    },
    onFileChange(event) {
      const file = event.target.files[0];
      if (!file) return;
      this.file = file;
      this.fileName = file.name;
      this.previewUrl = URL.createObjectURL(file);
    },
    upload() {
      if (!this.file) {
        this.error = "Please select a file first.";
        return;
      }
      this.error = "";
      // TODO: implement upload logic
      this.success = "File ready for upload.";
    },
    deletePicture() {
      this.previewUrl = "";
      this.$emit("deleted");
      this.success = "Picture removed.";
    },
    save() {
      if (!this.file && !this.previewUrl) {
        this.error = "No new image to save.";
        return;
      }
      this.$emit("saved", this.file || this.previewUrl);
      this.success = "Changes saved.";
      setTimeout(() => this.closeModal(), 800);
    },
    reset() {
      this.file = null;
      this.fileName = "No file selected";
      this.previewUrl = "";
      this.error = "";
      this.success = "";
    },
  },
};
</script>

<style scoped>
/* Optional: additional custom styles can be added here */
</style>