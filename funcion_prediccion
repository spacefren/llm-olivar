import joblib

pipeline = joblib.load("xgb_pipeline_olivar.joblib")

def calcular_prediccion_y_impacto(parcela_df):
    pred_pct = float(pipeline.predict(parcela_df)[0])
    pred_pct = max(0.0, min(1.0, pred_pct))

    impacto_eur_ha = (
        parcela_df["rendimiento_esperado_kg_ha"].iloc[0]
        * pred_pct
        * parcela_df["precio_mercado_eur_kg"].iloc[0]
    )

    impacto_total = impacto_eur_ha * parcela_df["superficie_ha"].iloc[0]

    return {
        "pct_perdida_pred": pred_pct,
        "impacto_eur_ha": impacto_eur_ha,
        "impacto_total_parcela_eur": impacto_total
    }
