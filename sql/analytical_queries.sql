-- =============================================================================
-- PROYECTO: NHANES Nutritional Analysis
-- ARCHIVO: analytical_queries.sql
-- DESCRIPCIÓN: Consultas analíticas avanzadas usando CTEs, CASE y COALESCE
-- =============================================================================

-- -----------------------------------------------------------------------------
-- QUERY 1: Estratificación de Riesgo por Sodio (CTE + CASE + Agregaciones)
-- -----------------------------------------------------------------------------
WITH patient_sodium_risk AS (
    SELECT 
        seqn_id,
        gender,
        energy_kcal,
        total_fat_g,
        sodium_mg,
        CASE 
            WHEN sodium_mg > 2300 THEN '1. High Risk (>2300mg)'
            WHEN sodium_mg >= 1500 THEN '2. Moderate (1500-2300mg)'
            ELSE '3. Optimal (<1500mg)'
        END AS sodium_risk_tier
    FROM nutrition_records
)
SELECT 
    sodium_risk_tier,
    COUNT(*) AS total_patients,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM nutrition_records), 1) AS pct_population,
    ROUND(AVG(energy_kcal), 0) AS avg_calories_kcal,
    ROUND(AVG(total_fat_g), 1) AS avg_fat_g,
    ROUND(AVG(sodium_mg), 0) AS avg_sodium_mg
FROM patient_sodium_risk
GROUP BY sodium_risk_tier
ORDER BY sodium_risk_tier ASC;


-- -----------------------------------------------------------------------------
-- QUERY 2: Impacto Socioeconómico y Pivoteo por Género (COALESCE + CASE en COUNT)
-- -----------------------------------------------------------------------------
WITH socioeconomic_profile AS (
    SELECT 
        seqn_id,
        gender,
        sugars_g,
        fiber_g,
        sodium_mg,
        -- Si poverty_ratio es NULL, COALESCE asigna -1 para identificarlo como no reportado
        CASE 
            WHEN COALESCE(poverty_ratio, -1) = -1 THEN '4. Unreported Income'
            WHEN poverty_ratio < 1.30 THEN '1. Low Income (PIR < 1.3)'
            WHEN poverty_ratio < 3.50 THEN '2. Middle Income (PIR 1.3-3.5)'
            ELSE '3. High Income (PIR >= 3.5)'
        END AS income_bracket
    FROM nutrition_records
)
SELECT 
    income_bracket,
    COUNT(*) AS total_patients,
    -- Pivoteo manual: contamos hombres y mujeres en columnas separadas
    COUNT(CASE WHEN gender = 'Female' THEN 1 END) AS female_count,
    COUNT(CASE WHEN gender = 'Male' THEN 1 END) AS male_count,
    ROUND(AVG(sugars_g), 1) AS avg_sugar_g,
    ROUND(AVG(fiber_g), 1) AS avg_fiber_g,
    -- Porcentaje de pacientes en este grupo que superan los 2300mg de sodio
    ROUND(
        COUNT(CASE WHEN sodium_mg > 2300 THEN 1 END) * 100.0 / COUNT(*), 
        1
    ) AS pct_high_sodium
FROM socioeconomic_profile
GROUP BY income_bracket
ORDER BY income_bracket ASC;