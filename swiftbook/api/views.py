from rest_framework import generics
from django.contrib.auth.models import User
from .models import Provider, Service, Booking, BusinessHours
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.serializers import serialize

def registerUserView(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, 'An error occurred duing registration')

    return render(request, 'login_register.html', {'form': form})


def loginUserView(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('homepage')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # session will be created in db and browser
            return redirect('homepage')
        else:
            try:
                User.objects.get(username=username)
                messages.error(request, 'Password is incorrect')
            except User.DoesNotExist:
                messages.error(request, 'User does not exist')

    context = {'page': page}
    return render(request, 'login_register.html', context)

@login_required(login_url='login')
def logoutUserView(request):
    logout(request)
    return redirect('homepage')

@login_required(login_url='login')
def userCalendarView(request):

    if request.method == 'GET':
        userid = request.GET.get('userid')
        start_datetime = request.GET.get('start')
        end_datetime = request.GET.get('end')
        calendar_type = request.GET.get('type')  # 'p' = provider and 'u' = user

        try:
            user = User.objects.get(id=userid)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found.'}, status=404)

        if calendar_type == "p":
            try:
                provider = Provider.objects.get(user=user)
            except Provider.DoesNotExist:
                return JsonResponse({'error': 'User is not a provider.'}, status=403)
            
            if request.user.id != provider.user.id:
                return JsonResponse({'error': 'Unauthorized access to provider calendar.'}, status=403)

            provider_bookings = Booking.objects.filter(provider=provider, start__range=[start_datetime, end_datetime])
            response = serialize('json', provider_bookings)
            return JsonResponse(response, safe=False)

        elif calendar_type == "u": #check here if maybe friends or if profile public or whatever tf
            if request.user.id != int(userid):
                return JsonResponse({'error': 'Unauthorized access to user calendar.'}, status=403)

            user_bookings = Booking.objects.filter(user=user, start__range=[start_datetime, end_datetime])
            response = serialize('json', user_bookings)
            return JsonResponse(response, safe=False)

        else:
            return JsonResponse({'error': 'Empty or invalid calendar type specified.'}, status=400)

    else:
        return JsonResponse({'error': 'Only GET method is allowed.'}, status=405)





# Added endpoint for homepage
def homepage(request):
    return render(request, 'homepage.html')