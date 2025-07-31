<template>
  <div
    v-if="visible"
    class="fixed inset-0 bg-black bg-opacity-60 backdrop-blur-sm flex items-center justify-center px-4 pt-10 z-50"
  >
    <div
      class="bg-gradient-to-br from-[#692a88] to-[#3b1555] p-6 rounded-2xl shadow-xl w-fit"
    >
      <div
        class="bg-[#1e1f22] w-[900px] rounded-xl shadow-2xl max-h-[90vh] overflow-y-auto flex flex-col relative"
      >
        <div class="w-full p-8 space-y-6">
          <!-- Header -->
          <div class="flex items-center justify-between gap-4">
            <h2 class="text-3xl font-bold text-gray-200">
              Создать новую задачу
            </h2>
            <div class="flex gap-2 items-center">
              <button @click="close" class="text-gray-400 hover:text-gray-200">
                <svg
                  class="w-6 h-6"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            </div>
          </div>

          <!-- Title -->
          <div>
            <label for="title" class="block mb-1 font-medium text-gray-200"
              >Название задачи</label
            >
            <input
              id="title"
              v-model="newTask.title"
              type="text"
              placeholder="Введите название"
              class="w-full p-3 bg-[#2a2c2e] border border-gray-600 text-gray-200 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-500"
              required
            />
          </div>

          <!-- Participants + Labels -->
          <div class="flex flex-wrap gap-4 items-start">
            <!-- Участники -->
            <div class="relative">
              <div class="flex items-center gap-2 mb-1">
                <span class="text-sm text-gray-400">Участники</span>

                <div class="flex items-center gap-1">
                  <div
                    v-for="id in newTask.marked_to_id"
                    :key="id"
                    class="w-8 h-8 rounded-full bg-green-600 text-white flex items-center justify-center text-xs"
                    :title="getUserName(id)"
                  >
                    {{ initials(getUserName(id)) }}
                  </div>
                </div>

                <button
                  @click.stop="
                    showParticipants = !showParticipants;
                    showLabels = false;
                  "
                  ref="participantButton"
                  class="w-8 h-8 rounded-full bg-white/10 border border-gray-600 flex items-center justify-center text-gray-200 hover:bg-white/20"
                >
                  <svg
                    class="w-5 h-5"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M12 4v16m8-8H4"
                    />
                  </svg>
                </button>
              </div>

              <!-- Participants Dropdown -->
              <div
                v-if="showParticipants"
                ref="participantDropdown"
                @click.stop
                class="absolute left-0 top-full mt-2 bg-[#1e1f22] border border-gray-600 rounded shadow-lg w-64 z-50"
              >
                <div class="p-2">
                  <input
                    v-model="participantSearch"
                    type="text"
                    placeholder="Поиск участников"
                    class="w-full p-2 bg-[#2a2c2e] border border-gray-600 rounded text-sm text-gray-200"
                  />
                </div>
                <div class="max-h-48 overflow-y-auto">
                  <label
                    v-for="u in filteredUsers"
                    :key="u.id"
                    class="flex items-center px-3 py-2 hover:bg-gray-700 cursor-pointer"
                    @click="toggleParticipant(u.id)"
                  >
                    <div
                      class="w-6 h-6 mr-3 rounded-full bg-green-600 text-white flex items-center justify-center text-xs"
                    >
                      {{ initials(u.username) }}
                    </div>
                    <span class="flex-1 text-sm text-gray-200">{{
                      u.username
                    }}</span>
                    <span
                      v-if="newTask.marked_to_id.includes(u.id)"
                      class="text-gray-400"
                    >
                      <svg
                        class="w-4 h-4"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          stroke-width="2"
                          d="M5 13l4 4L19 7"
                        />
                      </svg>
                    </span>
                  </label>
                </div>
              </div>
            </div>

            <!-- Метки -->
            <div class="relative">
              <div class="flex items-center gap-3">
                <button
                  ref="labelButton"
                  @click.stop="
                    showLabels = !showLabels;
                    showParticipants = false;
                  "
                  class="px-3 py-1 flex items-center gap-2 bg-white/10 border border-gray-600 rounded-md text-gray-200 hover:bg-white/20"
                >
                  <svg
                    class="w-5 h-5"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M3 7h18M3 12h18M3 17h18"
                    />
                  </svg>
                  Метка
                </button>

                <!-- Labels Dropdown -->
                <div
                  v-if="showLabels"
                  ref="labelDropdown"
                  @click.stop
                  class="absolute right-10 mt-[260px] w-48 bg-[#1e1f22] border border-gray-600 rounded shadow-lg z-50"
                >
                  <div
                    class="flex justify-between items-center px-4 py-2 border-b border-gray-700"
                  >
                    <span class="text-gray-200 font-medium">Метки</span>
                    <button
                      @click="showLabels = false"
                      class="text-gray-400 hover:text-gray-200"
                    >
                      <svg
                        class="w-5 h-5"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          stroke-width="2"
                          d="M6 18L18 6M6 6l12 12"
                        />
                      </svg>
                    </button>
                  </div>
                  <div class="p-2"></div>
                  <div class="max-h-40 overflow-y-auto">
                    <label
                      v-for="label in filteredLabels"
                      :key="label.id"
                      class="flex items-center px-4 py-2 hover:bg-gray-700 cursor-pointer"
                      @click="selectLabel(label)"
                    >
                      <div
                        :style="{ backgroundColor: label.color }"
                        class="w-4 h-4 rounded mr-2 border border-gray-300"
                      ></div>
                      <div
                        :style="{ backgroundColor: label.color }"
                        class="flex-1 h-4 rounded"
                      ></div>
                    </label>
                  </div>
                </div>
                <div
                  v-if="selectedLabel"
                  class="w-8 h-8 rounded-full border border-gray-900"
                  :style="{ backgroundColor: selectedLabel.color }"
                ></div>
              </div>
            </div>
          </div>

          <!-- Description -->
          <div>
            <label
              for="description"
              class="block mb-1 font-medium text-gray-200"
              >Описание</label
            >
            <textarea
              id="description"
              v-model="newTask.description"
              rows="3"
              placeholder="Опишите задачу"
              class="w-full p-3 bg-[#2a2c2e] border border-gray-600 text-gray-200 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-500 resize-none"
            ></textarea>
          </div>

          <!-- Assign & Due Date -->
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            <div class="w-[500px] md:col-span-2">
              <!-- md:col-span-2 -->
              <label
                class="block mb-2 font-semibold text-base text-gray-300"
                for="users"
                >Назначить сотрудника</label
              >
              <div class="relative">
                <Listbox v-model="newTask.assigned_to_id">
                  <div class="relative">
                    <ListboxButton
                      class="w-full px-4 py-3 rounded-lg bg-neutral-900 border border-neutral-600 text-white flex justify-between items-center focus:outline-none focus:ring-2 focus:ring-purple-500"
                    >
                      <span>
                        {{
                          users.find((u) => u.id === newTask.assigned_to_id)
                            ?.username || "Выберите сотрудника"
                        }}
                      </span>
                      <ChevronUpDownIcon class="w-5 h-5 text-gray-400" />
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
                        class="absolute bottom-full mb-2 w-full bg-neutral-800 rounded-lg shadow-lg z-50 ring-1 ring-black/20 focus:outline-none"
                      >
                        <ListboxOption
                          v-for="u in users"
                          :key="u.id"
                          :value="u.id"
                          class="cursor-pointer select-none relative py-2 pl-10 pr-4 hover:bg-neutral-700 rounded-lg"
                          v-slot="{ selected }"
                        >
                          <span
                            :class="[
                              selected
                                ? 'font-semibold text-white'
                                : 'text-gray-300',
                            ]"
                          >
                            {{ u.username }}
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
            </div>
            <div class="w-[250px]">
              <label
                class="block mb-2 font-semibold text-base text-gray-300"
                for="due_date"
                >Срок окончания</label
              >
              <flat-pickr
                v-model="newTask.due_date"
                id="due_date"
                :config="datePickerConfig"
                placeholder="Выберите дату"
                class="w-full px-4 py-3 rounded-lg border border-neutral-600 bg-neutral-900 text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
              />
            </div>
          </div>

          <div class="mt-4">
            <label for="file-upload" class="block mb-1 font-medium text-gray-200">
              Прикрепить файлы
            </label>
            <input
              id="file-upload"
              type="file"
              multiple
              @change="onFileChange"
              class="w-full text-gray-200"
              accept=".pdf,.docx,.xlsx,.jpg,.jpeg,.png"
            />
            <div class="mt-2 space-y-1 text-sm text-gray-300">
              <div v-for="(f, idx) in newTask.uploaded_files" :key="idx">
                {{ f.name }}
              </div>
            </div>
          </div>

          <!-- Actions -->
          <div class="flex justify-end space-x-4 pt-4">
            <button
              @click="close"
              type="button"
              class="px-6 py-2 text-sm font-medium text-gray-300 hover:text-gray-200"
            >
              Отменить
            </button>
            <button
              type="button"
              @click="handleCreateTask"
              class="px-6 py-2 bg-blue-600 text-black font-semibold rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              Создать
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { CheckIcon, ChevronUpDownIcon } from "@heroicons/vue/24/solid";
import { Transition } from "vue";
import { Russian } from "flatpickr/dist/l10n/ru.js";

