from django.urls import path
from .views import (
    UserListCreateView, UserDetailView,
    AnbieterListCreateView, AnbieterDetailView,
    DienstleistungListCreateView, DienstleistungDetailView,
    BuchungListCreateView, BuchungDetailView
)

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('anbieter/', AnbieterListCreateView.as_view(), name='anbieter-list-create'),
    path('anbieter/<int:pk>/', AnbieterDetailView.as_view(), name='anbieter-detail'),
    path('dienstleistungen/', DienstleistungListCreateView.as_view(), name='dienstleistung-list-create'),
    path('dienstleistungen/<int:pk>/', DienstleistungDetailView.as_view(), name='dienstleistung-detail'),
    path('buchungen/', BuchungListCreateView.as_view(), name='buchung-list-create'),
    path('buchungen/<int:pk>/', BuchungDetailView.as_view(), name='buchung-detail'),
]
