import json

def obtener_etiquetas_json(ruta_archivo):
    """
    Lee un archivo JSON y extrae las etiquetas o columnas disponibles.
    
    :param ruta_archivo: Ruta del archivo JSON limpio.
    :return: Lista de etiquetas o columnas presentes en el JSON.
    """
    try:
        # Leer el contenido del archivo JSON
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)  # Cargar el JSON como un objeto Python
        
        # Verificar si el JSON es una lista y obtener las claves del primer elemento
        if isinstance(datos, list) and datos:
            etiquetas = datos[0].keys()
        elif isinstance(datos, dict):  # Si es un diccionario directamente
            etiquetas = datos.keys()
        else:
            print("El formato del archivo JSON no es válido o está vacío.")
            return None

        # Mostrar las etiquetas encontradas
        print(f"Etiquetas encontradas: {list(etiquetas)}")
        return list(etiquetas)

    except json.JSONDecodeError:
        print("Error al decodificar el archivo JSON. Verifica que el formato sea válido.")
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
    return None

# Ruta del archivo JSON limpio
ruta_limpia = r"C:\Users\nahom\OneDrive - Universidad Técnica Particular de Loja - UTPL\Curso Documentos Accesibles\CSV\segundo\course-creaaa1\course-creaaa1_limpio.json"

# Llamar a la función para obtener las etiquetas
obtener_etiquetas_json(ruta_limpia)
