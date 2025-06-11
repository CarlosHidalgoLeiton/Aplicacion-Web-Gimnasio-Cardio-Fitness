from flask import Flask, request, jsonify

app = Flask(__name__)

faq_responses = {
    "hola": "Hola Cliente, un gusto saludarte. ¿En qué puedo ayudarte?",
    "horarios": "Nuestro gimnasio está abierto de lunes a viernes de 5:00 AM a 09:00 PM. Los sábados de 8:00 AM a 02:00 PM y los domingos de 8:00 AM a 12:00 AM.",
    "precios": "Tenemos mensualidad con un costo de ₡22 500.",
    "ubicación": "Nos encontramos en el Costado sur del Parque de Grecia, Grecia, Alajuela, 20301.",
    "contacto": "Puedes contactarnos al número +506 2444-5192 y por medio de WhatsApp 8927-5176",
}

def generate_bot_response(user_input):
    faq_responses = {
        "hola": "Hola Cliente, un gusto saludarte. ¿En qué puedo ayudarte?",
        "horarios": "Nuestro gimnasio está abierto de lunes a viernes de 5:00 AM a 09:00 PM. Los sábados de 8:00 AM a 02:00 PM y los domingos de 8:00 AM a 12:00 AM.",
        "precios": "Tenemos mensualidad con un costo de ₡22 500.",
        "ubicación": "Nos encontramos en el Costado sur del Parque de Grecia, Grecia, Alajuela, 20301.",
        "contacto": "Puedes contactarnos al número +506 2444-5192 y por medio de WhatsApp 8927-5176",
    }

    user_input = user_input.lower()
    for keyword, response in faq_responses.items():
        if keyword in user_input:
            return response

    return "Lo siento, no entendí tu pregunta. ¿Podrías intentarlo de nuevo?"