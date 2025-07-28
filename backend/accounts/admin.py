from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Organization
from projects.models import Project
from tasks.models import Task

class UserInline(admin.TabularInline):
    model = User
    fields = ('username', 'email', 'role', 'is_active')
    extra = 0
    show_change_link = True

class ProjectInline(admin.TabularInline):
    model = Project
    fields = ('name', 'director', 'manager', 'is_archived')
    extra = 0
    show_change_link = True


class TaskInline(admin.TabularInline):
    model = Task
    fields = ('title', 'assigned_to', 'status', 'is_archived')
    extra = 0
    show_change_link = True

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display    = ('id', 'name', 'inn', 'created_by', 'created_at')
    search_fields   = ('name',)
    ordering        = ('-created_at',)
    inlines         = (UserInline, ProjectInline, TaskInline)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        
        (_('Personal info'), {
            'fields': (
                'first_name', 'last_name', 'email', 'phone',
                'gender', 'date_of_birth',
                'location', 'address'
            )
        }),

        (_('Custom Fields'), {
            'fields': (
                'role', 'organization',
                'profile_picture', 'bio',
                'telegram_id', 'language',
                'social_links',
            )
        }),

        (_('Permissions'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),

        (_('Important dates'), {
            'fields': ('last_login', 'date_joined')
        }),
    )

    list_display = (
        'username', 'email', 'full_name',
        'organization', 'role', 'is_staff', 'is_active'
    )

    list_filter = (
        'organization', 'role',
        'gender', 'language',
        'is_staff', 'is_superuser', 'is_active'
    )

    search_fields = (
        'username', 'email',
        'first_name', 'last_name',
        'organization__name', 'phone'
    )

    list_per_page = 30
    filter_horizontal = ('groups', 'user_permissions',)
    readonly_fields = ('last_login', 'date_joined', 'password')
    ordering = ('-date_joined',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(organization=request.user.organization)

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = _('Full name')
