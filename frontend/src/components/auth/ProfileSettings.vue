<template>
  <div
    class="bg-[#1e293b] rounded-lg shadow-md p-6 space-y-6 border border-gray-700 relative"
  >
    <div class="w-full h-full flex flex-col">
      <!-- Header -->
      <header class="bg-gray-700 rounded-lg py-4 px-6">
        <h1 class="text-2xl text-white font-bold">Profile Settings</h1>
      </header>

      <!-- Form -->
      <main class="p-6">
        <form @submit.prevent="saveProfile" class="space-y-8 w-full">
          <div
            class="dark:bg-neutral-900/90 dark:border-neutral-700 dark:text-gray-200 rounded-lg p-4"
          >
            <!-- Basic Information -->
            <section class="space-y-4">
              <h2 class="text-xl text-white font-semibold">
                Basic Information
              </h2>
              <div
                class="flex flex-col md:flex-row md:space-x-6 space-y-4 md:space-y-0"
              >
                <div class="flex-1">
                  <label class="block text-gray-200 text-sm font-medium mb-1"
                    >First Name</label
                  >
                  <input
                    v-model="profile.first_name"
                    type="text"
                    class="w-full p-3 rounded-lg bg-gray-800 border border-gray-700 focus:outline-none focus:border-indigo-500 text-gray-300"
                  />
                </div>
                <div class="flex-1">
                  <label class="block text-gray-200 text-sm font-medium mb-1"
                    >Last Name</label
                  >
                  <input
                    v-model="profile.last_name"
                    type="text"
                    class="w-full p-3 rounded-lg bg-gray-800 border border-gray-700 focus:outline-none focus:border-indigo-500 text-gray-300"
                  />
                </div>
              </div>
              <!-- Biography -->
              <div>
                <label class="block text-gray-200 text-sm font-medium mb-1"
                  >Biography</label
                >
                <textarea
                  v-model="profile.bio"
                  rows="3"
                  class="w-full p-3 rounded-lg bg-gray-800 border border-gray-700 focus:outline-none focus:border-indigo-500 text-gray-300"
                  placeholder="Tell us about yourself..."
                ></textarea>
              </div>
            </section>
          </div>

          <div
            class="dark:bg-neutral-900/90 dark:border-neutral-700 dark:text-gray-200 rounded-lg p-4"
          >
            <!-- Contact Information -->
            <section class="space-y-4">
              <h2 class="text-white text-xl font-semibold">
                Contact Information
              </h2>
              <div
                class="flex flex-col md:flex-row md:space-x-6 space-y-4 md:space-y-0"
              >
                <div class="flex-1">
                  <label class="block text-gray-200 text-sm font-medium mb-1"
                    >Email</label
                  >
                  <input
                    v-model="profile.email"
                    type="email"
                    class="w-full p-3 rounded-lg bg-gray-800 border border-gray-700 focus:outline-none focus:border-indigo-500 text-gray-300"
                  />
                </div>
                <div class="flex-1">
                  <label class="block text-gray-200 text-sm font-medium mb-1"
                    >Phone</label
                  >
                  <input
                    v-model="profile.phone"
                    type="text"
                    class="w-full p-3 rounded-lg bg-gray-800 border border-gray-700 focus:outline-none focus:border-indigo-500 text-gray-300"
                  />
                </div>
                <div class="flex-1">
                  <label class="block text-gray-200 text-sm font-medium mb-1"
                    >Telegram ID</label
                  >
                  <input
                    v-model="profile.telegram_id"
                    type="text"
                    class="w-full p-3 rounded-lg bg-gray-800 border border-gray-700 focus:outline-none focus:border-indigo-500 cursor-not-allowed text-gray-300"
                  />
                </div>
                <div class="flex-1">
                  <label class="block text-gray-200 text-sm font-medium mb-1"
                    >Location</label
                  >
                  <input
                    v-model="profile.location"
                    type="text"
                    class="w-full p-3 rounded-lg bg-gray-800 border border-gray-700 focus:outline-none focus:border-indigo-500 text-gray-300"
                  />
                </div>
                <div class="flex-1">
                  <label class="block text-gray-200 text-sm font-medium mb-1"
                    >Location</label
                  >
                  <input
                    v-model="profile.location"
                    type="text"
                    class="w-full p-3 rounded-lg bg-gray-800 border border-gray-700 focus:outline-none focus:border-indigo-500 text-gray-300"
                  />
                </div>
              </div>
            </section>
          </div>

          <div
            class="dark:bg-neutral-900/90 dark:border-neutral-700 dark:text-gray-200 rounded-lg p-4"
          >
            <!-- Additional Details -->
            <section class="space-y-4">
              <h2 class="text-xl text-white font-semibold">
                Additional Details
              </h2>
              <div
                class="flex flex-col md:flex-row md:space-x-6 space-y-4 md:space-y-0"
              >
                <div class="flex-1">
                  <label class="block text-gray-100 text-sm font-medium mb-1"
                    >Date of Birth</label
                  >
                  <flat-pickr
                    v-model="profile.date_of_birth"
                    id="date_of_birth"
                    :config="datePickerConfig"
                    placeholder="Выберите дату"
                    class="w-full px-4 py-3 rounded-lg bg-gray-800 border border-gray-700 text-gray-300 focus:outline-none focus:border-indigo-500"
                  />
                </div>

                <div class="flex-1">
                  <label for="role" class="block text-white font-medium"
                    >Gender</label
                  >
                  <Listbox v-model="profile.gender">
                    <div class="relative">
                      <ListboxButton
                        class="w-full p-3 rounded-lg bg-gray-800 border border-gray-700 focus:outline-none focus:border-indigo-500 text-gray-300 flex justify-between items-center"
                      >
                        <span>{{
                          genderLabels[profile.gender] || "Выберите ген"
                        }}</span>
                        <ChevronUpDownIcon class="w-5 h-5 text-white/70" />
                      </ListboxButton>

                      <Transition
                        enter="transition ease-out duration-100"
                        enter-from="opacity-0 scale-95"
                        enter-to="opacity-100 scale-100"
                        leave="transition ease-in duration-75"
                        leave-from="opacity-100 scale-100"
                        leave-to="opacity-0 scale-95"
                      >
                        <ListboxOptions
                          class="absolute mt-2 w-full bg-black/60 backdrop-blur-lg rounded-lg shadow-lg z-50 ring-1 ring-black/20 focus:outline-none"
                        >
                          <ListboxOption
                            v-for="g in genders"
                            :key="g"
                            :value="g"
                            class="cursor-pointer text-white select-none relative py-2 pl-10 pr-4 hover:bg-white/20"
                            v-slot="{ selected }"
                          >
                            <span
                              :class="[
                                selected
                                  ? 'font-semibold text-white'
                                  : 'text-white',
                              ]"
                            >
                              {{ genderLabels[g] }}
                            </span>
                            <span
                              v-if="selected"
                              class="absolute inset-y-0 left-0 flex items-center pl-3 text-white"
                            >
                              <CheckIcon class="w-5 h-5" />
                            </span>
                          </ListboxOption>
                        </ListboxOptions>
                      </Transition>
                    </div>
                  </Listbox>
                </div>

                <div class="flex-1">
                  <label class="block text-gray-100 text-sm font-medium mb-1"
                    >Language</label
                  >

                  <span
                    class="mt-2 inline-block px-3 py-1 rounded-lg text-sm font-medium text-white"
                    :class="{
                      'bg-blue-600': profile.language === 'ru',
                      'bg-green-600': profile.language === 'uz',
                      'bg-indigo-600': profile.language === 'en',
                      'bg-gray-600': !['ru', 'uz', 'en'].includes(
                        profile.language
                      ),
                    }"
                  >
                    {{
                      profile.language === "ru"
                        ? "Русский"
                        : profile.language === "uz"
                        ? "O‘zbekcha"
                        : profile.language === "en"
                        ? "English"
                        : "Til tanlanmagan"
                    }}
                  </span>
                </div>
              </div>
            </section>
          </div>

          <div
            class="dark:bg-neutral-900/90 dark:border-neutral-700 dark:text-gray-200 rounded-lg p-4"
          >
            <!-- Social Links -->
            <section class="space-y-4">
              <h2 class="text-xl text-white font-semibold">Social Links</h2>

              <!-- Add Button -->
              <button
                type="button"
                class="flex items-center space-x-2 text-indigo-400 hover:text-indigo-300"
                @click="adding = !adding"
              >
                <span>Add social link</span>
              </button>

              <!-- Platform Selector -->
              <div
                v-if="adding"
                class="w-full max-w-[500px] flex items-center space-x-2"
              >
                <Listbox v-model="newPlatform">
                  <div class="relative w-full max-w-[300px]">
                    <ListboxButton
                      class="w-full p-3 rounded-lg bg-gray-800 text-white border border-gray-700 flex justify-between items-center"
                    >
                      <span>
                        {{
                          availablePlatforms.find((p) => p.key === newPlatform)
                            ?.name || "Choose platform"
                        }}
                      </span>
                      <ChevronUpDownIcon class="w-5 h-5 text-white/70" />
                    </ListboxButton>

                    <Transition
                      enter="transition ease-out duration-100"
                      enter-from="opacity-0 scale-95"
                      enter-to="opacity-100 scale-100"
                      leave="transition ease-in duration-75"
                      leave-from="opacity-100 scale-100"
                      leave-to="opacity-0 scale-95"
                    >
                      <ListboxOptions
                        class="absolute mt-2 w-full bg-black/60 backdrop-blur-lg rounded-lg shadow-lg z-50 ring-1 ring-black/20 focus:outline-none"
                      >
                        <ListboxOption
                          v-for="plat in availablePlatforms"
                          :key="plat.key"
                          :value="plat.key"
                          class="cursor-pointer select-none relative py-2 pl-4 pr-4 flex items-center space-x-3 hover:bg-white/20 disabled:opacity-50 disabled:cursor-not-allowed"
                          v-slot="{ selected, disabled }"
                        >
                          <!-- Icon -->
                          <img
                            :src="`/icons/${getPlatformData(plat.key).key}.png`"
                            :alt="getPlatformData(plat.key).key"
                            class="w-5 h-5"
                          />

                          <!-- Platform name -->
                          <span
                            :class="[
                              selected
                                ? 'font-semibold text-white'
                                : 'text-white',
                            ]"
                          >
                            {{ plat.name }}
                          </span>

                          <!-- Check icon (optional) -->
                          <span
                            v-if="selected"
                            class="absolute inset-y-0 left-0 flex items-center pl-3 text-white"
                          >
                            <!-- CheckIcon qo‘shmoqchi bo‘lsangiz shu yerga qo‘ying -->
                          </span>
                        </ListboxOption>
                      </ListboxOptions>
                    </Transition>
                  </div>

                  <div class="flex justify-end">
                    <button
                      type="button"
                      @click="addPlatform"
                      :disabled="!newPlatform"
                      class="px-4 py-2 bg-indigo-600 rounded-lg text-white disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      Add
                    </button>
                  </div>
                </Listbox>
              </div>

              <div class="space-y-4">
                <div
                  v-for="(item, idx) in socialList"
                  :key="item.key"
                  class="flex items-center space-x-4 bg-gray-800 p-3 rounded-lg"
                >
                  <!-- Icon -->
                  <img
                    :src="`/icons/${getPlatformData(item.key).key}.png`"
                    :alt="getPlatformData(item.key).key"
                    class="w-6 h-6"
                  />

                  <!-- URL Prefix -->
                  <span class="text-gray-400">
                    {{ getPlatformData(item.key).prefix }}
                  </span>

                  <!-- Handle Input -->
                  <input
                    v-model="item.handle"
                    type="text"
                    placeholder="username"
                    class="flex-1 p-2 bg-gray-800 border border-gray-600 rounded focus:outline-none"
                  />

                  <!-- Remove Button -->
                  <button
                    type="button"
                    class="text-red-500 hover:text-red-400"
                    @click="removePlatform(idx)"
                  >
                    ✕
                  </button>
                </div>
              </div>
            </section>
          </div>

          <!-- Save Button -->
          <div class="flex justify-end space-x-4">
            <button
              type="submit"
              :disabled="loading"
              class="bg-indigo-600 hover:bg-indigo-700 text-white font-medium px-8 py-3 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="loading">Saving...</span>
              <span v-else>Save Profile</span>
            </button>
          </div>
          <div
            v-if="showConfirmModal"
            id="popup-modal"
            tabindex="-1"
            class="fixed inset-0 z-50 flex items-center justify-center w-full md:inset-0 h-[calc(100%-1rem)] max-h-full"
          >
            <div class="relative p-4 w-full max-w-md max-h-full">
              <div
                class="relative bg-white rounded-lg shadow-sm dark:bg-gray-700"
              >
                <!-- <button type="button" @click="cancelDelete" class="absolute top-3 end-2.5 text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center dark:hover:bg-gray-600 dark:hover:text-white" data-modal-hide="popup-modal">
                           <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14">
                              <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"/>
                          </svg>
                          <span class="sr-only">Отменить</span> 
                      </button> -->
                <div class="p-4 md:p-5 text-center">
                  <svg
                    v-if="isSuccess"
                    class="mx-auto mb-4 text-green-500 w-12 h-12 dark:text-green-400"
                    aria-hidden="true"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 20 20"
                  >
                    <!-- Tashqi yumaloq aylana -->
                    <circle
                      cx="10"
                      cy="10"
                      r="9"
                      stroke="currentColor"
                      stroke-width="2"
                    />

                    <!-- Check belgisi -->
                    <path
                      d="M6 10.5l2.5 2.5L14 7"
                      stroke="currentColor"
                      stroke-width="2"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    />
                  </svg>
                  <svg
                    v-else
                    class="mx-auto mb-4 text-red-500 w-12 h-12 dark:text-gray-200"
                    aria-hidden="true"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 20 20"
                  >
                    <path
                      stroke="currentColor"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M10 11V6m0 8h.01M19 10a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
                    />
                  </svg>
                  <h3
                    class="mb-5 text-lg font-normal text-gray-500 dark:text-gray-400"
                  >
                    {{ confirmMessage }}
                  </h3>
                  <button
                    type="button"
                    @click="closeModal"
                    data-modal-hide="popup-modal"
                    class="text-white bg-red-600 hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 dark:focus:ring-red-800 font-medium rounded-lg text-sm inline-flex items-center px-5 py-2.5 text-center"
                  >
                    ОК ({{ countdown }})
                  </button>
                </div>
              </div>
            </div>
          </div>
        </form>
      </main>
    </div>
  </div>
