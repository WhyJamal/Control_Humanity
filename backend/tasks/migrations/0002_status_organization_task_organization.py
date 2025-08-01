# Generated by Django 5.2 on 2025-07-15 11:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_organization_address_organization_bank_account_and_more'),
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.organization'),
        ),
        migrations.AddField(
            model_name='task',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.organization'),
        ),
    ]
