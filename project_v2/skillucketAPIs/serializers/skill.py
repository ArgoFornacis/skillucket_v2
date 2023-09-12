from rest_framework import serializers
from skillucketApp.models.skill import Skill
from .category import CategorySerializer


class SkillSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    
    class Meta:
        model = Skill
        fields = '__all__'
