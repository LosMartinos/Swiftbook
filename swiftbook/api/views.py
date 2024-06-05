from rest_framework import generics
from django.contrib.auth.models import User
from .models import Provider, Service, Booking, BusinessHours
from .serializers import UserSerializer, ProviderSerializer, ServiceSerializer, BookingSerializer, BusinessHoursSerializer
from django.http import JsonResponse
from django.core.serializers import serialize

def user_calendar(request):
    if request.method == 'GET':
        userid = request.GET.get('userid')
        start_datetime = request.GET.get('start')
        end_datetime = request.GET.get('end')

        try:
            user = User.objects.get(id=userid)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found.'}, status=404)

        user_bookings = Booking.objects.filter(user=user, start__range=[start_datetime, end_datetime])
        response = serialize('json', user_bookings)
        return JsonResponse(response, safe=False)

    else:
        return JsonResponse({'error': 'Only GET method is allowed.'}, status=405)

def provider_calendar(request): #was hat die website zur verfügung
    if request.method == 'GET':
        service_name = request.GET.get('service_name')
        start_datetime = request.GET.get('start_datetime')
        end_datetime = request.GET.get('end_datetime')
        
        # Check if the service exists
        try:
            service = Service.objects.get(name=service_name)
        except Service.DoesNotExist:
            return JsonResponse({'error': 'Service not found.'}, status=404)

        # Get the bookings for the specified service and time range
        provider_bookings = Booking.objects.filter(service=service, start__range=[start_datetime, end_datetime])

        # Serialize the bookings data
        response = serialize('json', provider_bookings)
        return JsonResponse({response})
    else:
        return JsonResponse({'error': 'Only GET method is allowed.'}, status=405)

# List and create Users
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Retrieve, update, and delete a single User
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# List and create Provider
class ProviderListCreateView(generics.ListCreateAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer

# Retrieve, update, and delete a single Provider
class ProviderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer

# List and create Service
class ServiceListCreateView(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

# Retrieve, update, and delete a single Service
class ServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

# List and create Booking
class BookingListCreateView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

# Retrieve, update, and delete a single Booking
class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

# Retrieve, update, and delete a single BusinessHours
class BusinessHoursListCreateView(generics.ListCreateAPIView):
    queryset = BusinessHours.objects.all()
    serializer_class = BusinessHoursSerializer

# Retrieve, update, and delete a single BusinessHours
class BusinessHoursDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BusinessHours.objects.all()
    serializer_class = BusinessHoursSerializer
