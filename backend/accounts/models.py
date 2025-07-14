from django.contrib.auth.models import AbstractUser
from django.db import models

class Organization(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class User(AbstractUser):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
    ROLE_CHOICES = (
        ('employee', 'Employee'),
        ('manager', 'Manager'),
        ('admin', 'Admin'),
        ('director', 'Director'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True, unique=True) # unique=True
    telegram_id = models.CharField(max_length=32, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    LANG_CHOICES = [
        ('uz', 'O‘zbekcha'),
        ('ru', 'Русский'),
        ('en', 'English'),
    ]
    language = models.CharField(
        max_length=2,
        choices=LANG_CHOICES,
        default='ru',
    )

    def is_employee(self):
        return self.role == 'employee'

    def is_manager(self):
        return self.role == 'manager'

    def is_director(self):
        return self.role == 'director'

    def __str__(self):
        return f"{self.username} ({self.organization})"