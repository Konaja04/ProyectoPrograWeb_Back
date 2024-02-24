from django.urls import path

from .views import *
urlpatterns = [
    path("login-json", loginPostJsonEndpoint),
    path('ver-peliculas',verPeliculas),
    path('ver-salas',verSalas),
    path('enviar-correo', enviarReserva),
    path('ver-pelicula/<str:pelicula_slug>/', verPelicula),
    path('obtener-salas-disponibles/<int:pelicula_id>/', obtener_salas_disponibles),
    path('verificar-funcion/<int:funcion_id>/', funcion_reserva),

]