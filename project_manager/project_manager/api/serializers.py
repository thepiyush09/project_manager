from rest_framework import serializers
from .models import Client, Project
from django.contrib.auth.models import User

class ProjectDetailSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client', 'users', 'created_at', 'updated_at', 'created_by']

    def get_users(self, obj):
        return [{'id': user.id, 'name': user.username} for user in obj.users.all()]

class ClientDetailSerializer(serializers.ModelSerializer):
    projects = ProjectDetailSerializer(many=True, read_only=True)
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'projects', 'created_at', 'updated_at', 'created_by']

class ClientSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'created_at', 'updated_at', 'created_by']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client', 'users', 'created_at', 'updated_at']
