from rest_framework import generics
from django.contrib.auth.models import User
from .models import Provider, Service, Booking, BusinessHours
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize

def registerUserView(request):
    return 1

def loginUserView(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        name = request.POST.get('username')
        password = request.POST.get('password')

        try: 
            user = User.objects.get(name = name)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, name=name, password = password)
        if user is not None:
            login(request,user) # session will be created in db and broswer
            return redirect('home')
        else:
            messages.error(request, 'User OR password is wrong')
    context =  {} #?
    return render(request, 'templates/login.html', context)

@login_required(login_url='login')
def logoutUserView(request):
    logout(request)
    return redirect('home')

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
