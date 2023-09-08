from rest_framework.views import APIView
from ..serializers import (RegisterSerializer, LoginSerializer, UserProfileGetSerializer, UserProfileUpdateSerializer,
                           ChangePasswordSerializer)
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status
from ..validators import validate_base64_image
from rest_framework.permissions import IsAuthenticated


class RegisterApi(APIView):
    """ register new user create profile image if it was uploaded by user,
        if not profile created anyway with default pic
        Expected Payload: Contains user data including username, password, email,
        optional first name, optional last name, and an optional Base64-encoded profile picture.
        returns: successful registration message and users token
    """

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            # create user with hashed password:
            user = User.objects.create_user(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password'],
                email=serializer.validated_data['email'],
                first_name=serializer.validated_data.get('first_name', ''),
                last_name=serializer.validated_data.get('last_name', '')
            )
            # create profile image if provided:
            image_data = serializer.validated_data.get('image')  # get encoded image data

            if image_data:
                decoded_image = validate_base64_image(image_data)  # decode the image before save in db
                profile = user.profile
                profile.image.save(f"{user.username}_profile_image.jpg", decoded_image)
                profile.save()

            return Response({
                "message": "User registered successfully",
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginApi(APIView):
    """ login user return username and token or empty dict if no matching user
        returns: token, user_id
    """

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(**serializer.data)
            if user is not None:
                # create token:
                token = Token.objects.create(user=user)
                data = {'token': str(token), 'user_id': user.id}
                return Response(data)
        return Response(serializer.errors)


class UserProfileView(APIView):
    """ api view to manage the user profile """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """ view details in the users profile """
        user = request.user
        serializer = UserProfileGetSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        """ change details in users profile """
        user = request.user
        new_data = request.data
        if "image" in request.data:
            image = new_data.pop('image')  # encoded image
            decoded_image = validate_base64_image(image)  # convert to decoded image
            request.user.profile.image = decoded_image
            user.profile.image.save(f"{user.username}_profile_image.jpg", decoded_image)
        serializer = UserProfileUpdateSerializer(user, new_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            new_user_data = UserProfileGetSerializer(user)
            return Response(new_user_data.data)
        return Response(serializer.errors)


class ChangePasswordView(APIView):
    """ only put request for changing the password """
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            # early return if password doesn't match:
            if not request.user.check_password(serializer.validated_data["old_password"]):  # check if old_pass match
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            request.user.set_password(serializer.validated_data["new_password"])  # set new password
            request.user.save()
            return Response({"message": "Password updated successfully."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """ logout the user and delete his token """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.auth.delete()  # Deletes the token, effectively logging out the user
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
