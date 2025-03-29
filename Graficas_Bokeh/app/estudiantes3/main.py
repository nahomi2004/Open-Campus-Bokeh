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


# Direccionar al html
from os.path import dirname, join
from bokeh.models import Div

desc0 = Div(text=open(join(dirname(__file__), "title.html")).read(), sizing_mode="stretch_width")
desc = Div(text=open(join(dirname(__file__), "grafica1.html")).read(), sizing_mode="stretch_width")


# Cargar los archivos CSV
csv_profile_path = r"../../../CSVs/UTPL_CREAA1_2024_2_student_profile_info_2025-02-12-2117.csv"
csv_grade_path = r"../../../CSVs/UTPL_CREAA1_2024_2_grade_report_2025-02-12-2116.csv"

dataProfile = pd.read_csv(csv_profile_path, delimiter=',')
dataGrade = pd.read_csv(csv_grade_path, delimiter=',')

# Unir los CSVs por "username"
data = pd.merge(dataProfile, dataGrade, on="username")

# Columnas de evaluación semanal
eval_columns = ["EvalSemanal 01", "EvalSemanal 02", "EvalSemanal 03", "EvalSemanal 04"]

curdoc().add_root(column(desc0))