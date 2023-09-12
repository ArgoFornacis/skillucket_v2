from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    """  login serializer"""
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
