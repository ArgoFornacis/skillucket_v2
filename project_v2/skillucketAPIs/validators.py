import base64
from django.core.files.base import ContentFile
from rest_framework import serializers


def validate_base64_image(value):
    """
    Check that the image is a valid Base64-encoded string.
    Decode it and return a ContentFile (Django's in-memory file).
    """
    try:
        # Decode the Base64 image:
        decoded_image = base64.b64decode(value)
        return ContentFile(decoded_image)
    except Exception:
        raise serializers.ValidationError(
            "Invalid Base64-encoded string for image, check if the image was encoded"
        )
