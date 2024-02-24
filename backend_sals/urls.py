from django.urls import path

from .views import *
urlpatterns = [
    path('ver-peliculas',verPeliculas),
    path('ver-salas',verSalas),
    path('ver-pelicula/<str:pelicula_slug>/', verPelicula),
    path('obtener-salas-disponibles/<int:pelicula_id>/', obtener_salas_disponibles),

]