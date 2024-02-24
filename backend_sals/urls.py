from django.urls import path

from .views import *
urlpatterns = [
    path("login-json", loginPostJsonEndpoint),
    path('ver-peliculas',verPeliculas),
    path('ver-salas',verSalas),
    path('enviar-correo', enviarReserva)
]