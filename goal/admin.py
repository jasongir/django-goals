from django.contrib import admin
from . import models
# Register your models here.
''' MODELS '''


@admin.register(models.Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'updated_at')
    exclude = ['goal_slug']


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    exclude = ['category_slug']


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    exclude = ['username_slug', 'rating', 'rated']
    fieldsets = (
        (
            None, {
                'fields': ('username', 'email', 'password', 'bio')
            }
        ),
        (
            'Other', {
                'fields': ('first_name', 'last_name', 'groups', 'user_permissions', 'is_superuser', 'is_staff', 'last_login', 'date_joined', 'is_active', )
            }
        ),
    )
