def normalize_dataframe(data_dict):
    import pandas as pd

    dfs = []

    for source, df in data_dict.items():
        df = df.copy()

        # 🔥 detectar columnas de semanas
        week_cols = [col for col in df.columns if col.startswith("L")]

        if not week_cols:
            continue

        df_melted = df.melt(
            id_vars=[col for col in df.columns if col not in week_cols],
            value_vars=week_cols,
            var_name="WEEK_RAW",
            value_name="VALUE"
        )

        # 🔥 limpiar valores
        df_melted["VALUE"] = (
            df_melted["VALUE"]
            .astype(str)
            .str.replace(",", ".")
            .astype(float)
        )

        # 🔥 WEEK limpio
        df_melted["WEEK"] = df_melted["WEEK_RAW"].str.extract(r"(L\d+W)")

        # 🔥 WEEK_NUM
        df_melted["WEEK_NUM"] = (
            df_melted["WEEK"]
            .str.extract(r"L(\d+)")
            .astype(int)
        )

        # 🔥 SOURCE
        if "METRICS" in source:
            df_melted["SOURCE"] = "metrics"
        else:
            df_melted["SOURCE"] = "orders"

        dfs.append(df_melted)

    df_final = pd.concat(dfs, ignore_index=True)

    print("✅ Data final:", df_final.shape)
    print("📊 Sources:", df_final["SOURCE"].unique())
    print("📊 Metrics:", df_final.get("METRIC", "NO METRIC"))

    return df_final