from django.contrib import admin
from .models import Task, SubTask, Category

# Инлайн форма для подзадач
class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1  # Количество пустых подзадач, которое будет отображаться по умолчанию

# Класс админки для Task
class TaskAdmin(admin.ModelAdmin):
    inlines = [SubTaskInline]  # Добавляем инлайн форму для подзадач
    list_display = ('short_title', 'status', 'deadline', 'created_at')  # Используем метод для укороченного названия
    search_fields = ('title', 'description')
    list_filter = ('status', 'categories')
    ordering = ['-created_at']

    def short_title(self, obj):
        """Метод для отображения укороченного названия задачи в списке."""
        return obj.title[:10] + '...' if len(obj.title) > 10 else obj.title
    short_title.short_description = 'Title'

# Класс админки для SubTask
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'deadline', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('status',)
    actions = ['mark_as_done']  # Добавляем действие для изменения статуса на 'Done'

    def mark_as_done(self, request, queryset):
        """Action для подзадач: меняет статус на 'Done'."""
        queryset.update(status='Done')
        self.message_user(request, "Выбранные подзадачи изменены на 'Done'.")
    mark_as_done.short_description = "Пометить как 'Done'"

# Класс админки для Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Регистрация моделей
admin.site.register(Task, TaskAdmin)
admin.site.register(SubTask, SubTaskAdmin)
admin.site.register(Category, CategoryAdmin)
