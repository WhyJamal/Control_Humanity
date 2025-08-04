<template>
  <div
    class="button-[200px] relative h-full overflow-y-auto scrollbar-black sm:rounded-lg"
  >
    <!-- h-[340px] -->
    <!-- Add Task Modals -->
    <AddTaskModal
      :visible="showAddTaskModal"
      :project-id="selectedTaskContext.projectId"
      :module-id="selectedTaskContext.moduleId"
      :users="users"
      :marked_to="marked_to_id"
      @close="closeAddTaskModal"
      @save="handleTaskCreate"
    />
    <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
      <thead
        class="text-xs text-gray-700 uppercase bg-gray-300 dark:bg-gray-700 dark:text-gray-400 sticky top-0 z-20"
      >
        <tr>
          <th class="px-6 py-3"></th>
          <th class="px-6 py-3">{{ $t("project_Module_Tasks") }}</th>
          <th class="px-6 py-3">{{ $t("responsible") }}</th>
          <th class="px-6 py-3">Период</th>
          <th class="px-6 py-3">Статус</th>
          <th class="px-6 py-3">Прикольные файлы</th>
          <th class="px-6 py-3">Выполнения</th>
          <th class="px-6 py-3"></th>
          <!-- <th class="px-6 py-3 flex space-x-2 justify-end"></th> -->
        </tr>
      </thead>
      <tbody>
        <template v-for="proj in projects" :key="proj.id">
          <!-- Project Row -->
          <tr
            class="bg-white border-b dark:bg-gray-800 overflow-y-scroll rounded-lg dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
          >
            <td class="px-6 py-4">
              <button @click="toggleExpand(proj.id)" class="focus:outline-none">
                <svg
                  class="w-5 h-5 text-gray-500 dark:text-gray-400 transform transition-transform duration-200"
                  :class="{ 'rotate-180': expandedProjects.includes(proj.id) }"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M19 9l-7 7-7-7"
                  />
                </svg>
              </button>
            </td>
            <th
              scope="row"
              @click="selectProjectForChart(proj)"
              class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white"
            >
              {{ proj.name }}
            </th>
            <td class="px-6 py-4">{{ proj.manager?.username || "—" }}</td>
            <td class="px-6 py-4">{{ proj.period }}</td>
            <td class="px-6 py-4">
              <span
                :class="[
                  'text-sm font-medium me-2 px-2.5 py-0.5 rounded-sm',
                  getStatusClass(getProjectStatus(proj)),
                ]"
              >
                {{ getProjectStatus(proj)}}
              </span>
            </td>
            <td class="px-6 py-4 relative">
              <!-- Кнопка-иконка -->
              <button
                @click.stop="toggleFiles(proj.id)"
                class="p-1 rounded hover:bg-gray-200 dark:hover:bg-gray-700 transition"
              >
                <FolderIcon class="w-5 h-5 text-purple-300" />
              </button>

              <!-- Выпадающий блок файлов -->
              <div
                v-if="filesOpen.includes(proj.id)"
                class="absolute z-10 mt-2 p-2 bg-gray-50 dark:bg-gray-900 rounded shadow-lg max-h-48 overflow-auto w-48"
                style="top: 100%; left: 0"
              >
                <ul class="space-y-1">
                  <li
                    v-for="file in proj.files"
                    :key="file.id"
                    class="flex items-center space-x-1"
                  >
                    <DocumentIcon class="w-4 h-4 text-purple-300" />
                    <a
                      :href="file.file"
                      target="_blank"
                      class="text-blue-400 hover:underline truncate"
                      style="max-width: 120px"
                    >
                      {{ file.file.split("/").pop() }}
                    </a>
                  </li>
                </ul>
              </div>
            </td>
            <td class="px-6 py-4">{{ getProjectCompletion(proj) }}%</td>
            <td class="relative px-6 py-4 text-right">
              <Cog8ToothIcon
                @click.stop="toggleMenu(`proj-${proj.id}`)"
                class="w-6 h-6 rounded hover:bg-gray-200 text-green-700 hover:text-green-900 dark:text-gray-100 dark:hover:bg-gray-700 transition"
              />
              <ul
                v-if="openMenuId === `proj-${proj.id}`"
                class="absolute right-0 mt-2 w-[180px] bg-gray-100 text-black border border-gray-300 rounded-xl shadow-lg z-10 dark:bg-gray-800 dark:border-gray-700 dark:text-white"
              >
                <li
                  @click="goToProjectDetail(proj.id)"
                  class="flex items-center gap-2 px-4 py-2 rounded-xl hover:bg-gray-300 cursor-pointer text-left dark:hover:bg-gray-900"
                >
                  <EyeIcon class="w-4 h-4 text-black dark:text-indigo-400" />
                  Просмотр
                </li>
                <li
                  @click="startAddModuleInline(proj.id)"
                  class="flex items-center gap-2 px-4 py-2 rounded-xl hover:bg-gray-300 cursor-pointer text-left dark:hover:bg-gray-900"
                >
                  <PlusIcon class="w-4 h-4 text-black dark:text-blue-400" />
                  Добавить модуль
                </li>
                <li
                  @click="openAddTaskModal(proj.id, null)"
                  class="flex items-center gap-2 px-4 py-2 rounded-xl hover:bg-gray-300 cursor-pointer text-left dark:hover:bg-gray-900"
                >
                  <PlusIcon class="w-4 h-4 text-black dark:text-green-400" />
                  Добавить задачу
                </li>
                <li
                  @click="editProject(proj.id)"
                  class="flex items-center gap-2 px-4 py-2 rounded-xl hover:bg-gray-300 cursor-pointer text-left dark:hover:bg-gray-900"
                >
                  <PencilIcon class="w-4 h-4 text-black dark:text-blue-400" />
                  Изменить
                </li>
                <li
                  @click="prepareDelete('project', proj.id)"
                  class="flex items-center gap-2 px-4 py-2 rounded-xl hover:bg-gray-300 cursor-pointer text-left dark:hover:bg-gray-900 text-red-400"
                >
                  <TrashIcon class="w-4 h-4" />
                  Удалить
                </li>
              </ul>
            </td>
          </tr>

          <!-- New row -->
          <tr v-if="addingModuleProjectId === proj.id">
            <td
              class="px-6 py-4 bg-gray-300 font-medium text-gray-900 whitespace-nowrap dark:text-white dark:bg-gray-700"
            ></td>
            <td
              colspan="7"
              class="px-6 py-4 bg-gray-300 font-medium text-gray-900 whitespace-nowrap dark:text-white dark:bg-gray-700"
            >
              <div class="flex items-center space-x-2">
                <input
                  v-model="newModuleName"
                  type="text"
                  placeholder="Название модуля"
                  class="flex border text-white border-b dark:bg-gray-800 rounded px-3 py-1"
                />
                <svg class="flex-1 h-1"></svg>
                <button
                  @click="saveModuleInline(proj.id)"
                  class="px-3 py-1 bg-green-500 hover:bg-green-700 text-white rounded dark:bg-purple-600 dark:hover:bg-purple-700"
                >
                  Сохранить
                </button>
                <button
                  @click="cancelAddModuleInline"
                  class="px-3 py-1 bg-red-400 hover:bg-red-600 text-white rounded dark:bg-red-500"
                >
                  Отмена
                </button>
              </div>
            </td>
          </tr>

          <!-- Modules -->
          <template v-if="expandedProjects.includes(proj.id)">
            <template v-for="mod in proj.modules" :key="mod.id">
              <tr
                class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
              >
                <td class="px-6 py-4"></td>
                <th
                  scope="row"
                  class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white"
                >
                  <button
                    @click="toggleModule(mod.id)"
                    class="flex items-center space-x-2 focus:outline-none text-gray-900 dark:text-white"
                  >
                    <svg
                      class="w-5 h-5 transform transition-transform duration-200"
                      :class="{
                        'rotate-180': expandedModules.includes(mod.id),
                      }"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M19 9l-7 7-7-7"
                      />
                    </svg>
                    <span>{{ mod.name }}</span>
                  </button>
                </th>
                <td class="px-6 py-4"></td>
                <td class="px-6 py-4"></td>
                <td class="px-6 py-4"></td>
                <td class="px-6 py-4"></td>
                <td class="px-6 py-4"></td>
                <td class="relative px-6 py-4 text-right">
                  <button
                    @click.stop="toggleMenu(`mod-${mod.id}`)"
                    class="focus:outline-none text-gray-300 rounded hover:bg-gray-300 dark:hover:bg-gray-700"
                  >
                    <EllipsisHorizontalIcon class="w-6 h-6 text-gray-300" />
                  </button>
                  <ul
                    v-if="openMenuId === `mod-${mod.id}`"
                    class="absolute right-0 mt-2 w-[170px] bg-gray-100 text-black border border-gray-300 rounded-xl shadow-lg z-10 dark:bg-gray-800 dark:border-gray-700 dark:text-white"
                  >
                    <li
                      @click="openAddTaskModal(proj.id, mod.id)"
                      class="flex items-center gap-2 px-4 py-2 hover:bg-gray-300 rounded-xl cursor-pointer text-left dark:hover:bg-gray-900"
                    >
                      <PlusIcon class="w-4 h-4 text-black dark:text-green-400" />
                      Добавить задачу
                    </li>
                    <li
                      @click="editModule(mod.id)"
                      class="flex items-center gap-2 px-4 py-2 hover:bg-gray-300 rounded-xl cursor-pointer text-left dark:hover:bg-gray-900"
                    >
                      <PencilIcon class="w-4 h-4 text-black dark:text-blue-400" />
                      Изменить
                    </li>
                    <li
                      @click="prepareDelete('module', mod.id, proj.id)"
                      class="flex items-center gap-2 px-4 py-2 hover:bg-gray-300 rounded-xl cursor-pointer text-left dark:hover:bg-gray-900 text-red-400"
                    >
                      <TrashIcon class="w-4 h-4"/>
                      Удалить
                    </li>
                  </ul>
                </td>
              </tr>

              <!-- Tasks -->
              <template v-if="expandedModules.includes(mod.id)">
                <tr
                  v-for="task in filterTasks(mod.tasks)"
                  :key="task.id"
                  class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
                >
                  <td class="px-6 py-4"></td>
                  <td class="px-6 py-4">📌 {{ task.title }}</td>
                  <td class="px-6 py-4">
                    {{ task.assigned_to?.username || "—" }}
                  </td>
                  <td class="px-6 py-4">
                    {{ formatPeriod(task.created_at, task.due_date) }}
                  </td>
                  <td class="px-6 py-4">
                    <span
                      :class="[
                        'text-sm font-medium me-2 px-2.5 py-0.5 rounded-sm',
                        getStatusClass(statusLabel(task.status.name)),
                      ]"
                      >{{ statusLabel(task.status.name) }}</span
                    >
                  </td>
                  <td class="px-6 py-4"></td>
                  <td class="px-6 py-4">{{ getTaskCompletion(task) }}%</td>
                  <td class="relative px-6 py-4 text-right">
                    <button
                      @click.stop="toggleMenu(`task-${task.id}`)"
                      class="focus:outline-none p-1 rounded hover:bg-gray-300 dark:hover:bg-gray-700"
                    >
                      <EllipsisHorizontalIcon class="w-5 h-5 text-gray-300" />
                    </button>
                    <ul
                      v-if="openMenuId === `task-${task.id}`"
                      class="absolute right-0 mt-2 w-40 bg-gray-100 text-black border border-gray-300 rounded-xl shadow-lg z-10 dark:bg-gray-800 dark:border-gray-700 dark:text-white"
                    >
                      <li
                        @click="goToTaskForm(task.id)"
                        class="flex items-center gap-2 px-4 py-2 hover:bg-gray-300 rounded-xl cursor-pointer text-left dark:hover:bg-gray-900"
                      >
                        <EyeIcon class="w-4 h-4 text-black dark:text-indigo-400" />
                        <span>Просмотреть</span>
                      </li>
                      <li
                        @click="editTask(task.id)"
                        class="flex items-center gap-2 px-4 py-2 hover:bg-gray-300 rounded-xl cursor-pointer text-left dark:hover:bg-gray-900"
                      >
                        <PencilIcon class="w-4 h-4 text-black dark:text-blue-400" />
                        Изменить
                      </li>
                      <li
                        @click="prepareDelete('task', task.id, task.projectId)"
                        class="flex items-center gap-2 px-4 py-2 hover:bg-gray-300 rounded-xl cursor-pointer text-left dark:hover:bg-gray-900 text-red-400 text-sm"
                      >
                        <TrashIcon class="w-4 h-4" />
                        Удалить
                      </li>
                    </ul>
                  </td>
                </tr>
              </template>
            </template>

            <!-- Tasks without modules -->
            <tr
              v-for="task in getUnlinkedTasks(proj)"
              :key="task.id"
              class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
            >
              <td class="px-6 py-4"></td>
              <td class="px-6 py-4">📌 {{ task.title }}{{ task.module }}</td>
              <td class="px-6 py-4">{{ task.assigned_to?.username || "—" }}</td>
              <td class="px-6 py-4">
                {{ formatPeriod(task.created_at, task.due_date) }}
              </td>
              <td class="px-6 py-4">
                <span
                  :class="[
                    'text-sm font-medium me-2 px-2.5 py-0.5 rounded-sm',
                    getStatusClass(statusLabel(task.status.name)),
                  ]"
                >
                  {{ statusLabel(task.status.name) }}
                </span>
              </td>
              <td class="px-6 py-4"></td>
              <td class="px-6 py-4">{{ getTaskCompletion(task) }}%</td>
              <td class="relative px-6 py-4 text-right">
                <button
                  @click.stop="toggleMenu(`task-${task.id}`)"
                  class="focus:outline-none p-1 rounded hover:bg-gray-300 dark:hover:bg-gray-700"
                >
                  <EllipsisHorizontalIcon class="w-5 h-5 text-gray-300" />
                </button>
                <ul
                  v-if="openMenuId === `task-${task.id}`"
                  class="absolute right-0 mt-2 w-40 bg-gray-100 text-black border border-gray-300 rounded-xl shadow-lg z-10 dark:bg-gray-800 dark:border-gray-700 dark:text-white"
                >
                  <li
                    @click="goToTaskForm(task.id)"
                    class="flex items-center gap-2 px-4 py-2 hover:bg-gray-300 dark:hover:bg-gray-900 rounded-xl cursor-pointer text-left"
                  >
                    <EyeIcon class="w-4 h-4 text-black dark:text-indigo-400" />
                    Просмотреть
                  </li>
                  <li
                    @click="editTask(task.id)"
                    class="flex items-center gap-2 px-4 py-2 hover:bg-gray-300 dark:hover:bg-gray-900 rounded-xl cursor-pointer text-left"
                  >
                    <PencilIcon class="w-4 h-4 text-black dark:text-blue-400" />
                    Изменить
                  </li>
                  <li
                    @click="prepareDelete('task', task.id, task.projectId)"
                    class="flex items-center gap-2 px-4 py-2 hover:bg-gray-300 dark:hover:bg-gray-900 rounded-xl cursor-pointer text-left text-red-400"
                  >
                    <TrashIcon class="w-4 h-4" />
                    Удалить
                  </li>
                </ul>
              </td>
            </tr>
          </template>
        </template>
      </tbody>
    </table>

    <div
      v-if="showConfirmModal"
      id="popup-modal"
      tabindex="-1"
      class="fixed inset-0 z-50 flex items-center justify-center w-full md:inset-0 h-[calc(100%-1rem)] max-h-full"
    >
      <div class="relative p-4 w-full max-w-md max-h-full">
        <div class="relative bg-white rounded-lg shadow-sm dark:bg-gray-700">
          <button
            type="button"
            @click="cancelDelete"
            class="absolute top-3 end-2.5 text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center dark:hover:bg-gray-600 dark:hover:text-white"
            data-modal-hide="popup-modal"
          >
            <svg
              class="w-3 h-3"
              aria-hidden="true"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 14 14"
            >
              <path
                stroke="currentColor"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"
              />
            </svg>
            <span class="sr-only">Отменить</span>
          </button>
          <div class="p-4 md:p-5 text-center">
            <svg
              class="mx-auto mb-4 text-gray-400 w-12 h-12 dark:text-gray-200"
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
              Вы действительно хотите удалить
              {{
                inlineDeleteInfo.type === "project"
                  ? "проект"
                  : inlineDeleteInfo.type === "module"
                  ? "модуль"
                  : inlineDeleteInfo.type === "task"
                  ? "задачу"
                  : ""
              }}?
            </h3>
            <button
              type="button"
              @click="confirmDelete"
              data-modal-hide="popup-modal"
              class="text-white bg-red-600 hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 dark:focus:ring-red-800 font-medium rounded-lg text-sm inline-flex items-center px-5 py-2.5 text-center"
            >
              Удалить
            </button>
            <button
              @click="cancelDelete"
              data-modal-hide="popup-modal"
              type="button"
              class="py-2.5 px-5 ms-3 text-sm font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-4 focus:ring-gray-100 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700"
            >
              Отменить
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- <div class="fixed bottom-0 w-[1270px] z-50">
      <ProjectProgressChart
        class=""
        
        :all-projects="projects"
      />
    </div> -->
  </div>
