from django.urls import path
from .views import (UserListCreateView, UserProfileView, UserTweets,
                    ChangePasswordView, LoginView, LogoutView)

urlpatterns = [
    path('', UserListCreateView.as_view(), name='user-list-create'),
    path('<int:pk>', UserProfileView.as_view(), name='user-profile'),
    path('<int:pk>/tweets', UserTweets.as_view(), name='user-tweets'),
    path('password', ChangePasswordView.as_view(), name='change-password'),
    path('login', LoginView.as_view(), name='user-login'),
    path('logout', LogoutView.as_view(), name='user-logout'),
]
