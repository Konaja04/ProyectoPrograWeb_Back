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
from .mensaje_html import devolver_mensaje, generar_mensaje_recuperacion
from .credentials import *

import secrets
import base64

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
                "id":usuario.id,
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
@csrf_exempt
def guardarReserva(request):
    if request.method == "POST":
        data = request.body
        reservaData = json.loads(data)
        funcion = Funcion.objects.get(pk = reservaData['funcion_id'])
        usuario = User.objects.get(email = reservaData['usuario'])
        asientos = reservaData['asientos']
        nuevaReserva = Reserva(usuario = usuario, funcion = funcion, asientos = asientos)
        nuevaReserva.save()
        response  = {
            "msg": ""
        }
        return HttpResponse(json.dumps(response))

@csrf_exempt
def verUsuarioReservas(request):
    if request.method == "POST":
        data = request.body
        userData = json.loads(data)
        usuario_id = User.objects.get(email = userData['email']).pk
        funciones = list(Funcion.objects.all().values())
        peliculas = list(Pelicula.objects.all().values())
        ventanas = ventanas = [{"id":ventana['id'],"hora":ventana['hour'].strftime("%H:%M"),"fecha":ventana['date'].strftime('%Y-%m-%d')} for ventana in list(Ventana.objects.all().values())]
        reservas = [
            {
                "funcion": [
                    {
                        "pelicula": list(filter(lambda pelicula: pelicula['id'] == funcion['pelicula_id'], peliculas))[0],
                        "ventana": list(filter(lambda ventana: ventana['id'] == funcion['ventana_id'], ventanas))[0]
                    }
                    for funcion in funciones if funcion['id'] == reserva['funcion_id']
                ][0] ,
                "asientos": reserva['asientos']
            }
            for reserva in list(Reserva.objects.filter(usuario = usuario_id).values())
        ]
        response = {
            "reservas": reservas
        }
        
        return HttpResponse(json.dumps(response))
def verPelicula(request, pelicula_slug):

    if request.method == 'GET':
        pelicula = Pelicula.objects.get(path=pelicula_slug)
        actores = list(Actor.objects.all().values())
        actores = [
            [actor["name"] for actor in actores if actor["id"] == fila["actor_id"]][0]
                
            for fila in list(Pelicula_Actor.objects.all().values()) if fila["pelicula_id"] == pelicula.pk
        ]

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
                    "cast": actores,
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
    

def obtener_reservas_por_funcion(request, funcion_id):
    if request.method == 'GET':
        reservas = Reserva.objects.filter(funcion_id=funcion_id).values() 
        return HttpResponse(json.dumps(list(reservas)))


@csrf_exempt
def registrarUsuario(request):
    if request.method == "POST":
        data = request.body
        userDict = json.loads(data)

        if userDict["codigo"] == "" or userDict["password"] == "" or userDict["names"] == "" or userDict["last_names"] == "" or userDict["email"] == "" or userDict["last_names"] == "":
            errorDict = {
                "msg" : "Debe ingresar todos los datos requeridos"
            }
            return HttpResponse(json.dumps(errorDict))
        
        if userDict["img"] == "":
            userDict["img"] = "https://t3.ftcdn.net/jpg/05/16/27/58/360_F_516275801_f3Fsp17x6HQK0xQgDQEELoTuERO4SsWV.jpg"
    
        # insert user
        user = User(
            names=userDict["names"],
            last_names=userDict["last_names"],
            codigo=userDict["codigo"],
            email=userDict["email"],
            password=userDict["password"],
            img=userDict["img"]
        )
        user.save()

        respDict = {
            "msg" : ""
        }
        return HttpResponse(json.dumps(respDict))



