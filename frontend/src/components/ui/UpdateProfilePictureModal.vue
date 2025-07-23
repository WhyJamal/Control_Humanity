<template>
  <!-- Modal overlay -->
  <div
    v-if="editProfilePicture"
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
  >
    <!-- Modal box -->
    <div class="bg-[#1e293b] rounded-lg shadow-xl w-full max-w-md p-6 relative">
      <!-- Header -->
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-semibold text-white">Update profile picture</h3>
        <button @click="close" class="text-gray-400 hover:text-white">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none"
               viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round"
                  d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <!-- Body: preview + file input -->
      <div class="flex flex-col md:flex-row items-center md:items-start gap-4 mb-6">
        <!-- Image preview -->
        <img
          :src="previewUrl || profile.avatar || defaultAvatar"
          alt="Profile preview"
          class="w-24 h-24 rounded-lg object-cover border-2 border-gray-600"
        />

        <!-- File chooser -->
        <div class="flex-1 space-y-2">
          <label class="block text-sm font-medium text-gray-300 mb-1">
            Выберите файл
          </label>
          <div class="flex items-center bg-[#334155] rounded-md overflow-hidden">
            <input
              type="file"
              accept=".svg,.png,.jpg,.jpeg,.gif"
              @change="onFileChange"
              class="flex-1 px-3 py-2 bg-transparent text-gray-200 focus:outline-none"
            />
            <span class="px-3 py-2 bg-gray-600 text-gray-300 text-sm">
              {{ fileName }}
            </span>
          </div>
          <p class="text-xs text-gray-500">
            SVG, PNG, JPG or GIF (MAX. 800×400px).
          </p>
        </div>
      </div>

      <!-- Footer: action buttons -->
      <div class="flex items-center justify-between">
        <div class="flex space-x-2">
          <button
            @click="upload"
            class="flex-1 bg-[#334155] hover:bg-gray-600 text-gray-200 px-4 py-2 rounded-md"
          >
            Upload new picture
          </button>
          <button
            @click="deletePicture"
            class="flex-1 bg-transparent border border-gray-500 hover:bg-gray-700 text-gray-200 px-4 py-2 rounded-md"
          >
            Delete
          </button>
        </div>
        <button
          @click="save"
          class="ml-4 bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-md"
        >
          Save
        </button>
      </div>

      <!-- Success / Error messages -->
      <p v-if="success" class="mt-4 text-green-400">{{ success }}</p>
      <p v-if="error" class="mt-4 text-red-400">{{ error }}</p>
    </div>
  </div>
</template>

<script>
import defaultAvatar from '@/assets/defaultAvatar.png';

export default {
  name: 'UpdateProfilePictureModal',
  props: {
    // .sync modifier bilan bog'lanadi parentda
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
      fileName: 'Файл не выбран',
      previewUrl: '',
      error: '',
      success: '',
    };
  },
  methods: {
    close() {
      this.$emit('update:editProfilePicture', false);
      this.reset();
    },
    onFileChange(event) {
      const file = event.target.files[0];
      if (!file) return;
      this.file = file;
      this.fileName = file.name;
      // Preview
      this.previewUrl = URL.createObjectURL(file);
    },
    upload() {
      if (!this.file) {
        this.error = 'Пожалуйста, выберите файл для загрузки.';
        return;
      }
      this.error = '';
      // TODO: real upload logic here (e.g. axios.post)
      this.success = 'Файл подготовлен к загрузке.';
    },
    deletePicture() {
      // TODO: delete logic (e.g. API call)
      this.previewUrl = '';
      this.$emit('deleted');
      this.success = 'Фото удалено.';
    },
    save() {
      // TODO: finalize save (e.g. emit event with this.file, then parent saves)
      if (!this.file && !this.previewUrl) {
        this.error = 'Нет нового изображения для сохранения.';
        return;
      }
      this.$emit('saved', this.file);
      this.success = 'Изменения сохранены.';
      setTimeout(() => this.close(), 1000);
    },
    reset() {
      this.file = null;
      this.fileName = 'Файл не выбран';
      this.previewUrl = '';
      this.error = '';
      this.success = '';
    },
  },
};
</script>

<style scoped>
/* Qo‘shimcha maxsus CSS kerak bo‘lsa shu yerga */
</style>
