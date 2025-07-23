from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RideForm
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from .models import Ride
from django.http import JsonResponse
import json
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime


@login_required(login_url='/login/')
def home(request):
    if request.method == 'POST':
        form = RideForm(request.POST)
        if form.is_valid():
            ride = form.save(commit=False)
            ride.user = request.user
            ride.save()
            return redirect('select-payment-method', ride_id=ride.id)
    else:
        form = RideForm()

    user = request.user
    profile = user.profile

    return render(request, 'rides/dashboard.html', {
        'form': form,
        'user': user,
        'profile': profile,
        'timestamp': datetime.now().timestamp()
    })


def confirmation(request):
    return render(request, 'rides/confirmation.html')


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'rides/register.html', {'form': form})


@login_required
def ride_history(request):
    user_rides = Ride.objects.filter(user=request.user).order_by('-requested_at')
    return render(request, 'rides/ride_history.html', {'rides': user_rides})


@csrf_exempt
def book_ride(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        pickup = data.get('pickup')
        dropoff = data.get('dropoff')
        ride_type = data.get('ride_type')

        if request.user.is_authenticated:
            Ride.objects.create(
                user=request.user,
                pickup=pickup,
                dropoff=dropoff,
                ride_type=ride_type,
            )
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'unauthenticated'}, status=401)
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def ride_confirmed(request):
    # Get latest ride by the logged-in user
    ride = Ride.objects.filter(user=request.user).order_by('-requested_at').first()
    return render(request, 'rides/confirmed.html', {'ride': ride})


@login_required
def track_ride(request, ride_id):
    ride = get_object_or_404(Ride, id=ride_id, user=request.user)
    return render(request, 'rides/track.html', {'ride': ride})

