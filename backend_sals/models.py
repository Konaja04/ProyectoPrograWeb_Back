from django.db import models
from django.contrib import admin

class User(models.Model):
    names = models.CharField(max_length=200)
    last_names = models.CharField(max_length=200)
    email = models.CharField(max_length=200, unique = True)
    password = models.CharField(max_length=200)
    img = models.CharField(max_length = 300, unique = True)
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

class Pelicula_Actor(models.Model):
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)

class Pelicula_Genero(models.Model):
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE)

class Pelicula_Keyword(models.Model):
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)

class Usuario_Keyword(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    keyword = models.ForeignKey(Keyword, on_delete = models.CASCADE)
    peso = models.FloatField()
