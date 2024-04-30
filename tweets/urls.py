from django.urls import path
from . import views

urlpatterns = [
    path("", views.Tweets.as_view(), name="tweets-list"),
    path("<int:pk>", views.TweetDetail.as_view(), name="tweet-detail"),
]
