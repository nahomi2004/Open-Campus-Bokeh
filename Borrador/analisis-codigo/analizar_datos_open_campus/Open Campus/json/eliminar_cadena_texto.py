import re

def limpiar_tracking_logs(ruta_archivo):
    """
    Lee un archivo, elimina las cadenas que coinciden con el patrón 
    'tracking.log-<números>.gz:' antes de cada apertura de llaves, y 
    guarda el resultado limpio en un nuevo archivo.
    
    :param ruta_archivo: Ruta del archivo original.
    :return: Ruta del archivo limpio generado.
    """
    # Ruta para el archivo limpio
    archivo_limpio = ruta_archivo.replace(".txt", "_limpio.json")
    
    # Patrón de texto a eliminar
    patron = r"tracking\.log-\d+-\d+\.gz:"
    
    try:
        # Leer el archivo original
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()
        
        # Reemplazar el patrón con una cadena vacía
        contenido_limpio = re.sub(patron, '', contenido)
        
        # Guardar el contenido limpio en un nuevo archivo
        with open(archivo_limpio, 'w', encoding='utf-8') as archivo:
            archivo.write(contenido_limpio)
        
        print(f"Archivo limpio generado en: {archivo_limpio}")
        return archivo_limpio

    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
        return None

# Ruta del archivo original
ruta = r"C:\Users\nahom\OneDrive - Universidad Técnica Particular de Loja - UTPL\Curso Documentos Accesibles\CSV\segundo\course-creaaa1\course-creaaa1.txt"

# Llamar a la función para limpiar el archivo
limpiar_tracking_logs(ruta)
