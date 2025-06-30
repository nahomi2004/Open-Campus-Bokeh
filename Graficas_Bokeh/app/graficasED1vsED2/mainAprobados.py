import json
import pandas as pd
from collections import defaultdict
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Select, HoverTool
from bokeh.layouts import column
from bokeh.io import curdoc
from bokeh.models import Slider

# Direccionar al html
from os.path import dirname, join
from bokeh.models import Div
desc0 = Div(text=open(join(dirname(__file__), "TituloAprobados.html")).read(), sizing_mode="stretch_width")
desc1 = Div(text=open(join(dirname(__file__), "grafica1Apro.html")).read(), sizing_mode="stretch_width")
desc2 = Div(text=open(join(dirname(__file__), "grafica2Apro.html")).read(), sizing_mode="stretch_width")
curdoc().add_root(column(desc0))

# Ejemplo de uso:
codigo_a_nombre = {
    "video_intro": "vKq2NotGPJQ",
    "LR_1_Video1_Semana1": "U3cK1QMIIEQ",
    "LR_1_Video2_Semana1": "9aNQZ9dKXRY",
    "LR_1_Video3_Semana1": "lsNxh-lSpCY",
    "LR_1_Video4_Semana1": "C3LnEvN0qZ0",
    "LR_1_Video5_Semana1": "vbpbkQE5K_Q",
    "LR_1_Video6_Semana1": "zCFa0xjGXGQ",
    "LR_1_Video7_Semana1": "qlS7ShZfb-c",
    "LR_1_Video8_Semana1": "8cKRb9CKtxk",
    "LR_1_Video9_Semana1": "WyrfIZ6VBcM",
    "LR_1_Video10_Semana1": "NgUhK3rw1IE",
    "LR_1_Video11_Semana1": "ttP0EyzSbbo",
    "LR_1_Video12_Semana1": "Vy4FWDyjZo4",
    "LR_2_Video1_Semana1": "leg7NPlfNf0",
    "LR_2_Video2_Semana1": "avTMbQWrFgM",
    "LR_2_Video3_Semana1": "cNoUwGM1DQs",
    "LR_2_Video4_Semana1": "6Mst559v-Uc",
    "LR_2_Video5_Semana1": "CNQpefXv5DY",
    "LR_2_Video6_Semana1": "6W1_fBZFqns", #
    "LR_1_Video1_Semana2": "o5VwDVJ7N3Q",
    "LR_1_Video2_Semana2": "LluqYlh2xg4",
    "LR_1_Video3_Semana2": "eE658thjDj8",
    "LR_1_Video4_Semana2": "QbEpClHzTeM",
    "LR_1_Video5_Semana2": "MCG0or2ULB4",
    "LR_1_Video6_Semana2": "ol-vGTdHBNU",
    "LR_1_Video7_Semana2": "WTXS0IMQ3Ss",
    "LR_1_Video8_Semana2": "9kqXmM3b3wc",
    "VS1_Video1_Semana2": "_zQHV3vCGpA",
    "VS2_Video2_Semana2": "RropOrUc2AE",
    "Video1_Semana3": "VGHSSIUyFhI",
    "Video1_Semana4": "kyGRuJXaboU",
}

# Lista de interacciones relacionadas con videos
interacciones_video = ["play_video", "pause_video", "seek_video", "stop_video"]

# Cargar CSV con calificaciones
csv_path = r"../../../CSVs/Unificar Abr-Jun25 Nuevo/Reporte CursoAccesActual.csv"
df_grades = pd.read_csv(csv_path, delimiter=',')

# Obtener IDs de aprobados
usuarios_aprobados = df_grades[df_grades["grade"] >= 0.7]["username"].unique()

# Cargar datos JSON
json_path = "../../../Jsonl/course-v1_/course-v1_UTPL_CREAA2limpio.json"
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)
data = pd.DataFrame(data)

# Filtrar eventos solo de aprobados
data_aprobados = data[data["username"].isin(usuarios_aprobados)]

# Función para contar interacciones
def contar_interacciones(data, interacciones):
    conteos = defaultdict(lambda: defaultdict(int))
    for _, row in data.iterrows():
        if row.get("name") in interacciones:
            try:
                evento_json = json.loads(row.get("event", '{}'))
                codigo_video = evento_json.get("code", "")
                if codigo_video:
                    conteos[row.get("name")][codigo_video] += 1
            except json.JSONDecodeError as e:
                print(f"Error al decodificar línea: {e}")
    return conteos

