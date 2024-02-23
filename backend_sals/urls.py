from django.urls import path

from .views import *
urlpatterns = [
    # path('llenarPelis',llenarPelis),
    # path('llenarKeyword',llenarKeyword),
    # path('llenarGeneros',llenarGeneros),
    # path('llenarGenerosPeliculas',llenarGenerosPeliculas),
    path('llenarKeywordPeliculas',llenarKeywordPeliculas),
]