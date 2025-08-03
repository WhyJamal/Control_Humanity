<template>
  <!-- Overlay -->
  <transition name="fade">
    <div
      v-if="show"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    >
      <!-- Modal box -->
      <div class="bg-white dark:bg-gray-800 rounded-lg w-full max-w-md p-6 relative shadow-lg">
        <!-- Close button -->
        <button
          @click="close"
          class="absolute top-4 right-4 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none"
               viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>

        <!-- Header -->
        <h2 class="text-gray-900 dark:text-white text-lg font-semibold mb-4">
          Update profile picture
        </h2>

        <!-- Top row: avatar + file selection -->
        <div class="flex items-center space-x-4 mb-2">
          <!-- Avatar preview -->
          <div class="w-16 h-16 rounded-lg overflow-hidden bg-gray-100 dark:bg-gray-700 border border-gray-200 dark:border-gray-600">
            <img
              v-if="previewUrl"
              :src="previewUrl"
              alt="Avatar preview"
              class="w-full h-full object-cover"
            />
            <div v-else class="w-full h-full flex items-center justify-center text-gray-400 dark:text-gray-500">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none"
                   viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M5.121 17.804A13.937 13.937 0 0112 15c3.042 0 5.824.996 7.879 2.804M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
              </svg>
            </div>
          </div>
          <!-- File input + filename -->
          <div class="flex-1 grid grid-cols-2 rounded-lg overflow-hidden border border-gray-300 dark:border-gray-600">
            <label
              for="file"
              class="flex items-center justify-center bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 text-sm py-2 cursor-pointer hover:bg-gray-200 dark:hover:bg-gray-600 transition"
            >
              Выберите файл
              <input
                id="file"
                type="file"
                accept="image/*"
                class="hidden"
                @change="onFileChange"
              />
            </label>
            <div
              class="flex items-center justify-center bg-white dark:bg-gray-800 text-gray-500 dark:text-gray-400 text-sm py-2"
            >
              {{ fileName || 'Файл не выбран' }}
            </div>
          </div>
        </div>

        <!-- Note under top row -->
        <p class="text-gray-600 dark:text-gray-400 text-xs mb-4">
          SVG, PNG, JPG or GIF (MAX. 800×400px).
        </p>

        <!-- Upload / Delete buttons -->
        <div class="flex space-x-2 mb-4">
          <button
            @click="uploadNew"
            class="flex-1 flex items-center justify-center bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-200 text-sm font-medium py-2 rounded-md transition"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none"
                 viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4-4m0 0l-4 4m4-4v12"/>
            </svg>
            Upload new picture
          </button>
          <button
            @click="onDelete"
            class="flex-1 flex items-center justify-center bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-200 text-sm font-medium py-2 rounded-md transition"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none"
                 viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5-4h4m-4 0a1 1 0 00-1 1v1h6V4a1 1 0 00-1-1m-4 0h4"/>
            </svg>
            Delete
          </button>
        </div>

        <!-- Save button -->
        <button
          @click="onSave"
          class="w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-2 rounded-md transition"
        >
          Save
        </button>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  show: { type: Boolean, required: true },
  currentPic: { type: String, default: '' }
})
const emit = defineEmits(['update:show', 'save', 'delete', 'upload'])

const file = ref(null)
const fileName = ref('')
const previewUrl = ref(props.currentPic)

// Fayl tanlanganda chaqiriladi
function onFileChange(e) {
  const f = e.target.files[0]
  if (!f) return
  file.value = f
  fileName.value = f.name
  previewUrl.value = URL.createObjectURL(f)
}

// “Upload new picture” tugma
function uploadNew() {
  emit('upload', file.value)
}

// “Delete” tugma
function onDelete() {
  file.value = null
  fileName.value = ''
  previewUrl.value = ''
  emit('delete')
}

// “Save” tugma
function onSave() {
  emit('save', file.value)
  close()
}

// Close modal
function close() {
  emit('update:show', false)
}

// Agar tashqi prop o‘zgarsa, preview yangilansin
watch(() => props.currentPic, url => {
  previewUrl.value = url
})
</script>

<style scoped>
/* Fade transition */
.fade-enter-active, .fade-leave-active {
  transition: opacity .2s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
