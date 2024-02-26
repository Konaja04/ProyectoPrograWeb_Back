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
    path('obtener-reservas/<int:funcion_id>/', obtener_reservas_por_funcion),
    path('guardarReserva', guardarReserva),
    path('verReservas', verUsuarioReservas),
    path('register', registrarUsuario),
    path('enviarCorreoRecuperacion', enviarCorreoRecuperacion),
    path('cambiarPassword', cambiarContraseña),
    path('cartelera', cartelera),
    path('guardarCalificacion', guardarCalificacion)


]