import json

def limpiar_json(ruta_archivo, ruta_salida):
    """
    Limpia y convierte los valores del campo 'event' en un archivo JSONL para que sean JSON válidos.
    :param ruta_archivo: Ruta del archivo JSON de entrada.
    :param ruta_salida: Ruta del archivo JSONL de salida con los datos limpios.
    """
    datos_limpios = []

    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                if linea.strip():  # Ignorar líneas vacías
                    try:
                        objeto = json.loads(linea.strip())
                        # Limpiar y convertir el campo 'event' si es un string
                        if 'event' in objeto and isinstance(objeto['event'], str):
                            objeto['event'] = json.loads(objeto['event'])  # Convertir el string a JSON
                        datos_limpios.append(objeto)
                    except json.JSONDecodeError as e:
                        print(f"Error al decodificar línea: {e}")

        # Guardar los datos limpios en un nuevo archivo JSONL
        with open(ruta_salida, 'w', encoding='utf-8') as archivo_salida:
            for dato in datos_limpios:
                archivo_salida.write(json.dumps(dato, ensure_ascii=False) + '\n')

        print(f"Datos limpiados y guardados en: {ruta_salida}")

    except Exception as e:
        print(f"Error general: {e}")

# Rutas
ruta_entrada = r"C:\Users\nahom\OneDrive - Universidad Técnica Particular de Loja - UTPL\Curso Documentos Accesibles\CSV\analisis-codigo\analizar_datos_open_campus\Open Campus\json\txt\pause_video.json"
ruta_salida = r"C:\Users\nahom\OneDrive - Universidad Técnica Particular de Loja - UTPL\Curso Documentos Accesibles\CSV\analisis-codigo\analizar_datos_open_campus\Open Campus\json\txt\pause_video_limpio.jsonl"

# Llamar a la función
limpiar_json(ruta_entrada, ruta_salida)
