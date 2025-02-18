import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Select
from bokeh.layouts import column
from bokeh.io import curdoc
from bokeh.palettes import Category10
from bokeh.transform import factor_cmap, dodge, factor_mark
from bokeh.models import CDSView, GroupFilter

# Direccionar al html
from os.path import dirname, join
from bokeh.models import Div

desc = Div(text=open(join(dirname(__file__), "estudiantes.html")).read(), sizing_mode="stretch_width")

# Cargar los archivos CSV
csv_profile_path = r"../../../CSVs/UTPL_CREAA1_2024_2_student_profile_info_2025-02-12-2117.csv"
csv_grade_path = r"../../../CSVs/UTPL_CREAA1_2024_2_grade_report_2025-02-12-2116.csv"

dataProfile = pd.read_csv(csv_profile_path, delimiter=',')
dataGrade = pd.read_csv(csv_grade_path, delimiter=',')

# Unir los CSVs por "username"
data = pd.merge(dataProfile, dataGrade, on="username")

# Columnas de evaluación semanal
eval_columns = ["EvalSemanal 01", "EvalSemanal 02", "EvalSemanal 03", "EvalSemanal 04"]

# Calcular promedios por género
data_avg = data.groupby("gender")[eval_columns].mean().reset_index()

# Convertir DataFrame a formato compatible con Bokeh
data_melted = data_avg.melt(id_vars=["gender"], var_name="Evaluación", value_name="Promedio")
# print(data_melted)

# Crear la fuente de datos inicial con un solo género seleccionado
initial_gender = data_melted["gender"].unique()[0]  # Primer género disponible
filtered_data = data_melted[data_melted["gender"] == initial_gender]
source = ColumnDataSource(filtered_data)

# Crear la figura
p = figure(
    x_range=eval_columns,  # Las evaluaciones en el eje X
    title="Promedio de Evaluaciones Semanales por Género",
    x_axis_label="Evaluaciones",
    y_axis_label="Promedio",
    width=800,
    height=400,
)

# Dibujar las barras (Inicialmente con un solo género)
p.vbar(
    x="Evaluación", 
    top="Promedio",  
    source=source, 
    width=0.6, 
    color="dodgerblue"
)

# Crear Select para cambiar el género
gender_list = data_melted["gender"].unique().tolist()
select = Select(title="Selecciona un Género:", value=initial_gender, options=gender_list)

# Función para actualizar la gráfica
def update_plot(attr, old, new):
    selected_gender = select.value
    new_data = data_melted[data_melted["gender"] == selected_gender]
    source.data = dict(ColumnDataSource(new_data).data)  # 🔹 SOLUCIÓN: Convertir a dict

select.on_change("value", update_plot)

'''
GRAFICA 2
'''
# Crear la nueva figura para promedios agrupados
p1 = figure(
    x_range=eval_columns, 
    title="Promedio por género",
    x_axis_label="Evaluación",
    y_axis_label="Promedio",
    width=1600,
    height=800,
    tools="pan,box_zoom,wheel_zoom,save,reset",
    toolbar_location="right",
)

p1.xaxis.major_label_orientation = 1.0

# Usar colores para cada género
colors = Category10[len(gender_list)]

# Ancho y desplazamiento para que las barras no se sobrepongan
width = 0.2  
offsets = [dodge("Evaluación", (i + 0.3) * width - (width * len(gender_list) / 2), range=p1.x_range) for i in range(len(gender_list))]

# Agregar barras agrupadas por género
for i, gender in enumerate(gender_list):
    # Filtrar datos manualmente para cada género
    filtered_data = data_melted[data_melted["gender"] == gender]
    source_gender = ColumnDataSource(filtered_data)
    
    p1.vbar(
        x=offsets[i], 
        top="Promedio",  # Ahora toma el promedio correcto
        source=source_gender, 
        width=width, 
        color=colors[i], 
        legend_label=gender
    )

p1.legend.title = "Género"
p1.legend.location = "top_right"

# Agregar todo al layout

curdoc().add_root(column(desc, select, p, p1))

'''
GRAFICA 3
'''
# Obtener los géneros únicos
generos = data["gender"].unique()

# Convertir DataFrame a formato compatible con Bokeh (manteniendo todos los puntajes individuales)
data_melted_2 = data.melt(
    id_vars=["username", "gender"], 
    value_vars=eval_columns,  # 🔹 Solo derretir las evaluaciones
    var_name="Evaluación", 
    value_name="Puntaje"
)

# Asegurar que la columna 'gender' sea de tipo string
data_melted_2["gender"] = data_melted_2["gender"].astype(str)
print(data_melted_2)

# Definir colores y marcadores para cada género
marcadores = ["hex", "circle_x", "triangle", "square"]
colores = Category10[len(gender_list)]

# Crear fuente de datos
source_2 = ColumnDataSource(data_melted_2)

# Crear figura
p3 = figure(
    title="Distribución de Puntajes por Género",
    x_range=eval_columns,  # Usar las evaluaciones como categorías en X
    y_range=(0.0, 1.0),
    x_axis_label="Evaluación",
    y_axis_label="Puntaje",
    width=900,
    height=600,
    tools="pan,box_zoom,wheel_zoom,save,reset",
)

# Agregar puntos de dispersión con colores y marcadores por género
p3.scatter(
    x="Evaluación",
    y="Puntaje",
    source=source_2,
    legend_group="gender",  # Usar "gender" porque así está en el DataFrame
    size=10,
    fill_alpha=0.5,
    marker=factor_mark("gender", markers=marcadores[:len(gender_list)], factors=gender_list),
    color=factor_cmap("gender", palette=colores, factors=gender_list)
)

# Configurar leyenda
p3.legend.title = "Género"
p3.legend.location = "top_right"

# Agregar la gráfica al documento sin afectar otras gráficas
curdoc().add_root(column(desc, p3))