</template>

<script>
import api from "@/utils/axios";
import AddTaskModal from "@/components/tasks/AddTaskModal.vue";
import ProjectProgressChart from "@/components/ui/ProjectProgressChart.vue";
import {
  DocumentIcon,
  FolderIcon,
  Cog8ToothIcon,
} from "@heroicons/vue/24/solid";
import {
  EyeIcon,
  PlusIcon,
  PencilIcon,
  TrashIcon,
  EllipsisHorizontalIcon,
} from "@heroicons/vue/24/outline";

export default {
  components: {
    AddTaskModal,
    ProjectProgressChart,
    DocumentIcon,
    FolderIcon,
    Cog8ToothIcon,
    EyeIcon,
    PlusIcon,
    PencilIcon,
    TrashIcon,
    EllipsisHorizontalIcon,
  },
  data() {
    return {
      users: [],
      openMenuId: null,
      expandedProjects: [],
      expandedModules: [],
      inlineDeleteInfo: {
        type: null,
        id: null,
        projectId: null,
      },
      showConfirmModal: false,
      projects: [],
      addingModuleProjectId: null,
      editingModuleId: null,
      newModuleName: "",
      updatedName: "",
      showAddTaskModal: false,
      selectedProjectForModule: null,
      selectedTaskContext: { projectId: null, moduleId: null },
      selectedProjectForChart: null,
      filesOpen: [],
    };
  },
  computed: {
    currentTaskProject() {
      return (
        this.projects.find(
          (p) => p.id === this.selectedTaskContext.projectId
        ) || {}
      );
    },
    currentTaskModule() {
      const proj = this.currentTaskProject;
      return (
        proj.modules?.find((m) => m.id === this.selectedTaskContext.moduleId) ||
        null
      );
    },
  },
  async created() {
    await this.reloadProjects();
    // await this.loadUsers();
  },
  methods: {
    getStatusClass(status) {
      switch (status) {
        case "Start":
          return "bg-red-200 text-red-800 dark:bg-red-700 dark:text-red-200";
        case "Finish":
          return "bg-green-200 text-green-800 dark:bg-green-700 dark:text-green-200";
        case "—":
          return "bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300";
        default:
          return "bg-yellow-200 text-yellow-800 dark:bg-yellow-700 dark:text-yellow-200";
      }
    },
    getProjectTasks(project) {
      const fromModules =
        project.modules?.flatMap((m) =>
          (m.tasks || []).filter((t) => !t.is_archived)
        ) || [];
      const unlinked = this.getUnlinkedTasks(project);
      return [...fromModules, ...unlinked];
    },
    filterTasks(taskList) {
      if (!taskList || !Array.isArray(taskList)) return [];
      return taskList.filter((task) => !task.is_archived);
    },
    getProjectStatus(project) {
      const tasks = this.getProjectTasks(project);
      if (!tasks.length) return "—";

      const withOrder = tasks.filter(
        (t) => t.status && typeof t.status.order === "number"
      );
      if (!withOrder.length) return "—";

      const [minTask] = withOrder.sort(
        (a, b) => a.status.order - b.status.order
      );
      return this.statusLabel(minTask.status.name);
    },
    getProjectCompletion(project) {
      const tasks = this.getProjectTasks(project);
      if (!tasks.length) return 0;

      const doneCount = tasks.filter((t) => {
        return t.status?.name === "Finish";
      }).length;

      return Math.round((doneCount / tasks.length) * 100);
    },
    getTaskCompletion(task) {
      const name = task.status?.name;
      if (name === "Start") {
        return 0;
      }
      if (name === "Finish") {
        return 100;
      }
      if (name === "Overdue") {
        return 0;
      }
      return 50;
    },

    handleDocumentClick() {
      if (this.openMenuId || this.filesOpen.length > 0) {
        this.openMenuId = null;
        this.filesOpen = [];
      }
    },

    prepareDelete(type, id, projectId = null) {
      this.inlineDeleteInfo = { type, id, projectId };
      this.showConfirmModal = true;
    },

    cancelDelete() {
      this.showConfirmModal = false;
      this.inlineDeleteInfo = { type: null, id: null, projectId: null };
    },

    toggleFiles(projectId) {
      this.filesOpen = [];
      const idx = this.filesOpen.indexOf(projectId);
      if (idx === -1) {
        this.filesOpen.push(projectId);
      } else {
        this.filesOpen.splice(idx, 1);
      }
      this.openMenuId = null;
    },

    confirmDelete() {
      const { type, id, projectId } = this.inlineDeleteInfo;
      this.showConfirmModal = false;
      this.deleteInline(type, id, projectId);
      this.inlineDeleteInfo = { type: null, id: null, projectId: null };
    },

    async deleteInline(type, id, projectId) {
      try {
        let url;
        if (type === "project") {
          url = `/projects/${id}/`;
        } else if (type === "module") {
          url = `/projects/modules/${id}/`;
        } else if (type === "task") {
          url = `/tasks/${id}/`;
        } else {
          throw new Error("Unknown type: " + type);
        }

        await api.delete(url);
        await this.reloadProjects();

        if (projectId && !this.expandedProjects.includes(projectId)) {
          this.expandedProjects.push(projectId);
        }
      } catch (e) {
        console.error(`${type} o'chirish xatosi:`, e);
      }
    },

    async saveModuleInline(projectId) {
      if (!this.newModuleName.trim()) return;
      try {
        const response = await api.post(`/projects/modules/`, {
          name: this.newModuleName,
          project: projectId,
        });
        await this.reloadProjects();

        if (!this.expandedProjects.includes(projectId)) {
          this.expandedProjects.push(projectId);
        }

        this.cancelAddModuleInline();
      } catch (e) {
        console.error("Module yaratish xatosi:", e);
      }
    },

    async updateModuleInline(moduleId, projectId) {
      if (!this.updatedName.trim()) return;
      try {
        await api.patch(`/projects/modules/${moduleId}/`, {
          name: this.updatedName,
        });
        await this.reloadProjects();

        if (!this.expandedProjects.includes(projectId)) {
          this.expandedProjects.push(projectId);
        }

        this.cancelAddModuleInline();
      } catch (e) {
        console.error("Module yangilash xatosi:", e);
      }
    },

    async deleteModuleInline(moduleId, projectId) {
      try {
        await api.delete(`/projects/modules/${moduleId}/`);
        await this.reloadProjects();

        if (!this.expandedProjects.includes(projectId)) {
          this.expandedProjects.push(projectId);
        }

        this.cancelAddModuleInline();
      } catch (e) {
        console.error("Module o'chirish xatosi:", e);
      }
    },

    cancelAddModuleInline() {
      this.addingModuleProjectId = null;
      this.newModuleName = "";
      this.updatedName = "";
    },

    startAddModuleInline(projectId) {
      this.addingModuleProjectId = projectId;
      this.newModuleName = "";
    },

    startEditModuleInline(module) {
      this.editingModuleId = module.id;
      this.updatedName = module.name;
    },

    cancelEditModuleInline() {
      this.editingModuleId = null;
      this.updatedName = "";
    },
    toggleMenu(id) {
      this.openMenuId = this.openMenuId === id ? null : id;
      this.filesOpen = [];
    },
    goToTaskForm(taskId) {
      this.$router.push(`/taskform/${taskId}`);
    },
    goToProjectDetail(id) {
      this.$router.push(`/projects/${id}`);
    },
    async reloadProjects() {
      try {
        const { data } = await api.get("/projects/");
        this.projects = data.map((proj) => ({
          ...proj,
          modules: (proj.modules || []).map((mod) => ({
            ...mod,
            tasks: (mod.tasks || []).filter((t) => !t.is_archived),
          })),
          tasks: (proj.tasks || []).filter((t) => !t.is_archived),
        }));
      } catch (e) {
        console.error("Проекты не загружены", e);
      }
    },
    toggleExpand(id) {
      const i = this.expandedProjects.indexOf(id);
      i === -1
        ? this.expandedProjects.push(id)
        : this.expandedProjects.splice(i, 1);
    },
    toggleModule(id) {
      const i = this.expandedModules.indexOf(id);
      i === -1
        ? this.expandedModules.push(id)
        : this.expandedModules.splice(i, 1);
    },
    selectProjectForChart(project) {
      this.selectedProjectForChart = project;
    },
    //openAddTaskModal(projectId, moduleId, statusId) {
    //  this.selectedProjectForTask = { project: projectId, module: moduleId };
    //  this.showAddTaskModal = true;
    //},
    //closeAddTaskModal() {
    //  this.showAddTaskModal = false;
    //  this.selectedProjectForTask = { project: null, module: null };
    //},
    statusLabel(status) {
      const map = {
        done: "Завершен",
        in_progress: "В процессе",
        todo: "Не начат",
      };
      return map[status] || status;
    },
    formatPeriod(start, end) {
      const s = this.formatDate(start);
      const e = this.formatDate(end);
      return `${s} — ${e}`;
    },
    formatDate(dateStr) {
      if (!dateStr) return "?";
      return new Date(dateStr).toLocaleDateString("ru-RU");
    },
    getUnlinkedTasks(proj) {
      if (!proj || !proj.tasks) return [];
      return proj.tasks.filter((task) => !task.module && !task.is_archived);
    },
    async loadUsers() {
      try {
        const { data } = await api.get("/auth/users/employees/");
        this.users = data;
      } catch (e) {
        console.error("Пользователи не загружены", e);
      }
    },

    openAddTaskModal(projectId, moduleId) {
      this.selectedTaskContext = { projectId, moduleId };
      this.showAddTaskModal = true;
      this.loadUsers();
    },
    closeAddTaskModal() {
      this.showAddTaskModal = false;
      this.selectedTaskContext = { projectId: null, moduleId: null };
    },

    async handleTaskCreate(payload) {
      try {
        const response = await api.post("/tasks/", payload);
        console.log("Server javobi:", response.data);
        this.reloadProjects();

        // this.closeAddTaskModal();
      } catch (e) {
        console.error("Task yaratishda xatolik:", e.response?.data || e);
      }
    },
  },
  mounted() {
    document.addEventListener("click", this.handleDocumentClick);
  },
  beforeUnmount() {
    document.removeEventListener("click", this.handleDocumentClick);
  },
};
</script>

<style scoped>
.rotate-180 {
  transform: rotate(180deg);
}
</style>
