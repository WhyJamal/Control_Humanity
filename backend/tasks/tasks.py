from celery import shared_task
from django.utils import timezone
from tasks.models import Task, Status

@shared_task
def mark_overdue_tasks():
    now = timezone.now()
    try:
        overdue_status = Status.objects.get(name="Overdue")
    except Status.DoesNotExist:
        print("⚠️ 'Overdue' status topilmadi.")
        return

    overdue_tasks = Task.objects.filter(
        due_date__lt=now,
        done=False
    ).exclude(status=overdue_status)

    for task in overdue_tasks:
        task.status = overdue_status
        task.save()
