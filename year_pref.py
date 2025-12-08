def compute_year_pref(df, preference):
    target_year = 2025 if preference == "new" else 1950

    df["year_sim"] = 1 - abs(df["year"] - target_year) / 40
    df["year_sim"] = df["year_sim"].clip(0, 1)
    return df
