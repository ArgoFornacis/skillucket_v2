from rest_framework import serializers
from .validators import validate_base64_image


class RegisterSerializer(serializers.Serializer):
    """ register serializer
        make sure that the image field gets encoded picture from the frontend
    """
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=255, required=False)
    last_name = serializers.CharField(max_length=255, required=False)
    image = serializers.CharField(required=False, validators=[validate_base64_image])


class LoginSerializer(serializers.Serializer):
    """  login serializer"""
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