@csrf_exempt
def enviarCorreoRecuperacion(request):
    if request.method == "POST":
        data = request.body
        userData = json.loads(data)
        usuario = 'KONAHA'
        asunto = 'RECUPERACIÓN DE CUENTA'
        destinatarios = [userData['correo']]
        
        codigo = ''.join(secrets.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for i in range(5))
        codigo_codificado = base64.urlsafe_b64encode(codigo.encode()).decode()
        
        
        mensaje  = generar_mensaje_recuperacion(codigo)

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
                    "msg":"",
                    "codigo": codigo_codificado
                }
                return HttpResponse(json.dumps(respuesta))

        except:
            print("no envie nada xd")
            respuesta = {
                "msg" : "Error en el envio de correo"
            }
            return HttpResponse(json.dumps(respuesta))


@csrf_exempt
def cambiarContraseña(request):
    if request.method == "POST":
        data = request.body
        userData = json.loads(data)

        correo = userData["correo"]
        nueva_password = userData["password"]

        try:
            usuario = User.objects.get(email = correo)
            usuario.password = nueva_password
            usuario.save()
            respuesta = {
                "msg" : ""
            }
            return HttpResponse(json.dumps(respuesta))
        except:
            respuesta = {
                "msg" : "Error en el cambio"
            }
            return HttpResponse(json.dumps(respuesta))


def cartelera(request):
    if request.method == "GET":
        funciones = [funcion['pelicula_id'] for funcion in list(Funcion.objects.all().values())]
        cartelera = [pelicula for pelicula in list(Pelicula.objects.all().values()) if pelicula['id'] in funciones ]
        return HttpResponse(json.dumps(cartelera))
