import spacy
import re
from .generos import generos_es, traducciones_generos
import json
from django.urls import path
from .recomendaciones import recomendaciones
from .extraerData import extraerData
from .frases import generar_mensaje
nlp = spacy.load("es_core_news_lg")
regex_año = r'\b\d{4}\b'

class Etiqueta:
    def __init__(self, etiqueta, tipo):
        self.etiqueta = etiqueta
        self.tipo = tipo

def analizarTexto(texto):
    doc = nlp(texto)
    intenciones = {
        "generos": [],
        "actores": [],
        "años": [],
        "otros": []
    }

    palabras_texto = texto.lower().split()
    def encontrar_generos_similares(generos_es, umbral=0.7):
        generos_similares = []
        for genero in generos_es:
            doc_genero = nlp(genero)
            for token in palabras_texto:
                doc_text = nlp(token)
                similaridad = doc_text.similarity(doc_genero)
                if similaridad > umbral:
                    generos_similares.append(genero)
        
        print(generos_similares)
        return list(generos_similares)
    

    generos_aux = encontrar_generos_similares(generos_es)
    
    intenciones["generos"] = [traducciones_generos[genero].lower() for genero in generos_aux]


    intenciones['años'] = re.findall(regex_año, texto)
    for ent in doc.ents:
        if ent.label_ == "PER":
            intenciones["actores"].append(ent.text.lower())

    
    etiquetas = []
    etiquetas += intenciones["generos"]
    etiquetas += intenciones["actores"]
    etiquetas += intenciones["años"]
    
    pesos = [1/len(etiquetas)] * len(etiquetas) if etiquetas else []
    return {"etiquetas": etiquetas, "pesos": pesos}

def definirIntencion(texto):
    nlp_intenciones = spacy.load("backend_bot/modelo_intenciones")
    doc = nlp_intenciones(texto)
    max_score = -1.0
    max_label = ""

    for label, score in doc.cats.items():
        if score > max_score:
            max_score = score
            max_label = label

    # if max_label:  
    #     print(f"Etiqueta con mayor puntuación: {max_label}: {max_score:.4f}")
    # else:
    #     print("No se encontraron etiquetas con puntuaciones significativas.")
    return max_label



def extraerNombrePeli(texto):
    doc = nlp(texto)
    peli  = ""
    for ent in doc.ents:
        peli = ent.text
        print('ents = ',ent.text)
    if peli == "":
        for token in doc:
            if token.pos_ == "PROPN":
                peli = token.text
                print('token = ',token.text, "label: ", token.pos_)
        
    return peli

def ejecutarResponse(texto, user):
    intencion = definirIntencion(texto)
    if intencion == 'recomendacion':
        parametros = analizarTexto(texto)
        print(parametros)
        data = recomendaciones(parametros)
        print(data)
        response = []
        for pelicula in data:
            text = "- "+pelicula['pelicula']['title'] + ' ('+str(pelicula['pelicula']['year'])+')'
            response.append(text)
            url = pelicula['url']
            response.append(url)
        if response:
            response.insert(0,"Encontre estos resultados que pueden adecuarse a tu solicitud...")
            return response
        else:
            return ["No encontre nada que se acomode a tu solicitud"]
    elif intencion == 'agradecimiento':
        mensaje = generar_mensaje(user, "despedida")
        return mensaje

    elif intencion == 'saludo':
        mensaje = generar_mensaje(user, intencion)
        return mensaje


    elif intencion == 'actores':
        peli = extraerNombrePeli(texto)
        data = extraerData(peli)
        if data:
            text = 'Claro que si {} te mostrare los actores de {} en seguida'
            return [text.format(user,data['title']),str(data["cast"])]
        else:
            return ["No he encontrado resultados para tu solicitud, prueba con otra cosa"]


    elif intencion == 'plot': 
        peli = extraerNombrePeli(texto)
        data = extraerData(peli)
        if data:
            print(data['plot'])
            return [data['plot']]
        else:
            return ["No he encontrado resultados para tu solicitud, prueba con otra cosa"]

    elif intencion == 'fecha_lanzamiento': 
        peli = extraerNombrePeli(texto)
        data = extraerData(peli)
        if data:
            print(data['year'])
            return [data['year']]
        else:
            print("No he encontrado resultados para tu solicitud, prueba con otra cosa")
            return ["No he encontrado resultados para tu solicitud, prueba con otra cosa"]

    elif intencion == 'despedida':
        mensaje = generar_mensaje(user, intencion)
        return mensaje
        
    else: 
        return ['No pude identificar tu solicitud, trata de otra forma']

def main():
    print('Hola, soy tu asistente personalizado. ¿En qué puedo ayudarte el día de hoy?')
    texto = 'Cuando estreno Chemichal Hearts'
    ejecutarResponse(texto, "usuario")


if __name__ == '__main__':
    main()
