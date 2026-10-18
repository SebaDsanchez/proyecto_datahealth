
import os
import pandas as pd

# 1. Definir la ruta a diet.csv
ruta_diet = os.path.join("data", "raw", "diet.csv")

print(f"--> Leyendo archivo: {ruta_diet}")
df_diet = pd.read_csv(ruta_diet)

# 2. Dimensiones
filas, cols = df_diet.shape
print(f"\n[INFO] Dimensiones de diet.csv:")
print(f" - Registros de consumo: {filas:,}")
print(f" - Columnas: {cols}")

# 3. Primeras 25 columnas
print("\n[INFO] Primeras 25 columnas detectadas:")
print(df_diet.columns[:25].tolist())

# 4. Verificar presencia de la clave de enlace SEQN
if "SEQN" in df_diet.columns:
    print("\n✅ Columna 'SEQN' detectada con éxito. Se puede hacer JOIN con demographic.csv.")
else:
    print("\n⚠️ ALERTA: No se encontró la columna 'SEQN'.")

# 5. Muestra de las primeras filas
print("\n[INFO] Vista previa (primeras 3 filas):")
print(df_diet.head(3))