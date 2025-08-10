from django.contrib import admin
from .models import Task, SubTask, Category

# Инлайн для подзадач
class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1

# Класс админки для Task
class TaskAdmin(admin.ModelAdmin):
    inlines = [SubTaskInline]
    list_display = ('title', 'status', 'deadline', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('status', 'categories')
    ordering = ['-created_at']

# Класс админки для SubTask
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'deadline', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('status',)

# Класс админки для Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Регистрация моделей
admin.site.register(Task, TaskAdmin)
admin.site.register(SubTask, SubTaskAdmin)
admin.site.register(Category, CategoryAdmin)
