from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, ParseError
from rest_framework import generics
from .models import User
from tweets.models import Tweet
from tweets.serializers import TweetSerializer
from .serializers import UserSerializer
from config.authentication import UsernameAuthentication
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout


class UserTweets(APIView):
    authentication_classes = [UsernameAuthentication]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        user = self.get_object(pk)
        tweets = Tweet.objects.filter(user=user)
        serializer = TweetSerializer(tweets, many=True)
        return Response(serializer.data)


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        password = request.data.get('password')
        if password:
            user.set_password(password)
            user.save()
            return Response({"message": "Password updated successfully"},
                            status=status.HTTP_200_OK)
        return Response({"error": "Password not provided"},
                        status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):

        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            raise ParseError

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return Response({"message": "User logged in successfully"})
        else:
            return Response({"error": "Invalid credentials"},
                            status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "User logged out successfully"})
