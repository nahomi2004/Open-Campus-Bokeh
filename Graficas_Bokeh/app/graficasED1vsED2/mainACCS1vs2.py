import pandas as pd
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, HoverTool, FactorRange, Div
from bokeh.layouts import column, row
from bokeh.transform import cumsum
from math import pi
from os.path import dirname, join

desc0 = Div(text=open(join(dirname(__file__), "TituloACCS1vs2.html"), encoding="utf-8").read(), sizing_mode="stretch_width")
# desc1 = Div(text=open(join(dirname(__file__), "grafica1VS.html"), encoding="utf-8").read(), sizing_mode="stretch_width")
desc2 = Div(text=open(join(dirname(__file__), "grafica2VS.html"), encoding="utf-8").read(), sizing_mode="stretch_width")
desc3 = Div(text=open(join(dirname(__file__), "grafica3VS.html"), encoding="utf-8").read(), sizing_mode="stretch_width")
desc3v2 = Div(text=open(join(dirname(__file__), "grafica3v2VS.html"), encoding="utf-8").read(), sizing_mode="stretch_width")
desc3v3 = Div(text=open(join(dirname(__file__), "grafica3v3VS.html"), encoding="utf-8").read(), sizing_mode="stretch_width")
# desc4 = Div(text=open(join(dirname(__file__), "grafica4VS.html"), encoding="utf-8").read(), sizing_mode="stretch_width")
curdoc().add_root(column(desc0))

csv_path_ed1 = r"../../../CSVs/Unificar Abr-Jun25/Curso accesibilidad/Reporte CursoAcces.csv" # enlace de la edicion 2 anterior
# csv_path_ed1 = r"../../../CSVs/Unificar Oct-Nov24/xd.csv"
csv_path_ed2 = r"../../../CSVs/Unificar Abr-Jun25 Nuevo/Reporte CursoAccesActual.csv"

data_ed1 = pd.read_csv(csv_path_ed1)
data_ed2 = pd.read_csv(csv_path_ed2)

# Columnas de evaluación por edición
eval_ed1 = ["EvalSemanal 01", "EvalSemanal 02", "EvalSemanal 03", "EvalSemanal 04", "EvalLud 01", "EvalLud 02"]
eval_ed2 = ["EvalSemanal 01", "EvalSemanal 02", "EvalSemanal 03", "EvalSemanal 04", "EvalLud 01", "EvalLud 02"]

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



