from rest_framework import serializers
from skillucketApp.models.skill import Skill
from skillucketApp.models.category import Category
from django.contrib.auth.models import User


class RegisterSerializer(serializers.Serializer):
    """ register serializer"""
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=255, required=False)
    last_name = serializers.CharField(max_length=255, required=False)
    image = serializers.CharField(required=False)   # expect to receive encoded file from frontend


class LoginSerializer(serializers.Serializer):
    """  login serializer"""
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)


class UserProfileGetSerializer(serializers.ModelSerializer):
    """  user model base serializer for get request"""
    image = serializers.ImageField(source='profile.image', required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'image')


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """  user model base serializer for ut request"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')


class ChangePasswordSerializer(serializers.Serializer):
    """ change password serializer"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


#  these are out of use at the moment:

class CategorySerializer(serializers.ModelSerializer):
    """ category serializer """
    class Meta:
        model = Category
        fields = '__all__'


class SkillSerializer(serializers.ModelSerializer):
    """  skill serializer """
    class Meta:
        model = Skill
        fields = '__all__'
