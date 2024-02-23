from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
import json
from .models import *
from datetime import datetime


def llenarKeywordPeliculas(request):
    data_peliculas  = 'backend_sals/salida.json'
    with open (data_peliculas, "r") as peliculas:
        try:
            data_peliculas = json.load(peliculas)
        except json.JSONDecodeError:
            print("Error al cargar el archivo JSON.")
            data_peliculas = []
            return HttpResponse("xd")
    if request.method == 'GET':
        for peliculaJSON in data_peliculas:
            for keywordJSON in peliculaJSON['keywords']: 
                if Pelicula.objects.get(path = peliculaJSON['path']):
                    peli = Pelicula.objects.get(path = peliculaJSON['path'])
                    keyword = Keyword.objects.get(name = keywordJSON)
                    pxk = Pelicula_Keyword(pelicula = peli, keyword = keyword)
                    pxk.save()
        return HttpResponse("ptmre")

    
def llenarActoresPeliculas(request):
    data_peliculas  = 'backend_sals/datos.json'
    with open (data_peliculas, "r") as peliculas:
        try:
            data_peliculas = json.load(peliculas)
        except json.JSONDecodeError:
            print("Error al cargar el archivo JSON.")
            data_peliculas = []
            return HttpResponse("xd")
    if request.method == 'GET':
        conta = 1
        for peliculaJSON in data_peliculas:
            for actorJSON in peliculaJSON['cast']: 
                if Pelicula.objects.get(path = peliculaJSON['path']):
                    peliX = Pelicula.objects.get(path = peliculaJSON['path'])
                    actorX = Actor.objects.get(name = actorJSON)
                    pxk = Pelicula_Actor(pelicula = peliX, actor = actorX)
                    pxk.save()
            print(conta)
            conta+=1
        return HttpResponse("llenadoActores xd")

