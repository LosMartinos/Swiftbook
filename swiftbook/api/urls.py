from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginUserView, name ='Login'),
    path('logout/', views.logoutUserView, name ='Logout'),
    path('register/', views.registerUserView, name ='Register'),



    path('user-calendar/', views.userCalendarView, name='User_Calender')
]
