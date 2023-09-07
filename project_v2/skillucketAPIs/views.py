from django.http import Http404
from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer, CategorySerializer, SkillSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .validators import validate_base64_image
from skillucketApp.models.category import Category
from skillucketApp.models.skill import Skill


class RegisterApi(APIView):
    """ register new user, create token automatically, create profile image if it was uploaded by user,
        if not profile created anyway with default pic
        returns: username, password, email, (first last name and image if created)
    """

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            # create user with hashed password:
            user = User.objects.create_user(**serializer.data)
            # create profile:
            file = validate_base64_image(request.data["image"])  # get image data and convert it to file
            profile = user.profile
            profile.image.save(f"{user.username}_profile_image.jpg", file)
            profile.save()
            # create token:
            Token.objects.create(user=user)
            return Response(serializer.data)
        return Response(serializer.errors)


class LoginApi(APIView):
    """ login user return username and token or empty dict if no matching user
        returns: token, user_id
    """

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(**serializer.data)
            if user is not None:
                token = Token.objects.get(user=user)
                data = {'token': str(token), 'user_id': user.id}
                return Response(data)
        return Response(serializer.errors)

# todo : after fixing the model test category apis with postman
class CategoryListCreateApi(APIView):
    """  api that handles get request for listing all the categories and post request for creating a new one """
    def get(self, request):
        """ list all the categories """
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        """  create new category """
        category = request.data
        serializer = CategorySerializer(data=category)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class CategoryByIdApi(APIView):
    """ api that handles get put and delete request by the category id """
    def get_object(self, category_id):
        """ get the category if exists, general function for the class"""
        try:
            return Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, category_id):
        """ retrieve category by its id """
        category = self.get_object(category_id)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request,  category_id):
        """ change category details """
        category = self.get_object(category_id)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, category_id):
        """ delete category by id """
        category = self.get_object(category_id)
        category.delete()
        return Response({"message": "Category was successfully deleted"}, status=204)

    def handle_exception(self, exc):
        """ adding custom error handling """
        if isinstance(exc, Http404):
            return Response({"error": "Category does not exist"})
        return super().handle_exception(exc)


class SkillListCreateApi(APIView):
    """ api class that handles get request for listing all the skills and post request for creating new skill in db """
    def get(self, request):
        """ list all skills """
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response(serializer.data)

    def post(self, request):
        """ create new skill """
        skill = request.data
        serializer = SkillSerializer(data=skill)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class SkillByIdApi(APIView):
    """ api that handles get put and delete request by the skill id """
    def get_object(self, skill_id):
        """ get the skill if exists, general function for the class"""
        try:
            return Skill.objects.get(id=skill_id)
        except Skill.DoesNotExist:
            raise Http404

    def get(self, request, skill_id):
        """ retrieve skill by its id """
        skill = self.get_object(skill_id)
        serializer = SkillSerializer(skill)
        return Response(serializer.data)

    def put(self, request,  skill_id):
        """ change skill details """
        skill = self.get_object(skill_id)
        serializer = SkillSerializer(skill, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, skill_id):
        """ delete skill by id """
        skill = self.get_object(skill_id)
        skill.delete()
        return Response({"message": "Skill was successfully deleted"}, status=204)

    def handle_exception(self, exc):
        """ adding custom error handling """
        if isinstance(exc, Http404):
            return Response({"error": "Skill does not exist"})
        return super().handle_exception(exc)
