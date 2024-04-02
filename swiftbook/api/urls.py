from django.urls import path
from .views import MyUserView

urlpatterns = [
    path('', MyUserView.as_view())
]