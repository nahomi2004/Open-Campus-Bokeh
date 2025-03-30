import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Select, HoverTool, FactorRange
from bokeh.layouts import column
from bokeh.io import curdoc
from bokeh.palettes import Category10
from bokeh.transform import factor_cmap, dodge, factor_mark
from bokeh.models import CDSView, GroupFilter
from bokeh.models import Div
from math import pi
from bokeh.transform import cumsum
import numpy as np
from os.path import dirname, join
from bokeh.models import LabelSet, ColumnDataSource
from bokeh.plotting import figure, curdoc
from bokeh.layouts import column
from bokeh.palettes import Spectral4


# Direccionar al html
from os.path import dirname, join
from bokeh.models import Div

desc0 = Div(text=open(join(dirname(__file__), "title.html")).read(), sizing_mode="stretch_width")
desc = Div(text=open(join(dirname(__file__), "grafica1.html")).read(), sizing_mode="stretch_width")
desc1 = Div(text=open(join(dirname(__file__), "grafica2.html")).read(), sizing_mode="stretch_width")
desc2 = Div(text=open(join(dirname(__file__), "grafica3.html")).read(), sizing_mode="stretch_width")
desc3 = Div(text=open(join(dirname(__file__), "grafica4.html")).read(), sizing_mode="stretch_width")

# Cargar el archivo CSV
csv_path = r"D:/Users/LENOVO/Desktop/Codigo-OpenCampus/CSVs/Unificacar_CSVs/xd.csv"
data = pd.read_csv(csv_path, delimiter=',')

curdoc().add_root(column(desc0))

# Contar total de estudiantes
total_estudiantes = len(data)

# Contar aprobados y reprobados según la columna "grade"
total_aprobados = len(data[data["grade"] >= 0.7])
total_reprobados = len(data[data["grade"] < 0.7])

# Crear un DataFrame con los valores
df_estudiantes = pd.DataFrame({
    "Categoría": ["Total Estudiantes", "Aprobados", "Reprobados"],
    "Cantidad": [total_estudiantes, total_aprobados, total_reprobados]
})

df_estudiantes["Color"] = ["grey", "green", "crimson"]

# Actualizar la fuente de datos
source_estudiantes = ColumnDataSource(df_estudiantes)

''' 
GRAFICA 1: Total de estudiantes, aprobados y reprobados 
'''
# Crear la figura
p_estudiantes = figure(
    x_range=FactorRange(*df_estudiantes["Categoría"].astype(str)),  
    title="Cantidad de Estudiantes: Totales, Aprobados y Reprobados",
    x_axis_label="Categoría",
    y_axis_label="Cantidad",
    width=800,
    height=400
)

# Agregar las barras correctamente
p_estudiantes.vbar(
    x="Categoría", 
    top="Cantidad",  
    source=source_estudiantes, 
    width=0.6, 
    color="Color"
)

# Agregar al documento
curdoc().add_root(column(desc, p_estudiantes))

''' 
GRAFICA 2: Promedios por Evaluacion Semanal
'''
# Columnas de evaluación semanal
eval_columns = ["EvalSemanal 01", "EvalSemanal 02", "EvalSemanal 03", "EvalSemanal 04"]

# Calcular promedio por semana
promedios_semanales = data[eval_columns].mean()

# Crear DataFrame con los valores
hist_data = pd.DataFrame({
    "Semana": eval_columns,
    "Promedio": promedios_semanales
})

# Fuente de datos para Bokeh
source_hist = ColumnDataSource(hist_data)

# Crear la figura para el histograma
p_hist = figure(
    x_range=FactorRange(*hist_data["Semana"].astype(str)),  
    title="Promedio de Notas por Semana",
    x_axis_label="Semana",
    y_axis_label="Promedio",
    width=800,
    height=400
)

# Agregar barras al histograma
p_hist.vbar(
    x="Semana", 
    top="Promedio",  
    source=source_hist, 
    width=0.6, 
    color="dodgerblue"
)

# Agregar línea de tendencia
p_hist.line(
    x=hist_data["Semana"], 
    y=hist_data["Promedio"], 
    line_width=2, 
    color="red"
)

# Agregar las gráficas al documento
curdoc().add_root(column(desc1, p_hist))

''' 
GRAFICA 2.2: Promedios por Evaluacion Semanal (Excluyendo estudiantes con solo 0s)
'''
# eval_columns = ["EvalSemanal 01", "EvalSemanal 02", "EvalSemanal 03", "EvalSemanal 04"]

# Filtrar estudiantes que no tengan 0 en todas las evaluaciones
filtered_data = data[(data[eval_columns] != 0).any(axis=1)]

# Calcular promedios por semana
data_avg_filtered = filtered_data[eval_columns].mean()

