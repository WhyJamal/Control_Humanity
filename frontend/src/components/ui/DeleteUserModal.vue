<template>
  <transition name="fade">
    <div
      v-if="show"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50"
    >
      <div
        class="bg-white dark:bg-[#242629] rounded-2xl w-full max-w-md mx-4 shadow-xl overflow-hidden"
      >
        <!-- Header -->
        <div
          class="flex items-center justify-between px-6 py-4 border-b border-gray-200 dark:border-gray-700"
        >
          <h3 class="text-lg font-semibold text-gray-800 dark:text-white">
            Delete user?
          </h3>
          <button @click="cancel" class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none"
              viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round"
                stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Body -->
        <div class="px-6 py-4">
          <p class="text-gray-700 dark:text-gray-300 mb-4">
            Are you sure you want to delete this user from the Flowbite platform?
          </p>

          <!-- Warning Box -->
          <div
            class="bg-yellow-100 dark:bg-[#1e1f22] border border-yellow-300 dark:border-gray-700 rounded-lg p-4 flex items-start space-x-3"
          >
            <svg xmlns="http://www.w3.org/2000/svg"
              class="h-6 w-6 flex-shrink-0 text-yellow-600 dark:text-yellow-400"
              viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd"
                d="M8.257 3.099c.765-1.36 2.681-1.36 3.446 0l5.516 9.82c.75 1.334-.213 2.981-1.723 2.981H4.464c-1.51 0-2.473-1.647-1.723-2.98l5.516-9.821zM11 13a1 1 0 10-2 0 1 1 0 002 0zm-1-2a1 1 0 01-1-1V7a1 1 0 112 0v3a1 1 0 01-1 1z"
                clip-rule="evenodd" />
            </svg>
            <div>
              <h4 class="text-yellow-700 dark:text-yellow-400 font-medium">
                Warning
              </h4>
              <p class="text-sm text-gray-700 dark:text-gray-300">
                By deleting this user {{ postCount }} associated posts will also be permanently deleted.
              </p>
            </div>
          </div>
        </div>

        <!-- Footer -->
        <div
          class="flex justify-end items-center px-6 py-4 bg-gray-100 dark:bg-[#1b1c1f] border-t border-gray-200 dark:border-gray-700"
        >
          <button
            @click="cancel"
            class="px-4 py-2 mr-2 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700"
          >
            No, cancel
          </button>
          <button
            @click="confirm"
            class="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg flex items-center"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2"
              viewBox="0 0 20 20" fill="currentColor">
              <path
                d="M6 2a1 1 0 00-1 1v1H3.5A1.5 1.5 0 002 5.5v1A.5.5 0 002.5 7h15a.5.5 0 00.5-.5v-1A1.5 1.5 0 0016.5 4H15V3a1 1 0 00-1-1H6z" />
              <path fill-rule="evenodd"
                d="M4 9a1 1 0 011 1v7a2 2 0 002 2h6a2 2 0 002-2v-7a1 1 0 112 0v7a4 4 0 01-4 4H7a4 4 0 01-4-4v-7a1 1 0 011-1z"
                clip-rule="evenodd" />
            </svg>
            Yes, confirm delete
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  show: Boolean,
  postCount: {
    type: Number,
    default: 0
  }
})
const emit = defineEmits(['update:show', 'confirm'])

function cancel() {
  emit('update:show', false)
}

function confirm() {
  emit('confirm')
  emit('update:show', false)
}
</script>
