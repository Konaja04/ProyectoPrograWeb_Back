from django.contrib import admin
from .models import *
# Administradores de modelos
class UserAdmin(admin.ModelAdmin):
    list_display = ['names', 'last_names', 'email']

class ActorAdmin(admin.ModelAdmin):
    list_display = ['name']

class GeneroAdmin(admin.ModelAdmin):
    list_display = ['name']

class KeywordAdmin(admin.ModelAdmin):
    list_display = ['name']

class PeliculaAdmin(admin.ModelAdmin):
    list_display = ['title', 'year']

class CiudadAdmin(admin.ModelAdmin):
    list_display = ['name']

class VentanaAdmin(admin.ModelAdmin):
    list_display = ['date', 'hour']

class FormatoAdmin(admin.ModelAdmin):
    list_display = ['name']

class PeliculaActorAdmin(admin.ModelAdmin):
    list_display = ['pelicula', 'actor']

class PeliculaGeneroAdmin(admin.ModelAdmin):
    list_display = ['pelicula', 'genero']

class PeliculaKeywordAdmin(admin.ModelAdmin):
    list_display = ['pelicula', 'keyword']

class SalaAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone_number', 'address', 'ciudad']

class SalaFormatoAdmin(admin.ModelAdmin):
    list_display = ['sala', 'formato']
class PeliculaUsuarioAdmin(admin.ModelAdmin):
    list_display = ['pelicula', 'usuario','calificacion']

class FuncionAdmin(admin.ModelAdmin):
    list_display = ['pelicula', 'sala', 'ventana']

class ReservaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'funcion', 'asientos']

class UsuarioKeywordAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'keyword', 'peso']

class UsuarioActorAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'actor', 'peso']

class UsuarioGeneroAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'genero', 'peso']

# Registro de modelos y sus administradores
admin.site.register(User, UserAdmin)
admin.site.register(Actor, ActorAdmin)
admin.site.register(Genero, GeneroAdmin)
admin.site.register(Keyword, KeywordAdmin)
admin.site.register(Pelicula, PeliculaAdmin)
admin.site.register(Ciudad, CiudadAdmin)
admin.site.register(Ventana, VentanaAdmin)
admin.site.register(Formato, FormatoAdmin)
admin.site.register(Pelicula_Actor, PeliculaActorAdmin)
admin.site.register(Pelicula_Genero, PeliculaGeneroAdmin)
admin.site.register(Pelicula_Keyword, PeliculaKeywordAdmin)
admin.site.register(Sala, SalaAdmin)
admin.site.register(Sala_Formato, SalaFormatoAdmin)
admin.site.register(Funcion, FuncionAdmin)
admin.site.register(Reserva, ReservaAdmin)
admin.site.register(Usuario_Keyword, UsuarioKeywordAdmin)
admin.site.register(Usuario_Actor, UsuarioActorAdmin)
admin.site.register(Usuario_Genero, UsuarioGeneroAdmin)
admin.site.register(Pelicula_Usuario, PeliculaUsuarioAdmin)