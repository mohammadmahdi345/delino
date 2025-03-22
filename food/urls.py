from django.urls import path
from .views import RestorantDetailView, RestorantView, LikeView, Search, BestSellingRestaurantsAPIView, OrderView, \
    PaymentView

urlpatterns = [
    path('restorant/', RestorantView.as_view(), name='restorant'),
    path('restorant/<str:name>/', RestorantDetailView.as_view(), name='RestorantDetail'),
    path('likes/<str:name>/', LikeView.as_view(), name='likes'),
    path('search/', Search.as_view(), name='search'),
    path('best-restorant/', BestSellingRestaurantsAPIView.as_view(), name='poplar res'),
    path('orders/<str:name>/', OrderView.as_view(), name='orders'),
    path('payment/<int:gateway_id>/', PaymentView.as_view(), name='payments')

    # path('profile/',ProfileView.as_view(),name='profile'),
    # path('orders/',OrderView.as_view(),name='orders'),
    # path('order-detail/',OrderDetail.as_view(),name='order-detail'),
]