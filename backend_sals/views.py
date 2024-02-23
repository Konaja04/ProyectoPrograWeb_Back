from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
import json
from .models import *


def llenarPelis(request):
    data_peliculas  = 'backend_sals/datos.json'
    with open (data_peliculas, "r") as peliculas:
        try:
            data_peliculas = json.load(peliculas)
        except json.JSONDecodeError:
            print("Error al cargar el archivo JSON.")
            data_peliculas = []
            return HttpResponse("xd")
    if request.method == 'GET':
        paths = []
        conta = 1
        for peliculaJSON in data_peliculas:
            if peliculaJSON['path'] not in paths:
                paths.append(peliculaJSON['path'])
                nuevaPeli = Pelicula(
                    title = peliculaJSON["title"],
                    year = peliculaJSON['year'],
                    href = peliculaJSON['href'],
                    extract = peliculaJSON['extract'],
                    thumbnail = peliculaJSON['thumbnail'],
                    thumbnail_width = peliculaJSON['thumbnail_width'],
                    thumbnail_height = peliculaJSON['thumbnail_height'],
                    path = peliculaJSON['path']
                )
                print(conta)
                conta+=1
                nuevaPeli.save()
        print(len(paths))
        return HttpResponse("xdsdaewf")   
            

def llenarKeyword(request):
    data_peliculas  = 'backend_sals/salida.json'
    with open (data_peliculas, "r") as peliculas:
        try:
            data_peliculas = json.load(peliculas)
        except json.JSONDecodeError:
            print("Error al cargar el archivo JSON.")
            data_peliculas = []
            return HttpResponse("xd")
    if request.method == 'GET':    
        keywords = []
        for peliculaJSON in data_peliculas:
            for keywordJSON in peliculaJSON['keywords']: 
                if keywordJSON not in keywords:
                    keywords.append(keywordJSON)
                    nuevaKeyword = Keyword(name = keywordJSON)
                    nuevaKeyword.save()
        return HttpResponse("aewfaw")
    
def llenarGeneros(request):
    data_peliculas  = 'backend_sals/datos.json'
    with open (data_peliculas, "r") as peliculas:
        try:
            data_peliculas = json.load(peliculas)
        except json.JSONDecodeError:
            print("Error al cargar el archivo JSON.")
            data_peliculas = []
            return HttpResponse("xd")
    if request.method == 'GET':    
        generos = []
        for peliculaJSON in data_peliculas:
            for generoJSON in peliculaJSON['genres']: 
                if generoJSON not in generos:
                    generos.append(generoJSON)
                    nuevoGenero= Genero(name = generoJSON)
                    nuevoGenero.save()
        return HttpResponse("gaga")

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

def llenarGenerosPeliculas(request):
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
            for genero in peliculaJSON['genres']: 
                print(conta, " ", genero)
                if Pelicula.objects.get(path = peliculaJSON['path']):
                    peliX = Pelicula.objects.get(path = peliculaJSON['path'])
                    generoX = Genero.objects.get(name = genero)
                    pxk = Pelicula_Genero(pelicula = peliX, genero = generoX)
                    pxk.save()
            print(conta)
            conta+=1
        return HttpResponse("llenadogeneros xd")

