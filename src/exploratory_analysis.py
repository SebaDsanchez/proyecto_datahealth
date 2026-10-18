import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def generar_eda():
    print("=== INICIANDO ANÁLISIS EXPLORATORIO Y VISUALIZACIÓN ===")

    # 1. Cargar el dataset limpio que generamos en el paso anterior
    ruta_datos = os.path.join("data", "processed", "nhanes_nutrition_clean.csv")
    df = pd.read_csv(ruta_datos)

    # 2. Crear el lienzo de 2 filas x 2 columnas
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # =========================================================================
    # GRÁFICO 1 (axes[0, 0]): Calorías Promedio por Rango de Edad y Género
    # =========================================================================
    bins = [0, 18, 35, 50, 65, 100]
    labels = ["<18", "19-35", "36-50", "51-65", "65+"]
    df["age_group"] = pd.cut(df["age_years"], bins=bins, labels=labels)

    cal_edad = (
        df.groupby(["age_group", "gender"], observed=True)["energy_kcal"]
        .mean()
        .reset_index()
    )

    sns.barplot(
        data=cal_edad,
        x="age_group",
        y="energy_kcal",
        hue="gender",
        palette={"Male": "#2b5c8f", "Female": "#d95f02"},
        ax=axes[0, 0],
    )
    axes[0, 0].set_title(
        "Average Daily Caloric Intake by Age Group & Gender",
        fontsize=13,
        fontweight="bold",
    )
    axes[0, 0].set_xlabel("Age Group (Years)")
    axes[0, 0].set_ylabel("Mean Energy (kcal)")

    # =========================================================================
    # GRÁFICO 2 (axes[0, 1]): % de Población que Supera el Límite de Sodio
    # =========================================================================
    limite_sodio = 2300.0  # Límite saludable OMS/AHA (mg/día)
    df["excess_sodium"] = df["sodium_mg"] > limite_sodio
    pct_sodio = df["excess_sodium"].value_counts(normalize=True) * 100

    etiquetas = ["Exceeds Limit (>2,300 mg)", "Within Healthy Limit"]
    valores = [pct_sodio.get(True, 0), pct_sodio.get(False, 0)]

    axes[0, 1].barh(
        etiquetas, valores, color=["#e74c3c", "#2ecc71"], height=0.5
    )
    axes[0, 1].set_title(
        "Population Sodium Intake vs. Recommended Limit (2,300 mg)",
        fontsize=13,
        fontweight="bold",
    )
    axes[0, 1].set_xlabel("Percentage of Population (%)")
    axes[0, 1].set_xlim(0, 100)

    # Escribir el número exacto al final de cada barra
    for i, valor in enumerate(valores):
        axes[0, 1].text(
            valor + 1.5, i, f"{valor:.1f}%", va="center", fontweight="bold"
        )

    # =========================================================================
    # GRÁFICO 3 (axes[1, 0]): Mapa de Calor de Correlación de Nutrientes
    # =========================================================================
    cols_nutrientes = [
        "energy_kcal",
        "protein_g",
        "carbohydrates_g",
        "sugars_g",
        "fiber_g",
        "total_fat_g",
        "sodium_mg",
    ]
    matriz_corr = df[cols_nutrientes].corr()

    sns.heatmap(
        matriz_corr,
        annot=True,
        cmap="coolwarm",
        fmt=".2f",
        vmin=-1,
        vmax=1,
        ax=axes[1, 0],
    )
    axes[1, 0].set_title(
        "Macronutrient & Sodium Correlation Matrix",
        fontsize=13,
        fontweight="bold",
    )

    # =========================================================================
    # GRÁFICO 4 (axes[1, 1]): Boxplot de Consumo de Azúcar y Outliers
    # =========================================================================
    sns.boxplot(
        data=df,
        x="gender",
        y="sugars_g",
        hue="gender",
        legend=False,
        palette={"Male": "#2b5c8f", "Female": "#d95f02"},
        ax=axes[1, 1],
    )
    axes[1, 1].set_title(
        "Daily Sugar Intake Distribution & Outliers by Gender",
        fontsize=13,
        fontweight="bold",
    )
    axes[1, 1].set_xlabel("Gender")
    axes[1, 1].set_ylabel("Total Sugars (g)")

    # =========================================================================
    # 3. Exportar resumen numérico en consola y guardar imagen
    # =========================================================================
    print("\n--- RESUMEN EJECUTIVO DE INSIGHTS ---")
    print(f"1. Porcentaje que supera 2300mg de sodio: {valores[0]:.1f}%")
    print(
        f"2. Correlación Calorías vs Grasas Totales: {matriz_corr.loc['energy_kcal', 'total_fat_g']:.2f}"
    )
    print(
        f"3. Correlación Calorías vs Carbohidratos:  {matriz_corr.loc['energy_kcal', 'carbohydrates_g']:.2f}"
    )
    print(
        f"4. Mediana de azúcar (Hombres vs Mujeres): "
        f"{df[df['gender']=='Male']['sugars_g'].median():.1f}g vs "
        f"{df[df['gender']=='Female']['sugars_g'].median():.1f}g"
    )

    plt.tight_layout()
    ruta_img = os.path.join("data", "processed", "eda_dashboard.png")
    plt.savefig(ruta_img, dpi=150)
    print(f"\n✅ Dashboard guardado como imagen en: {ruta_img}")
    plt.show()


if __name__ == "__main__":
    generar_eda()