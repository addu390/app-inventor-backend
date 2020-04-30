from rest_framework import serializers
from .models import Application, User, Component


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'


class ApplicationResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ["user_id", "app_id", "is_active", "name", "description"]


class ApplicationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ["is_active", "name", "description"]


class ApplicationShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ["app_id", "is_active", "name", "description"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_id", "email", "display_name", "image_url", "access_token", "refresh_token", "id_token"]


class UserResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_id", "email", "display_name", "image_url"]


class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = ["app_id", "component_id", "is_active", "request"]
