from django.db import models
from django.contrib import admin

class User(models.Model):
    names = models.CharField(max_length=200)
    last_names = models.CharField(max_length=200)
    codigo = models.IntegerField()
    email = models.CharField(max_length=200, unique = True)
    password = models.CharField(max_length=200)
    img = models.CharField(max_length = 400)
    def __str__(self):
        return self.names

class Actor(models.Model):
    name = models.CharField(max_length=200, unique = True)
    def __str__(self):
        return self.name

class Genero(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
    
class Keyword(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
class Pelicula(models.Model):
    title = models.CharField(max_length=200)
    year = models.IntegerField()
    href = models.CharField(max_length=200)
    extract = models.TextField()
    thumbnail = models.CharField(max_length=300)
    thumbnail_width = models.IntegerField()
    thumbnail_height = models.IntegerField()
    path = models.CharField(max_length=300, default = "the-grudge")
    def __str__(self):
        return self.title


class Ciudad(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
class Ventana(models.Model):
    date = models.DateField()
    hour = models.TimeField()

class Formato(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    
#DEBILES Y ASOCIATIVAS
class Pelicula_Actor(models.Model):
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)

class Pelicula_Genero(models.Model):
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE)


#Preferencias
class Pelicula_Keyword(models.Model):
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
class Sala(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.IntegerField()
    address = models.CharField(max_length=100)
    second_address = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    path = models.CharField(max_length=50, blank=True, null=True)
    img = models.CharField(max_length=200, blank=True, null=True)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)  # Asumiendo que hay un modelo llamado 'Ciudad'

    def __str__(self):
        return self.name
    

class Sala_Formato(models.Model):
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    formato = models.ForeignKey(Formato, on_delete=models.CASCADE)

class Funcion(models.Model):
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    ventana = models.ForeignKey(Ventana, on_delete=models.CASCADE)

class Reserva(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    funcion = models.ForeignKey(Funcion, on_delete=models.CASCADE)
    asientos = models.CharField(max_length=100)

class Usuario_Keyword(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    keyword = models.ForeignKey(Keyword, on_delete = models.CASCADE)
    peso = models.FloatField()
class Usuario_Actor(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, on_delete = models.CASCADE)
    peso = models.FloatField()
class Usuario_Genero(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    genero = models.ForeignKey(Genero, on_delete = models.CASCADE)
    peso = models.FloatField()
class Pelicula_Usuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    pelicula = models.ForeignKey(Pelicula, on_delete = models.CASCADE)
    calificacion = models.FloatField()

