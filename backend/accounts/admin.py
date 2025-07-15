from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Organization

class UserInline(admin.TabularInline):
    model = User
    fields = ('username', 'email', 'role', 'is_active')
    extra = 0
    show_change_link = True

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display    = ('id', 'name', 'inn', 'created_by', 'created_at')
    search_fields   = ('name',)
    ordering        = ('-created_at',)
    inlines         = (UserInline,)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        (_('Custom Fields'), {
            'fields': (
                'role', 'organization',
                'profile_picture', 'bio',
                'telegram_id', 'language'
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

    list_display    = (
        'username', 'email', 'full_name',
        'organization', 'role', 'is_staff', 'is_active'
    )
    list_filter     = (
        'organization', 'role',
        'is_staff', 'is_superuser', 'is_active'
    )
    search_fields   = (
        'username', 'email',
        'first_name', 'last_name',
        'organization__name'
    )
    list_per_page   = 30
    filter_horizontal = ('groups', 'user_permissions',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(organization=request.user.organization)

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = _('Full name')



# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from .models import User, Organization
# from django.utils.translation import gettext_lazy as _

# @admin.register(User)
# class UserAdmin(BaseUserAdmin):
#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),
#         (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'phone')}),
#         (_('Permissions'), {
#             'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
#         }),
#         (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
#         (_('Custom Fields'), {'fields': ('role','organization', 'profile_picture', 'bio', 'telegram_id', 'language')}),
#     )
    
#     list_display = ('username', 'email', 'full_name', 'role', 'is_staff', 'is_active')
#     list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
#     search_fields = ('username', 'email', 'first_name', 'last_name')
#     list_per_page = 30
#     filter_horizontal = ('groups', 'user_permissions',)
    
#     def full_name(self, obj):
#         return f"{obj.first_name} {obj.last_name}"
#     full_name.short_description = 'Полное имя'

# @admin.register(Organization)
# class OrganizationAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'created_at')
#     search_fields = ('name',)                         
#     ordering = ('-created_at',)
    
# @admin.register(User)
# class UserAdmin(BaseUserAdmin):
#     fieldsets = BaseUserAdmin.fieldsets + (
#         ('Role and Permissions', {
#             'fields': ('role',),
#         }),
#     )
#     list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff', 'is_superuser')
#     list_filter = ('role', 'is_staff', 'is_superuser')
#     search_fields = ('username', 'email', 'first_name', 'last_name')
