# Generated by Django 5.2 on 2025-07-31 11:20

import django.db.models.deletion
import tasks.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_alter_task_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='task_files/', validators=[tasks.models.validate_task_file_extension])),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='tasks.task')),
            ],
        ),
    ]
