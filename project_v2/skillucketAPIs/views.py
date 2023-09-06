from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate


class RegisterApi(APIView):
    """ register new user, create token automatically, create profile image if it was uploaded by user,
        if not profile created anyway with default pic
        returns: username, password, email, (first last name and image if created)
    """

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            # create user:
            user = User.objects.create_user(username=serializer.data["username"],
                                            password=serializer.data["password"],
                                            email=serializer.data["email"],
                                            first_name=serializer.data.get('first_name', ''),
                                            last_name=serializer.data.get('last_name', '')
                                            )
            # create profile:
            profile = user.profile
            profile.image.save = (f"{user.username}_profile_image.jpg", serializer.validated_data["image"])
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
