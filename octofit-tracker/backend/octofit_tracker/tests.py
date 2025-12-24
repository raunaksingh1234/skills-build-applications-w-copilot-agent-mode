from django.test import TestCase
from .models import User, Team, Activity, Workout, Leaderboard
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from datetime import date

class OctofitTrackerModelTests(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name='Test Team', description='A test team')
        self.user = User.objects.create(name='Test User', email='test@example.com', team=self.team)
        self.activity = Activity.objects.create(user=self.user, activity_type='Running', duration=30, date=date.today())
        self.workout = Workout.objects.create(name='Test Workout', description='A test workout')
        self.workout.suggested_for.set([self.team])
        self.leaderboard = Leaderboard.objects.create(team=self.team, points=100)

    def test_team_str(self):
        self.assertEqual(str(self.team), 'Test Team')
    def test_user_str(self):
        self.assertEqual(str(self.user), 'Test User')
    def test_activity_str(self):
        self.assertIn('Running', str(self.activity))
    def test_workout_str(self):
        self.assertEqual(str(self.workout), 'Test Workout')
    def test_leaderboard_str(self):
        self.assertIn('Test Team', str(self.leaderboard))

class OctofitTrackerAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.team = Team.objects.create(name='API Team', description='API test team')
        self.user = User.objects.create(name='API User', email='api@example.com', team=self.team)

    def test_api_root(self):
        response = self.client.get(reverse('api-root'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_team_list(self):
        response = self.client.get('/api/teams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_user_list(self):
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
