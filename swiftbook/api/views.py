from rest_framework import generics
from django.contrib.auth.models import User
from .models import Provider, Service, Booking, BusinessHours
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.serializers import serialize
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Provider, Service, BusinessHours, Timeslot
from django.views.decorators.http import require_POST
import json
from django.core.serializers.json import DjangoJSONEncoder


def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    business_hours = []  # Fetch or define business hours here
    return render(request, 'service_detail.html', {
        'service': service,
        'business_hours_json': json.dumps(business_hours),
    })

@require_POST
def book_timeslot(request):
    timeslot_id = request.POST.get('id')
    timeslot = get_object_or_404(Timeslot, id=timeslot_id)
    if timeslot.is_free:
        timeslot.is_free = False
        timeslot.booked_by = request.user
        timeslot.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def fetch_timeslots(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    timeslots = Timeslot.objects.filter(date__range=[start, end])
    timeslots_dict = {}
    for timeslot in timeslots:
        date_str = timeslot.date.isoformat()
        if date_str not in timeslots_dict:
            timeslots_dict[date_str] = []
        timeslots_dict[date_str].append({
            'id': timeslot.id,
            'time': timeslot.time.strftime('%H:%M'),
            'is_free': timeslot.is_free,
        })
    return JsonResponse(timeslots_dict)


def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    business_hours = BusinessHours.objects.filter(provider=service.provider).order_by('day')

    # Serialize business hours to JSON, ensuring it is an empty list if no business hours are found
    business_hours_json = json.dumps(list(business_hours.values('day', 'open_time', 'close_time')), cls=DjangoJSONEncoder)

    context = {
        'service': service,
        'business_hours_json': business_hours_json,
    }
    return render(request, 'service_detail.html', context)

def offersView(request):
    return render(request, 'offers.html')

def offers(request):
    query = request.GET.get('q', '')
    page_number = request.GET.get('page', 1)
    if query:
        providers = Provider.objects.filter(name__icontains=query).order_by('name')
    else:
        providers = Provider.objects.all().order_by('name')
    paginator = Paginator(providers, 6)  # 6 results per page
    page_obj = paginator.get_page(page_number)
    
    offers = []
    for provider in page_obj.object_list:
        services = Service.objects.filter(provider=provider)
        for service in services:
            offers.append({
                'provider_name': provider.name,
                'service_name': service.name,
                'description': service.description,
                'length': service.length,
                'service_id': service.id,
            })
    
    data = {
        'offers': offers,
        'num_pages': paginator.num_pages,
    }
    return JsonResponse(data)
    

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