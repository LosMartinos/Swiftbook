from django.urls import path
from .views import MyuserView

urlpatterns = [
    path('', MyuserView.as_view())
]