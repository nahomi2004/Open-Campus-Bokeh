import pandas as pd
import os

# Rutas de los archivos CSV
file1 = r"D:/Users/LENOVO/Desktop/Codigo-OpenCampus/CSVs/Unificacar_CSVs/UTPL_CREAA1_2024_2_student_profile_info_2025-02-12-2117.csv"
file2 = r"D:/Users/LENOVO/Desktop/Codigo-OpenCampus/CSVs/Unificacar_CSVs/UTPL_CREAA1_2024_2_grade_report_2025-02-12-2116.csv"
output_file = r"D:/Users/LENOVO/Desktop/Codigo-OpenCampus/CSVs/Unificacar_CSVs/UTPL_CREAA1_2024_2_profile&grade_totalreport_2025.csv"

# Verificar si los archivos existen
if not os.path.exists(file1) or not os.path.exists(file2):
    print("⚠️ Error: Uno o ambos archivos no existen.")
    exit()

try:
    # 📌 Cargar ambos CSVs
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    print("📊 Columnas en archivo 1:", df1.columns.tolist())
    print("📊 Columnas en archivo 2:", df2.columns.tolist())

    # 📌 Definir claves comunes para unir los archivos
    claves_comunes = ["id", "username", "email"]

    # 📌 Fusionar los DataFrames usando las claves comunes
    df_combined = pd.merge(df1, df2, on=claves_comunes, how="outer")  # Usa "outer" para no perder datos

    # 📌 Guardar el CSV unificado
    df_combined.to_csv(output_file, index=False)

    print(f"✅ CSV unificado guardado en: {output_file}")
    print(f"📊 Filas totales: {len(df_combined)} | Columnas totales: {len(df_combined.columns)}")

except Exception as e:
    print(f"❌ Error al procesar los archivos: {e}")
