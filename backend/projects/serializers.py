
from rest_framework import serializers
from .models import Project, Module, ProjectFile
from accounts.serializers import UserSerializer
from django.contrib.auth import get_user_model
from tasks.serializers import TaskSerializer
from django.db import transaction

User = get_user_model()

class ModuleSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    organization = serializers.IntegerField(source='organization.id', read_only=True)
    
    class Meta:
        model = Module
        fields = ['id', 'name', 'project', 'tasks', 'organization']

class ProjectFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectFile
        fields = ['id', 'file', 'uploaded_at']

class ProjectSerializer(serializers.ModelSerializer):
    organization = serializers.IntegerField(source='organization.id', read_only=True)
    director    = UserSerializer(read_only=True)
    manager     = UserSerializer(read_only=True)
    manager_id  = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='manager'),
        source='manager',
        write_only=True,
        required=False
    )
    modules     = ModuleSerializer(many=True, read_only=True)
    tasks       = TaskSerializer(many=True, read_only=True)
    period      = serializers.SerializerMethodField()
    is_archived = serializers.BooleanField()

    files = ProjectFileSerializer(many=True, read_only=True)
    uploaded_files = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Project
        fields = (
            'id', 'name', 'description',
            'director', 'manager', 'manager_id',
            'start_date', 'end_date', 'period',
            'is_archived', 'modules', 'tasks',
            'image', 'organization',
            'files', 'uploaded_files',
        )

    def create(self, validated_data):
        uploaded_files = validated_data.pop('uploaded_files', [])
        image = validated_data.pop('image', None)  # Rasmni ajratib olamiz
        user = self.context['request'].user
        validated_data['director'] = user

        with transaction.atomic():
            project = super().create(validated_data)

            for f in uploaded_files:
                ProjectFile.objects.create(project=project, file=f)

            if image:
                project.image = image
                project.save()

        return project

    def update(self, instance, validated_data):
        uploaded_files = validated_data.pop('uploaded_files', [])
        with transaction.atomic():
            project = super().update(instance, validated_data)
            for f in uploaded_files:
                ProjectFile.objects.create(project=project, file=f)
        return project

    def get_period(self, obj):
        if obj.end_date:
            return f"{obj.start_date:%d.%m.%Y} — {obj.end_date:%d.%m.%Y}"
        return f"{obj.start_date:%d.%m.%Y}"