</template>

<script>
import api from "@/utils/axios";
import { mapState } from "vuex";
import { Russian } from "flatpickr/dist/l10n/ru.js";
import { ChevronUpDownIcon, CheckIcon } from "@heroicons/vue/24/solid";
import { Transition } from "vue";

export default {
  name: "ProfileSettings",
  components: {
    ChevronUpDownIcon,
    CheckIcon,
    Transition,
  },
  data() {
    return {
      profile: {
        first_name: "",
        last_name: "",
        bio: "",
        email: "",
        phone: "",
        telegram_id: "",
        location: "",
        address: "",
        date_of_birth: "",
        gender: "",
        language: "",
        social_links: {
          facebook: "",
          instagram: "",
          twitter: "",
        },
      },
      showConfirmModal: false,
      confirmMessage: "",
      loading: false,
      isSuccess: false,
      countdown: 10,
      countdownTimer: null,
      datePickerConfig: {
        locale: Russian,
        dateFormat: "Y-m-d",
        altInput: true,
        altFormat: "j F, Y",
      },
      genders: ["male", "female", "other"],
      genderLabels: {
        male: "Мужчина",
        female: "Женский",
        other: "Другой",
      },

      socialList: [],
      adding: false,
      newPlatform: "",
      availablePlatforms: [
        { key: "telegram", name: "Telegram", prefix: "https://t.me/" },
        {
          key: "instagram",
          name: "Instagram",
          prefix: "https://instagram.com/",
        },
        { key: "facebook", name: "Facebook", prefix: "https://facebook.com/" },
        { key: "twitter", name: "Twitter", prefix: "https://twitter.com/" },
        { key: "linkedin", name: "LinkedIn", prefix: "https://linkedin.com/" },
        { key: "github", name: "GitHub", prefix: "https://github.com/" },
      ],
    };
  },
  computed: {
    ...mapState("auth", ["token"]),
  },
  async created() {
    try {
      const res = await api.get("/auth/users/me/", {
        headers: { Authorization: `Bearer ${this.token}` },
      });
      this.profile = { ...this.profile, ...res.data };
      if (!this.profile.social_links) {
        this.profile.social_links = {};
      }
      this.socialList = Object.entries(this.profile.social_links).map(
        ([key, url]) => {
          const handle = url.replace(/^@/, "");
          return { key, handle };
        }
      );
    } catch (e) {
      console.error("Failed to load profile:", e);
    }
  },
  watch: {
    showConfirmModal(newVal) {
      if (newVal) {
        this.countdown = 10;
        this.startCountdown();
      } else {
        clearInterval(this.countdownTimer);
      }
    },
  },
  methods: {
    getPlatformData(key) {
      const baseKey = key.split("_")[0];
      return this.availablePlatforms.find((p) => p.key === baseKey);
    },
    platformConfig(key) {
      return this.availablePlatforms.find((p) => p.key === key) || {};
    },
    startCountdown() {
      this.countdownTimer = setInterval(() => {
        if (this.countdown > 0) {
          this.countdown--;
        } else {
          this.closeModal();
        }
      }, 1000);
    },
    closeModal() {
      this.showConfirmModal = false;
      this.isSuccess = false;
      this.confirmMessage = "";
      clearInterval(this.countdownTimer);
    },
    addPlatform() {
      if (!this.newPlatform) return;

      const count = this.socialList.filter((item) =>
        item.key.startsWith(this.newPlatform)
      ).length;

      const uniqueKey =
        count === 0 ? this.newPlatform : `${this.newPlatform}_${count + 1}`;

      this.socialList.push({ key: uniqueKey, handle: "" });
      this.newPlatform = "";
      this.adding = false;
    },
    removePlatform(idx) {
      this.socialList.splice(idx, 1);
    },

    async saveProfile() {
      this.loading = true;
      const links = {};
      this.socialList.forEach((item) => {
        links[item.key] = "@" + item.handle;
      });

      try {
        await api.patch(
          "/auth/users/me/",
          {
            first_name: this.profile.first_name,
            last_name: this.profile.last_name,
            email: this.profile.email,
            bio: this.profile.bio,
            phone: this.profile.phone,
            telegram_id: this.profile.telegram_id,
            location: this.profile.location,
            address: this.profile.address,
            gender: this.profile.gender,
            date_of_birth: this.profile.date_of_birth,
            social_links: links,
            language: this.profile.language,
          },
          {
            headers: { Authorization: `Bearer ${this.token}` },
          }
        );
        this.isSuccess = true;
        this.confirmMessage = "Профиль успешно сохранен.";
      } catch (e) {
        console.error("Save error:", e);
        this.isSuccess = false;
        this.confirmMessage = "Произошла ошибка при сохранении профиля.";
      } finally {
        this.loading = false;
        this.showConfirmModal = true;
      }
    },
  },
};
</script>

<style scoped></style>
