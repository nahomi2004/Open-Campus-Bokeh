import pandas as pd
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, HoverTool, FactorRange, Div
from bokeh.layouts import column, row
from bokeh.transform import cumsum
from math import pi
from os.path import dirname, join
from bokeh.palettes import Spectral4
from funciones import *

desc0 = Div(text=open(join(dirname(__file__), "TituloACCS1vs2.html"), encoding="utf-8").read(), sizing_mode="stretch_width")
desc1 = Div(text=open(join(dirname(__file__), "grafica1VS.html"), encoding="utf-8").read(), sizing_mode="stretch_width")
desc2 = Div(text=open(join(dirname(__file__), "grafica2VS.html"), encoding="utf-8").read(), sizing_mode="stretch_width")
desc3 = Div(text=open(join(dirname(__file__), "grafica3VS.html"), encoding="utf-8").read(), sizing_mode="stretch_width")
desc3v2 = Div(text=open(join(dirname(__file__), "grafica3v2VS.html"), encoding="utf-8").read(), sizing_mode="stretch_width")
desc3v3 = Div(text=open(join(dirname(__file__), "grafica3v3VS.html"), encoding="utf-8").read(), sizing_mode="stretch_width")
desc4 = Div(text=open(join(dirname(__file__), "grafica4VS.html"), encoding="utf-8").read(), sizing_mode="stretch_width")
curdoc().add_root(column(desc0))

# csv_path_ed1 = r"../../../CSVs/Unificar Abr-Jun25/Curso accesibilidad/Reporte CursoAcces.csv" # enlace de la edicion 2 anterior
csv_path_ed1 = r"../../../CSVs/Unificar Oct-Nov24/xd.csv"
csv_path_ed2 = r"../../../CSVs/Unificar Abr-Jun25 Nuevo/Reporte CursoAccesActual.csv"

json_ed1 = "../../../Jsonl/course-creaaa1/course-creaaa1-limpio.json"
json_ed2 = "../../../Jsonl/course-v1_/course-v1_UTPL_CREAA2limpio.json"

data_ed1 = pd.read_csv(csv_path_ed1)
data_ed2 = pd.read_csv(csv_path_ed2)

# Columnas de evaluación por edición
# eval_ed1 = ["EvalSemanal 01", "EvalSemanal 02", "EvalSemanal 03", "EvalSemanal 04", "EvalLud 01", "EvalLud 02"] # Para la comparación entre mismas ediciones
eval_ed1 = ["EvalSemanal 01", "EvalSemanal 02", "EvalSemanal 03", "EvalSemanal 04"]
eval_ed2 = ["EvalSemanal 01", "EvalSemanal 02", "EvalSemanal 03", "EvalSemanal 04", "EvalLud 01", "EvalLud 02"]

# 📺 Mapeo código a nombre para los videos
codigo_a_nombre = {
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
    "LR_1_Video1_Semana2": "o5VwDVJ7N3Q",
    "LR_1_Video2_Semana2": "LluqYlh2xg4",
    "LR_1_Video3_Semana2": "eE658thjDj8",
    "LR_1_Video4_Semana2": "QbEpClHzTeM",
    "LR_1_Video5_Semana2": "MCG0or2ULB4",
    "LR_1_Video6_Semana2": "ol-vGTdHBNU",
    "LR_1_Video7_Semana2": "WTXS0IMQ3Ss",
    "LR_1_Video8_Semana2": "9kqXmM3b3wc"
}
nombre_a_codigo = {v: k for k, v in codigo_a_nombre.items()}

# 📊 Cargar datos de JSON y CSV
json1_df = cargar_json(json_ed1)
json2_df = cargar_json(json_ed2)
df_ed1 = pd.read_csv(csv_path_ed1)
df_ed2 = pd.read_csv(csv_path_ed2)

# 📈 Calcular usuarios únicos por video (play_video)
ed1_usuarios = contar_usuarios_unicos_por_video(json1_df)
ed2_usuarios = contar_usuarios_unicos_por_video(json2_df)

# 📈 Datos para gráfico de líneas
df_linea = preparar_datos_linea(ed1_usuarios, ed2_usuarios, nombre_a_codigo)
source_linea = ColumnDataSource(df_linea)

# print(source_linea.data)

