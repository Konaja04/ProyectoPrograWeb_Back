from django.urls import path

from .views import *
urlpatterns = [
    
    path("login-json", loginPostJsonEndpoint),
    path('ver-peliculas',verPeliculas),
    path('ver-salas',verSalas),
    path('enviar-correo', enviarReserva),

    path('ver-pelicula/<str:pelicula_slug>/', verPelicula),
    path('obtener-salas-disponibles/<int:pelicula_id>/', obtener_salas_disponibles),

    path('ver-sala/<str:sala_slug>/', verSala),
    path('obtener_peliculas_disponibles/<int:sala_id>/', obtener_peliculas_disponibles),

    path('verificar-funcion/<int:funcion_id>/', funcion_reserva),

]