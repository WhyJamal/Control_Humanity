import os, uuid, re
from django.db import models
from django.core.exceptions import ValidationError
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
    
    def project_image_upload_path(instance, filename):
        name, ext = os.path.splitext(filename)
        safe_name = re.sub(r'[^\w\d_-]+', '', instance.name)
        uid = str(uuid.uuid4())[:5]
        return f'projects_media/project_{instance.id}_{safe_name}/{safe_name}_{uid}{ext}'
    
    image = models.ImageField(upload_to=project_image_upload_path, blank=True, null=True)
    #image = models.ImageField(upload_to='media/projects/', null=True, blank=True) 
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
        
    def __str__(self):
        return self.name

def validate_project_file_extension(file):
    valid_ext = ['.pdf', '.docx', '.xlsx', '.jpg', '.jpeg', '.png']
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in valid_ext:
        raise ValidationError(f"{ext} Нет разрешения на файл типа. Разрешено: {', '.join(valid_ext)}")

def project_file_upload_path(instance, filename):
    name, ext = os.path.splitext(filename)
    safe_name = re.sub(r'[^\w\d_-]+', '', instance.project.name)
    uid = str(uuid.uuid4())[:5]
    return f'projects_media/project_{instance.project.id}_{safe_name}/files/{safe_name}_{uid}{ext}'

class ProjectFile(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to=project_file_upload_path, validators=[validate_project_file_extension])
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Module(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='modules')
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.project.name} – {self.name}"