# 🎯 Crear gráfico de líneas
p_lineas = figure(
    x_range=df_linea["Video"],
    title="Usuarios únicos por Video (Comparación Ediciones)",
    x_axis_label="Video",
    y_axis_label="Usuarios Únicos",
    width=1100,
    height=400,
    toolbar_location="above",
    tools="pan,wheel_zoom,box_zoom,reset,save"
)

p_lineas.add_tools(
    HoverTool(tooltips=[("Video", "@Video"), ("Edición 1", "@{Edición 1}"), ("Edición 2", "@{Edición 2}")], 
            show_arrow=False,
            point_policy='follow_mouse'))

p_lineas.line(x="Video", y="Edición 1", source=source_linea, line_width=2, color=Spectral4[0], legend_label="Edición 1")
p_lineas.line(x="Video", y="Edición 2", source=source_linea, line_width=2, color=Spectral4[1], legend_label="Edición 2")

p_lineas.circle(x="Video", y="Edición 1", source=source_linea, size=6, color=Spectral4[0])
p_lineas.circle(x="Video", y="Edición 2", source=source_linea, size=6, color=Spectral4[1])

p_lineas.xaxis.major_label_orientation = pi / 2
p_lineas.legend.location = "top_left"
p_lineas.legend.click_policy="mute"


# 🎯 Datos de pastel para Edición 1 (EvalSemanal Avg + FormAutoevaluacion Avg)
ap1, rep1 = calcular_estado_aprobacion(df_ed1, ["EvalSemanal Avg", "FormAutoevaluacion Avg"])
data_pie1 = generar_pie_data(ap1, rep1)
source_pie1 = ColumnDataSource(data_pie1)

p_pastel1 = figure(title="Edición 1 - Aprobados vs Reprobados", width=400, height=400)

p_pastel1.add_tools(
    HoverTool(tooltips=[("Porcentaje", "@Porcentaje{0.0%}"), ("Estado:", "@Estado"), ("Cantidad", "@Cantidad"),], 
            show_arrow=False,
            point_policy='follow_mouse'))

p_pastel1.wedge(x=0, y=0, radius=0.8,
    start_angle=cumsum("angle", include_zero=True), end_angle=cumsum("angle"),
    line_color="white", fill_color="color", legend_field="Estado", source=source_pie1)
p_pastel1.axis.visible = False
p_pastel1.grid.grid_line_color = None

# 🎯 Datos de pastel para Edición 2 (promedio de 3 columnas)
ap2, rep2 = calcular_estado_aprobacion(df_ed2, ["EvalSemanal 01", "EvalSemanal 02", "EvalSemanal 03"])
data_pie2 = generar_pie_data(ap2, rep2)
source_pie2 = ColumnDataSource(data_pie2)

p_pastel2 = figure(title="Edición 2 - Aprobados vs Reprobados", width=400, height=400)

p_pastel2.add_tools(
    HoverTool(tooltips=[("Porcentaje", "@Porcentaje{0.0%}"), ("Estado:", "@Estado"), ("Cantidad", "@Cantidad"),], 
            show_arrow=False,
            point_policy='follow_mouse'
            ))

p_pastel2.wedge(x=0, y=0, radius=0.8,
    start_angle=cumsum("angle", include_zero=True), end_angle=cumsum("angle"),
    line_color="white", fill_color="color", legend_field="Estado", source=source_pie2)
p_pastel2.axis.visible = False
p_pastel2.grid.grid_line_color = None



'''
#################################
    OTRAS GRAFICAS
#################################
'''

# Cargar CSVs
df_ed1 = pd.read_csv(csv_path_ed1)
df_ed2 = pd.read_csv(csv_path_ed2)

actividad_df_completo = preparar_dataframe_conjunto(df_ed1, df_ed2, excluir_ceros=False)
actividad_df_sin_ceros = preparar_dataframe_conjunto(df_ed1, df_ed2, excluir_ceros=True)

# 🧩 Layout final
layout = column(desc1,
    row(p_pastel1, p_pastel2),
    p_lineas,
    desc4,
    generar_graficas(actividad_df_completo, "(incluyendo estudiantes con nota 0)"),
    generar_graficas(actividad_df_sin_ceros, "(excluyendo estudiantes con nota 0)")
)

curdoc().add_root(layout)
curdoc().title = "Comparación Ediciones"

