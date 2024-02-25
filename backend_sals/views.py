from django.shortcuts import render
from django.db.models import Prefetch
from django.http import HttpResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
import json
from .models import *
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .mensaje_html import devolver_mensaje
from .credentials import *
def verPeliculas(request):
    response = []
    if request.method == 'GET':
        peliculas = Pelicula.objects.all()

        genresPelis = list(Pelicula_Genero.objects.all().values())
        # print(genresPelis)
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

def verSalas(request):
    response = []
    if request.method == 'GET':
        salas = Sala.objects.all()
        ciudades =  list(Ciudad.objects.all().values())
        ventanas = [{"id":ventana['id'],"hora":ventana['hour'].strftime("%H:%M")} for ventana in list(Ventana.objects.all().values())]
        funciones =  [
            {
                "sala_id": funcion['sala_id'],
                "hora": [ ventana['hora'] for ventana in ventanas if ventana['id'] == funcion['ventana_id']][0]
            } 
            for funcion in list(Funcion.objects.all().values())
        ]
        for sala in salas:
            ciudad = [ciudad['name'] for ciudad in ciudades if ciudad['id'] == sala.ciudad]
            funcionesDispo = [funcion['hora'] for funcion in funciones if funcion['sala_id'] == sala.pk]
            data = {
                "name": sala.name,
                "phone_number": sala.phone_number ,
                "address": sala.address ,
                "second_address": sala.second_address,
                "description": sala.description,
                "path": sala.path,
                "img": sala.img,
                "ciudad": ciudad,
                "available_times": funcionesDispo
            }
            response.append(data)

    return HttpResponse(json.dumps(response))

@csrf_exempt
def loginPostJsonEndpoint(request):
    if request.method == "POST":
        data = request.body
        userData = json.loads(data)

        codigo = userData["codigo"]
        password = userData["password"]

        # Interactuamos con la bd mediante el modelo (Query)
        listaUsuariosFiltrada = User.objects.filter(
            codigo=codigo, password=password
        )

        if len(listaUsuariosFiltrada) > 0 :
            usuario = listaUsuariosFiltrada[0]
            respuesta = {
                "msg" : "",
                "names": usuario.names,
                "last_names": usuario.last_names,
                "mail": usuario.email,
                "img": usuario.img
            }
            return HttpResponse(json.dumps(respuesta))
        else :
            respuesta = {
                "msg" : "Error en el login"
            }
            return HttpResponse(json.dumps(respuesta))


@csrf_exempt
def enviarReserva(request):
    if request.method == "POST":
        data = request.body
        msgData = json.loads(data)
        print(msgData)
        usuario = 'KONAHA'
        asunto = 'Confirmacion de Reserva'
        destinatarios = [msgData['correo']]
        mensaje  = devolver_mensaje(msgData)

        msg = MIMEMultipart('alternative')
        msg['From'] = usuario
        msg['To'] = ', '.join(destinatarios)
        msg['Subject'] = asunto
        msg.attach(MIMEText(mensaje, 'html'))

        try: 
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(USER_MAIL, PASSWORD)
                server.sendmail(USER_MAIL, destinatarios, msg.as_string())
                print('Correo enviado')
                respuesta = {
                   "msg" : "Error en el login"
                }
                return HttpResponse(json.dumps(respuesta))

        except:
            print("no envie nada xd")
            respuesta = {
                "msg" : "Error en el envio de correo"
            }
            return HttpResponse(json.dumps(respuesta))

def verPelicula(request, pelicula_slug):

    if request.method == 'GET':
        pelicula = Pelicula.objects.get(path=pelicula_slug)

        genresPelis = Pelicula_Genero.objects.filter(pelicula=pelicula).values('genero__name')

        generos = [genero['genero__name'] for genero in genresPelis]
        data = {
                    "id":pelicula.id,
                    "title": pelicula.title,
                    "year": pelicula.year,
                    "href": pelicula.href,
                    "extract": pelicula.extract,
                    "thumbnail": pelicula.thumbnail,
                    "thumbnail_width": pelicula.thumbnail_width,
                    "thumbnail_height": pelicula.thumbnail_height,
                    "path": pelicula.path,
                    "cast": [],
                    "genres": generos
                }


        return HttpResponse(json.dumps(data))

