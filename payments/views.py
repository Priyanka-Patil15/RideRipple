from django.contrib.auth.decorators import login_required
import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import Ride


stripe.api_key = settings.STRIPE_SECRET_KEY


def index(request):
    return render(request, 'payments/index.html')


def checkout(request):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'unit_amount': 5000,  # $50.00 in cents
                'product_data': {
                    'name': 'Ride Booking Fee',
                },
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri('/payments/success/'),
        cancel_url=request.build_absolute_uri('/payments/cancel/'),
    )
    return redirect(session.url, code=303)


def success(request):
    return render(request, 'payments/success.html')


def cancel(request):
    return render(request, 'payments/cancel.html')


@login_required
@require_POST
def wallet_pay(request):
    ride_id = request.POST.get('ride_id')
    # You can deduct from user's wallet balance here and confirm the booking
    messages.success(request, "Payment successful via wallet.")
    return redirect('confirmation')


@login_required
def select_payment_method(request, ride_id):
    ride = get_object_or_404(Ride, id=ride_id, user=request.user)
    return render(request, 'payments/select_method.html', {'ride': ride})