########################################################################################
def generar_figuras_por_edicion(data, titulo_barras, titulo_pastel):
    total_estudiantes = len(data)
    total_aprobados = len(data[data["grade"] >= 0.7])
    total_reprobados = len(data[data["grade"] < 0.7])
    total_inactivos = len(data[data["grade"] == 0])
    total_reprobados_sin_inactivos = total_reprobados - total_inactivos

    # GRAFICA DE BARRAS
    df = pd.DataFrame({
        "Categoría": ["Total Estudiantes", "Inactivos", "Reprobados Totales", "Aprobados", "Reprobados no Inactivos"],
        "Cantidad": [total_estudiantes, total_inactivos, total_reprobados, total_aprobados, total_reprobados_sin_inactivos],
        "Color": ["orange", "gray", "crimson", "green", "red"]
    })
    source_bar = ColumnDataSource(df)
    p_bar = figure(
        x_range=FactorRange(*df["Categoría"].astype(str)),
        title=titulo_barras,
        x_axis_label="Categoría",
        y_axis_label="Cantidad",
        width=600,
        height=400
    )
    p_bar.vbar(x="Categoría", top="Cantidad", source=source_bar, width=0.6, color="Color")
    p_bar.add_tools(HoverTool(tooltips=[("Cantidad", "@Cantidad")], show_arrow=False, point_policy='follow_mouse'))

    # GRAFICA PASTEL
    df_pie = pd.DataFrame({
        "Estado": ["Aprobado", "Reprobado"],
        "Cantidad": [total_aprobados, total_reprobados],
        "color": ["green", "crimson"]
    })
    df_pie["Porcentaje"] = df_pie["Cantidad"] / df_pie["Cantidad"].sum()
    df_pie["angle"] = df_pie["Porcentaje"] * 2 * pi
    source_pie = ColumnDataSource(df_pie)
    p_pie = figure(title=titulo_pastel, width=400, height=400)
    p_pie.wedge(
        x=0, y=0, radius=0.8,
        start_angle=cumsum('angle', include_zero=True),
        end_angle=cumsum('angle'),
        line_color='white',
        fill_color='color',
        source=source_pie,
        legend_field='Estado'
    )
    p_pie.axis.axis_label = None
    p_pie.axis.visible = False
    p_pie.grid.grid_line_color = None
    p_pie.add_tools(HoverTool(
        tooltips=[("Estado", "@Estado"), ("Cantidad", "@Cantidad"), ("Porcentaje", "@Porcentaje{0.0%}")],
        show_arrow=False,
        point_policy='follow_mouse'
    ))

    return p_bar, p_pie

def generar_grafica_porcentaje_semanal(data, columnas, titulo):
    total = len(data)
    resultados = []

    for col in columnas:
        aprobados = len(data[data[col] >= 0.7])
        reprobados = len(data[data[col] < 0.7])
        resultados.append({
            "Semana": col,
            "Estado": "Aprobado",
            "Porcentaje": round((aprobados / total) * 100, 2),
            "Cantidad": aprobados
        })
        resultados.append({
            "Semana": col,
            "Estado": "Reprobado",
            "Porcentaje": round((reprobados / total) * 100, 2),
            "Cantidad": reprobados
        })

    df_resultado = pd.DataFrame(resultados)
    df_resultado["Color"] = df_resultado["Estado"].map({"Aprobado": "green", "Reprobado": "crimson"})
    df_resultado["x"] = list(zip(df_resultado["Semana"], df_resultado["Estado"]))  # clave combinada

    source = ColumnDataSource(df_resultado)

    p = figure(
        x_range=FactorRange(*df_resultado["x"]),
        title=titulo,
        y_range=(0, 100),
        x_axis_label="Semana",
        y_axis_label="Porcentaje (%)",
        width=700,
        height=400
    )

    p.vbar(
        x="x",
        top="Porcentaje",
        width=0.6,
        color="Color",
        legend_field="Estado",
        source=source
    )

    # Hover con porcentaje y cantidad
    p.add_tools(HoverTool(tooltips=[
        ("Semana", "@Semana"),
        ("Estado", "@Estado"),
        ("Cantidad", "@Cantidad"),
        ("Porcentaje", "@Porcentaje%")
    ]))

    p.xaxis.major_label_orientation = pi / 4
    p.legend.orientation = "horizontal"
    p.legend.location = "top_center"

    return p

