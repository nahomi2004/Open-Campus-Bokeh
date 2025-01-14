import json

# Funcion 1
def obtener_llaves(objeto, llaves_unicas):
    """
    Función recursiva para extraer todas las llaves de un objeto JSON.
    :param objeto: Objeto JSON (puede ser dict o lista).
    :param llaves_unicas: Conjunto de llaves únicas acumuladas.
    """
    if isinstance(objeto, dict):  # Si es un diccionario, iterar por sus llaves y valores
        for clave, valor in objeto.items():
            llaves_unicas.add(clave)
            obtener_llaves(valor, llaves_unicas)  # Llamada recursiva para explorar el valor
    elif isinstance(objeto, list):  # Si es una lista, iterar por sus elementos
        for elemento in objeto:
            obtener_llaves(elemento, llaves_unicas)

def leer_jsonl_obtener_llaves(ruta_archivo):
    """
    Lee un archivo JSONL y obtiene todas las llaves únicas de los objetos JSON.
    :param ruta_archivo: Ruta del archivo JSONL.
    :return: Conjunto de llaves únicas.
    """
    llaves_unicas = set()  # Usamos un conjunto para evitar duplicados

    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                if linea.strip():  # Ignorar líneas vacías
                    try:
                        objeto = json.loads(linea.strip())
                        obtener_llaves(objeto, llaves_unicas)  # Extraer llaves del objeto actual
                    except json.JSONDecodeError as e:
                        print(f"Error al decodificar línea: {e}")

        print("Llaves únicas extraídas correctamente.")
        return llaves_unicas
    except Exception as e:
        print(f"Error general: {e}")
    return None

# Funcion 2
def leer_jsonl_y_obtener_paths_unicos(ruta_archivo):
    """
    Lee un archivo JSONL y extrae los valores únicos del campo 'path'.
    :param ruta_archivo: Ruta del archivo JSONL.
    :return: Lista de valores únicos del campo 'path'.
    """
    paths_unicos = set()  # Usamos un conjunto para almacenar valores únicos

    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                if linea.strip():  # Ignorar líneas vacías
                    try:
                        objeto = json.loads(linea.strip())
                        # Verificar si 'path' existe en el objeto
                        if 'path' in objeto.get('context', {}):
                            paths_unicos.add(objeto['context']['path'])
                    except json.JSONDecodeError as e:
                        print(f"Error al decodificar línea: {e}")

        print("Datos procesados correctamente.")
        return list(paths_unicos)  # Convertimos el conjunto en una lista para el resultado
    except Exception as e:
        print(f"Error general: {e}")
    return None

# Funcion 3

def buscar_path_especifico(ruta_archivo, path_buscar):
    """
    Busca un 'path' específico y aquellos que inicien con él en un archivo JSONL.
    :param ruta_archivo: Ruta del archivo JSONL.
    :param path_buscar: El 'path' que se desea buscar.
    :return: Diccionario con coincidencias exactas y ampliadas.
    """
    resultados = {
        "coincidencias_exactas": [],  # Lista para almacenar coincidencias exactas
        "coincidencias_ampliadas": []  # Lista para almacenar coincidencias ampliadas
    }

    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                if linea.strip():  # Ignorar líneas vacías
                    try:
                        objeto = json.loads(linea.strip())
                        path_actual = objeto.get('event_type', {}) # Obtener el 'path' objeto.get('context', {}).get('path', '') 

                        if path_actual == path_buscar:
                            resultados["coincidencias_exactas"].append(objeto)
                        elif path_actual.startswith(path_buscar):
                            resultados["coincidencias_ampliadas"].append(objeto)
                    except json.JSONDecodeError as e:
                        print(f"Error al decodificar línea: {e}")

        # Resumen de resultados
        print(f"Se encontraron {len(resultados['coincidencias_exactas'])} coincidencias exactas.")
        print(f"Se encontraron {len(resultados['coincidencias_ampliadas'])} coincidencias ampliadas.")
        return resultados

    except Exception as e:
        print(f"Error general: {e}")
    return None

def leer_jsonl_y_obtener_names_unicos(ruta_archivo):
    """
    Lee un archivo JSONL y extrae los valores únicos del campo 'name'.
    :param ruta_archivo: Ruta del archivo JSONL.
    :return: Lista de valores únicos del campo 'path'.
    """
    names_unicos = set()  # Usamos un conjunto para almacenar valores únicos

    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                if linea.strip():  # Ignorar líneas vacías
                    try:
                        objeto = json.loads(linea.strip())
                        # Verificar si 'path' existe en el objeto
                        if 'name' in objeto:
                            names_unicos.add(objeto['name'])
                    except json.JSONDecodeError as e:
                        print(f"Error al decodificar línea: {e}")

        print("Datos procesados correctamente.")
        return list(names_unicos)  # Convertimos el conjunto en una lista para el resultado
    except Exception as e:
        print(f"Error general: {e}")
    return None

