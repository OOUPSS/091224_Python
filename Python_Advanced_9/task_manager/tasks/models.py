from django.db import models

# Модель Category
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'task_manager_category'  # Имя таблицы в базе данных
        verbose_name = 'Category'  # Человекочитаемое имя модели
        unique_together = ('name',)  # Уникальность по полю name


# Модель Task
class Task(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('In progress', 'In progress'),
        ('Pending', 'Pending'),
        ('Blocked', 'Blocked'),
        ('Done', 'Done'),
    ]
    
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    categories = models.ManyToManyField(Category)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_task'  # Имя таблицы в базе данных
        ordering = ['-created_at']  # Сортировка по убыванию даты создания
        verbose_name = 'Task'  # Человекочитаемое имя модели
        unique_together = ('title',)  # Уникальность по полю title


# Модель SubTask
class SubTask(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('In progress', 'In progress'),
        ('Pending', 'Pending'),
        ('Blocked', 'Blocked'),
        ('Done', 'Done'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    task = models.ForeignKey(Task, related_name='subtasks', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_subtask'  # Имя таблицы в базе данных
        ordering = ['-created_at']  # Сортировка по убыванию даты создания
        verbose_name = 'SubTask'  # Человекочитаемое имя модели
        unique_together = ('title',)  # Уникальность по полю title
