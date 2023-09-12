from rest_framework import serializers
from skillucketApp.models.bucket_skill import BucketSkill


class BucketSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = BucketSkill
        fields = '__all__'
