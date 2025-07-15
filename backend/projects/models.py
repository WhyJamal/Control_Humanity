from django.db import models
from django.conf import settings
from django.utils import timezone
from accounts.models import Organization

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
    director = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='directed_projects',
        limit_choices_to={'role': 'director'}
    )
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='managed_projects',
        null=True,
        blank=True,
        limit_choices_to={'role': 'manager'}
    )
    start_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_archived = models.BooleanField(default=False)
    image = models.ImageField(upload_to='projects/images/', null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
        
    def __str__(self):
        return self.name


class Module(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='modules')
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.project.name} – {self.name}"