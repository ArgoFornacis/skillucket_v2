from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from skillucketApp.models.user_skill import UserSkill
from skillucketApp.models.bucket_skill import BucketSkill
from skillucketApp.models.category import Category
from skillucketApp.models.skill import Skill
from ..serializers.skill_management_serializers import (
    UserSkillSerializer,
    BucketSkillSerializer,
    CategorySerializer,
    SkillSerializer,
)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_categories(request):
    """
    Get a list of all skill categories.
    Returns:
    Response: A JSON response containing the serialized list of skill categories.
    """
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_skills_by_category(request, category_id):
    """
    Get a list of skills within a specific category.
    Args:
    request (Request): The HTTP request object.
    category_id (int): The ID of the category to filter skills.
    Returns:
    Response: A JSON response containing the serialized list of skills in the specified category.
    """
    skills = Skill.objects.filter(category=category_id)
    serializer = SkillSerializer(skills, many=True)
    return Response(serializer.data)


@api_view(["POST", "DELETE"])
@permission_classes([IsAuthenticated])
def manage_user_skills(request):
    """
    Add or remove a skill to/from the user's skill list.
    Args:
    request (Request): The HTTP request object.
    Returns:
    Response: A JSON response confirming the action or providing an error message.
    """
    user = request.user
    skill_id = request.data.get("skill_id")

    if request.method == "POST":
        # Try to add the skill to the user's skills
        # Handle cases where the skill does not exist or already exists in the user's skills.
        try:
            skill = Skill.objects.get(id=skill_id)
            user_skill, created = UserSkill.objects.get_or_create(
                user=user, skill=skill
            )
            if created:
                serializer = UserSkillSerializer(user_skill)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {"message": "Skill already exists in User Skills"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Skill.DoesNotExist:
            return Response(
                {"message": "Skill not found"}, status=status.HTTP_404_NOT_FOUND
            )

    if request.method == "DELETE":
        # Try to remove the skill from the user's skills
        # Handle cases where the skill does not exist in the user's skills.
        try:
            skill = Skill.objects.get(id=skill_id)
            user_skill = UserSkill.objects.get(user=user, skill=skill)
            user_skill.delete()
            return Response(
                {"message": "Skill removed from User Skills"},
                status=status.HTTP_204_NO_CONTENT,
            )

        except (Skill.DoesNotExist, UserSkill.DoesNotExist):
            return Response(
                {"message": "Skill not found in User Skills"},
                status=status.HTTP_404_NOT_FOUND,
            )


@api_view(["POST", "DELETE"])
@permission_classes([IsAuthenticated])
def manage_bucket_skills(request):
    """
    Add or remove a skill to/from the user's bucket list.
    Args:
    request (Request): The HTTP request object.
    Returns:
    Response: A JSON response confirming the action or providing an error message.
    """
    user = request.user
    skill_id = request.data.get("skill_id")

    if request.method == "POST":
        # Try to add the skill to the user's bucket list
        # Handle cases where the skill does not exist or already exists in the user's bucket list.
        try:
            skill = Skill.objects.get(pk=skill_id)
            bucket_skill, created = BucketSkill.objects.get_or_create(
                user=user, skill=skill
            )
            if not created:
                return Response(
                    {"message": "Skill already exists in Bucket List"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer = BucketSkillSerializer(bucket_skill)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Skill.DoesNotExist:
            return Response(
                {"message": "Skill not found"}, status=status.HTTP_404_NOT_FOUND
            )

    if request.method == "DELETE":
        # Try to remove the skill from the user's bucket list
        # Handle cases where the skill does not exist in the user's bucket list.
        try:
            skill = Skill.objects.get(pk=skill_id)
            bucket_skill = BucketSkill.objects.get(user=user, skill=skill)
            bucket_skill.delete()
            return Response(
                {"message": "Skill removed from Bucket List"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except (Skill.DoesNotExist, BucketSkill.DoesNotExist):
            return Response(
                {"message": "Skill not found"}, status=status.HTTP_404_NOT_FOUND
            )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_skills(request):
    """
    Get a list of the user's current skills.
    Args:
    request (Request): The HTTP request object.
    Returns:
    Response: A JSON response containing the serialized list of user's current skills.
    """
    user = request.user
    user_skills = UserSkill.objects.filter(user=user)
    serializer = UserSkillSerializer(user_skills, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_bucket_skills(request):
    """
    Get a list of the user's current bucket list skills.
    Args:
    request (Request): The HTTP request object.
    Returns:
    Response: A JSON response containing the serialized list of user's current bucket list skills.
    """
    user = request.user
    bucket_skills = BucketSkill.objects.filter(user=user)
    serializer = BucketSkillSerializer(bucket_skills, many=True)
    return Response(serializer.data)


@api_view(["GET", "PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def user_skill_detail(request, user_skill_id):
    """
    Retrieve or update user skill details.

    Args:
    request (Request): The HTTP request object.
    user_skill_id (int): The ID of the user skill to retrieve or update.

    Returns:
    Response: A JSON response containing the user skill details or confirming the update or providing validation errors.
    """
    try:
        user_skill = UserSkill.objects.get(id=user_skill_id, user=request.user)
    except UserSkill.DoesNotExist:
        return Response(
            {"message": "User skill not found"}, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "GET":
        serializer = UserSkillSerializer(user_skill)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == "PUT" or request.method == "PATCH":
        # Create a serializer instance with partial=True
        serializer = UserSkillSerializer(user_skill, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def bucket_skill_detail(request, bucket_skill_id):
    """
    Retrieve or update bucket skill details.

    Args:
    request (Request): The HTTP request object.
    bucket_skill_id (int): The ID of the bucket skill to retrieve or update.

    Returns:
    Response: A JSON response containing the bucket skill details or confirming the update or providing validation errors.
    """
    try:
        bucket_skill = BucketSkill.objects.get(id=bucket_skill_id, user=request.user)
    except BucketSkill.DoesNotExist:
        return Response(
            {"message": "Bucket skill not found"}, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "GET":
        serializer = BucketSkillSerializer(bucket_skill)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == "PUT" or request.method == "PATCH":
        # Create a serializer instance with partial=True
        serializer = BucketSkillSerializer(
            bucket_skill, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
