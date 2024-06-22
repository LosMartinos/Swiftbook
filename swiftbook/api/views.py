from rest_framework import generics
from django.contrib.auth.models import User
from .models import Provider, Service, Booking, BusinessHours
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.serializers import serialize
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.forms import modelformset_factory
from .models import Provider, Service, BusinessHours, Timeslot
from django.views.decorators.http import require_POST
from .forms import ProviderForm, ServiceForm, BusinessHoursForm
import json, requests
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from urllib.parse import quote
import dicttoxml

def to_xml(data):
    xml = dicttoxml.dicttoxml(data, custom_root='response', attr_type=False)
    print(xml.decode)
    return xml.decode()

def create_response(data, response_type='json', stat=0):
    if response_type == 'application/xml':
        xml_response = to_xml(data)
        return HttpResponse(xml_response, content_type='application/xml')
    else:
        if(stat):
            return JsonResponse(data,stat)
        return JsonResponse(data)


@login_required
def my_offers(request):
    try:
        provider = Provider.objects.get(user=request.user)
        services = Service.objects.filter(provider=provider)
    except Provider.DoesNotExist:
        provider = None
        services = []

    context = {
        'provider': provider,
        'services': services,
    }

    return render(request, 'my_offers.html', context)

@login_required
def delete_offer(request, service_id):
    service = get_object_or_404(Service, id=service_id, provider__user=request.user)
    provider = get_object_or_404(Provider, id=service.provider_id, user=request.user)
    provider.delete()
    return redirect('my_offers')

@login_required
def create_offer(request):
    BusinessHoursFormSet = modelformset_factory(BusinessHours, form=BusinessHoursForm, extra=7)

    if request.method == 'POST':
        provider_form = ProviderForm(request.POST)
        service_form = ServiceForm(request.POST)
        formset = BusinessHoursFormSet(request.POST)

        if provider_form.is_valid() and service_form.is_valid() and formset.is_valid():
            provider = provider_form.save(commit=False)
            provider.user = request.user
            address = f"{provider.address}, {provider.city}, {provider.postalcode}, {provider.country}"
            geocode_api_key = settings.GOOGLE_API_KEY
            encoded_address = quote(address)
            geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={encoded_address}&key={geocode_api_key}"
            print(geocode_url)
            try:
                response = requests.get(geocode_url)
                response.raise_for_status()  # Raise an error for non-2xx responses
                location = response.json()['results'][0]['geometry']['location']
                provider.latitude = location['lat']
                provider.longitude = location['lng']
                
            except (requests.RequestException, IndexError, KeyError) as e:
                return JsonResponse({'error': 'Google API error: ' + str(e)}, status=500)
            
            provider.save()

            service = service_form.save(commit=False)
            service.provider = provider
            service.additional_fields = []  # Save additional_fields as empty
            service.save()

            for form in formset:
                business_hour = form.save(commit=False)
                business_hour.provider = provider
                business_hour.save()

            return redirect('/my_offers/')  # Redirect to a success page
        else:
            count = 1
            errors = {}
            if not provider_form.is_valid():
                errors['provider_form_errors'] = provider_form.errors
            if not service_form.is_valid():
                errors['service_form_errors'] = service_form.errors
            if not formset.is_valid():
                formset_errors = []
                for form in formset:
                    if form.errors:
                        count += 1
                        formset_errors.append(form.errors)
                        formset_errors.append(count)
                errors['formset_errors'] = formset_errors

            return JsonResponse(errors, status=400)

    else:
        provider_form = ProviderForm()
        service_form = ServiceForm()
        formset = BusinessHoursFormSet(queryset=BusinessHours.objects.none())
        DAYS_OF_WEEK = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for index, form in enumerate(formset.forms):
            form.initial = {'day': index, 'day_label': DAYS_OF_WEEK[index]}
            form.fields['day_label'].initial = DAYS_OF_WEEK[index]

    context = {
        'provider_form': provider_form,
        'service_form': service_form,
        'business_hours_formset': formset,
    }

    return render(request, 'create_offer.html', context)



def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def faq(request):
    return render(request, 'FAQ.html')

