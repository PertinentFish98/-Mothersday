from django.urls import path
from .views import puzzle_view, start_game

urlpatterns = [
    path('', start_game, name='start_game'),
    path('puzzle/<int:pk>/', puzzle_view, name='puzzle_view'),
]
