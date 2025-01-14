import json
import os
import matplotlib.pyplot as plt

def analizar_pausas_y_graficar(ruta_lectura, ruta_salida_grafica, ruta_salida_txt):
    """
    Analiza las pausas en los videos y grafica el tiempo máximo antes de cada pausa.
    :param ruta_lectura: Ruta del archivo JSONL de entrada.
    :param ruta_salida_grafica: Ruta donde se guardará la gráfica de barras.
    :param ruta_salida_txt: Ruta donde se guardará el archivo TXT con los datos analizados.
    """
    datos_pausas = {}

    try:
        # Leer el archivo JSONL
        with open(ruta_lectura, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                if linea.strip():  # Ignorar líneas vacías
                    try:
                        objeto = json.loads(linea.strip())  # Cargar cada línea como JSON
                        evento = json.loads(objeto.get('event', '{}'))  # Convertir el campo 'event' a JSON
                        codigo_video = evento.get('code', '')
                        tiempo_pausa = evento.get('currentTime', 0) / 60

                        # Actualizar el tiempo máximo para el código de video
                        if codigo_video:
                            datos_pausas[codigo_video] = max(datos_pausas.get(codigo_video, 0), tiempo_pausa)
                    except json.JSONDecodeError as e:
                        print(f"Error al decodificar línea: {e}")
        
        # Odenar los datos en orden alafabetico con respecto al codigo del video
        sorted_by_codigo = dict(sorted(datos_pausas.items(), key=lambda item: item[0]))
        
        # Guardar los datos analizados en un archivo TXT
        with open(ruta_salida_txt, 'w', encoding='utf-8') as archivo_txt:
            archivo_txt.write("Código de Video\tTiempo Máximo Antes de Pausa (segundos)\n")
            for codigo, tiempo in sorted_by_codigo.items():
                archivo_txt.write(f"{codigo}\t{tiempo:.2f}\n")

        # Crear el gráfico de barras
        codigos = list(sorted_by_codigo.keys())
        tiempos = list(sorted_by_codigo.values())

        plt.figure(figsize=(12, 6))
        plt.bar(codigos, tiempos, color='skyblue')
        plt.xlabel('Código de Video', fontsize=12)
        plt.ylabel('Tiempo Máximo Antes de Pausa (segundos)', fontsize=12)
        plt.title('Tiempo Máximo Antes de Pausa por Código de Video', fontsize=14)
        plt.xticks(rotation=45, ha='right')  # Rotar etiquetas en el eje X
        plt.tight_layout()  # Ajustar el diseño para evitar que se superpongan

        # Guardar la gráfica
        plt.savefig(ruta_salida_grafica)
        plt.close()

        print(f"Gráfica guardada en: {ruta_salida_grafica}")
        print(f"Datos guardados en: {ruta_salida_txt}")

    except Exception as e:
        print(f"Error general: {e}")


def analizar_stops_y_graficar(ruta_lectura, ruta_salida_grafica, ruta_salida_txt):
    """
    Analiza las pausas en los videos y grafica el tiempo máximo antes de cada pausa.
    :param ruta_lectura: Ruta del archivo JSONL de entrada.
    :param ruta_salida_grafica: Ruta donde se guardará la gráfica de barras.
    :param ruta_salida_txt: Ruta donde se guardará el archivo TXT con los datos analizados.
    """
    datos_stop = {}

    try:
        # Leer el archivo JSONL
        with open(ruta_lectura, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                if linea.strip():  # Ignorar líneas vacías
                    try:
                        objeto = json.loads(linea.strip())  # Cargar cada línea como JSON
                        evento = json.loads(objeto.get('event', '{}'))  # Convertir el campo 'event' a JSON
                        codigo_video = evento.get('code', '')
                        tiempo_stop = evento.get('currentTime', 0) / 60

                        # Actualizar el tiempo máximo para el código de video
                        if codigo_video:
                            datos_stop[codigo_video] = max(datos_stop.get(codigo_video, 0), tiempo_stop)
                    except json.JSONDecodeError as e:
                        print(f"Error al decodificar línea: {e}")
        
        # Odenar los datos en orden alafabetico con respecto al codigo del video
        sorted_by_codigo = dict(sorted(datos_stop.items(), key=lambda item: item[0]))
        
        # Guardar los datos analizados en un archivo TXT
        with open(ruta_salida_txt, 'w', encoding='utf-8') as archivo_txt:
            archivo_txt.write("Código de Video\tTiempo Máximo Antes de Stop (segundos)\n")
            for codigo, tiempo in sorted_by_codigo.items():
                archivo_txt.write(f"{codigo}\t{tiempo:.2f}\n")

        # Crear el gráfico de barras
        codigos = list(sorted_by_codigo.keys())
        tiempos = list(sorted_by_codigo.values())

        plt.figure(figsize=(12, 6))
        plt.bar(codigos, tiempos, color='skyblue')
        plt.xlabel('Código de Video', fontsize=12)
        plt.ylabel('Tiempo Máximo Antes de Stop (segundos)', fontsize=12)
        plt.title('Tiempo Máximo Antes de Stop por Código de Video', fontsize=14)
        plt.xticks(rotation=45, ha='right')  # Rotar etiquetas en el eje X
        plt.tight_layout()  # Ajustar el diseño para evitar que se superpongan

        # Guardar la gráfica
        plt.savefig(ruta_salida_grafica)
        plt.close()

        print(f"Gráfica guardada en: {ruta_salida_grafica}")
        print(f"Datos guardados en: {ruta_salida_txt}")

    except Exception as e:
        print(f"Error general: {e}")

def analizar_reproducciones_time_y_graficar(ruta_lectura, ruta_salida_grafica, ruta_salida_txt):
    """
    Analiza las reproducciones (play) en los videos y genera un gráfico de barras.
    :param ruta_lectura: Ruta del archivo JSONL de entrada.
    :param ruta_salida_grafica: Ruta donde se guardará la gráfica de barras.
    :param ruta_salida_txt: Ruta donde se guardará el archivo TXT con los datos analizados.
    """
    conteo_reproducciones = {}

    try:
        # Leer el archivo JSONL
        with open(ruta_lectura, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                if linea.strip():  # Ignorar líneas vacías
                    try:
                        objeto = json.loads(linea.strip())  # Cargar cada línea como JSON
                        evento = json.loads(objeto.get('event', '{}'))  # Convertir el campo 'event' a JSON
                        codigo_video = evento.get('code', '')
                        tiempo = evento.get('currentTime', '') / 60
                        
                        # Incrementar el conteo de reproducciones para el código de video
                        if codigo_video and tiempo > 1:
                            conteo_reproducciones[codigo_video] = conteo_reproducciones.get(codigo_video, 0) + 1
                    except json.JSONDecodeError as e:
                        print(f"Error al decodificar línea: {e}")
        
        # Odenar los datos en orden alafabetico con respecto al codigo del video
        sorted_by_codigo = dict(sorted(conteo_reproducciones.items(), key=lambda item: item[0]))
        
        # Guardar los datos analizados en un archivo TXT
        with open(ruta_salida_txt, 'w', encoding='utf-8') as archivo_txt:
            archivo_txt.write("Código de Video\tReproducciones Totales luego de 1min\n")
            for codigo, reproducciones in sorted_by_codigo.items():
                archivo_txt.write(f"{codigo}\t{reproducciones}\n")

        # Crear el gráfico de barras
        codigos = list(sorted_by_codigo.keys())
        reproducciones = list(sorted_by_codigo.values())

        plt.figure(figsize=(12, 6))
        plt.bar(codigos, reproducciones, color='skyblue')
        plt.xlabel('Código de Video', fontsize=12)
        plt.ylabel('Reproducciones Totales', fontsize=12)
        plt.title('Reproducciones Totales por Código de Video (+1min)', fontsize=14)
        plt.xticks(rotation=45, ha='right')  # Rotar etiquetas en el eje X
        plt.tight_layout()  # Ajustar el diseño para evitar que se superpongan

        # Guardar la gráfica
        plt.savefig(ruta_salida_grafica)
        plt.close()

        print(f"Gráfica guardada en: {ruta_salida_grafica}")
        print(f"Datos guardados en: {ruta_salida_txt}")

    except Exception as e:
        print(f"Error general: {e}")

def contar_pausas_y_graficar(ruta_lectura, ruta_salida_grafica, ruta_salida_txt):
    """
    Analiza las pausas totales (pause) en los videos y genera un gráfico de barras.
    :param ruta_lectura: Ruta del archivo JSONL de entrada.
    :param ruta_salida_grafica: Ruta donde se guardará la gráfica de barras.
    :param ruta_salida_txt: Ruta donde se guardará el archivo TXT con los datos analizados.
    """
    conteo_pausas = {}

    try:
        # Leer el archivo JSONL
        with open(ruta_lectura, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                if linea.strip():  # Ignorar líneas vacías
                    try:
                        objeto = json.loads(linea.strip())  # Cargar cada línea como JSON
                        evento = json.loads(objeto.get('event', '{}'))  # Convertir el campo 'event' a JSON
                        codigo_video = evento.get('code', '')

                        # Incrementar el conteo de reproducciones para el código de video
                        if codigo_video:
                            conteo_pausas[codigo_video] = conteo_pausas.get(codigo_video, 0) + 1
                    except json.JSONDecodeError as e:
                        print(f"Error al decodificar línea: {e}")
        
        # Odenar los datos en orden alafabetico con respecto al codigo del video
        sorted_by_codigo = dict(sorted(conteo_pausas.items(), key=lambda item: item[0]))
        
        # Guardar los datos analizados en un archivo TXT
        with open(ruta_salida_txt, 'w', encoding='utf-8') as archivo_txt:
            archivo_txt.write("Código de Video\Pausas Totales\n")
            for codigo, reproducciones in sorted_by_codigo.items():
                archivo_txt.write(f"{codigo}\t{reproducciones}\n")

        # Crear el gráfico de barras
        codigos = list(sorted_by_codigo.keys())
        reproducciones = list(sorted_by_codigo.values())

        plt.figure(figsize=(12, 6))
        plt.bar(codigos, reproducciones, color='skyblue')
        plt.xlabel('Código de Video', fontsize=12)
        plt.ylabel('Pausas Totales', fontsize=12)
        plt.title('Pausas Totales por Código de Video', fontsize=14)
        plt.xticks(rotation=45, ha='right')  # Rotar etiquetas en el eje X
        plt.tight_layout()  # Ajustar el diseño para evitar que se superpongan

        # Guardar la gráfica
        plt.savefig(ruta_salida_grafica)
        plt.close()

        print(f"Gráfica guardada en: {ruta_salida_grafica}")
        print(f"Datos guardados en: {ruta_salida_txt}")

    except Exception as e:
        print(f"Error general: {e}")
        
# Rutas
ruta_lectura = r"C:\Users\nahom\OneDrive - Universidad Técnica Particular de Loja - UTPL\Curso Documentos Accesibles\CSV\analisis-codigo\analizar_datos_open_campus\Open Campus\json\docs\jsonl\play_video.jsonl"
ruta_salida_grafica = r"C:\Users\nahom\OneDrive - Universidad Técnica Particular de Loja - UTPL\Curso Documentos Accesibles\CSV\analisis-codigo\analizar_datos_open_campus\Open Campus\json\docs\images\grafica_barras_play_nmin_videos.jpg"
ruta_salida_txt = r"C:\Users\nahom\OneDrive - Universidad Técnica Particular de Loja - UTPL\Curso Documentos Accesibles\CSV\analisis-codigo\analizar_datos_open_campus\Open Campus\json\docs\txt\datos_play_nmin_videos.txt"

# Llamar a la función
# analizar_pausas_y_graficar(ruta_lectura, ruta_salida_grafica, ruta_salida_txt)

# Llamar a la función
# analizar_stops_y_graficar(ruta_lectura, ruta_salida_grafica, ruta_salida_txt)

# Llamar a la función
# analizar_reproducciones_y_graficar(ruta_lectura, ruta_salida_grafica, ruta_salida_txt)

# Llamar a la función
# contar_pausas_y_graficar(ruta_lectura, ruta_salida_grafica, ruta_salida_txt)

# Llamar a la función
analizar_reproducciones_time_y_graficar(ruta_lectura, ruta_salida_grafica, ruta_salida_txt)