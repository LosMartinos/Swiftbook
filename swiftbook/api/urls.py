from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginUserView, name ='login'),
    path('logout/', views.logoutUserView, name ='logout'),
    path('register/', views.registerUserView, name ='register'),
    
    path('user-calendar/', views.userCalendarView, name='User_Calender'),



    # Added new path for homepage
    path('', views.homepage, name='homepage'),
]