def verSala(request, sala_slug):

    if request.method == 'GET':

        sala = Sala.objects.get(path=sala_slug)
        ciudad = Ciudad.objects.get(id=sala.ciudad.id)
        formato = Sala_Formato.objects.filter(sala=sala) 

        formatoDisponible = [formato.formato.name for formato in formato]

        response = {
            "id":sala.pk,
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
        ventanas = [{"id":ventana['id'],"hora":ventana['hour'].strftime("%H:%M")} for ventana in list(Ventana.objects.all().values())]
        funciones =  [
            {
                "funcion_id": funcion['id'],
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
            funcionesDispo = [{"funcion_id": funcion['funcion_id'], "hora": funcion['hora']} for funcion in funciones if funcion['pelicula_id'] == pelicula.id]
            generos = [genero['genero_name'] for genero in generosTranformado if genero['pelicula_id'] == pelicula.id ]
            if len(funcionesDispo) > 0 :
                    
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
                        "genres": generos,
                        "available_times":funcionesDispo,
                    }

                    peliculasDisponibles.append(data)

        return HttpResponse(json.dumps(peliculasDisponibles))


# @csrf_exempt
# def guardarCalificacion(request):
#     if request.method == "POST":
#         data = request.body
#         calificacionesData = json.loads(data)
#         pelicula = Pelicula.objects.get(pk = calificacionesData['pelicula_id'])
#         usuario = User.objects.get(pk = calificacionesData['usuario_id'])
#         calificacion = reservaData['calificacion']        
#         nuevaCalificacion = Pelicula_Usuario(usuario = usuario, pelicula = pelicula, calificacion = calificacion)
#         nuevaCalificacion.save()
#         response  = {
#             "msg": ""
#         }
#         return HttpResponse(json.dumps(response))
    
def definirPreferenciasUsuario(user_id):
        user_id = 4
        Usuario_Keyword.objects.filter(usuario_id=user_id).delete()
        Usuario_Genero.objects.filter(usuario_id=user_id).delete()
        Usuario_Actor.objects.filter(usuario_id=user_id).delete()
        pesoGeneros = 0.60
        pesoKeywords = 0.30
        pesoCast = 0.10

        calificaciones = list(Pelicula_Usuario.objects.filter(usuario_id = user_id).values())
        peliculas = Pelicula.objects.all()

        # peliculas_usuario_ids = list(map(lambda x: x['pelicula_id'] , calificaciones))
        peliculas_usuario = Pelicula_Usuario.objects.filter(usuario_id=user_id).values_list('pelicula_id', flat=True)

        # actoresPelis = list(
        #     filter(
        #         lambda actor: actor['pelicula__id'] in peliculas_usuario_ids ,
        #         list(Pelicula_Actor.objects.filter().values('actor__id', 'pelicula__id'))
        #     )
        # )

        # genresPelis = list(
        #     filter(
        #     lambda genero: genero['pelicula__id'] in peliculas_usuario_ids,
        #     Pelicula_Genero.objects.all().values('genero__id', 'pelicula__id')
        #     )
        # )
        
        # keywordsPelis = list(
        #     filter(
        #        lambda keyword: keyword['pelicula__id'] in peliculas_usuario_ids ,
        #     Pelicula_Keyword.objects.all().values('keyword__id','pelicula__id')
        #     )
        # )
        actoresPelis = Pelicula_Actor.objects.filter(pelicula_id__in=peliculas_usuario).values('actor_id', 'pelicula_id').distinct()
        genresPelis = Pelicula_Genero.objects.filter(pelicula_id__in=peliculas_usuario).values('genero_id', 'pelicula_id').distinct()
        keywordsPelis = Pelicula_Keyword.objects.filter(pelicula_id__in=peliculas_usuario).values('keyword_id', 'pelicula_id').distinct()

        calificacionesTransformado = [
            [   {
                "pelicula_id": pelicula.pk,
                "actores_ids": [actor['actor_id'] for actor in actoresPelis if actor['pelicula_id'] == pelicula.pk],
                "generos_ids": [genero['genero_id'] for genero in genresPelis if genero['pelicula_id'] == pelicula.pk],
                "keywords_ids": [keyword['keyword_id'] for keyword in keywordsPelis if keyword['pelicula_id'] == pelicula.pk],
                # "actores_ids": [actor['actor__id'] for actor in actoresPelis if actor['pelicula__id'] == pelicula.pk],
                # "generos_ids": [genero['genero__id'] for genero in genresPelis if genero['pelicula__id'] == pelicula.pk],
                # "keywords_ids": [keyword['keyword__id'] for keyword in keywordsPelis if keyword['pelicula__id'] == pelicula.pk],
                "calificacion": fila['calificacion']
            } 
            for pelicula in peliculas if pelicula.pk== fila['pelicula_id']
            ][0]
            for fila in calificaciones
        ]
        # actoresPelis = list({d['actor__id']: d for d in actoresPelis}.values())
        # genresPelis = list({d['genero__id']: d for d in genresPelis}.values())
        # keywordsPelis = list({d['keyword__id']: d for d in keywordsPelis}.values())
        actoresPelis = list({d['actor_id']: d for d in actoresPelis}.values())
        genresPelis = list({d['genero_id']: d for d in genresPelis}.values())
        keywordsPelis = list({d['keyword_id']: d for d in keywordsPelis}.values())



        total = 0
        preferencias_actores = []
        for actor in actoresPelis:
            sum_etiqueta = 0
            for pelicula in calificacionesTransformado:
                # if actor['actor__id'] in pelicula['actores_ids']:
                if actor['actor_id'] in pelicula['actores_ids']:
                    sum_etiqueta += pelicula['calificacion'] * pesoCast
            # preferencias_actores.append({"id": actor['actor__id'], "peso": sum_etiqueta})
            preferencias_actores.append({"id": actor['actor_id'], "peso": sum_etiqueta})
            total += sum_etiqueta

        preferencias_generos = []
        for genero in genresPelis:
            sum_etiqueta = 0
            for pelicula in calificacionesTransformado:
                # if genero['genero__id'] in pelicula['generos_ids']:
                if genero['genero_id'] in pelicula['generos_ids']:
                    sum_etiqueta += pelicula['calificacion'] * pesoGeneros
            # preferencias_generos.append({"id": genero['genero__id'], "peso": sum_etiqueta})
            preferencias_generos.append({"id": genero['genero_id'], "peso": sum_etiqueta})
            total += sum_etiqueta

        preferencias_keywords = []
        for keyword in keywordsPelis:
            sum_etiqueta = 0
            for pelicula in calificacionesTransformado:
                # if keyword['keyword__id'] in pelicula['keywords_ids']:
                if keyword['keyword_id'] in pelicula['keywords_ids']:
                    sum_etiqueta += pelicula['calificacion'] * pesoKeywords
            # preferencias_keywords.append({"id": keyword['keyword__id'], "peso": sum_etiqueta})
            preferencias_keywords.append({"id": keyword['keyword_id'], "peso": sum_etiqueta})
            total += sum_etiqueta

        #Creando data
        for preferencia in preferencias_actores:
            nuevaPreferencia = Usuario_Actor(
                usuario_id = user_id,  
                actor_id = preferencia['id'], 
                peso = preferencia['peso']/total
            )
            nuevaPreferencia.save()
        for preferencia in preferencias_generos:
            nuevaPreferencia = Usuario_Genero(
                usuario_id = user_id,  
                genero_id = preferencia['id'], 
                peso = preferencia['peso']/total
            )
            nuevaPreferencia.save()
        for preferencia in preferencias_keywords:
            nuevaPreferencia = Usuario_Keyword(
                usuario_id = user_id,  
                keyword_id = preferencia['id'], 
                peso = preferencia['peso']/total
            )
            nuevaPreferencia.save()

        return HttpResponse(json.dumps(calificacionesTransformado))



def getRecomendaciones(request, user_id):
    if request.method == 'GET':
        # data = request.body
        # user_id = json.loads(data)['user_id']
        calificaciones = list(map(lambda x: x['pelicula_id'],list(Pelicula_Usuario.objects.filter(usuario_id = user_id).values('pelicula_id'))))
        preferenciasCast = list(Usuario_Actor.objects.filter(usuario_id = user_id).values('actor__id', 'peso'))
        preferenciasGeneros = list(Usuario_Genero.objects.filter(usuario_id = user_id).values('genero__id', 'peso'))
        preferenciasKeywords = list(Usuario_Keyword.objects.filter(usuario_id = user_id).values('keyword__id', 'peso'))

        actoresPelis = list(Pelicula_Actor.objects.all().values('actor__id', 'pelicula__id'))
        genresPelis = list(Pelicula_Genero.objects.all().values('genero__id', 'pelicula__id'))
        keywordsPelis = list(Pelicula_Keyword.objects.all().values('keyword__id', 'pelicula__id'))

        peliculas = Pelicula.objects.all()
        recomendaciones = []
        for pelicula in peliculas:
            puntuacion = 0
            cast = [row['actor__id'] for row in actoresPelis if  row['pelicula__id'] == pelicula.pk]
            genres = [row['genero__id'] for row in genresPelis if  row['pelicula__id'] == pelicula.pk]
            keywords = [row['keyword__id'] for row in keywordsPelis if  row['pelicula__id'] == pelicula.pk]
            for preferencia in preferenciasCast:
                if preferencia['actor__id'] in cast:
                    puntuacion += preferencia['peso']
            for preferencia in preferenciasGeneros:
                if preferencia['genero__id'] in genres:
                    puntuacion += preferencia['peso']
            for preferencia in preferenciasKeywords:
                if preferencia['keyword__id'] in keywords:
                    puntuacion += preferencia['peso']
            data = {
                        "id":pelicula.pk,
                        "title": pelicula.title,                    
                        "year": pelicula.year,
                        "href": pelicula.href,
                        "extract": pelicula.extract,
                        "thumbnail": pelicula.thumbnail,
                        "thumbnail_width": pelicula.thumbnail_width,
                        "thumbnail_height": pelicula.thumbnail_height,
                        "path": pelicula.path,
                        "path": pelicula.path,
                        "puntuacion": puntuacion
            }
            if (puntuacion > 0):
                recomendaciones.append(data)
        recomendaciones_ordenadas = sorted(recomendaciones, key=lambda x: x['puntuacion'], reverse=True)
        response = []
        conta = 0
        for recomendacion in recomendaciones_ordenadas:
            if recomendacion['id'] not in calificaciones:
                response.append(recomendacion)
            if conta == 10:
                break
            conta += 1
        return HttpResponse(json.dumps(response))