def buscar_name_especifico_y_guardar(ruta_archivo, name_buscar, ruta_salida):
    """
    Busca un 'name' específico y aquellos que inicien con él en un archivo JSONL.
    Guarda los resultados en un archivo de texto.
    :param ruta_archivo: Ruta del archivo JSONL.
    :param name_buscar: El 'name' que se desea buscar.
    :param ruta_salida: Ruta del archivo de salida donde se guardarán los resultados.
    :return: Diccionario con coincidencias exactas y ampliadas.
    """
    resultados = {
        "coincidencias_exactas": [],  # Lista para almacenar coincidencias exactas
        "coincidencias_ampliadas": []  # Lista para almacenar coincidencias ampliadas
    }
    
    try:
        # Leer el archivo JSONL
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                if linea.strip():  # Ignorar líneas vacías
                    try:
                        objeto = json.loads(linea.strip())
                        name_actual = objeto.get('name', '')  # Obtener el 'name'

                        if name_actual == name_buscar:
                            resultados["coincidencias_exactas"].append(objeto)
                        elif name_actual.startswith(name_buscar):
                            resultados["coincidencias_ampliadas"].append(objeto)
                    except json.JSONDecodeError as e:
                        print(f"Error al decodificar línea: {e}")
        
        # Guardar los resultados en el archivo de salida
        with open(ruta_salida, 'w', encoding='utf-8') as archivo_salida:
            for item in resultados["coincidencias_exactas"]:
                archivo_salida.write(json.dumps(item, ensure_ascii=False) + "\n")
            
            for item in resultados["coincidencias_ampliadas"]:
                archivo_salida.write(json.dumps(item, ensure_ascii=False) + "\n")

        # Resumen de resultados
        print(f"Se encontraron {len(resultados['coincidencias_exactas'])} coincidencias exactas.")
        print(f"Se encontraron {len(resultados['coincidencias_ampliadas'])} coincidencias ampliadas.")
        print(f"Resultados guardados en: {ruta_salida}")
        return resultados

    except Exception as e:
        print(f"Error general: {e}")
    return None

# Ruta del archivo
ruta_jsonl = r"C:\Users\nahom\OneDrive - Universidad Técnica Particular de Loja - UTPL\Curso Documentos Accesibles\CSV\analisis-codigo\documento json\course-creaaa1\course-creaaa1_limpio.json"

# Ruta donde se va a guardar
ruta_salida_txt = r"C:\Users\nahom\OneDrive - Universidad Técnica Particular de Loja - UTPL\Curso Documentos Accesibles\CSV\analisis-codigo\analizar_datos_open_campus\Open Campus\json\docs\jsonl\seek_video.jsonl"

""" 
# Llamar a la función para obtener llaves únicas
llaves = leer_jsonl_obtener_llaves(ruta_jsonl)

# Mostrar las llaves únicas
if llaves:
    print(f"Se encontraron {len(llaves)} llaves únicas:")
    for llave in sorted(llaves):
        print(f"- {llave}")

 
# Llamar a la función para saber que datos hay en path (# Funcion 2)
paths = leer_jsonl_y_obtener_paths_unicos(ruta_jsonl)

# Mostrar los resultados

if paths:
    print(f"Se encontraron {len(paths)} valores únicos para 'path':")
    for path in paths:
        print(f"- {path}")

# Ruta específica que deseas buscar
path_a_buscar = "/courses/course-v1:UTPL+CREAA1+2024_2/courseware/b096611277ef4c0781ad54695164870b/7b4b1fb76f8a48939b4a9cd3e3f27e24/"

resultados = buscar_path_especifico(ruta_jsonl, path_a_buscar)

# Mostrar resultados si se encontraron
if resultados:
    print("\n=== Coincidencias Exactas ===")
    for obj in resultados["coincidencias_exactas"]:
        print(obj)

    print("\n=== Coincidencias Ampliadas ===")
    for obj in resultados["coincidencias_ampliadas"]:
        print(obj)
        
# Llamar a la función para saber que datos hay en name
names = leer_jsonl_y_obtener_names_unicos(ruta_jsonl)

# Mostrar los resultados

if names:
    print(f"Se encontraron {len(names)} valores únicos para 'name':")
    for path in names:
        print(f"- {path}")
""" 

# name específico que deseas buscar
name_a_buscar = "seek_video"

resultados = buscar_name_especifico_y_guardar(ruta_jsonl, name_a_buscar, ruta_salida_txt)

