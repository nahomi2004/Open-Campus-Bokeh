import pandas as pd
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, HoverTool, FactorRange, Div
from bokeh.layouts import column, row
from bokeh.transform import cumsum
from math import pi
from os.path import dirname, join

desc0 = Div(text=open(join(dirname(__file__), "TituloACCS1vs2.html"), encoding="utf-8").read(), sizing_mode="stretch_width")
desc1 = Div(text=open(join(dirname(__file__), "grafica1VS.html"), encoding="utf-8").read(), sizing_mode="stretch_width")
desc2 = Div(text=open(join(dirname(__file__), "grafica2VS.html"), encoding="utf-8").read(), sizing_mode="stretch_width")
curdoc().add_root(column(desc0))

csv_path_ed1 = r"../../../CSVs/Unificar Oct-Nov24/xd.csv"
csv_path_ed2 = r"../../../CSVs/Unificar Abr-Jun25 Nuevo/Reporte CursoAccesActual.csv"

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

data_ed1 = pd.read_csv(csv_path_ed1)
data_ed2 = pd.read_csv(csv_path_ed2)

bar1, pie1 = generar_figuras_por_edicion(data_ed1,
    "Edición 1: Estudiantes Totales, Aprobados, Reprobados", 
    "Edición 1: Porcentaje Aprobados vs Reprobados")

bar2, pie2 = generar_figuras_por_edicion(data_ed2,
    "Edición 2: Estudiantes Totales, Aprobados, Reprobados", 
    "Edición 2: Porcentaje Aprobados vs Reprobados")

# Añadir al docuemtno
curdoc().add_root(column(desc1, row(bar1, bar2)))
curdoc().add_root(column(desc2,row(pie1, pie2)))