# Crear DataFrame con los valores
hist_data_filtered = pd.DataFrame({
    "Semana": eval_columns,
    "Promedio": data_avg_filtered
})

# Fuente de datos para Bokeh
source_hist_filtered = ColumnDataSource(hist_data_filtered)

# Crear la figura para el histograma
p_hist_filtered = figure(
    x_range=FactorRange(*hist_data_filtered["Semana"].astype(str)),  
    title="Promedio de Notas por Semana (Excluyendo Solo 0s Totales)",
    x_axis_label="Semana",
    y_axis_label="Promedio",
    width=800,
    height=400
)

# Agregar barras al histograma
p_hist_filtered.vbar(
    x="Semana", 
    top="Promedio",  
    source=source_hist_filtered, 
    width=0.6, 
    color="orange"
)

# Agregar línea de tendencia
p_hist_filtered.line(
    x=hist_data_filtered["Semana"], 
    y=hist_data_filtered["Promedio"], 
    line_width=2, 
    color="red"
)

curdoc().add_root(column(desc2, p_hist_filtered))

''' 
GRAFICA 3: Cantidad de personas que tienen una nota menor y mayor a 7
'''
# Calcular cantidad de aprobados y reprobados por semana
aprobados = [len(data[data[col] >= 0.7]) for col in eval_columns]
reprobados = [len(data[data[col] < 0.7]) for col in eval_columns]

# Crear DataFrame con los valores
df_estudiantes = pd.DataFrame({
    "Semana": eval_columns,
    "Aprobados": aprobados,
    "Reprobados": reprobados
})

# Fuente de datos para Bokeh
source_aprepo = ColumnDataSource(df_estudiantes)

# Crear la figura
p_aprepo = figure(
    x_range=FactorRange(*df_estudiantes["Semana"].astype(str)),  
    title="Cantidad de Estudiantes Aprobados y Reprobados por Semana",
    x_axis_label="Semana",
    y_axis_label="Cantidad",
    width=800,
    height=400
)

# Apilar las barras correctamente
p_aprepo.vbar(
    x=dodge("Semana", -0.15, range=p_aprepo.x_range), 
    top="Aprobados",  
    source=source_aprepo, 
    width=0.3, 
    color="green",
    legend_label="Aprobados"
)

p_aprepo.vbar(
    x=dodge("Semana", 0.15, range=p_aprepo.x_range), 
    top="Reprobados",  
    source=source_aprepo, 
    width=0.3, 
    color="crimson",
    legend_label="Reprobados"
)

# Configurar leyenda
p_aprepo.legend.location = "top_right"

# Agregar al documento
curdoc().add_root(column(desc3, p_aprepo))

''' 
GRAFICA 3.2: Cantidad de personas que tienen una nota menor y mayor a 7 (Excluyendo estudiantes con solo 0s)
'''
# Filtrar estudiantes que no tengan 0 en todas las evaluaciones
filtered_data_aprepo = data[(data[eval_columns] != 0).any(axis=1)]

# Calcular cantidad de aprobados y reprobados por semana después del filtro
aprobados_filtered = [len(filtered_data_aprepo[filtered_data_aprepo[col] >= 0.7]) for col in eval_columns]
reprobados_filtered = [len(filtered_data_aprepo[filtered_data_aprepo[col] < 0.7]) for col in eval_columns]

# Crear DataFrame con los valores filtrados
df_aprepo_filtered = pd.DataFrame({
    "Semana": eval_columns,
    "Aprobados": aprobados_filtered,
    "Reprobados": reprobados_filtered
})

# Fuente de datos para Bokeh
source_aprepo_filtered = ColumnDataSource(df_aprepo_filtered)

# Crear la figura
p_aprepo_filtered = figure(
    x_range=FactorRange(*df_aprepo_filtered["Semana"].astype(str)),  
    title="Cantidad de Estudiantes Aprobados y Reprobados por Semana (Excluyendo Solo 0s Totales)",
    x_axis_label="Semana",
    y_axis_label="Cantidad",
    width=800,
    height=400
)

# Apilar las barras correctamente
p_aprepo_filtered.vbar(
    x=dodge("Semana", -0.15, range=p_aprepo_filtered.x_range), 
    top="Aprobados",  
    source=source_aprepo_filtered, 
    width=0.3, 
    color="green",
    legend_label="Aprobados"
)

p_aprepo_filtered.vbar(
    x=dodge("Semana", 0.15, range=p_aprepo_filtered.x_range), 
    top="Reprobados",  
    source=source_aprepo_filtered, 
    width=0.3, 
    color="crimson",
    legend_label="Reprobados"
)

# Configurar leyenda
p_aprepo_filtered.legend.location = "top_right"

# Agregar la gráfica al documento
curdoc().add_root(column(desc3, p_aprepo_filtered))



