from django.apps import apps
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Task
from tasks.utils import send_telegram_message

# @receiver(post_save, sender=Task)
# def notify_on_task_create(sender, instance, created, **kwargs):
#     if created and instance.assigned_to and instance.assigned_to.telegram_id:
#         text = f"Salom {instance.assigned_to.first_name}!\nSizga yangi vazifa: {instance.title}"
#         send_telegram_message.delay(instance.assigned_to.telegram_id, text)

