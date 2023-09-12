from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from skillucketApp.models.category import Category
from skillucketApp.models.skill import Skill
from skillucketApp.models.user_skill import UserSkill
from skillucketApp.models.bucket_skill import BucketSkill
from ..serializers.category import CategorySerializer
from ..serializers.skill import SkillSerializer
from ..serializers.bucket_skill import BucketSkillSerializer
from ..serializers.user_skill import UserSkillSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_skills_by_category(request, category_id):
    skills = Skill.objects.filter(category=category_id)
    serializer = SkillSerializer(skills, many=True)
    return Response(serializer.data)


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def manage_user_skills(request):
    user = request.user
    skill_id = request.data.get('skill_id')

    if request.method == 'POST':
        try:
            # Check if the user already has this skill
            skill = Skill.objects.get(id=skill_id)
            user_skill, created = UserSkill.objects.get_or_create(user=user, skill=skill)

            if created:
                serializer = UserSkillSerializer(user_skill)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "Skill already exists in User Skills"}, status=status.HTTP_400_BAD_REQUEST)
        except Skill.DoesNotExist:
            return Response({"message": "Skill not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        try:
            # Find and delete the UserSkill record for the user and skill
            skill = Skill.objects.get(id=skill_id)
            user_skill = UserSkill.objects.get(user=user, skill=skill)
            user_skill.delete()
            return Response({"message": "Skill removed from User Skills"}, status=status.HTTP_204_NO_CONTENT)

        except (Skill.DoesNotExist, UserSkill.DoesNotExist):
            return Response({"message": "Skill not found in User Skills"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def manage_bucket_skills(request):
    user = request.user
    skill_id = request.data.get('skill_id')  # Assuming you send the skill ID in the request data

    if request.method == 'POST':
        try:
            # Check if the user already has this skill in their BucketSkills
            skill = Skill.objects.get(pk=skill_id)  # Get the Skill instance
            bucket_skill, created = BucketSkill.objects.get_or_create(user=user, skill=skill)
            if not created:
                return Response({"message": "Skill already exists in Bucket List"}, status=status.HTTP_400_BAD_REQUEST)

            serializer = BucketSkillSerializer(bucket_skill)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Skill.DoesNotExist:
            return Response({"message": "Skill not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        try:
            # Find and delete the BucketSkill record for the user and skill
            skill = Skill.objects.get(pk=skill_id)  # Get the Skill instance
            bucket_skill = BucketSkill.objects.get(user=user, skill=skill)
            bucket_skill.delete()
            return Response({"message": "Skill removed from Bucket List"}, status=status.HTTP_204_NO_CONTENT)
        except (Skill.DoesNotExist, BucketSkill.DoesNotExist):
            return Response({"message": "Skill not found"}, status=status.HTTP_404_NOT_FOUND)