def format_duration(duration):
    total_seconds = int(duration.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f'{hours}h {minutes}m' if hours > 0 else f'{minutes}m'

def get_user_booked_timeslots(request):
    # Fetch user-specific booked timeslots for the days shown in the calendar
    user_booked_timeslots = Timeslot.objects.filter(
        booked_by=request.user,
        date__gte=request.GET.get('start_date'),  # Filter by start_date parameter from frontend
        date__lte=request.GET.get('end_date')     # Filter by end_date parameter from frontend
    ).values('id', 'date', 'time', 'service__length', 'service__provider__name', 'service__name')

    # Serialize datetime fields to ISO format and format the length
    for timeslot in user_booked_timeslots:
        timeslot['date'] = timeslot['date'].isoformat()
        timeslot['service__length'] = format_duration(timeslot['service__length'])

    return create_response({'user_booked_timeslots': list(user_booked_timeslots)}, request.META.get('HTTP_ACCEPT', 'application/json')
)

def reservations(request):
    if request.user.is_authenticated:
        return render(request, 'my_reservations.html')
    return redirect('homepage')

def get_map_url(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    maps_api_key = settings.GOOGLE_API_KEY
    map_url = f"https://maps.googleapis.com/maps/api/staticmap?center={service.provider.latitude},{service.provider.longitude}&zoom=15&size=300x300&maptype=roadmap&markers=color:red%7C{service.provider.latitude},{service.provider.longitude}&key={maps_api_key}"
    return create_response({'map_url': map_url}, request.META.get('HTTP_ACCEPT', 'application/json'))


def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    business_hours = BusinessHours.objects.filter(provider=service.provider).order_by('day')
    
    business_hours_json = json.dumps(list(business_hours.values('day', 'open_time', 'close_time')), cls=DjangoJSONEncoder)
    
    # Fetch Google Maps Static API image
    context = {
        'service': service,
        'business_hours_json': business_hours_json,
        'csrf_token': request.COOKIES.get('csrftoken'),  # Get CSRF token from cookies
    }
    return render(request, 'service_detail.html', context)

def fetch_weather_forecast(request):
    provider_id = request.GET.get('providerId')
    
    try:
        provider = Provider.objects.get(id=provider_id)
    except Provider.DoesNotExist:
        return create_response({'error': 'Provider not found'}, request.META.get('HTTP_ACCEPT', 'application/json', 404))

    
    lat = provider.latitude
    lon = provider.longitude
    api_key = settings.WEATHER_API_KEY
    
    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}"
    forecast_response = requests.get(forecast_url)
    
    if forecast_response.status_code == 200:
        forecast_data = forecast_response.json()
        forecast_list = forecast_data['list']
        
        forecast_info = []
        for forecast in forecast_list:
            forecast_info.append({
                'date': forecast['dt_txt'],
                'temperature': round(forecast['main']['temp'] - 273.15),  # Convert from Kelvin to Celsius
                'description': forecast['weather'][0]['description'],
                'icon_url': f"http://openweathermap.org/img/wn/{forecast['weather'][0]['icon']}.png"
            })
        return create_response({'forecast': forecast_info}, request.META.get('HTTP_ACCEPT', 'application/json'))
    return create_response(({'error': 'Could not fetch weather data'}, request.META.get('HTTP_ACCEPT', 'application/json',status=400)))


@login_required
@require_POST
def book_timeslot(request):
    try:
        data = json.loads(request.body)
        service_id = data.get('service_id')
        date = data.get('date')
        time = data.get('time')

        service = get_object_or_404(Service, id=service_id)
        timeslot, created = Timeslot.objects.get_or_create(
            service=service,
            date=date,
            time=time,
            defaults={'is_free': False, 'booked_by': request.user}
        )

        if not created and timeslot.is_free:
            timeslot.is_free = False
            timeslot.booked_by = request.user
            timeslot.save()

        return create_response({'success': True}, request.META.get('HTTP_ACCEPT', 'application/json'))
    except Exception as e:
        return create_response({'success': False, 'error': str(e)}, request.META.get('HTTP_ACCEPT', 'application/json'))


def fetch_timeslots(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    provider_id = request.GET.get('provider_id')
    
    # Assuming Timeslot is related to Service, and Service is related to Provider
    timeslots = Timeslot.objects.filter(service__provider_id=provider_id, date__range=[start, end])
    
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
    
    business_hours = BusinessHours.objects.filter(provider_id=provider_id)
    business_hours_dict = {}
    for hours in business_hours:
        business_hours_dict[hours.day] = {
            'open_time': hours.open_time.strftime('%H:%M'),
            'close_time': hours.close_time.strftime('%H:%M'),
        }

    return create_response({'timeslots': timeslots_dict,'business_hours': business_hours_dict}, request.META.get('HTTP_ACCEPT', 'application/json'))




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
    return create_response((data), request.META.get('HTTP_ACCEPT', 'application/json'))

    

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
            return create_response({'error': 'User not found.'}, request.META.get('HTTP_ACCEPT', 'application/json'),404)
        if calendar_type == "p":
            try:
                provider = Provider.objects.get(user=user)
            except Provider.DoesNotExist:
                return create_response({'error': 'User is not a provider.'}, request.META.get('HTTP_ACCEPT', 'application/json'),403)

            if request.user.id != provider.user.id:
                return create_response({'error': 'Unauthorized access to provider calendar.'}, request.META.get('HTTP_ACCEPT', 'application/json'),403)


            provider_bookings = Booking.objects.filter(provider=provider, start__range=[start_datetime, end_datetime])
            response = serialize('json', provider_bookings)
            return JsonResponse(response, safe=False)
            return create_response({response}, request.META.get('HTTP_ACCEPT', 'application/json'),403)


        elif calendar_type == "u": #check here if maybe friends or if profile public or whatever tf
            if request.user.id != int(userid):
                return create_response({'error': 'Unauthorized access to user calendar.'}, request.META.get('HTTP_ACCEPT', 'application/json'),403)


            user_bookings = Booking.objects.filter(user=user, start__range=[start_datetime, end_datetime])
            response = serialize('json', user_bookings)
            return JsonResponse(response, safe=False)

        else:
            return create_response({'error': 'Empty or invalid calendar type specified.'}, request.META.get('HTTP_ACCEPT', 'application/json'),400)

    else:
        return create_response({'error': 'Only GET method is allowed.'}, request.META.get('HTTP_ACCEPT', 'application/json'),405)



# Added endpoint for homepage
def homepage(request):
    return render(request, 'homepage.html')