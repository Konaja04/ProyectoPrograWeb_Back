from django.urls import path

from .views import mensajeEndPoint

urlpatterns = [
    path("mensaje", mensajeEndPoint)
]