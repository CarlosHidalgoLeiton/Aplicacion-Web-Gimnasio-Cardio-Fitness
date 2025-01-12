from transformers import pipeline

# Inicializar el pipeline de conversación de Hugging Face
chatbot = pipeline("text-generation", model="microsoft/DialoGPT-medium")

# Respuestas de FAQ
faq_responses = {
    "hola":"Hola Cliente, un gusto saludarte en que puedo ayudarte",
    "horarios": "Nuestro gimnasio está abierto de lunes a viernes de 5:00 AM a 09:00 PM. Los sábados de 8:00 AM a 02:00 PM y los domingos de 8:00 AM a 12:00 AM.",
    "precios": "Tenemos mensualidad con un costo de ₡22 500.",
    "ubicación": "Nos encontramos en el Costado sur del Parque de Grecia, Grecia, Alajuela, 20301.",
    "contacto": "Puedes contactarnos al número +506 2444-5192 y por medio de WhatsApp 8927-5176",
}

def get_response(user_input):
    user_input_lower = user_input.lower()  

    if user_input_lower in faq_responses:
        return faq_responses[user_input_lower]
    
    response = chatbot(user_input, max_length=1000, num_return_sequences=1)
    return response[0]['generated_text']