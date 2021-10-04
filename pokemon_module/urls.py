from django.contrib import admin
from django.urls import path, include
from pokemon_module.views import PokemonAPIView
urlpatterns = [
    path('', PokemonAPIView.as_view(), name='pokemon_list'),
    path('<int:pk>', PokemonAPIView.as_view(), name='pokemon_list'),
]