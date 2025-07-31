from django.apps import apps
from django.db.models.signals import post_migrate, post_save, post_delete
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from .models import Task
from tasks.utils import send_telegram_message

# User = get_user_model()

# @receiver(post_save, sender=Task)
# def update_task_counters_on_save(sender, instance, created, **kwargs):
#     user = instance.assigned_to
#     if user:
#         user.current_tasks = Task.objects.filter(
#             assigned_to=user, done=False, is_archived=False
#         ).count()
#         user.completed_tasks = Task.objects.filter(
#             assigned_to=user, done=True, is_archived=False
#         ).count()
#         user.save(update_fields=["current_tasks", "completed_tasks"])

# @receiver(post_delete, sender=Task)
# def update_task_counters_on_delete(sender, instance, **kwargs):
#     user = instance.assigned_to
#     if user:
#         user.current_tasks = Task.objects.filter(
#             assigned_to=user, done=False, is_archived=False
#         ).count()
#         user.completed_tasks = Task.objects.filter(
#             assigned_to=user, done=True, is_archived=False
#         ).count()
#         user.save(update_fields=["current_tasks", "completed_tasks"])

# @receiver(post_save, sender=Task)
# def notify_on_task_create(sender, instance, created, **kwargs):
#     if created and instance.assigned_to and instance.assigned_to.telegram_id:
#         text = f"Salom {instance.assigned_to.first_name}!\nSizga yangi vazifa: {instance.title}"
#         send_telegram_message.delay(instance.assigned_to.telegram_id, text)

