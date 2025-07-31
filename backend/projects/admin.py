from django.contrib import admin
from .models import Project, Module, ProjectFile
from import_export.admin import ImportExportModelAdmin
from tasks.models import Task

class TaskInline(admin.TabularInline):
    model = Task
    fields = ('title', 'assigned_to', 'status', 'is_archived')
    extra = 0
    show_change_link = True

class ModuleInline(admin.TabularInline):
    model = Module
    fields = ('name',)
    extra = 0
    show_change_link = True

@admin.register(Project)
class ProjectAdmin(ImportExportModelAdmin):
    list_display = ('name', 'organization', 'director', 'manager', 'start_date', 'end_date')  
    list_filter = ('start_date', 'organization', 'director', 'manager')  
    search_fields = ('name', 'description', 'director__username', 'manager__username')
    autocomplete_fields = ('director', 'manager')  
    date_hierarchy = 'start_date'
    list_per_page = 25
    list_select_related = ('director', 'manager')
    inlines = (TaskInline, ModuleInline) 

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'project')
    search_fields = ('name',)
    list_filter = ('project',)

admin.site.register(ProjectFile)