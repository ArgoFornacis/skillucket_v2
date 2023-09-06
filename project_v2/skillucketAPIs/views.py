from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .validators import validate_base64_image


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
