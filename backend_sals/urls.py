from django.urls import path

from .views import *
urlpatterns = [
    path('ver-peliculas',verPeliculas),
    path('ver-salas',verSalas),
    path('ver-pelicula/<str:pelicula_slug>/', verPelicula, name='ver_pelicula'),
]