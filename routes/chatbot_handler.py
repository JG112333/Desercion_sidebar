from flask import Blueprint, request, render_template, jsonify
from thefuzz import fuzz
from config import GEMINI
import google.generativeai as genai

# Crear un Blueprint para las rutas del chatbot
chatbot_bp = Blueprint('chatbot_handler', __name__)

# Configurar Gemini
genai.configure(api_key=GEMINI)
model = genai.GenerativeModel("gemini-2.0-flash")

@chatbot_bp.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    if request.method == 'POST':
        user_message = request.form['message'].lower()

        # Diccionario de respuestas predefinidas
        predefined_responses = {
            "qué es la deserción": "La deserción es el proceso por el cual los estudiantes dejan de asistir a sus estudios, abandonando su educación antes de completarla.",
            "¿Cuáles son las causas comunes de la deserción?": (
                "1. <b>Factores económicos</b>: Muchos estudiantes abandonan debido a problemas financieros.<br>"
                "2. <b>Desajustes académicos</b>: Dificultades para adaptarse a las exigencias académicas.<br>"
                "3. <b>Falta de apoyo institucional</b>: Falta de recursos o atención adecuada por parte de las instituciones educativas.<br>"
                "4. <b>Problemas personales</b>: Factores como la salud, problemas familiares o falta de motivación."
            ),
            "¿Cómo prevenir la deserción?": (
                "1. <b>Mejorar la calidad educativa</b>: Ofrecer educación accesible y relevante.<br>"
                "2. <b>Apoyo emocional</b>: Brindar atención psicológica a los estudiantes.<br>"
                "3. <b>Incentivos económicos</b>: Ayudar con becas y apoyo financiero."
            ),
             "¿Cómo funciona la aplicación?": (
                "<b>Los usuarios pueden realizar multiples funciones:</b><br>"
                "1. <b>Apartado del formulario:</b> Permite al usuario ingresar información por estudiante para ser analizada.<br>"
                "2. <b>Apartado de carga de datos masivos:</b> Permite al usuario cargar un archivo CSV o XLSX con múltiples perfiles, lo que facilita el análisis de muchos estudiantes a la vez.<br>"
                "<br>Ambos apartados son posibles gracias al modelo previamente entrenado de Machine Learning, el cual analiza cada perfil para determinar la probabilidad de deserción."
            ), 
            "¿Qué tipo de datos necesita la aplicación?": (
                "Datos académicos, socioeconómicos y demográficos como las notas, la profesión de los padres, acceso a becas, la edad y el género, etc."
            ),
            "¿Cómo funciona el modelo ml?": (
                "Nuestra app carga un modelo previamente entrenado, este modelo procesa los datos ingresados y devuelve una predicción con dos posibles resultados:<br>"
                "<b>Deserción: 'Sí' o 'No'</b><br>"
                "<br>Cada uno con su respectiva probabilidad."
            ),
            # Agregar más preguntas y respuestas aquí...
        }

        # Verificar si el mensaje coincide con una respuesta predefinida antes de llamar a la IA
        for key, response in predefined_responses.items():
            if fuzz.partial_ratio(user_message, key) >= 90:
                bot_message = response
                skip_restriction = True
                break
        else:
            skip_restriction = False

        # Si no hay respuesta predefinida, llamar a la API de IA
        if not skip_restriction:
            instructions = instructions = """
                      Por favor, responde solo en español y de manera concisa.
                      Si te saludan, tambien saluda.
                      No des rodeos y en un solo parrafo con un unico punto final o aparte.
                      Los únicos temas a los que irá enfocada tu respuesta serán en el tema de la deserción en la educación.
                      Evita respuestas largas y mantenlas claras.
                      Si la respuesta involucra ejemplos, deben ser breves y relevantes.
                      No uses tecnicismos o jerga innecesaria.
                      Mantén un tono educado y amigable.
                      Si la pregunta está muy fuera de lugar con respecto al tema de deserción en la educación, responde:
                      "<b>¡Solo preguntas relacionadas a la deserción en la educación, por favor!</b>".
                      Si la pregunta contiene palabras en otro idioma que no sea el español, o si la palabra en sí no existe, 
                      como por ejemplo, cuando hay varias vocales juntas o varias consonantes juntas, responde:
                      "<b>¡Por favor!, usa palabras en español y asegúrate de que sean correctas.</b>".
                      Si la pregunta lleva números sin sentido, responde:
                      "<b>¡Por favor!, asegúrate de que los números tengan sentido en el contexto de la pregunta.</b>"
                      """
            chat = model.start_chat()
            response = chat.send_message(f"{instructions}\n\n{user_message}")
            bot_message = response.text

        # Aplicar restricciones solo si no es una respuesta predefinida
        
        #if "." in bot_message and not skip_restriction:
        #   bot_message = bot_message.split(".")[0] + "."

       # if len(bot_message) > 300 and not skip_restriction:
           # bot_message = bot_message[:300] + "..."
     

        # Agregar un salto de línea al inicio de la respuesta
        bot_message = "<br>" + bot_message  

        return jsonify({"message": bot_message})

    return render_template('chatbot.html')

# Ruta adicional para solo renderizar el HTML del chatbot
@chatbot_bp.route('/chatbot_page', methods=['GET'])
def chatbot_page():
    return render_template('chatbot.html')