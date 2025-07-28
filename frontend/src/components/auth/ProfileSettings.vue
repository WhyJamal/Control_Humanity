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
          <div class="bg-gray-900 rounded-lg p-4">
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

          <div class="bg-gray-900 rounded-lg p-4">
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
              </div>
            </section>
          </div>

          <div class="bg-gray-900 rounded-lg p-4">
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
                    class="w-full px-4 py-3 rounded-lg border border-gray-700 bg-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                  />
                </div>

                <div class="flex-1">
                  <label for="role" class="block text-white font-medium"
                    >Gender</label
                  >
                  <Listbox v-model="profile.gender">
                    <div class="relative">
                      <ListboxButton
                        class="w-full p-3 rounded-lg bg-white/10 text-white border border-white/30 focus:outline-none focus:ring-2 focus:ring-white flex justify-between items-center"
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
                              {{ genderLabels[gender] }}
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
                  <input
                    v-model="profile.language"
                    type="text"
                    class="w-full p-3 rounded-lg bg-gray-800 border border-gray-700 focus:outline-none focus:border-indigo-500 text-gray-300"
                  />
                </div>
              </div>
            </section>
          </div>

          <div class="bg-gray-900 rounded-lg p-4">
            <!-- Social Links -->
            <section class="space-y-4">
              <h2 class="text-xl text-white font-semibold">Social Links</h2>
              <div class="space-y-4">
                <div
                  v-for="(url, key) in profile.social_links"
                  :key="key"
                  class="flex flex-col md:flex-row md:items-center md:space-x-4"
                >
                  <label
                    class="w-full md:w-32 text-sm font-medium capitalize mb-1 md:mb-0"
                    >{{ key }}</label
                  >
                  <input
                    v-model="profile.social_links[key]"
                    type="url"
                    placeholder="https://..."
                    class="flex-1 p-3 rounded-lg bg-gray-800 border border-gray-700 focus:outline-none focus:border-indigo-500"
                  />
                </div>
              </div>
            </section>
          </div>

          <!-- Save Button -->
          <div class="flex justify-end space-x-4">
            <!-- <button
              class="bg-gray-600 hover:bg-gray-700 text-white font-medium px-8 py-3 rounded-lg"
            >
              <span>Back</span>
            </button> -->

            <button
              type="submit"
              :disabled="loading"
              class="bg-indigo-600 hover:bg-indigo-700 text-white font-medium px-8 py-3 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="loading">Saving...</span>
              <span v-else>Save Profile</span>
            </button>
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
        social_links: {},
      },
      loading: false,
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
      if (!this.profile.social_links) this.profile.social_links = {};
    } catch (e) {
      console.error("Failed to load profile:", e);
    }
  },
  methods: {
    async saveProfile() {
      this.loading = true;
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
            social_links: this.profile.social_links,
            language: this.profile.language,
          },
          {
            headers: { Authorization: `Bearer ${this.token}` },
          }
        );
        alert("Profile updated successfully!");
      } catch (e) {
        console.error("Save error:", e);
        alert("Failed to update profile");
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped></style>
