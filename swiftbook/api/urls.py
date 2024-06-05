from django.urls import path
from .views import (
    UserListCreateView, UserDetailView,
    ProviderListCreateView, ProviderDetailView,
    ServiceListCreateView, ServiceDetailView,
    BookingListCreateView, BookingDetailView,
    user_calendar, provider_calendar
)

urlpatterns = [
    path('user-calendar/', user_calendar, name='user_calender'),
    path('provider-calendar/', provider_calendar, name='provider_calendar'),
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('provider/', ProviderListCreateView.as_view(), name='anbieter-list-create'),
    path('provider/<int:pk>/', ProviderDetailView.as_view(), name='anbieter-detail'),
    path('service/', ServiceListCreateView.as_view(), name='dienstleistung-list-create'),
    path('service/<int:pk>/', ServiceDetailView.as_view(), name='dienstleistung-detail'),
    path('booking/', BookingListCreateView.as_view(), name='buchung-list-create'),
    path('booking/<int:pk>/', BookingDetailView.as_view(), name='buchung-detail'),
]
