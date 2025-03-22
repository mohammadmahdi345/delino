from django.urls import path
from .views import RegisterView, GetTokenView, UserView, aer, CommentView, UpdateUserPassword

urlpatterns = [
    path('register-login/', RegisterView.as_view(), name='register-login'),
    path('verified/', GetTokenView.as_view(), name='verified'),
    path('user/', UserView.as_view(), name='user'),
    path('comments/<str:name>/', CommentView.as_view(), name='comments'),
    path('change-password/', UpdateUserPassword.as_view(), name='change-password')

    # path('profile/',ProfileView.as_view(),name='profile'),
    # path('orders/',OrderView.as_view(),name='orders'),
    # path('order-detail/',OrderDetail.as_view(),name='order-detail'),

]