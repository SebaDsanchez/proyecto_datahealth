import os
import sqlite3
import pandas as pd


def ejecutar_consultas_sql():
    print("=== EJECUTANDO ANÁLISIS SQL SOBRE EL DATASET NHANES ===")

    # 1. Definir rutas a los archivos
    ruta_csv = os.path.join("data", "processed", "nhanes_nutrition_clean.csv")
    ruta_sql = os.path.join("sql", "analytical_queries.sql")

    # 2. Cargar el dataset limpio con Pandas
    df = pd.read_csv(ruta_csv)

    # 3. Crear base de datos SQLite en memoria RAM y volcar la tabla
    conexion = sqlite3.connect(":memory:")
    df.to_sql("nutrition_records", conexion, index=False, if_exists="replace")

    # 4. Leer el archivo .sql y separar las consultas por el punto y coma (;)
    with open(ruta_sql, "r", encoding="utf-8") as archivo:
        contenido_sql = archivo.read()

    consultas = [q.strip() for q in contenido_sql.split(";") if q.strip()]

    # 5. Ejecutar cada consulta y mostrar la tabla resultante
    titulos = [
        "REPORTE 1: Estratificación de Riesgo por Sodio (CTE + CASE)",
        "REPORTE 2: Perfil Socioeconómico y Pivoteo por Género (COALESCE + CASE)",
    ]

    for i, query in enumerate(consultas):
        print(f"\n{'='*75}")
        print(f" {titulos[i]}")
        print(f"{'='*75}")
        resultado = pd.read_sql_query(query, conexion)
        print(resultado.to_string(index=False))

    conexion.close()
    print("\n✅ Ejecución de SQL finalizada con éxito.")


if __name__ == "__main__":
    ejecutar_consultas_sql()