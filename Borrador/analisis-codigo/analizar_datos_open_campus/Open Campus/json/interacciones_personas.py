import json

# FUNCIÓN 1
def filtrar_interacciones(ruta_archivo, filtro_clave, filtro_valor):
    """
    Filtra interacciones basadas en una clave y un valor específicos.
    :param ruta_archivo: Ruta del archivo JSONL.
    :param filtro_clave: Clave a buscar en el JSON.
    :param filtro_valor: Valor asociado a la clave para filtrar.
    :return: Lista de objetos JSON que cumplen con el filtro.
    """
    interacciones_filtradas = []
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                if linea.strip():
                    try:
                        objeto = json.loads(linea.strip())
                        if filtro_clave in objeto and objeto[filtro_clave] == filtro_valor:
                            interacciones_filtradas.append(objeto)
                    except json.JSONDecodeError as e:
                        print(f"Error al decodificar línea: {e}")
        print(f"Se encontraron {len(interacciones_filtradas)} interacciones que cumplen con el filtro.")
        return interacciones_filtradas
    except Exception as e:
        print(f"Error general: {e}")
    return None

# FUNCIÓN 2
def obtener_eventos_por_usuario(ruta_archivo, username_buscar=None):
    """
    Obtiene todos los eventos (event_type) agrupados por usuario (username) en un archivo JSONL.
    :param ruta_archivo: Ruta del archivo JSONL.
    :param username_buscar: El username para filtrar los resultados. Si es None, devuelve todos los usuarios.
    :return: Diccionario con usernames como claves y listas de event_type realizados como valores.
    """
    eventos_por_usuario = {}

    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                if linea.strip():  # Ignorar líneas vacías
                    try:
                        objeto = json.loads(linea.strip())
                        username = objeto.get('username', 'Usuario_Desconocido')  # Asignar "Usuario_Desconocido" si no hay username
                        event_type = objeto.get('event_type', None)  # Obtener el event_type

                        if username and event_type:  # Verificar que ambos valores existan
                            if username not in eventos_por_usuario:
                                eventos_por_usuario[username] = []  # Crear lista para el usuario
                            eventos_por_usuario[username].append(event_type)  # Agregar el evento

                    except json.JSONDecodeError as e:
                        print(f"Error al decodificar línea: {e}")

        # Si se ha especificado un username, filtrar los resultados
        if username_buscar:
            if username_buscar in eventos_por_usuario:
                eventos_por_usuario = {username_buscar: eventos_por_usuario[username_buscar]}
            else:
                print(f"No se encontraron eventos para el usuario: {username_buscar}")
        else:
            print(f"Se procesaron datos para {len(eventos_por_usuario)} usuarios.")

        return eventos_por_usuario

    except Exception as e:
        print(f"Error general: {e}")
    return None

# FUNCIÓN 3
def obtener_eventos_por_usuarios_unicos(ruta_archivo):
    """
    Obtiene todos los event_type únicos agrupados por usuario (username) en un archivo JSONL.
    :param ruta_archivo: Ruta del archivo JSONL.
    :return: Diccionario con usernames como claves y listas únicas de event_type realizados como valores.
    """
    eventos_por_usuario = {}

    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                if linea.strip():  # Ignorar líneas vacías
                    try:
                        objeto = json.loads(linea.strip())
                        username = objeto.get('username', 'Usuario_Desconocido')  # Asignar "Usuario_Desconocido" si no hay username
                        event_type = objeto.get('event_type', None)  # Obtener el event_type

                        if username and event_type:  # Verificar que ambos valores existan
                            if username not in eventos_por_usuario:
                                eventos_por_usuario[username] = set()  # Usar un conjunto para evitar duplicados
                            eventos_por_usuario[username].add(event_type)  # Agregar el evento

                    except json.JSONDecodeError as e:
                        print(f"Error al decodificar línea: {e}")

        # Convertir los conjuntos en listas para la salida
        eventos_por_usuario = {usuario: list(eventos) for usuario, eventos in eventos_por_usuario.items()}
        print(f"Se procesaron eventos para {len(eventos_por_usuario)} usuarios.")
        return eventos_por_usuario

    except Exception as e:
        print(f"Error general: {e}")
    return None


# Ruta del archivo
ruta_jsonl = r"D:\Users\LENOVO\Desktop\Practicum 2.1\course-creaaa1_limpio.json"

"""
# Para ver especificamente quienes realizaron una interacción concreta (filtrar interacciones)
clave_a_filtrar = "event_type"  # Cambiar por la clave que desees filtrar
valor_a_filtrar = "play_video"  # Cambiar por el valor específico

interacciones = filtrar_interacciones(ruta_jsonl, clave_a_filtrar, valor_a_filtrar)

# Mostrar resultados
if interacciones:
    print(f"\n=== Interacciones Filtradas ({clave_a_filtrar}={valor_a_filtrar}) ===")
    for interaccion in interacciones:
        print(interaccion)
"""

"""
# Especifica el username a buscar
username_a_buscar = "JanethUrrego"

# Llamar a la función para obtener eventos por usuario específico
eventos = obtener_eventos_por_usuario(ruta_jsonl, username_a_buscar)

# Mostrar los resultados
if eventos:
    print("Eventos por usuario:")
    for usuario, eventos_realizados in eventos.items():
        print(f"Usuario: {usuario}")
        print(f"  Eventos realizados: {', '.join(eventos_realizados)}\n")
"""

# Llamar a la función para obtener eventos por usuarios únicos
eventos_por_usuarios = obtener_eventos_por_usuarios_unicos(ruta_jsonl)

# Mostrar los resultados
if eventos_por_usuarios:
    print("Eventos únicos por usuario:")
    for usuario, eventos in eventos_por_usuarios.items():
        print(f"Usuario: {usuario}")
        print(f"  Eventos únicos realizados: {', '.join(eventos)}\n")