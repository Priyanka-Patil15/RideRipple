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
import os
import openai
import google.generativeai as genai
import requests
from dotenv import load_dotenv
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from .models import SharedRide, SharedRideInvite, check_ride_status
from django.contrib.auth.models import User
from django.utils.dateparse import parse_datetime
from .models import ChatMessage

load_dotenv()


# openai.api_key = os.getenv("openai_key")
genai.configure(api_key=os.getenv("gemini_key"))


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
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)

    if request.method == 'POST':
        data = json.loads(request.body)
        pickup = data.get('pickup')
        dropoff = data.get('dropoff')
        ride_type = data.get('ride_type')

        if not (pickup and dropoff and ride_type):
            return JsonResponse({'error': 'Missing required fields'}, status=400)

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


@login_required
def schedule_ride(request):
    if request.method == 'POST':
        scheduled_date = request.POST.get('scheduled_date')
        scheduled_time = request.POST.get('scheduled_time')

        Ride.objects.create(
            user=request.user,
            pickup="Scheduled Ride",
            dropoff="Scheduled Ride",
            ride_type="UberX",
            date=scheduled_date,
            time=scheduled_time,
            is_scheduled=True
        )

        return redirect('home')
    return render(request, 'rides/schedule_ride.html')


@login_required
def reserved_rides(request):
    rides = Ride.objects.filter(user=request.user, is_scheduled=True).order_by('-date', '-time')
    return render(request, 'rides/reserved_rides.html', {'rides': rides})


@csrf_exempt
def help_ai_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message")

            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "mistral",
                    "prompt": user_message,
                    "stream": False
                }
            )
            result = response.json()
            reply = result.get("response", "Sorry, I didn't get that.")

            return JsonResponse({"reply": reply})

        except Exception as e:
            print(f"❌ Ollama error: {e}")
            return JsonResponse({
                "reply": "There was an error with the AI.Our Agent will be connecting to this chat to help shortly!.."},
                status=500
            )

    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def create_shared_ride(request):
    if request.method == 'POST':
        pickup = request.POST.get('pickup')
        dropoff = request.POST.get('dropoff')
        scheduled_time_str = request.POST.get('scheduled_time')
        friend_ids = request.POST.getlist('friends')  # list of user IDs

        # Convert datetime string to object
        scheduled_time = parse_datetime(scheduled_time_str)

        ride = SharedRide.objects.create(
            organizer=request.user,
            pickup=pickup,
            dropoff=dropoff,
            scheduled_time=scheduled_time
        )

        for friend_id in friend_ids:
            user = User.objects.get(id=friend_id)
            SharedRideInvite.objects.create(ride=ride, invitee=user)

        return redirect('shared_ride_detail', ride.id)
    # Show form
    friends = User.objects.exclude(id=request.user.id)
    return render(request, 'rides/create_shared_ride.html', {'friends': friends})


@login_required
def shared_ride_detail(request, ride_id):
    ride = get_object_or_404(SharedRide, id=ride_id)

    # Access control
    is_invited = ride.invites.filter(invitee=request.user).exists()
    if request.user != ride.organizer and not is_invited:
        return HttpResponseForbidden("You're not allowed to view this ride.")

    # Handle Accept/Decline
    if request.method == 'POST':
        action = request.POST.get('action')
        invite = ride.invites.get(invitee=request.user)
        if action == 'accept':
            invite.accepted = True
        elif action == 'decline':
            invite.accepted = False
        invite.save()
        return redirect('shared_ride_detail', ride_id=ride.id)

    # Fetch chat history
    chat_messages = ChatMessage.objects.filter(ride=ride).select_related('sender')

    return render(
        request,
        'rides/shared_ride_detail.html',
        {
            'ride': ride,
            'chat_messages': chat_messages
        }
    )

def respond_to_invite(request, ride_id):
    ride = get_object_or_404(SharedRide, id=ride_id)
    invite = ride.invites.get(invitee=request.user)

    action = request.POST.get("action")
    if action == "accept":
        invite.accepted = True
    elif action == "decline":
        invite.accepted = False
    invite.save()

    # Check ride status after updating
    check_ride_status(ride)

    return redirect("shared_ride_detail", ride_id=ride.id)


@login_required
def my_shared_rides(request):
    organized = SharedRide.objects.filter(organizer=request.user)
    invited = SharedRide.objects.filter(invites__invitee=request.user)

    return render(request, 'rides/my_shared_rides.html', {
        'organized_rides': organized,
        'invited_rides': invited
    })
