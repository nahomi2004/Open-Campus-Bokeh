import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Div
from bokeh.palettes import Category10
from bokeh.transform import factor_cmap
from bokeh.layouts import column, row
from bokeh.io import output_file, show, curdoc
from math import pi

# Para la dirección del HTML
from os.path import dirname, join

desc = Div(text=open(join(dirname(__file__), "estudiantes2.html")).read(), sizing_mode="stretch_width")

# Cargar los archivos CSV
csv_profile_path = r"../../../CSVs/UTPL_CREAA1_2024_2_student_profile_info_2025-02-12-2117.csv"
csv_grade_path = r"../../../CSVs/UTPL_CREAA1_2024_2_grade_report_2025-02-12-2116.csv"

dataProfile = pd.read_csv(csv_profile_path, delimiter=',')
dataGrade = pd.read_csv(csv_grade_path, delimiter=',')

# Unir los CSVs por "username"
data = pd.merge(dataProfile, dataGrade, on="username")

# Definir el puntaje mínimo requerido
puntaje_minimo = 0.7  

data_no_filtrada = data
data_no_filtrada["gender"] = data["gender"].fillna("Desconocido")
print(data_no_filtrada)
conteo_genero_0 = data_no_filtrada["gender"].value_counts().reset_index()
print(conteo_genero_0)
conteo_genero_0.columns = ["Género", "Cantidad"]

# Filtrar los estudiantes que no alcanzaron el puntaje mínimo en "EvalSemanal Avg"
data_filtrada = data[data["EvalSemanal Avg"] < puntaje_minimo]
data_filtrada_apro = data[data["EvalSemanal Avg"] > puntaje_minimo]

# Reemplazar valores NaN en "gender"
data_filtrada["gender"] = data_filtrada["gender"].fillna("Desconocido")
data_filtrada_apro["gender"] = data_filtrada_apro["gender"].fillna("Desconocido")

# Contar cantidad de estudiantes por género
conteo_genero = data_filtrada["gender"].value_counts().reset_index()
conteo_genero_apro = data_filtrada_apro["gender"].value_counts().reset_index()
print(conteo_genero)
conteo_genero.columns = ["Género", "Cantidad"]
conteo_genero_apro.columns = ["Género", "Cantidad"]

# Crear la fuente de datos para Bokeh
source_bar = ColumnDataSource(conteo_genero)
source_bar_apro = ColumnDataSource(conteo_genero_apro)
source_bar_total = ColumnDataSource(conteo_genero_0)

# Paleta de colores
colores0 = Category10[len(conteo_genero_0)]

# 📊 **Gráfico de Barras**
p_barras_0 = figure(
    x_range=conteo_genero_0["Género"],
    title="Cantidad de Estudiantes",
    x_axis_label="Género",
    y_axis_label="Cantidad",
    width=500,
    height=400
)

p_barras_0.vbar(
    x="Género",
    top="Cantidad",
    source=source_bar_total,
    width=0.6,
    color=factor_cmap("Género", palette=colores0, factors=conteo_genero_0["Género"])
)

curdoc().add_root(column(desc, p_barras_0))

# Paleta de colores
colores = Category10[len(conteo_genero)]

# 📊 **Gráfico de Barras**
p_barras = figure(
    x_range=conteo_genero["Género"],
    title="Cantidad de Estudiantes que NO Alcanzaron el Puntaje Mínimo en las Evaluaciones",
    x_axis_label="Género",
    y_axis_label="Cantidad",
    width=500,
    height=400
)

p_barras.vbar(
    x="Género",
    top="Cantidad",
    source=source_bar,
    width=0.6,
    color=factor_cmap("Género", palette=colores, factors=conteo_genero["Género"])
)

curdoc().add_root(column(desc, p_barras))


# 📊 **Gráfico de Barras**
p_barras2 = figure(
    x_range=conteo_genero_apro["Género"],
    title="Cantidad de Estudiantes que SI Alcanzaron el Puntaje Mínimo en las Evaluaciones",
    x_axis_label="Género",
    y_axis_label="Cantidad",
    width=500,
    height=400
)

p_barras2.vbar(
    x="Género",
    top="Cantidad",
    source=source_bar_apro,
    width=0.6,
    color=factor_cmap("Género", palette=colores0, factors=conteo_genero_apro["Género"])
)

curdoc().add_root(column(desc, p_barras2))


# 📊 **Gráfico de Pastel**
data_pie = conteo_genero.copy()
data_pie["angle"] = data_pie["Cantidad"] / data_pie["Cantidad"].sum() * 2 * pi
data_pie["color"] = colores[:len(data_pie)]

source_pie = ColumnDataSource(data_pie)

p_pastel = figure(
    title="Distribución de Género en los que No Alcanzaron el Puntaje Mínimo",
    width=500,
    height=400,
    tools="",
    toolbar_location=None
)

p_pastel.wedge(
    x=0,
    y=0,
    radius=0.8,
    start_angle="angle",
    end_angle={"field": "angle", "transform": lambda a: a.cumsum()},
    fill_color="color",
    source=source_pie,
    legend_field="Género"
)

p_pastel.axis.axis_label = None
p_pastel.axis.visible = False
p_pastel.grid.grid_line_color = None

curdoc().add_root(column(desc, p_pastel))

# 📊 **Gráfico de Dispersión**
source_dispersion = ColumnDataSource(data_filtrada)

p_dispersion = figure(
    title="Distribución de Puntajes de Estudiantes que No Alcanzaron el Mínimo",
    x_range=["EvalSemanal Avg"],
    y_range=(0, 1),
    x_axis_label="Evaluación",
    y_axis_label="Puntaje",
    width=500,
    height=400
)

p_dispersion.scatter(
    x="EvalSemanal Avg",
    y="EvalSemanal Avg",
    source=source_dispersion,
    color=factor_cmap("gender", palette=colores, factors=conteo_genero["Género"]),
    size=10,
    fill_alpha=0.6
)

curdoc().add_root(column(desc, p_dispersion))
