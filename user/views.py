from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import redirect,HttpResponseRedirect
from django.core.cache import cache
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from django.contrib import messages

from django.shortcuts import get_object_or_404
from delino.authentication import CustomTokenAuthentication

import random

from food.models import Restorant
from user.serializer import RegisterSerializer, LoginSerializer, TokenSerializer, UserSerializer, \
    UpdatePasswordSerializer

from .models import User, Gateway
from .serializer import CommentSerializer


class RegisterView(APIView):
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            try:
                user = User.objects.get(phone_number=phone_number)
            except User.DoesNotExist:
                # user = User.objects.create_user(phone_number=phone_number)
                code = random.randint(10000, 99999)
                cache.set(str(phone_number), code, 5 * 60)
                return Response({'register-code': code})

            messages.success(request,'رمز را وارد کنید')
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                password = serializer.validated_data['password']
                if password == user.password:
                    refresh = RefreshToken.for_user(user)
                    access_token = str(refresh.access_token)
                    return Response({'detail': 'login successful',
                                     'access_token': access_token,
                                     'refresh_token': str(refresh)}, status=status.HTTP_200_OK)
                else:
                    return Response({'detail': 'password is wrong'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(serializer.errors)

class GetTokenView(APIView):

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone_number = serializer.validated_data['phone_number']
            code = serializer.validated_data['code']


            cached_code = cache.get(str(phone_number))

            if code == cached_code:
                user = User.objects.create_user(phone_number=phone_number)

                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                return Response({'detail': 'register successful',
                                 'access_token': access_token,
                                 'refresh_token': str(refresh)}, status=status.HTTP_200_OK)

            else:
                return Response({'detail':'code is wrong'},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self,request):
        user = User.objects.get(id=request.user.id)
        if user:
            serializer = UserSerializer(user,data=request.data)
            if serializer.is_valid(raise_exception=True):
                # full_name = serializer.validated_data['full_name']
                # password = serializer.validated_data['password']
                # email = serializer.validated_data['email']
                serializer.save()
                return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

def aer(request):
    print(request.user)
    print(request.user)
    return HttpResponse('fuck you')


class CommentView(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,name):
        try:
            restorant = Restorant.objects.get(name=name)
        except Restorant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        comments = restorant.comments.filter(is_approved=True)
        serializer = CommentSerializer(comments,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


    def post(self,request,name):
        restorant = Restorant.objects.get(name=name)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user,res=restorant)
            return Response({"detail":"comment is post wait to geted ok"},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UpdateUserPassword(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def put(self,request):
        user = request.user
        serializer = UpdatePasswordSerializer(user,data=request.data)

        if serializer.is_valid():
            new_password = serializer.validated_data['password']

            user.password = new_password
            user.save()
            print(user.password)
            return Response({'detail':'password change'})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)




