from django.contrib.auth import login, logout
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from accounts.permissions import IsNotAuthenticated
from accounts.serializers import UserLoginSerializer, UserSerializer


class LoginAPIView(GenericAPIView):
    permission_classes = [IsNotAuthenticated]
    serializer_class = UserLoginSerializer

    @swagger_auto_schema(
        operation_summary='Login',
        operation_description='Log in and get auth token',
        responses={403: 'cant login because user already logged in ',
                   400: 'invalid credentials or not credentials provided', }
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return JsonResponse({'msg': 'successfully logged in', 'token': token.key}, status=status.HTTP_200_OK)
        return JsonResponse({'detail': 'invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class SignUpAPIView(GenericAPIView):
    permission_classes = [IsNotAuthenticated]
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_summary='Signup',
        operation_description='Create new account',
        responses={403: 'cant signup because user already logged in',
                   400: 'invalid credentials or username and email are taken'}
    )
    def post(self, request):
        self.check_permissions(request)
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return JsonResponse({'message': 'user created successfully'}, status=status.HTTP_201_CREATED)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    @swagger_auto_schema(
        operation_summary='Logout',
        operation_description='Sign out from account',
        responses={403: 'cant logout because user is not logged in'}
    )
    def post(self, request):
        logout(request)
        return JsonResponse({'message': 'successfully logged out'}, status=200)
