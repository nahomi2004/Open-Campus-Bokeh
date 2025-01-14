import pandas as pd
import matplotlib.pyplot as plt
import os

# Ruta del archivo CSV y archivo de salida
ruta_csv = r"C:\Users\nahom\OneDrive - Universidad Técnica Particular de Loja - UTPL\Curso Documentos Accesibles\CSV\tercero\UTPL_CREAA1_2024_2_grade_report_2024-12-02-1435.csv"
ruta_salida_txt = r"C:\Users\nahom\OneDrive - Universidad Técnica Particular de Loja - UTPL\Curso Documentos Accesibles\CSV\datos-evaluacion-semanas.txt"

# Leer el archivo CSV
df = pd.read_csv(ruta_csv, delimiter=',')

# Seleccionar la columna "EvalSemanal 01"
columna_eval = df["EvalSemanal 01"]

# Calcular la frecuencia de los valores
frecuencia = columna_eval.value_counts().sort_index()

# Calcular el número total de datos
total_datos = len(columna_eval)

# Guardar los resultados en un archivo .txt
with open(ruta_salida_txt, "w") as file:
    file.write("Frecuencia de valores en la columna 'EvalSemanal 01':\n")
    file.write(frecuencia.to_string())
    file.write(f"\n\nNúmero total de datos: {total_datos}")

# Ruta base para guardar los gráficos
ruta_base = os.path.dirname(ruta_salida_txt)

# Generar gráfico de barras
plt.figure(figsize=(10, 6))
frecuencia.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title("Frecuencia de valores - EvalSemanal 01")
plt.xlabel("Valores")
plt.ylabel("Frecuencia")
plt.xticks(rotation=45)
plt.tight_layout()
ruta_grafico_barras = os.path.join(ruta_base, "grafico_barras_eval_semana01.jpg")
plt.savefig(ruta_grafico_barras)
plt.close()

# Generar gráfico de pastel
plt.figure(figsize=(8, 8))
frecuencia.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=plt.cm.tab10.colors)
plt.title("Distribución porcentual - EvalSemanal 01")
plt.ylabel("")  # Quitar etiqueta del eje y
ruta_grafico_pastel = os.path.join(ruta_base, "grafico_pastel_eval_semana01.jpg")
plt.savefig(ruta_grafico_pastel)
plt.close()

print(f"Los resultados han sido guardados en: {ruta_salida_txt}")
print(f"Gráfico de barras guardado en: {ruta_grafico_barras}")
print(f"Gráfico de pastel guardado en: {ruta_grafico_pastel}")
