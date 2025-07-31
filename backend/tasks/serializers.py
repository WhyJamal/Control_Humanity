from rest_framework import serializers
from .models import Task, Status, SimpleTask, TaskMarkedUser, TaskFile
from accounts.serializers import UserSerializer
from django.contrib.auth import get_user_model
from projects.models import Project, Module
from django.db import transaction

User = get_user_model()

class StatusSerializer(serializers.ModelSerializer):
    organization = serializers.IntegerField(source='organization.id', read_only=True)
    
    class Meta:
        model = Status
        fields = ('id', 'name', 'order', 'project', 'color', 'is_default', 'organization')

class TaskFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskFile
        fields = ['id', 'file', 'uploaded_at']  
        
class TaskSerializer(serializers.ModelSerializer):
    organization = serializers.IntegerField(source='organization.id', read_only=True)    
    assigned_to = UserSerializer(read_only=True)
    status = StatusSerializer(read_only=True)
    project = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by = UserSerializer(read_only=True)
    module = serializers.IntegerField(source='module.id', read_only=True, allow_null=True)
    files = TaskFileSerializer(many=True, read_only=True)

    assigned_to_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='employee'),
        source='assigned_to',
        write_only=True,
        required=False
    )
    marked_to_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='employee'),
        source='marked_to',
        many=True,
        write_only=True,
        required=False
    )
    marked_to = UserSerializer(many=True, read_only=True)
    status_id = serializers.PrimaryKeyRelatedField(
        queryset=Status.objects.all(),
        source='status',
        write_only=True
    )
    project_id = serializers.PrimaryKeyRelatedField(
         queryset=Project.objects.all(),
         source='project',
         write_only=True
     )

    module_id = serializers.PrimaryKeyRelatedField(
            queryset=Module.objects.all(),
            source='module',
            allow_null=True,
            required=False,
            write_only=True,
        )
    uploaded_files = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Task
        fields = (
            'id', 'title', 'description',
            'project',      'project_id',
            'assigned_to',  'assigned_to_id',
            'marked_to',    'marked_to_id',
            'status',       'status_id',
            'created_by',   'created_at',
            'updated_at',   'due_date',
            'color',        'data_input',
            'module', 'module_id', 'organization',
            'is_archived',  'done',
            'files', 'uploaded_files', 
        )
        read_only_fields = ('created_by',)
        extra_kwargs = {
          'is_archived': {'required': False},
        }
        
    def validate_assigned_to(self, user):

        if user and user.role != 'employee':
            raise serializers.ValidationError("Назначить можно только сотрудника.")
        return user

    def create(self, validated_data):
        uploaded_files = validated_data.pop('uploaded_files', [])
        marked_users = validated_data.pop('marked_to', [])

        with transaction.atomic():
            task = super().create(validated_data)

            for idx, user in enumerate(marked_users):
                TaskMarkedUser.objects.create(task=task, user=user, order=idx)

            for file in uploaded_files:
                TaskFile.objects.create(task=task, file=file)

        return task


    def update(self, instance, validated_data):
        uploaded_files = validated_data.pop('uploaded_files', [])
        marked_users = validated_data.pop('marked_to', None)

        with transaction.atomic():
            instance = super().update(instance, validated_data)

            if marked_users is not None:
                TaskMarkedUser.objects.filter(task=instance).delete()
                for idx, user in enumerate(marked_users):
                    TaskMarkedUser.objects.create(task=instance, user=user, order=idx)

            for file in uploaded_files:
                TaskFile.objects.create(task=instance, file=file)

        return instance 

class SimpleTaskSerializer(serializers.ModelSerializer):
    status_detail = serializers.StringRelatedField(source='status', read_only=True)

    class Meta:
        model = SimpleTask
        fields = [
            'id',
            'title',
            'description',
            'status',
            'status_detail',
            'created_by',
            'color',
            'created_at',
            'due_date'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'status_detail']