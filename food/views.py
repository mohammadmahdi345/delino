from django.db import IntegrityError
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from django.contrib import messages
from django.db.models import Q,Count

from user.models import Gateway
from .models import City, Food, Restorant, Order
from .serializer import RestorantSerializer, LikeSerializer, OrderGetSerializer
from delino.authentication import CustomTokenAuthentication


class Search(APIView):

    def post(self,request):
        search = request.data.get('search')
        search = Restorant.objects.filter(Q(name__icontains=search) | Q(meno__name__icontains=search))
        serializer = RestorantSerializer(search,many=True)
        return Response(serializer.data)




class RestorantView(APIView):

    def get(self,request):
        res = Restorant.objects.all()
        serializer = RestorantSerializer(res,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class RestorantDetailView(APIView):

    def get(self,request,name):
        try:
            res = Restorant.objects.get(name=name)
        except Restorant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = RestorantSerializer(res)
        return Response(serializer.data, status=status.HTTP_200_OK)
#
# class LikeView(APIView):
#     authentication_classes = [CustomTokenAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     def get(self,request,name):
#         try:
#             res = Restorant.objects.get(name=name)
#         except Restorant.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         likes = res.likes(is_liked=True).count()
#         return Response({'likes':likes})
#
#     def post(self,request,name):
#         try:
#             res = Restorant.objects.get(name=name)
#         except Restorant.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         if res.objects.filter(liked__user=request.user,liked=True):
#             return Response({'detail': 'you liked in past'}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             serializer = LikeSerializer(data=request.data)
#             if serializer.is_valid(raise_exception=True):
#                 serializer.save(user=request.user)
#                 return Response({'detail':'is liked'})
#             else:
#                 return Response(status=status.HTTP_400_BAD_REQUEST)
#
class BestSellingRestaurantsAPIView(APIView):
    def get(self, request):
        best_restaurants = Restorant.objects.annotate(order_count=Count('meno__order')).order_by('-order_count')[:10]
        serializer = RestorantSerializer(best_restaurants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Category(APIView):
    pass


class LikeView(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,name):
        try:
            res = Restorant.objects.get(name=name)
        except Restorant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        likes = res.likes.filter(is_liked=True).count()
        return Response({'likes':likes})

    def post(self,request,name):
        try:
            res = Restorant.objects.get(name=name)
        except Restorant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            serializer = LikeSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=request.user,res=res)
                return Response({'detail':'is liked'})
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response({'detail':'you liked before'},status=status.HTTP_400_BAD_REQUEST)
    # else:
    #     return Response({'detail':'you liked in past'},status=status.HTTP_400_BAD_REQUEST)


class OrderView(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,name):
        try:
            res = Restorant.objects.get(name=name)
        except Restorant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        orders = Order.objects.filter(user=request.user,status='PENDING',res=res)
        other_orders = Order.objects.filter(user=request.user,res=res).exclude(status='PENDING')
        order_data = OrderGetSerializer(orders,many=True).data
        other_order_data = OrderGetSerializer(orders, many=True).data

        return Response({'orders':order_data,
                         'other_order':other_order_data})

class PaymentView(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request,gateway_id):
        food_name = request.data.get('food_name')
        res_name = request.data.get('res_name')
        quantity = request.data.get('quantity')
        try:
            gateway = Gateway.objects.get(id=gateway_id)
            food = Food.objects.get(name=food_name)
            res = Restorant.objects.get(name=res_name)
        except (Food.DoesNotExist, Gateway.DoesNotExist, Restorant.DoesNotExist):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(user=request.user,res=res,food=food,gateway=gateway,quantity=quantity)

        return Response({'detail':'sefaresh sabt shod'},status=status.HTTP_200_OK)





