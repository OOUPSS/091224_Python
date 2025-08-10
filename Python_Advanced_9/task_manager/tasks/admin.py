from django.contrib import admin
from .models import Task, SubTask, Category

# Инлайн для подзадач
class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1  # По умолчанию добавляется 1 дополнительная строка для подзадачи

# Класс админки для Task
class TaskAdmin(admin.ModelAdmin):
    inlines = [SubTaskInline]  # Добавляем подзадачи как инлайн
    list_display = ('title', 'status', 'deadline', 'created_at')  # Столбцы для отображения
    search_fields = ('title', 'description')  # Поиск по этим полям
    list_filter = ('status', 'categories')  # Фильтрация по статусу и категориям
    ordering = ['-created_at']  # Сортировка по убыванию даты создания

# Класс админки для SubTask
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'deadline', 'created_at')  # Столбцы для отображения
    search_fields = ('title', 'description')  # Поиск по этим полям
    list_filter = ('status',)  # Фильтрация по статусу

# Класс админки для Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Столбцы для отображения
    search_fields = ('name',)  # Поиск по имени категории

# Регистрация моделей
admin.site.register(Task, TaskAdmin)
admin.site.register(SubTask, SubTaskAdmin)
admin.site.register(Category, CategoryAdmin)
