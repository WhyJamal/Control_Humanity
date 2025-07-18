from rest_framework import serializers
from .models import User, Organization
from django.contrib.auth.password_validation import validate_password
from tasks.models import Status

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'first_name', 'last_name', 'role', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn’t match."})
        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data.pop('password2')
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=validated_data['role'],
            organization=request.user.organization
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class OrganizationRegisterSerializer(serializers.Serializer):
    organization = OrganizationSerializer()
    user = RegisterSerializer()

    def validate(self, data):
        org_serializer = OrganizationSerializer(data=data['organization'])
        user_serializer = RegisterSerializer(data=data['user'], context=self.context)

        if not org_serializer.is_valid():
            raise serializers.ValidationError({'organization': org_serializer.errors})
        if not user_serializer.is_valid():
            raise serializers.ValidationError({'user': user_serializer.errors})

        return data

    def create(self, validated_data):
        org_data = validated_data.get('organization')
        user_data = validated_data.get('user')

        password = user_data.pop('password')
        user_data.pop('password2', None)

        user = User(**user_data)
        user.set_password(password)
        user.save()

        organization = Organization.objects.create(**org_data, created_by=user)

        user.organization = organization
        user.save()

        default_statuses = [
            ("Start",   0, True),
            ("Overdue", 1, False),
            ("Finish",  2, False),
        ]
        for name, order, is_default in default_statuses:
            Status.objects.create(
                name=name,
                order=order,
                is_default=is_default,
                organization=organization 
            )
        
        return {
            "user": user,
            "organization": organization
        }

class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(use_url=True)
    organization_name = serializers.CharField(source='organization.short_name', read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'organization_name', 'role', 'profile_picture', 'phone', 'telegram_id', 'language', 'is_active',)
