from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
import re
from .models import create_auth_token, User
from .serializers import SignUpSerializer
from .tokens import create_jwt_pair_for_user

# Create your views here.
class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = []

    def post(self, request: Request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            print('-'*20, serializer.data)
            # Token.objects.create(user=User.objects.get(email=serializer.data.email))
            response = {
                "message": "User Created Successfully", 
                "data": serializer.data
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = []

    # /accounts/login/?format=api&next=%2Fswagger%2F
    def post(self, request: Request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)
        # next_page = request.query_params.get("next")
        if user is not None:
            tokens = create_jwt_pair_for_user(user)
            response = {
                "message": "Login Successful", 
                "tokens": tokens,
                "token_django_auth": user.auth_token.key
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request: Request):
        content = {"user": str(request.user), "auth": str(request.auth)}
        return Response(data=content, status=status.HTTP_200_OK)
