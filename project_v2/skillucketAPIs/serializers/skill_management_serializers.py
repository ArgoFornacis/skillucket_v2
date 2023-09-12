from rest_framework import serializers
from skillucketApp.models.bucket_skill import BucketSkill
from skillucketApp.models.category import Category
from skillucketApp.models.skill import Skill
from skillucketApp.models.user_skill import UserSkill


class BucketSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = BucketSkill
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SkillSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Skill
        fields = '__all__'


class UserSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSkill
        fields = '__all__'
