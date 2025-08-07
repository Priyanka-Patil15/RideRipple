from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Ride
from datetime import datetime, timedelta
import json


class RideRippleTestSuite(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='pass1234')

    def test_homepage_redirects_without_login(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)  # redirect to login

    def test_homepage_with_login(self):
        self.client.login(username='testuser', password='pass1234')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_ride_model_creation(self):
        ride = Ride.objects.create(
            user=self.user,
            pickup="A",
            dropoff="B",
            ride_type="UberX",
            date=datetime.now().date() + timedelta(days=1),
            time=datetime.now().time()
        )
        self.assertEqual(ride.pickup, "A")
        self.assertEqual(ride.dropoff, "B")
        self.assertEqual(ride.ride_type, "UberX")

    def test_booking_requires_login(self):
        response = self.client.post(reverse('book-ride'), content_type='application/json', data={
            "pickup": "A", "dropoff": "B", "ride_type": "UberX"
        })
        self.assertEqual(response.status_code, 401)

    def test_schedule_ride_get_view(self):
        self.client.login(username='testuser', password='pass1234')
        response = self.client.get(reverse('schedule_ride'))
        self.assertEqual(response.status_code, 200)

    def test_ride_booking_with_missing_data(self):
        self.client.login(username='testuser', password='pass1234')
        response = self.client.post(
            reverse('book-ride'),
            content_type='application/json',
            data=json.dumps({  # Missing pickup/dropoff
                'ride_type': 'UberX'
            })
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing required fields", response.json().get("error", ""))

    def test_booking_with_empty_fields(self):
        # Missing ride_type
        self.client.login(username='testuser', password='pass1234')
        response = self.client.post(
            reverse('book-ride'),
            data=json.dumps({
                "pickup": "A",
                "dropoff": "B",
                "ride_type": ""  # empty ride type
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing required fields", response.json().get("error", ""))

    def test_booking_unauthenticated(self):
        # Try booking without login
        response = self.client.post(
            reverse('book-ride'),
            data=json.dumps({
                "pickup": "Central Park",
                "dropoff": "Times Square",
                "ride_type": "UberX"
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json().get("error"), "Authentication required")