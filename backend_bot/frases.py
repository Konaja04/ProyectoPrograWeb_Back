import random

saludos = [
    "¡Hola, {}! ¿Cómo podemos ayudarte hoy?",
    "Buen día, {}. ¡Bienvenido a nuestro servicio!",
    "¡Hola! Espero que estés teniendo un gran día, {}.",
    "¡Qué alegría verte, {}! ¿En qué puedo asistirte?",
    "¡Saludos, {}! Estoy aquí para lo que necesites.",
    "Hola a todos, espero que estén bien.",
    "Buenas vibras para ti hoy, {}."
]

despedidas = [
    "Fue un placer ayudarte, {}. ¡Hasta la próxima!",
    "Adiós, {}. No dudes en volver si necesitas más ayuda.",
    "¡Que tengas un buen día, {}! Siempre a tu servicio.",
    "Espero haber sido de ayuda, {}. ¡Cuídate mucho!",
    "Hasta luego, {}. Recuerda que estamos aquí para ayudarte.",
    "Nos vemos pronto, {}. ¡Gracias por visitarnos!",
    "¡Adiós! Espero que tengas un excelente día.",
    "Cualquier otra cosa que necesites, aquí estaré, {}.",
    "Fue genial charlar contigo, {}. ¡Vuelve pronto!"
]

def generar_mensaje(nombre_usuario, tipo_mensaje):
    if tipo_mensaje.lower() == "saludo":
        mensaje = random.choice(saludos)
    elif tipo_mensaje.lower() == "despedida":
        mensaje = random.choice(despedidas)
    else:
        return ["Tipo de mensaje no reconocido"]
    
    return [mensaje.format(nombre_usuario)]
