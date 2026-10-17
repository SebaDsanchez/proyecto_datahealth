import os
import pandas as pd


def ejecutar_pipeline():
    print("=== INICIANDO PIPELINE DE INTEGRACIÓN Y LIMPIEZA ===")

    # 1. Definir rutas relativas
    ruta_demo = os.path.join("data", "raw", "demographic.csv")
    ruta_diet = os.path.join("data", "raw", "diet.csv")
    ruta_salida = os.path.join("data", "processed", "nhanes_nutrition_clean.csv")

    # 2. Cargar datasets crudos
    print("--> Leyendo datasets crudos...")
    df_demo = pd.read_csv(ruta_demo)
    df_diet = pd.read_csv(ruta_diet)

    # 3. Filtrar columnas demográficas de interés
    cols_demo = {
        "SEQN": "seqn_id",
        "RIDAGEYR": "age_years",
        "RIAGENDR": "gender_code",
        "INDFMPIR": "poverty_ratio",
    }
    df_demo_clean = df_demo[list(cols_demo.keys())].rename(columns=cols_demo)

    # Convertir género numérico (1 = Male, 2 = Female) a texto descriptivo
    df_demo_clean["gender"] = df_demo_clean["gender_code"].map(
        {1: "Male", 2: "Female"}
    )
    df_demo_clean.drop(columns=["gender_code"], inplace=True)

    # 4. Filtrar columnas nutricionales de interés
    cols_diet = {
        "SEQN": "seqn_id",
        "DR1TKCAL": "energy_kcal",
        "DR1TPROT": "protein_g",
        "DR1TCARB": "carbohydrates_g",
        "DR1TSUGR": "sugars_g",
        "DR1TFIBE": "fiber_g",
        "DR1TTFAT": "total_fat_g",
        "DR1TSODI": "sodium_mg",
    }
    df_diet_clean = df_diet[list(cols_diet.keys())].rename(columns=cols_diet)

    # 5. Cruzar las tablas mediante INNER JOIN
    print("--> Cruzando tablas por SEQN...")
    df_merged = pd.merge(df_demo_clean, df_diet_clean, on="seqn_id", how="inner")

    # 6. Diagnóstico de calidad: descartar filas sin registro calórico (nulos en energy_kcal)
    filas_antes = len(df_merged)
    df_merged = df_merged.dropna(subset=["energy_kcal"])
    filas_despues = len(df_merged)
    print(
        f"--> Filtrados {filas_antes - filas_despues} registros sin datos nutricionales válidos."
    )

    # 7. Exportar el dataset procesado
    df_merged.to_csv(ruta_salida, index=False)
    print(f"\n✅ PIPELINE EXITOSO:")
    print(f" - Filas finales: {df_merged.shape[0]:,}")
    print(f" - Columnas limpias: {df_merged.shape[1]}")
    print(f" - Archivo guardado en: {ruta_salida}")

    print("\n--- PRIMERAS 3 FILAS DEL DATASET PROCESADO ---")
    print(df_merged.head(3))


if __name__ == "__main__":
    ejecutar_pipeline()