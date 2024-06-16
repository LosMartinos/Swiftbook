from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginUserView, name ='login'),
    path('logout/', views.logoutUserView, name ='logout'),
    path('register/', views.registerUserView, name ='register'),
    path('offers/', views.offers, name="offers"),
    path('offersView/', views.offersView, name='offersView'),
    path('service/<int:service_id>/', views.service_detail, name='service_detail'),
    path('api/book/', views.book_timeslot, name='book_timeslot'),
    path('api/timeslots/', views.fetch_timeslots, name='fetch_timeslots'),

    path('user-calendar/', views.userCalendarView, name='User_Calender'),



    # Added new path for homepage
    path('', views.homepage, name='homepage'),
]
