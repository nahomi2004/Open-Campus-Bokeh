import pandas as pd
import os

# Rutas de los archivos CSV
csv_profile_path = r"CSVs\Unificacar_CSVs\UTPL_CREAA1_2024_2_student_profile_info_2025-02-12-2117.csv"
csv_grade_path = r"Open-Campus-Bokeh\CSVs\Unificacar_CSVs\UTPL_CREAA1_2024_2_grade_report_2025-02-12-2116.csv"
csv_niu = r"Open-Campus-Bokeh\CSVs\Unificacar_CSVs\xd.csv"


# Verificar si los archivos existen
if not os.path.exists(csv_profile_path) or not os.path.exists(csv_grade_path):
    print("⚠️ Error: Uno o ambos archivos no existen.")
    exit()

try:
    # 📌 Cargar ambos CSVs
    df1 = pd.read_csv(csv_profile_path)
    df2 = pd.read_csv(csv_grade_path)

    print("📊 Columnas en archivo 1:", df1.columns.tolist())
    print("📊 Columnas en archivo 2:", df2.columns.tolist())

    # 📌 Definir claves comunes para unir los archivos
    claves_comunes = ["id", "username", "email"]

    # 📌 Fusionar los DataFrames usando las claves comunes
    df_combined = pd.merge(df1, df2, on=claves_comunes, how="outer")  # Usa "outer" para no perder datos

    # 📌 Reemplazar celdas vacías con "N/A"
    df_combined.fillna("N/A", inplace=True)

    # 📌 Lista de usuarios a eliminar
    usuarios_excluir = ["VeronicaLuna", "NahomiCabrera", "opencampus", "reroes3100"]

    # 📌 Filtrar para eliminar esos usuarios
    df_combined = df_combined[~df_combined["username"].isin(usuarios_excluir)]

    # 📌 Guardar el CSV unificado
    df_combined.to_csv(csv_niu, index=False)

    print(f"✅ CSV unificado guardado en: {csv_niu}")
    print(f"📊 Filas después de eliminar usuarios: {len(df_combined)} | Columnas totales: {len(df_combined.columns)}")

except Exception as e:
    print(f"❌ Error al procesar los archivos: {e}")