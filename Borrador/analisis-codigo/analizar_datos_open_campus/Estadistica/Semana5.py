# pip install openpyxl
# pip install pandas
# pip install matplotlib

import pandas as pd
import matplotlib.pyplot as plt

# Ruta del archivo
ruta_excel = r"C:\Users\nahom\Downloads\dataset_aleatorio.xlsx"

# Leer el archivo Excel
df = pd.read_excel(ruta_excel)

# Seleccionar la columna "Ingreso"
ingreso = df["Ingreso"]

# Calcular las estadísticas
media = ingreso.mean()
mediana = ingreso.median()
varianza = ingreso.var()
desviacion_estandar = ingreso.std()
cuartiles = ingreso.quantile([0.25, 0.5, 0.75, 1.0])
quintiles = ingreso.quantile([0.2, 0.4, 0.6, 0.8, 1.0])

# Imprimir los resultados
print("Estadísticas de la columna 'Ingreso':")
print(f"Media: {media}")
print(f"Mediana: {mediana}")
print(f"Varianza: {varianza}")
print(f"Desviación Estándar: {desviacion_estandar}")
print("\nCuartiles:")
print(cuartiles)
print("\nQuintiles:")
print(quintiles)

# Crear el boxplot
plt.figure(figsize=(8, 6))
plt.boxplot(ingreso, vert=False, patch_artist=True)
plt.title("Boxplot de la columna 'Ingreso'")
plt.xlabel("Ingreso")
plt.show()
