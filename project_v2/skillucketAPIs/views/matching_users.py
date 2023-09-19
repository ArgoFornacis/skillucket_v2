from rest_framework import status
from rest_framework.response import Response
from ..serializers.user_management_serializers import UserProfileGetSerializer
from rest_framework.views import APIView
from django.contrib.auth.models import User
from skillucketApp.models.skill import Skill
from rest_framework.permissions import IsAuthenticated


class MatchingUsersView(APIView):
    permission_classes = [IsAuthenticated]
    """ list all users that have the skill matches to the skill the authenticated user has on his bucket skill
        example: I want to learn: python (my bucket skill) -> matches: user1, user2 (have python on their skill list)
        response: A list of user profiles that match the criteria
      """

    def get(self, request):
        """get request to list all the matching users"""
        # get bucket skills:
        wanted_skills = Skill.objects.filter(bucketskill__user=request.user)

        # get matching users:
        matching_users = (
            User.objects.filter(userskill__skill__in=wanted_skills)
            .distinct()
            .exclude(id=request.user.id)
        )

        serializer = UserProfileGetSerializer(matching_users, many=True)
        return Response(serializer.data)


class SearchUserBySkill(APIView):
    permission_classes = [IsAuthenticated]
    """ allow users to search for other users based on a specific skill
    response: A list of users who have the skill
    """

    def get(self, request):
        """get request to list users with matches skills to the bucket skill of the authenticated user"""
        skill_name = request.query_params.get(
            "name"
        )  # get skill name from query params
        if not skill_name:
            return Response({"error": "Skill name was not provided"})
        try:
            # get the skill objects:
            skill = Skill.objects.get(
                name__icontains=skill_name
            )  # case-insensitive and partial str match
        except Skill.DoesNotExist:
            return Response(
                {"error": f"No skill found with name: {skill_name}"},
                status=status.HTTP_404_NOT_FOUND,
            )
        # get the matching users:
        matching_users = (
            User.objects.filter(userskill__skill=skill)
            .distinct()
            .exclude(id=request.user.id)
        )
        serializer = UserProfileGetSerializer(matching_users, many=True)
        return Response(serializer.data)
