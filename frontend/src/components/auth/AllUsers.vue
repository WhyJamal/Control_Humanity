<template>
  <div
    class="p-6 min-h-screen bg-white text-gray-900 dark:bg-[#1e1f22] dark:text-gray-200"
  >
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-3xl">All Users</h1>
      <button
        @click="goToRegister"
        class="bg-green-600 hover:bg-green-700 text-white font-medium px-4 py-2 rounded-lg dark:bg-indigo-950 dark:hover:bg-indigo-900"
      >
        + Add new user
      </button>
    </div>

    <!-- Filters -->
    <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-4">
      <input
        v-model="filters.search"
        type="text"
        placeholder="Search for users"
        class="col-span-1 md:col-span-2 bg-white text-gray-900 border border-gray-300 dark:bg-[#242629] dark:text-white dark:border-gray-700 rounded-lg px-4 py-2 focus:outline-none"
      />

      <select
        v-model="filters.role"
        class="bg-white text-gray-900 border border-gray-300 dark:bg-[#242629] dark:text-white dark:border-gray-700 rounded-lg px-4 py-2 focus:outline-none"
      >
        <option value="">Role</option>
        <option v-for="r in roles" :key="r" :value="r">{{ r }}</option>
      </select>

      <select
        v-model="filters.status"
        class="bg-white text-gray-900 border border-gray-300 dark:bg-[#242629] dark:text-white dark:border-gray-700 rounded-lg px-4 py-2 focus:outline-none"
      >
        <option value="">Status</option>
        <option v-for="s in statuses" :key="s" :value="s">{{ s }}</option>
      </select>

      <select
        v-model="filters.type"
        class="bg-white text-gray-900 border border-gray-300 dark:bg-[#242629] dark:text-white dark:border-gray-700 rounded-lg px-4 py-2 focus:outline-none"
      >
        <option value="">Type</option>
        <option v-for="t in types" :key="t" :value="t">{{ t }}</option>
      </select>

      <select
        v-model="filters.country"
        class="bg-white text-gray-900 border border-gray-300 dark:bg-[#242629] dark:text-white dark:border-gray-700 rounded-lg px-4 py-2 focus:outline-none"
      >
        <option value="">Country</option>
        <option v-for="c in countries" :key="c" :value="c">{{ c }}</option>
      </select>
    </div>

    <!-- Show radio-group -->
    <div class="flex items-center space-x-6 mb-6">
      <span>Show:</span>
      <label class="inline-flex items-center space-x-1">
        <input
          type="radio"
          v-model="showFilter"
          value="all"
          class="form-radio dark:bg-gray-700"
        />
        <span>All</span>
      </label>
      <label class="inline-flex items-center space-x-1">
        <input
          type="radio"
          v-model="showFilter"
          value="role"
          class="form-radio dark:bg-gray-700"
        />
        <span>User Role</span>
      </label>
      <label class="inline-flex items-center space-x-1">
        <input
          type="radio"
          v-model="showFilter"
          value="type"
          class="form-radio dark:bg-gray-700"
        />
        <span>Account Type</span>
      </label>
      <label class="inline-flex items-center space-x-1">
        <input
          type="radio"
          v-model="showFilter"
          value="status"
          class="form-radio dark:bg-gray-700"
        />
        <span>Status</span>
      </label>
      <label class="inline-flex items-center space-x-1">
        <input
          type="radio"
          v-model="showFilter"
          value="rating"
          class="form-radio dark:bg-gray-700"
        />
        <span>Rating</span>
      </label>
    </div>

    <!-- Table -->
    <div class="overflow-x-auto">
      <table
        class="min-w-full bg-white dark:bg-[#242629] rounded-lg overflow-visible"
      >
        <thead>
          <tr
            class="text-left bg-gray-300 text-gray-400 text-sm uppercase dark:bg-gray-700"
          >
            <th class="px-4 py-3 rounded-tl-lg">
              <input type="checkbox" class="dark:bg-gray-700" />
            </th>
            <th class="px-4 py-3">User</th>
            <th class="px-4 py-3">User Role</th>
            <th class="px-4 py-3">Email</th>
            <th class="px-4 py-3">Account Type</th>
            <th class="px-4 py-3">Rating</th>
            <th class="px-4 py-3">Country</th>
            <th class="px-4 py-3">Status</th>
            <th class="px-4 py-3 rounded-tr-lg">Actions</th>
          </tr>
        </thead>
        <tbody class="space-y-2">
          <tr
            v-for="user in filteredUsers"
            :key="user.email"
            class="bg-white dark:bg-[#1e1f22] rounded-lg overflow-hidden shadow-sm border border-gray-200 dark:border-gray-700 hover:bg-gray-100 dark:hover:bg-[#2a2c31] transition"
          >
            <td class="px-4 py-3 rounded-l-lg">
              <input type="checkbox" class="dark:bg-gray-700" />
            </td>
            <td class="px-4 py-3 flex items-center space-x-3">
              <img
                :src="user.avatar"
                alt=""
                class="w-8 h-8 rounded-full object-cover"
              />
              <span>{{ user.name }}</span>
            </td>
            <td class="px-4 py-3">
              <span
                :class="[
                  'px-2 py-1 rounded-full text-xs font-medium',
                  roleClasses[user.role] || 'bg-gray-600',
                ]"
              >
                {{ user.role }}
              </span>
            </td>
            <td class="px-4 py-3">{{ user.email }}</td>
            <td class="px-4 py-3 font-semibold">{{ user.type }}</td>
            <td class="px-4 py-3 flex items-center space-x-1">
              <svg
                v-if="user.ratingDir === 'up'"
                class="w-4 h-4 text-green-400"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fill-rule="evenodd"
                  d="M3 10a1 1 0 011-1h3V4a1 1 0 112 0v5h3a1 1 0 110 2H9v5a1 1 0 11-2 0v-5H4a1 1 0 01-1-1z"
                  clip-rule="evenodd"
                />
              </svg>
              <svg
                v-else
                class="w-4 h-4 text-red-400"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fill-rule="evenodd"
                  d="M3 10a1 1 0 011 1h3v5a1 1 0 11-2 0v-5H4a1 1 0 01-1-1zm5-6a1 1 0 10-2 0v5H4a1 1 0 100 2h2v5a1 1 0 102 0v-5h2a1 1 0 100-2H8V4z"
                  clip-rule="evenodd"
                />
              </svg>
              <span>{{ user.rating }}</span>
            </td>
            <td class="px-4 py-3">{{ user.country }}</td>
            <td class="px-4 py-3 flex items-center space-x-2">
              <span
                :class="[
                  'inline-block w-2 h-2 rounded-full',
                  user.status === 'Active'
                    ? 'bg-green-500 dark:bg-green-400'
                    : 'bg-red-600 dark:bg-red-500',
                ]"
              />
              <span>{{ user.status }}</span>
            </td>
            <td class="px-4 py-3 relative">
              <button
                @click.stop="toggleDropdown(user.email)"
                class="p-1 rounded hover:bg-gray-200 dark:hover:bg-gray-700 transition"
              >
                <EllipsisHorizontalIcon
                  class="w-5 h-5 text-gray-600 dark:text-gray-300"
                />
              </button>
              <!-- Dropdown menu -->
              <div
                v-if="dropdownOpen === user.email"
                class="absolute top-full right-0 mt-2 w-40 bg-white dark:bg-[#242629] text-gray-900 dark:text-gray-200 rounded-lg shadow-lg z-10"
              >
                <ul class="py-1">
                  <li>
                    <button
                      @click="
                        onEdit(user);
                        toggleDropdown(null);
                      "
                      class="w-full flex hover:bg-gray-300 items-center px-4 py-2 text-gray-400 dark:hover:bg-[#2a2c31]"
                    >
                      <!-- edit icon -->
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="h-5 w-5 mr-2 text-gray-400"
                        viewBox="0 0 20 20"
                        fill="currentColor"
                      >
                        <path
                          d="M17.414 2.586a2 2 0 00-2.828 0L7 10.172V13h2.828l7.586-7.586a2 2 0 000-2.828z"
                        />
                        <path
                          fill-rule="evenodd"
                          d="M2 15.5A1.5 1.5 0 013.5 14H6v1a2 2 0 002 2h6.5a1.5 1.5 0 001.5-1.5V14h-1v1.5a.5.5 0 01-.5.5H8a1 1 0 01-1-1v-1H3.5a.5.5 0 01-.5-.5z"
                          clip-rule="evenodd"
                        />
                      </svg>
                      Edit
                    </button>
                  </li>
                  <li>
                    <button
                      @click="viewProfile(user.id)"
                      class="w-full flex hover:bg-gray-300 items-center px-4 py-2 text-gray-400 dark:hover:bg-[#2a2c31]"
                    >
                      <!-- view icon -->
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="h-5 w-5 mr-2 text-gray-400"
                        viewBox="0 0 20 20"
                        fill="currentColor"
                      >
                        <path
                          d="M10 3a7 7 0 00-7 7 7 7 0 0014 0 7 7 0 00-7-7z"
                        />
                        <path d="M10 9a2 2 0 110 4 2 2 0 010-4z" />
                      </svg>
                      View
                    </button>
                  </li>
                  <li>
                    <button
                      @click="
                        onArchive(user);
                        toggleDropdown(null);
                      "
                      class="w-full flex hover:bg-gray-300 items-center px-4 py-2 text-gray-400 dark:hover:bg-[#2a2c31]"
                    >
                      <!-- archive icon -->
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="h-5 w-5 mr-2 text-gray-400"
                        viewBox="0 0 20 20"
                        fill="currentColor"
                      >
                        <path d="M4 4h12v2H4V4z" />
                        <path
                          fill-rule="evenodd"
                          d="M4 7h12v9a1 1 0 01-1 1H5a1 1 0 01-1-1V7zm3 3a1 1 0 000 2h6a1 1 0 000-2H7z"
                          clip-rule="evenodd"
                        />
                      </svg>
                      Archive
                    </button>
                  </li>
                  <li>
                    <button
                      @click="
                        openDeleteModal(user);
                        toggleDropdown(null);
                      "
                      class="w-full flex hover:bg-gray-300 items-center px-4 py-2 text-red-500 dark:hover:bg-[#2a2c31]"
                    >
                      <!-- delete icon -->
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="h-5 w-5 mr-2"
                        viewBox="0 0 20 20"
                        fill="currentColor"
                      >
                        <path
                          fill-rule="evenodd"
                          d="M6 2a1 1 0 00-1 1v1H3.5A1.5 1.5 0 002 5.5v1A.5.5 0 002.5 7h15a.5.5 0 00.5-.5v-1A1.5 1.5 0 0016.5 4H15V3a1 1 0 00-1-1H6z"
                          clip-rule="evenodd"
                        />
                        <path
                          fill-rule="evenodd"
                          d="M4 9a1 1 0 011 1v7a2 2 0 002 2h6a2 2 0 002-2v-7a1 1 0 112 0v7a4 4 0 01-4 4H7a4 4 0 01-4-4v-7a1 1 0 011-1z"
                          clip-rule="evenodd"
                        />
                      </svg>
                      Delete
                    </button>
                  </li>
                </ul>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  <DeleteUserModal
    v-model:show="showDeleteModal"
    :postCount="selectedUser ? selectedUser.postCount : 0"
    @confirm="confirmDelete"
  />
  <Register
    v-if="showRegisterModal"
    :show="showRegisterModal"
    @close="showRegisterModal = false"
  />
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from "vue";
import api from "@/utils/axios";
import DeleteUserModal from "@/components/ui/DeleteUserModal.vue";
import Register from "@/components/auth/Register.vue";
import { EllipsisHorizontalIcon } from "@heroicons/vue/24/outline";
import { useRouter } from 'vue-router';