# Convertir los códigos a nombres
def convertir_codigos_a_nombres(datos_eventos, mapeo_codigos):
    codigo_a_nombre_rev = {codigo: nombre for nombre, codigo in mapeo_codigos.items()}
    datos_con_nombres = {
        evento: {
            codigo_a_nombre_rev.get(codigo, f"Desconocido ({codigo})"): conteo
            for codigo, conteo in conteos.items()
        } for evento, conteos in datos_eventos.items()
    }
    return datos_con_nombres

# Aplicar funciones solo sobre aprobados
conteos = contar_interacciones(data_aprobados, interacciones_video)
conteos_con_nombres = convertir_codigos_a_nombres(conteos, codigo_a_nombre)

# --- GRAFICA 1: SOLO APROBADOS ---
tipo_inicial_grafica3 = "play_video"
conteos_play = conteos_con_nombres[tipo_inicial_grafica3]
orden_videos = list(codigo_a_nombre.keys())
conteos_ordenados = {v: conteos_play.get(v, 0) for v in orden_videos}

# Fuente para gráfica
source_grafica3 = ColumnDataSource(data=dict(
    videos=list(conteos_ordenados.keys()),
    reproducciones=list(conteos_ordenados.values())
))

# Crear figura de línea
p_grafica3 = figure(
    x_range=list(conteos_ordenados.keys()),
    title=f'Evolución de {tipo_inicial_grafica3} (solo aprobados)', 
    x_axis_label='Videos en orden de la malla', 
    y_axis_label='Cantidad de interacciones',
    width=900, height=400,
    tools='pan,box_zoom,wheel_zoom,save,reset',
    toolbar_location='right'
)

p_grafica3.add_tools(HoverTool(tooltips=[
        ("Videos", "@videos"),
        ("Cantidad de interacciones", "@reproducciones")
    ]))

p_grafica3.xaxis.major_label_orientation = 1.0
p_grafica3.line(x='videos', y='reproducciones', source=source_grafica3, color='green', line_width=2)
p_grafica3.circle(x='videos', y='reproducciones', source=source_grafica3, color='green', size=8)

# Dropdown de interacciones
select_grafica3 = Select(title='Selecciona una interacción:',
                         value=tipo_inicial_grafica3,
                         options=interacciones_video)

# Actualizar gráfica con cambios del Select
def actualizar_grafica3(attr, old, new):
    nuevo_tipo = select_grafica3.value
    conteos = conteos_con_nombres[nuevo_tipo]
    nuevos_vals = {v: conteos.get(v, 0) for v in orden_videos}

    source_grafica3.data = dict(videos=list(nuevos_vals.keys()), reproducciones=list(nuevos_vals.values()))
    p_grafica3.title.text = f'Evolución de {nuevo_tipo} (solo aprobados)'

select_grafica3.on_change('value', actualizar_grafica3)

# Mostrar layout
curdoc().add_root(column(desc1))
layout = column(select_grafica3, p_grafica3)
curdoc().add_root(layout)
curdoc().title = "Gráfica Interacciones Aprobados"

# --- GRAFICA 2: RANKING TOP N Aprobados por usuario ---

# Invertir diccionario para obtener nombre a partir de código
codigo_a_nombre_rev = {v: k for k, v in codigo_a_nombre.items()}
orden_videos_top = list(codigo_a_nombre.values())  # Lista de códigos en orden

# Todos los aprobados ordenados por nota
usuarios_aprobados_ordenados = df_grades[df_grades["grade"] >= 0.7].sort_values(by="grade", ascending=False)

# Slider para elegir cantidad de participantes
slider_top_n = Slider(title="Cantidad de participantes a mostrar", start=1, end=min(30, len(usuarios_aprobados_ordenados)), value=10, step=1)

# Función para actualizar usernames del Select según slider
def obtener_top_usernames(n):
    return usuarios_aprobados_ordenados.head(n)["username"].tolist()

# Inicializar con top-N
top_usernames = obtener_top_usernames(slider_top_n.value)