def generar_grafica_porcentaje_sin_inactivos(data, columnas, titulo):
    resultados = []
    total_estudiantes = len(data)

    for col in columnas:
        # Subconjuntos por estado
        col_aprobados = data[(data["grade"] != 0) & (data[col] >= 0.7)]
        col_reprobados = data[(data["grade"] != 0) & (data[col] < 0.7) & (data[col] != 0)]
        col_inactivos = data[data[col] == 0]

        total_validos = len(col_aprobados) + len(col_reprobados)
        total_semana = total_validos + len(col_inactivos)

        # Cálculos de porcentaje
        porcentaje_ap = round((len(col_aprobados) / total_semana) * 100, 2) if total_semana else 0
        porcentaje_rep = round((len(col_reprobados) / total_semana) * 100, 2) if total_semana else 0
        porcentaje_inac = round((len(col_inactivos) / total_semana) * 100, 2) if total_semana else 0

        # Añadir resultados
        resultados.append({
            "Semana": col,
            "Estado": "Aprobado",
            "Porcentaje": porcentaje_ap,
            "Cantidad": len(col_aprobados)
        })
        resultados.append({
            "Semana": col,
            "Estado": "Reprobado",
            "Porcentaje": porcentaje_rep,
            "Cantidad": len(col_reprobados)
        })
        resultados.append({
            "Semana": col,
            "Estado": "Inactivo",
            "Porcentaje": porcentaje_inac,
            "Cantidad": len(col_inactivos)
        })

    df_resultado = pd.DataFrame(resultados)
    df_resultado["Color"] = df_resultado["Estado"].map({
        "Aprobado": "green", 
        "Reprobado": "crimson", 
        "Inactivo": "gray"
    })
    df_resultado["x"] = list(zip(df_resultado["Semana"], df_resultado["Estado"]))

    source = ColumnDataSource(df_resultado)

    p = figure(
        x_range=FactorRange(*df_resultado["x"]),
        title=titulo,
        y_range=(0, 100),
        x_axis_label="Semana",
        y_axis_label="Porcentaje (%)",
        width=700,
        height=400
    )

    p.vbar(
        x="x",
        top="Porcentaje",
        width=0.6,
        color="Color",
        legend_field="Estado",
        source=source
    )

    p.add_tools(HoverTool(tooltips=[
        ("Semana", "@Semana"),
        ("Estado", "@Estado"),
        ("Cantidad", "@Cantidad"),
        ("Porcentaje", "@Porcentaje%")
    ]))

    p.xaxis.major_label_orientation = pi / 4
    p.legend.orientation = "horizontal"
    p.legend.location = "top_center"

    return p

bar1, pie1 = generar_figuras_por_edicion(data_ed1,
    "Edición 1: Estudiantes Totales, Aprobados, Reprobados", 
    "Edición 1: Porcentaje Aprobados vs Reprobados")

bar2, pie2 = generar_figuras_por_edicion(data_ed2,
    "Edición 2: Estudiantes Totales, Aprobados, Reprobados", 
    "Edición 2: Porcentaje Aprobados vs Reprobados")

# Crear gráficas de porcentaje por semana
grafica_porcentaje_ed1 = generar_grafica_porcentaje_semanal(
    data_ed1, eval_ed1, "Edición 1: % Aprobados y Reprobados por Semana")

grafica_porcentaje_ed2 = generar_grafica_porcentaje_semanal(
    data_ed2, eval_ed2, "Edición 2: % Aprobados y Reprobados por Semana")

grafica_porcentaje_ed1_sin_inactivos = generar_grafica_porcentaje_sin_inactivos(
    data_ed1, eval_ed1, "Edición 1: % Aprobados y Reprobados (sin Inactivos) por Semana")

grafica_porcentaje_ed2_sin_inactivos = generar_grafica_porcentaje_sin_inactivos(
    data_ed2, eval_ed2, "Edición 2: % Aprobados y Reprobados (sin Inactivos) por Semana")

# Añadir al docuemtno
curdoc().add_root(column(desc2,row(bar1, bar2)))
curdoc().add_root(column(desc3,row(pie1, pie2)))
curdoc().add_root(column(desc3v2,row(grafica_porcentaje_ed1, grafica_porcentaje_ed2)))
curdoc().add_root(column(desc3v3,row(grafica_porcentaje_ed1_sin_inactivos, grafica_porcentaje_ed2_sin_inactivos)))



