from django.shortcuts import render
from django.db.models import Prefetch
from django.http import HttpResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
import json
from .models import *
from datetime import datetime

   
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
        for peliculaJSON in data_peliculas:
            for actorJSON in peliculaJSON['cast']: 
                if Pelicula.objects.get(path = peliculaJSON['path']):
                    peliX = Pelicula.objects.get(path = peliculaJSON['path'])
                    actorX = Actor.objects.get(name = actorJSON)
                    pxk = Pelicula_Actor(pelicula = peliX, actor = actorX)
                    pxk.save()
        return HttpResponse("llenadoActores xd")

def verPeliculas(request):
    response = []
    if request.method == 'GET':
        peliculas = Pelicula.objects.all()

        genresPelis = list(Pelicula_Genero.objects.all().values())
        print(genresPelis)
        genres =  list(Genero.objects.all().values())

        generosTranformado = [
            {
                "pelicula_id": genero['pelicula_id'],
                "genero_name": [
                    genre['name']
                    for genre in genres 
                    if genre['id'] == genero['genero_id']
                    ][0]
            }
            for genero in genresPelis]

        for pelicula in peliculas:
            generos = [genero['genero_name'] for genero in generosTranformado if genero['pelicula_id'] == pelicula.id ]
            data = {
            "title" : pelicula.title,
            "year" : pelicula.year,
            "href": pelicula.href,
            "extract": pelicula.extract,
            "thumbnail": pelicula.thumbnail,
            "thumbnail_width": pelicula.thumbnail_width,
            "thumbnail_height": pelicula.thumbnail_width,
            "path": pelicula.path,
            "cast": [],
            "genres": generos
            }
            response.append(data)

    return HttpResponse(json.dumps(response))