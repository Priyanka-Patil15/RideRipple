from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile

class AccountTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='pass1234')
        self.profile = self.user.profile

    def test_account_web_requires_login(self):
        response = self.client.get(reverse('account-web'))
        self.assertEqual(response.status_code, 302)  # should redirect to login

    def test_account_web_success(self):
        self.client.login(username='testuser', password='pass1234')
        response = self.client.get(reverse('account-web'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    def test_personal_info_update(self):
        self.client.login(username='testuser', password='pass1234')
        response = self.client.post(reverse('account-personal-info'), {
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '1234567890',
            'city': 'TestCity'
        })

        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.profile.refresh_from_db()

        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.last_name, 'User')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.profile.phone, '1234567890')
        self.assertEqual(self.profile.city, 'TestCity')
