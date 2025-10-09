

import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

#esto sirve para cargar un archivo del env, sirve para ocultar apis y cosas que no interesa subir
load_dotenv()

#aqui le pasamos la api key de la ia en cuestion al cliente
client = InferenceClient(token=os.getenv("HUGGINGFACE_API_KEY"))

# Esta funcion es para usar HuggingFace, una ia limitada pero gratuita.
# Cada IA tiene su estructura que puedes encontrar en la documentacion.
def create_simple_task_Hugging(description):

    #si la api esta mal montada return error    
    if not client.token:
        return ["Error: la Api no esta bien montada"]
    
    #prueba a hacer:
    try:
        #prompt de lo que quieres hacer
        prompt = f"""Desglosa la siguiente tarea compleja en una lista de 3 a 5 subtareas simples y accesibles.

        Tarea: {description}
        
        Formato de respuesta:
            - Una frase breve que describa la primera subtarea
            - Otra frase breve para la siguiente subtarea
            - Continúa igual hasta completar la lista

        No incluyas numeración ni la palabra "Subtarea".
        Responde solo con la lista, una línea por subtarea, cada una empezando con un guion (-). El idioma de respuesta siempre tiene que ser castellano (español de españa)
        """

        params = {
            "model": "mistralai/Mistral-7B-Instruct-v0.2",
            "messages": [
                {
                    "role": "system",
                    "content": "Eres un asistente experto en gestion de tareas que ayuda a dividir tareas complejas en pasos simples y accionables"
                },
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 300,
            "temperature": 0.7,
            "top_p": 0.9
        }

        response = client.chat.completions.create(**params)

        content= response.choices[0].message.content.strip()

        subtasks = []

        #desmontamos la respuesta en varias tareas
        for line in content.split("\n"):
            line = line.strip()
            if line and line.startswith("-"):
                subtask = line[1:].strip()
                if subtask:
                    subtasks.append(subtask)
        return subtasks if subtasks else ["Error: No se han podido generar las subtareas."]

    except Exception as e:
        print("Error real", e)
        return ["Error: No se ha podido conectar"]
    

#Esta es la version a usar si usamos OpenAI
clientOpenAI = InferenceClient(api_key=os.getenv("HUGGINGFACE_API_KEY"))
def create_simple_task_OpenAI(task):
    if not clientOpenAI.api_key:
        return ["Error: la Api no esta bien montada"]
    
    try:
        prompt = f"""Desglosa la siguiente tarea compleja en una lista de 3 a 5 subtareas simples y accesibles.

        Tarea: {task.description}
        
        Formato de respuesta: 
        - Subtarea 1
        - Subtarea 2
        - Subtarea 3
        - etc.

        Responde solo con la linea de subtareas, una por linea, empezando cada linea con un guion (-)
        """
        params = {
            "model": "gpt-5",
            "messages": [
                {"role": "system", "content": "Eres un asistente experto en gestion de tareas que ayuda a dividir tareas complejas en pasos simples y accionables"},
                {"role": "user", "content": prompt}
            ],
            "max_completion_tokens": 300,
            "verbosity":"medium",
            "reasoning_effort": "minimal"
        }
        response = clientOpenAI.chat.completions.create(**params)

        content= response.choices[0].message.content.strip()

        subtasks = []

        for line in content.split("\n"):
            line = line.strip()
            if line and line.startswith("-"):
                subtask = line[1:].strip()
                if subtask:
                    subtasks.append(subtask)
        return subtasks if subtasks else ["Error: No se han podido generar las subtareas."]


    except Exception as e:
        print("error real", e)
        return ["Error: No se ha podido conectar"]