export default {
  name: "TaskFormModal",
  components: {
    ChevronUpDownIcon,
    CheckIcon,
  },
  props: {
    visible: Boolean,
    users: { type: Array, default: () => [] },
    projectId: Number,
    moduleId: { type: Number, default: null },
    labels: {
      type: Array,
      default: () => [
        { id: 1, color: "#2ecc71" },
        { id: 2, color: "#f1c40f" },
        { id: 3, color: "#e67e22" },
        { id: 4, color: "#e74c3c" },
        { id: 5, color: "#9b59b6" },
        { id: 6, color: "#3498db" },
      ],
    },
  },
  data() {
    return {
      newTask: {
        showSidebar: false,
        title: "",
        description: "",
        marked_to_id: [],
        assigned_to_id: null,
        due_date: "",
        status_id: 1,
        color: "#FFFFFF",
        uploaded_files: [],
        datePickerConfig: {
          locale: Russian,
          dateFormat: "d.m.Y",
          altInput: true,
          altFormat: "j F, Y",
          minDate: "today",
        },
      },
      showParticipants: false,
      participantSearch: "",
      showLabels: false,
      search: "",
      selectedLabel: null,
    };
  },
  computed: {
    selectedLabel() {
      return (
        this.labels.find((label) => label.id === this.newTask.label_id) || null
      );
    },
    filteredUsers() {
      const s = this.participantSearch.toLowerCase();
      return this.users.filter((u) => u.username.toLowerCase().includes(s));
    },
    filteredLabels() {
      const s = this.search.toLowerCase();
      return this.labels.filter((l) => l.color.toLowerCase().includes(s));
    },
  },
  methods: {
    onFileChange(event) {
      // FileList → Array
      this.newTask.uploaded_files = Array.from(event.target.files);
    },    
    selectLabel(label) {
      this.showLabels = false;
      this.newTask.label_id = label.id;
      this.newTask.color = label.color;
      this.$emit("label-selected", label);
    },
    createNewLabel() {
      this.$emit("create-label");
    },
    handleClickOutside(event) {},
    handleClickOutside(e) {
      const participantDropdown = this.$refs.participantDropdown;
      const participantButton = this.$refs.participantButton;
      const labelDropdown = this.$refs.labelDropdown;
      const labelButton = this.$refs.labelButton;

      // Participants dropdown
      if (
        this.showParticipants &&
        participantDropdown &&
        participantButton &&
        !participantDropdown.contains(e.target) &&
        !participantButton.contains(e.target)
      ) {
        this.showParticipants = false;
      }

      // Labels dropdown
      if (
        this.showLabels &&
        labelDropdown &&
        labelButton &&
        !labelDropdown.contains(e.target) &&
        !labelButton.contains(e.target)
      ) {
        this.showLabels = false;
      }
    },
    initials(name) {
      return name
        .split(" ")
        .map((n) => n[0])
        .join("")
        .toUpperCase();
    },
    getUserName(id) {
      const u = this.users.find((x) => x.id === id);
      return u ? u.username : "";
    },
    toggleParticipant(id) {
      const idx = this.newTask.marked_to_id.indexOf(id);
      if (idx === -1) {
        this.newTask.marked_to_id.push(id);
        if (!this.newTask.assigned_to_id) this.newTask.assigned_to_id = id;
      } else {
        this.newTask.marked_to_id.splice(idx, 1);
        if (this.newTask.assigned_to_id === id) {
          this.newTask.assigned_to_id = this.newTask.marked_to_id[0] || null;
        }
      }
    },
    close() {
      this.$emit("close");
      this.resetForm();
    },
    resetForm() {
      this.newTask = {
        title: "",
        description: "",
        marked_to_id: [],
        assigned_to_id: null,
        due_date: "",
        status_id: 1,
        color: "#FFFFFF",
      };
      this.showParticipants = false;
      this.participantSearch = "";
    },
    handleCreateTask() {
      // FormData yaratamiz
      const formData = new FormData();
      formData.append("title", this.newTask.title);
      formData.append("description", this.newTask.description);
      formData.append("assigned_to_id", this.newTask.assigned_to_id);
      formData.append("due_date", this.newTask.due_date || "");
      formData.append("status_id", this.newTask.status_id);
      formData.append("color", this.newTask.color);
      formData.append("project_id", this.projectId);
      if (this.moduleId !== null) formData.append("module_id", this.moduleId);

      // marked_to_id (array)
      this.newTask.marked_to_id.forEach(id => {
        formData.append("marked_to_id", id);
      });

      // Fayllar
      this.newTask.uploaded_files.forEach(file => {
        formData.append("uploaded_files", file);
      });

      // Emit FormData obyekti
      this.$emit("save", formData);

      this.close();
    },
  },
  mounted() {
    document.addEventListener("click", this.handleClickOutside);
  },
  beforeUnmount() {
    document.removeEventListener("click", this.handleClickOutside);
  },
};
</script>

<style scoped></style>