def obtener_salas_disponibles(request, pelicula_id):
    if request.method == 'GET':
        
        salas = Sala.objects.all()    
        ventanas = [{"id":ventana['id'],"hora":ventana['hour'].strftime("%H:%M")} for ventana in list(Ventana.objects.all().values())]
        
        
        funciones =  [
            {
                "funcion_id": funcion['id'],   
                "sala_id": funcion['sala_id'],
                "hora": [ ventana['hora'] for ventana in ventanas if ventana['id'] == funcion['ventana_id']][0]
            } 
            for funcion in list(Funcion.objects.filter(pelicula_id=pelicula_id).values())
        ]

        salas_disponibles = [] 
        
        for sala in salas:
                funcionesDispo =[{"funcion_id": funcion['funcion_id'], "hora": funcion['hora']} for funcion in funciones if funcion['sala_id'] == sala.pk]
                
                if len(funcionesDispo) > 0 :
                        
                    data = {
                        "name":sala.name,
                        "phone_number":sala.phone_number ,
                        "address": sala.address ,
                        "second_address": sala.second_address,
                        "description":sala.description,
                        "path":sala.path,
                        "img":sala.img,
                        "available_times":funcionesDispo,
                    }

                    salas_disponibles.append(data)

    return HttpResponse(json.dumps(salas_disponibles))


def funcion_reserva(request, funcion_id):
    if request.method == 'GET':
        
        peliculas = list(Pelicula.objects.all().values())
        salas = list(Sala.objects.all().values())
        ventanas = list(Ventana.objects.all().values())

        funcion =  [
            {
                "pelicula": [pelicula for pelicula in peliculas if pelicula["id"]== funcion["pelicula_id"]] [0],
                "sala": [sala for sala in salas if sala["id"]== funcion["sala_id"]] [0],
                "ventana": [ {"id":ventana['id'],"hora":ventana['hour'].strftime("%H:%M"),"fecha":ventana['date'].strftime('%Y-%m-%d')} for ventana in ventanas if ventana["id"] == funcion["ventana_id"]] [0],
            } 

            for funcion in list(Funcion.objects.filter(id=funcion_id).values())
        ]

        if len(funcion) > 0:
            respuesta = {
                "msg":"",
                "data": funcion[0]
            }
            
        else :
            respuesta = {
                "msg" : "No existe"
            }
        
        return HttpResponse(json.dumps(respuesta))


def verSala(request, sala_slug):

    if request.method == 'GET':

        sala = Sala.objects.get(path=sala_slug)
        ciudad = Ciudad.objects.get(id=sala.ciudad.id)
        formato = Sala_Formato.objects.filter(sala=sala) 

        formatoDisponible = [formato.formato.name for formato in formato]

        response = {
            "name": sala.name,
            "phone_number": sala.phone_number,
            "address": sala.address,
            "second_address": sala.second_address,
            "description": sala.description,
            "path": sala.path,
            "img": sala.img,
            "ciudad": ciudad.name,
            "formats": formatoDisponible,
        }

    
    return HttpResponse(json.dumps(response))    

def obtener_peliculas_disponibles(request, sala_id):
    if request.method == 'GET':
        
        peliculas = Pelicula.objects.all()
        salas = list(Sala.objects.all().values())
        ventanas = [{"id":ventana['id'],"hora":ventana['hour'].strftime("%H:%M")} for ventana in list(Ventana.objects.all().values())]
        funciones =  [
            {
                "sala_id": funcion['sala_id'],
                "hora": [ ventana['hora'] for ventana in ventanas if ventana['id'] == funcion['ventana_id']][0],
                "pelicula_id": funcion['pelicula_id'],
            }
            for funcion in list(Funcion.objects.filter(sala_id=sala_id).values())
        ]

        genresPelis = list(Pelicula_Genero.objects.all().values())
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

        peliculasDisponibles = []

        for pelicula in peliculas: 
            funcionesDispo = [funcion['hora'] for funcion in funciones if funcion['pelicula_id'] == pelicula.id]
            generos = [genero['genero_name'] for genero in generosTranformado if genero['pelicula_id'] == pelicula.id ]
            if len(funcionesDispo) > 0 :
                    
                    data = {
                        "id":pelicula.id,
                        "title": pelicula.title,
                        # "year": pelicula.year,
                        # "href": pelicula.href,
                        # "extract": pelicula.extract,
                        # "thumbnail": pelicula.thumbnail,
                        # "thumbnail_width": pelicula.thumbnail_width,
                        # "thumbnail_height": pelicula.thumbnail_height,
                        # "path": pelicula.path,
                        # "cast": [],
                        # "genres": generos,
                        "available_times":funcionesDispo,
                    }

                    peliculasDisponibles.append(data)

        return HttpResponse(json.dumps(peliculasDisponibles))