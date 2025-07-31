import os
from django.db import models
from django.conf import settings
from projects.models import Project, Module
from django.utils import timezone
from accounts.models import Organization
from django.core.exceptions import ValidationError

class Status(models.Model):
    name = models.CharField(max_length=50)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, related_name='statuses')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='statuses')
    order = models.PositiveIntegerField(default=0)
    color = models.CharField(max_length=7, default='#FFFFFF')
    is_default = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('name', 'project')
        ordering = ['order', 'id']

    def __str__(self):

            if self.project:
                return f"{self.project.name} – {self.name}"

            return self.name
        
class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)    
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='tasks',
        null=True,
        blank=True,
        limit_choices_to={'role': 'employee'}
    )
    marked_to = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='TaskMarkedUser',
        related_name='task_to_be_marked',
        limit_choices_to={'role': 'employee'},
        blank=True,
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name='tasks'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_tasks'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    data_input = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(null=True, blank=True)
    color = models.CharField(max_length=7, default='#FFFFFF')
    is_archived = models.BooleanField(default=False)
    done = models.BooleanField(default=False)
    module = models.ForeignKey(Module, on_delete=models.CASCADE,
                                related_name='tasks', null=True, blank=True)

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        
    def __str__(self):
        return f"{self.title} ({self.project.name})"

class SimpleTask(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        related_name='simple_tasks'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='simple_created_tasks'
    )
    color = models.CharField(max_length=7, default='#FFFFFF')    
    created_at = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.title
    
class TaskMarkedUser(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        unique_together = ('task', 'user')
        ordering = ['order']     

def validate_task_file_extension(file):
    valid_extensions = ['.pdf', '.docx', '.xlsx', '.jpg', '.jpeg', '.png']
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError(f"Недопустимый тип файла: {ext}. Фиксированный: {', '.join(valid_extensions)}")

class TaskFile(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='task_files/', validators=[validate_task_file_extension])
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name}"

