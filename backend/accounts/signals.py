import os
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings
from .models import User 

@receiver(pre_save, sender=User)
def delete_old_profile_picture(sender, instance, **kwargs):
    if not instance.pk:
        return  

    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    old_file = old_instance.profile_picture
    new_file = instance.profile_picture

    if old_file and old_file != new_file:
        try:
            old_path = old_file.path
            if os.path.isfile(old_path):
                os.remove(old_path)
        except Exception as e:
            print(f"Ошибка: {e}")