# Filtrar eventos solo de esos usuarios
def filtrar_data_usuarios(usernames):
    return data[data["username"].isin(usernames)]

# Contar interacciones por username y por video
def contar_interacciones_por_usuario(data, interacciones):
    conteos = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    for _, row in data.iterrows():
        if row.get("name") in interacciones and row.get("username") in top_usernames:
            try:
                evento_json = json.loads(row.get("event", '{}'))
                codigo = evento_json.get("code", "")
                if codigo:
                    usuario = row.get("username")
                    conteos[usuario][row["name"]][codigo] += 1
            except:
                continue
    return conteos

# Función para obtener datos de usuario + interacción
def obtener_datos_usuario(username, interaccion):
    conteos = conteos_usuario.get(username, {}).get(interaccion, {})
    datos_ordenados = {codigo_a_nombre_rev.get(codigo, f"({codigo})"): conteos.get(codigo, 0) for codigo in orden_videos_top}
    return datos_ordenados

# Inicializar con primeros valores
data_top10 = filtrar_data_usuarios(top_usernames)
conteos_usuario = contar_interacciones_por_usuario(data_top10, interacciones_video)
username_inicial = top_usernames[0]
interaccion_inicial = "play_video"
datos_iniciales_top = obtener_datos_usuario(username_inicial, interaccion_inicial)

# Fuente de datos
source_grafica_top = ColumnDataSource(data=dict(
    videos=list(datos_iniciales_top.keys()),
    reproducciones=list(datos_iniciales_top.values())
))

# Crear figura
p_grafica_top = figure(
    x_range=list(datos_iniciales_top.keys()),
    title=f"Interacciones de {username_inicial} - {interaccion_inicial}",
    x_axis_label="Videos",
    y_axis_label="Cantidad de interacciones",
    width=900, height=400,
    tools="pan,box_zoom,wheel_zoom,save,reset",
    toolbar_location="right"
)
p_grafica_top.add_tools(HoverTool(tooltips=[
        ("Videos", "@videos"),
        ("Cantidad de interacciones", "@reproducciones")
    ]))

p_grafica_top.xaxis.major_label_orientation = 1.0
p_grafica_top.line(x="videos", y="reproducciones", source=source_grafica_top, line_color="navy", line_width=2)
p_grafica_top.scatter(x="videos", y="reproducciones", source=source_grafica_top, size=8, color="navy")

# Dropdowns
select_usuario_top = Select(title="Selecciona participante:", value=username_inicial, options=top_usernames)
select_interaccion_top = Select(title="Selecciona interacción:", value=interaccion_inicial, options=interacciones_video)

# Callback para actualizar gráfica
def actualizar_grafica_top(attr, old, new):
    username = select_usuario_top.value
    interaccion = select_interaccion_top.value
    nuevos_datos = obtener_datos_usuario(username, interaccion)
    source_grafica_top.data = dict(videos=list(nuevos_datos.keys()), reproducciones=list(nuevos_datos.values()))
    p_grafica_top.title.text = f"Interacciones de {username} - {interaccion}"
    p_grafica_top.x_range.factors = list(nuevos_datos.keys())

# Callback para actualizar usuarios cuando se mueve el slider
def actualizar_slider_top(attr, old, new):
    global top_usernames, conteos_usuario

    # Calcular nuevos top N ordenados por nota
    top_usernames = obtener_top_usernames(slider_top_n.value)
    
    # Filtrar los datos para estos nuevos top
    data_nueva = filtrar_data_usuarios(top_usernames)
    
    # Recontar interacciones con nuevos top N
    conteos_usuario = contar_interacciones_por_usuario(data_nueva, interacciones_video)
    
    # Actualizar opciones del select
    select_usuario_top.options = top_usernames
    select_usuario_top.value = top_usernames[0]  # Reiniciar al primero del nuevo top
    actualizar_grafica_top(None, None, None)  # Redibujar gráfica

# Enlazar eventos
select_usuario_top.on_change("value", actualizar_grafica_top)
select_interaccion_top.on_change("value", actualizar_grafica_top)
slider_top_n.on_change("value", actualizar_slider_top)

# Layout separado
curdoc().add_root(column(desc2))
layout_top = column(slider_top_n, select_usuario_top, select_interaccion_top, p_grafica_top)
curdoc().add_root(layout_top)