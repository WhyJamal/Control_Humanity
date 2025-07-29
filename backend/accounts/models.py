import uuid
import os
import re
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings

class Organization(models.Model):
    name = models.CharField("Полное название", max_length=100)
    short_name = models.CharField("Краткое название", max_length=50, blank=True, null=True)
    inn = models.CharField(
        "ИНН",
        max_length=12,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{12}$',
                message='INN must be exactly 12 digits'
            )
        ]
    )
    pnfl = models.CharField(
        "ПНФЛ",
        max_length=14, blank=True, null=True,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{14}$',
                message='PNFL must be exactly 14 digits'
            )
        ]
    )
    address = models.CharField("Адрес", max_length=255, blank=True, null=True)
    email = models.EmailField("Email", unique=True, blank=True, null=True)
    phone = models.CharField(
        "Телефон",
        max_length=20, blank=True, null=True,
        validators=[
            RegexValidator(
                regex=r'^\+?\d{7,20}$',
                message='Введите корректный номер телефона'
            )
        ]
    )
    bank_name = models.CharField("Наименование банка", max_length=100, blank=True, null=True)
    bank_account = models.CharField(
        "Расчётный счёт",
        max_length=34,
        blank=True,
        null=True,
        help_text="Номер расчетного счёта (до 34 символов, IBAN поддерживается)"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="owned_organizations",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Создатель организации"
    )
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    def __str__(self):
        return self.short_name or self.name 
       
class User(AbstractUser):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
    ROLE_CHOICES = (
        ('employee', 'Employee'),
        ('manager', 'Manager'),
        ('admin', 'Admin'),
        ('director', 'Director'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20, blank=True, null=True, unique=True)
    telegram_id = models.CharField(max_length=32, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)   
    bio = models.TextField(blank=True, null=True)
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    social_links = models.JSONField(default=dict, blank=True)

    def profile_upload_path(instance, filename):
        ext = os.path.splitext(filename)[1]
        username = re.sub(r'\W+', '_', instance.username) 
        user_id = instance.id if instance.id else 'new'
        return f'profiles/{username}_{user_id}_{uuid.uuid4()}{ext}'
    
    profile_picture = models.ImageField(upload_to=profile_upload_path, blank=True, null=True)
    # profile_picture = models.ImageField(upload_to='media/profiles/', blank=True, null=True) 
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

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        
    def is_employee(self):
        return self.role == 'employee'

    def is_manager(self):
        return self.role == 'manager'

    def is_director(self):
        return self.role == 'director'

    def __str__(self):
        return f"{self.username} ({self.organization})"