const router = useRouter();

const users = ref([]);
const loading = ref(false);
const error = ref(null);

const fetchUsers = async () => {
  loading.value = true;
  try {
    const response = await api.get("/auth/users/");
    users.value = response.data;
  } catch (err) {
    error.value = "Не удалось загрузить пользователей.";
  } finally {
    loading.value = false;
  }
};

onMounted(fetchUsers);

const roles = ["admin", "manager", "employee", "director"];
const statuses = ["Active", "Inactive"];
const countries = computed(() => {
  const unique = new Set(users.value.map((u) => u.location));
  return Array.from(unique).filter(Boolean);
});

const filters = ref({
  search: "",
  role: "",
  status: "",
  type: "",
  country: "",
});

const showFilter = ref("all");

const roleClasses = {
  admin: "bg-red-600 text-white",
  manager: "bg-blue-600 text-white",
  employee: "bg-green-600 text-white",
  director: "bg-purple-600 text-white",
};

const filteredUsers = computed(() => {
  return users.value
    .filter((u) => {
      const { search, role, status, country } = filters.value;
      const fullName = `${u.first_name ?? ""} ${
        u.last_name ?? ""
      }`.toLowerCase();

      return (
        (!search || fullName.includes(search.toLowerCase())) &&
        (!role || u.role === role) &&
        (!status ||
          (status === "Active" && u.is_active) ||
          (status === "Inactive" && !u.is_active)) &&
        (!country || u.location === country)
      );
    })
    .map((u) => {
      const name =
        `${u.first_name ?? ""} ${u.last_name ?? ""}`.trim() || u.username;
      const ratingTotal = (u.completed_tasks ?? 0) + (u.current_tasks ?? 0);
      const rating =
        ratingTotal > 0
          ? +((u.completed_tasks / ratingTotal) * 5).toFixed(1)
          : 0;
      const ratingDir =
        (u.completed_tasks ?? 0) >= (u.current_tasks ?? 0) ? "up" : "down";

      return {
        ...u,
        name,
        avatar: u.profile_picture || "/avatar.png",
        rating,
        ratingDir,
        type: "PRO",
        country: u.location || "Unknown",
        status: u.is_active ? "Active" : "Inactive",
      };
    });
});

// Dropdown
const dropdownOpen = ref(null);
function toggleDropdown(email) {
  dropdownOpen.value = dropdownOpen.value === email ? null : email;
}

// Delete modal
const showDeleteModal = ref(false);
const selectedUser = ref(null);

function openDeleteModal(user) {
  selectedUser.value = user;
  showDeleteModal.value = true;
}

function confirmDelete() {
  if (selectedUser.value) {
    users.value = users.value.filter(
      (u) => u.email !== selectedUser.value.email
    );
    selectedUser.value = null;
  }
}

const showRegisterModal = ref(false);

function goToRegister() {
  showRegisterModal.value = true;
}

function onEdit(user) {
  console.log("Edit", user);
}
const viewProfile = (id) => {
  router.push({ path: `/profileview/${id}` });
};
function onArchive(user) {
  console.log("Archive", user);
}
function handleClickOutside(event) {
  dropdownOpen.value = null;
}

onMounted(() => {
  document.addEventListener("click", handleClickOutside);
});
onBeforeUnmount(() => {
  document.removeEventListener("click", handleClickOutside);
});
</script>
