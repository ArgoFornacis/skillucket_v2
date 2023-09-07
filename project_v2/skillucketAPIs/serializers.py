from rest_framework import serializers
from skillucketApp.models.skill import Skill
from skillucketApp.models.category import Category


class RegisterSerializer(serializers.Serializer):
    """ register serializer"""
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=255, required=False)
    last_name = serializers.CharField(max_length=255, required=False)


class LoginSerializer(serializers.Serializer):
    """  login serializer"""
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)


class CategorySerializer(serializers.ModelSerializer):
    """ category serializer """
    class Meta:
        model = Category
        fields = '__all__'


class SkillSerializer(serializers.ModelSerializer):   # do we want to add any validations?
    """  skill serializer """
    class Meta:
        model = Skill
        fields = '__all__'
