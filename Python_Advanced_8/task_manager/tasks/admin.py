from django.contrib import admin
from .models import Task, SubTask, Category

class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1

class TaskAdmin(admin.ModelAdmin):
    inlines = [SubTaskInline]
    list_display = ('title', 'status', 'deadline', 'created_at')
    search_fields = ('title', 'description')

class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'deadline', 'created_at')
    search_fields = ('title', 'description')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Task, TaskAdmin)
admin.site.register(SubTask, SubTaskAdmin)
admin.site.register(Category, CategoryAdmin)
