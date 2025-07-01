# Open-Campus-Bokeh
Graficas utilizando la libreria de bokeh, con la intencion de analizar la interaccion y relacion entre, videos, estudiantes y notas 

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

from graficas_final.funciones import *

# Direccionar al html
from os.path import dirname, join
from bokeh.models import Div

'''
desc0 = Div(text=open(join(dirname(__file__), "title.html")).read(), sizing_mode="stretch_width")
desc = Div(text=open(join(dirname(__file__), "graficaBarrasFiltro.html")).read(), sizing_mode="stretch_width")
desc2 = Div(text=open(join(dirname(__file__), "graficaBarrasFiltro1.html")).read(), sizing_mode="stretch_width")
desc3 = Div(text=open(join(dirname(__file__), "graficaBarrasFiltro2.html")).read(), sizing_mode="stretch_width")
desc4 = Div(text=open(join(dirname(__file__), "graficaBarrasSimple.html")).read(), sizing_mode="stretch_width")
desc5 = Div(text=open(join(dirname(__file__), "graficaCircular.html")).read(), sizing_mode="stretch_width")
'''

# 📁 Rutas a los archivos
json_ed1 = "../../Jsonl/course-creaaa1/course-creaaa1-limpio.json"
json_ed2 = "../../Jsonl/course-v1_/course-v1_UTPL_CREAA2limpio.json"
csv_ed2_profile = "../../CSVs/Unificar Abr-Jun25/Curso accesibilidad/UTPL_CREAA2_2025_1_student_report_2025-05-19-2249.csv"
csv_ed2_grade = "../../CSVs/Unificar Abr-Jun25/Curso accesibilidad/UTPL_CREAA2_2025_1_grade_report_2025-05-19-2109.csv"

# Aprobados
data_grade = pd.read_csv(csv_ed2_grade)
aprobados = data_grade[data_grade["grade"] >= 0.7]
aprobados = aprobados[["username", "grade"]]
print(aprobados)

