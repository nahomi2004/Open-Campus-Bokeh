import pandas as pd

# Ruta del archivo
ruta_csv = r"C:\Users\nahom\OneDrive - Universidad Técnica Particular de Loja - UTPL\Curso Documentos Accesibles\CSV\UTPL_CREAA1_2024_2_grade_report_2024-11-08-2038.csv"
ruta_salida = r"C:\Users\nahom\OneDrive - Universidad Técnica Particular de Loja - UTPL\Curso Documentos Accesibles\CSV\datos-evaluacion-sem1.txt"

# Leer el archivo CSV
df = pd.read_csv(ruta_csv, delimiter=',')

# Seleccionar la columna "EvalSemanal 01"
columna_eval = df["EvalSemanal 01"]

# Calcular la frecuencia de los valores
frecuencia = columna_eval.value_counts().sort_index()

# Calcular el número total de datos
total_datos = len(columna_eval)

# Guardar los resultados en un archivo .txt
with open(ruta_salida, "w") as file:
    file.write("Frecuencia de valores en la columna 'EvalSemanal 01':\n")
    file.write(frecuencia.to_string())
    file.write(f"\n\nNúmero total de datos: {total_datos}")

print(f"Los resultados han sido guardados en: {ruta_salida}")
