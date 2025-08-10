from django.shortcuts import render
from tasks.models import Task, SubTask

# Пример представления для отображения задач
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})
