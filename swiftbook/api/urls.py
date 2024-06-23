from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginUserView, name='login'),
    path('logout/', views.logoutUserView, name='logout'),
    path('register/', views.registerUserView, name='register'),
    path('offers/', views.offers, name='offers'),
    path('offersView/', views.offersView, name='offersView'),
    path('service/<int:service_id>/', views.service_detail, name='service_detail'),
    path('api/book/', views.book_timeslot, name='book_timeslot'),
    path('api/timeslots/', views.fetch_timeslots, name='fetch_timeslots'),
    path('api/weather/', views.fetch_weather_forecast, name='fetch_weather_forecast'),  # New path for fetch_weather_data
    path('user-calendar/', views.userCalendarView, name='userCalendarView'),  # New path for userCalendarView
    path('', views.homepage, name='homepage'),  # Homepage path
    path('get_map_url/<int:service_id>/', views.get_map_url, name='get_map_url'),
    path('api/user_timeslots', views.get_user_booked_timeslots, name='get_user_booked_timeslots'),
    path('reservations/', views.reservations, name="reservations"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('faq/', views.faq, name="faq"),
    path('create_offer/', views.create_offer, name='create_offer'),
    path('my_offers/', views.my_offers, name='my_offers'),
    path('delete_offer/<int:service_id>/', views.delete_offer, name='delete_offer'),
    path('api/provider_timeslots', views.provider_timeslots, name='provider_timeslots'),
    path('update_service_description', views.update_service_description, name='update_service_description'),
    path('user/update/', views.update_user, name='update-user'),
]
