from rest_framework import serializers
from skillucketApp.models.user_skill import UserSkill


class UserSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSkill
        fields = '__all__'
