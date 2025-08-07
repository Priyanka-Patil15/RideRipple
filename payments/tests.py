from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Ride

class PaymentTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='pass1234')
        self.ride = Ride.objects.create(
            user=self.user,
            pickup="Point A",
            dropoff="Point B",
            ride_type="UberX"
        )

    def test_index_page_access(self):
        response = self.client.get(reverse('payment_index'))
        self.assertEqual(response.status_code, 200)

    def test_select_payment_requires_login(self):
        response = self.client.get(reverse('select-payment', args=[self.ride.id]))
        self.assertEqual(response.status_code, 302)  # should redirect to login

    def test_select_payment_success(self):
        self.client.login(username='testuser', password='pass1234')
        response = self.client.get(reverse('select-payment', args=[self.ride.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.ride.pickup)

    def test_wallet_payment_post(self):
        self.client.login(username='testuser', password='pass1234')
        response = self.client.post(reverse('wallet_payment'), {
            'ride_id': self.ride.id
        })
        self.assertEqual(response.status_code, 302)  # Redirects to confirmation
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any("Payment successful via wallet" in str(m) for m in messages))

    def test_stripe_checkout_redirect(self):
        response = self.client.get(reverse('stripe_payment'))
        self.assertEqual(response.status_code, 302)  # Stripe redirects to hosted checkout
