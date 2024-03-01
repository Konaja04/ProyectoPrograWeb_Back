import json

data_peliculas  = 'backend_bot/datos.json'


with open (data_peliculas, "r") as peliculas:
    try:
        data_peliculas = json.load(peliculas)
    except json.JSONDecodeError:
        print("Error al cargar el archivo JSON.")
        data_peliculas = []


class Pelicula:
    def __init__(self, pelicula,puntuacion):
        self.pelicula = pelicula
        self.puntuacion = puntuacion

def filtrarPelis(preferencias):
    recomendaciones = []
    etiquetas_pref = [etiqueta.lower() for etiqueta in preferencias['etiquetas']]
    peliculas_filtradas = [pelicula for pelicula in data_peliculas 
        if any(
            etiqueta.lower() in (map(lambda x: x.lower(), pelicula['genres'] + pelicula['cast'] + [str(pelicula['year'])])) 
            for etiqueta in etiquetas_pref
        )
    ]
    for pelicula in peliculas_filtradas:
        puntuacion = 0
        for i in range(len(preferencias['etiquetas'])):
            generos = list(map(lambda x: x.lower(), pelicula['genres'] + pelicula['cast'] + [str(pelicula['year'])]))
            cast = list(map(lambda x: x.lower(), pelicula['cast']))
            if (preferencias['etiquetas'][i] in generos):
                puntuacion+=preferencias['pesos'][i]
    
        recomendaciones.append(Pelicula(pelicula, puntuacion))
    return recomendaciones

def recomendaciones(preferencias):
    recomendaciones = filtrarPelis(preferencias)
    
    recomendaciones_filtradas = [peli for peli in recomendaciones if peli.puntuacion >= 0.7]
    
    recomendaciones_ordenadas = sorted(recomendaciones_filtradas, key=lambda x: x.puntuacion, reverse=True)
    
    data = [{"pelicula":pelicula.pelicula, "url": ("https://konaja04.github.io/ProyectoPrograWeb_Front/#/pelicula/{}").format(pelicula.pelicula['path'])} for pelicula in recomendaciones_ordenadas[:5]]

    return data