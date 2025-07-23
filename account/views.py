from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from datetime import datetime


@login_required
def account_web(request):
    profile = request.user.profile
    return render(request, 'account/account_web.html', {
        'user': request.user,
        'profile': profile,
        'timestamp': datetime.now().timestamp()
    })


@login_required
def personal_info(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        full_name = request.POST.get('name')
        user.first_name = full_name.split()[0]
        user.last_name = ' '.join(full_name.split()[1:])
        user.email = request.POST.get('email')
        user.save()

        profile.phone = request.POST.get('phone')
        profile.city = request.POST.get('city')

        if 'profile_photo' in request.FILES:
            profile.photo = request.FILES['profile_photo']
        profile.save()

        messages.success(request, "Your profile was updated successfully!")

    return render(request, 'account/personal_info.html', {
        'user': user,
        'profile': profile,
        'timestamp': datetime.now().timestamp()
    })