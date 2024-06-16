from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from .serializers import UserSerializer

User = get_user_model()

# Create your views here.
class RegisterView(APIView):
    permission_classes = (permissions.AllowAny, ) #to allow users to use api

    def post(self, request):
        try:
            data = request.data #is in a dictionary

            name = data['name']
            email = data['email']
            email = email.lower()
            
            password = data['password']
            re_password = data['re_password']
            is_realtor = data['is_realtor']

            if not all([name, email, password, re_password]):
                return Response({"status": "error", "data": "Please fill in all the fields"}, status=status.HTTP_400_BAD_REQUEST)

            if is_realtor == 'True':
                is_realtor = True
            else:
                is_realtor = False


            if password == re_password:
                if len(password) >= 8:
                    if not User.objects.filter(email=email).exists():
                        if not is_realtor:
                            User.objects.create_user(name=name, email=email, password=password)
                            return Response({"status": "success", "data": "User created successfully"}, status=status.HTTP_201_CREATED)
                        else:
                            User.objects.create_realtor(name=name, email=email, password=password)
                            return Response({"status": "success", "data": "Realtor account created successfully"}, status=status.HTTP_201_CREATED)
                    else:
                        return Response({"status": "error", "error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

                else:
                    return Response({"status": "error", "error": "Passwords must be at-least 8 characters in length"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"status": "error", "error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response({"status": "error", "error": "Something went wrong when registering account"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class RetrieveUserView(APIView):
    
    def get(self, request, format=None):
        try:
            user = request.user
            user = UserSerializer(user)
            
            return Response({"status": "success", "data": user.data}, status=status.HTTP_200_OK)
        except:
            return Response({"status": "error", "error": "Something went wrong when retrieving user details"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 