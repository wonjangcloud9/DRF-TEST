from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Tweet
from users.models import User


class TweetsAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        Tweet.objects.create(payload='First tweet', user=self.user)
        Tweet.objects.create(payload='Second tweet', user=self.user)

    def test_get_all_tweets(self):
        url = reverse('tweets-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_post_new_tweet(self):
        url = reverse('tweets-list')
        data = {'payload': 'Hello world!', 'username': self.user.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tweet.objects.count(), 3)

    def test_tweet_detail(self):
        tweet = Tweet.objects.first()
        url = reverse('tweet-detail', args=[tweet.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['payload'], tweet.payload)

    def test_update_tweet(self):
        tweet = Tweet.objects.first()
        url = reverse('tweet-detail', args=[tweet.id])
        data = {'payload': 'Updated content', 'id': self.user.id}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tweet.refresh_from_db()
        self.assertEqual(tweet.payload, 'Updated content')

    def test_delete_tweet(self):
        tweet = Tweet.objects.first()
        url = reverse('tweet-detail', args=[tweet.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Tweet.objects.count(), 1)
