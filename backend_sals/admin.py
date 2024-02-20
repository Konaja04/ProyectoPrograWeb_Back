from django.contrib import admin
from .models import *
# Register your models here.
class tablaPeliculaActores(admin.ModelAdmin):
    list_display = ["pelicula","actor"]
class tablaPeliculaGeneros(admin.ModelAdmin):
    list_display = ["pelicula","genero"]
class tablaPeliculaKeyword(admin.ModelAdmin):
    list_display = ["pelicula","keyword"]
admin.site.register(Pelicula)
admin.site.register(Actor)
admin.site.register(Genero)
admin.site.register(User)
admin.site.register(Keyword)
admin.site.register(Pelicula_Actor,tablaPeliculaActores)
admin.site.register(Pelicula_Genero, tablaPeliculaGeneros)
admin.site.register(Pelicula_Keyword, tablaPeliculaKeyword)