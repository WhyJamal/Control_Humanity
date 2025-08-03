<template>
  <!-- Overlay -->
  <transition name="fade">
    <div
      v-if="show"
      class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50"
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
              for="fileInput"
              class="flex items-center justify-center bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 text-sm py-2 cursor-pointer hover:bg-gray-200 dark:hover:bg-gray-600 transition"
            >
              Выберите файл
            </label>
            <div
              class="flex items-center justify-center bg-white dark:bg-gray-800 text-gray-500 dark:text-gray-400 text-sm py-2"
              >
              {{ fileName || 'Файл не выбран' }}
            </div>
          </div>
          <input
            id="fileInput"
            ref="fileInput"
            type="file"
            accept="image/*"
            class="hidden"
            @change="onFileChange"
          />
        </div>

        <!-- Note under top row -->
        <p class="text-gray-600 dark:text-gray-400 text-xs mb-4">
          SVG, PNG, JPG or GIF (MAX. 800×400px).
        </p>

        <!-- Upload / Delete buttons -->
        <div class="flex space-x-2 mb-4">
          <button
            @click="triggerFileSelect"
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
            @click="clearSelection"
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
          @click="saveProfile"
          :disabled="isUploading"
          class="w-full flex items-center justify-center bg-green-600 hover:bg-green-700 text-white font-semibold py-2 rounded-md transition disabled:opacity-50"
        >
          <svg v-if="isUploading" class="animate-spin h-5 w-5 mr-2 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
          </svg>
          <span>{{ isUploading ? 'Saving...' : 'Save' }}</span>
        </button>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, watch } from 'vue'
import api from '@/utils/axios'
import eventBus from '@/utils/eventBus'

const props = defineProps({
  show: { type: Boolean, required: true },
  currentPic: { type: String, default: '' }
})
const emit = defineEmits(['update:show', 'saved'])

const file = ref(null)
const fileName = ref('')
const previewUrl = ref('')
const isUploading = ref(false)
const fileInput = ref(null)

watch(() => props.currentPic, url => {
  previewUrl.value = url
}, { immediate: true })

function triggerFileSelect() {
  fileInput.value.click()
}

function onFileChange(e) {
  const f = e.target.files[0]
  if (!f) return
  file.value = f
  fileName.value = f.name
  previewUrl.value = URL.createObjectURL(f)
}

function clearSelection() {
  file.value = null
  fileName.value = ''
  previewUrl.value = ''
}

async function saveProfile() {
  isUploading.value = true
  try {
    const form = new FormData()

    if (file.value) {
      form.append('profile_picture', file.value)
    } else {
      form.append('profile_picture', '')  
    }

    const { data } = await api.patch('auth/users/me/', form)

    eventBus.emit('profile-updated', data)

    emit('saved', data)
    emit('update:show', false)
  } catch (err) {
    console.error(err)
  } finally {
    isUploading.value = false
  }
}

function close() {
  emit('update:show', false)
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity .2s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>