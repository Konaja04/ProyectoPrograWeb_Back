import spacy
import json
data_peliculas  = 'backend_bot/datos.json'
nlp = spacy.load("en_core_web_lg")
with open (data_peliculas, "r") as peliculas:
    try:
        data_peliculas = json.load(peliculas)
    except json.JSONDecodeError:
        print("Error al cargar el archivo JSON.")
        data_peliculas = []

def extraerData(pelicula):
    doc1 = nlp(pelicula.lower())
    plot = ""
    cast = []
    year = 0
    title = ''
    coeficiente = 0
    for peli in data_peliculas:
        doc2 = nlp(peli['title'].lower())
        similaridad = doc1.similarity(doc2)
        if similaridad > coeficiente:
            coeficiente = similaridad
            plot = peli['extract']
            year = peli['year']
            title = peli['title']
            cast = peli['cast']

    print(f"Encontré: {title} con puntuación de {coeficiente}")
    if coeficiente>0.65:
        return { 
            'cast':cast,
            'year': year,
            "plot":plot, 
            "title": title}
    else: 
        return {}