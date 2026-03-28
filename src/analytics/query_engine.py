import re
from src.analytics.nlp_parser import extract_metric, extract_country, detect_query_type


def parse_week_from_question(question):
    q = question.lower()

    match = re.search(r"hace\s+(\d+)", q)
    if match:
        return int(match.group(1))

    if any(x in q for x in ["esta semana", "actual", "última"]):
        return 0

    return 0


def answer_question(df, question, history=None):
  
   
    if "VALUE" not in df.columns or "WEEK_NUM" not in df.columns:
        raise ValueError("❌ DataFrame no normalizado correctamente")

    q = question.lower()

    follow_up_words = ["esto", "eso", "detalle", "más", "explica", "por qué", "qué hacer"]

    is_follow_up = any(word in q for word in follow_up_words)

    if is_follow_up and history:
        last = history[-1]

        print("🧠 Usando contexto anterior")

        return last.get("result")

    metric = extract_metric(question, df)
    country = extract_country(question)
    query_type = detect_query_type(question)
    week = parse_week_from_question(question)

    # =========================
    # FALLBACK MÉTRICA
    # =========================
    if metric is None:
        if "crecimiento" in q:
            metric = "orders"
        else:
            metric = "lead penetration"

    print("Metric:", metric)
    print("Week:", week)

    # =========================
    # FILTRO BASE
    # =========================
    df_filtered = df.copy()

    if country:
        df_filtered = df_filtered[df_filtered["COUNTRY"] == country]

    # =========================
    # FILTRO POR SEMANA (CLAVE)
    # =========================
    def filter_week(df, week):
        if week is None:
            return df
        return df[df["WEEK_NUM"] == week]

    # =========================
    # ZONAS PROBLEMÁTICAS
    # =========================
    if "problem" in q:

        df_metrics = df_filtered[df_filtered["SOURCE"] == "metrics"]
        df_orders = df_filtered[df_filtered["SOURCE"] == "orders"]

        df_metrics = filter_week(df_metrics, week)
        df_orders = filter_week(df_orders, week)

        df_lead = df_metrics[df_metrics["METRIC"].str.contains("lead", case=False)]
        df_lead_low = df_lead[df_lead["VALUE"] < df_lead["VALUE"].mean()]

        df_orders_low = df_orders[df_orders["VALUE"] < df_orders["VALUE"].mean()]

        merged = df_lead_low.merge(df_orders_low, on="ZONE")

        return merged[["ZONE", "VALUE_x", "VALUE_y"]] \
            .rename(columns={"VALUE_x": "lead", "VALUE_y": "orders"}) \
            .sort_values("lead") \
            .head(5)

    # =========================
    # TOP / BOTTOM
    # =========================
    if query_type == "top":

        df_metric = df_filtered[
            (df_filtered["SOURCE"] == "metrics") &
            (df_filtered["METRIC"].str.contains(metric, case=False))
        ]

        df_metric = filter_week(df_metric, week)

        if "menor" in q:
            return df_metric.sort_values("VALUE").head(5)

        return df_metric.sort_values("VALUE", ascending=False).head(5)

    # =========================
    # COMPARACIÓN
    # =========================
    elif query_type == "comparison":

        df_metric = df_filtered[
            (df_filtered["SOURCE"] == "metrics") &
            (df_filtered["METRIC"].str.contains(metric, case=False))
        ]

        df_metric = filter_week(df_metric, week)

        return df_metric.groupby("ZONE_TYPE")["VALUE"] \
            .mean().reset_index()

    # =========================
    # TENDENCIA
    # =========================
    elif query_type == "trend":

        df_metric = df_filtered[
            (df_filtered["SOURCE"] == "metrics") &
            (df_filtered["METRIC"].str.contains(metric, case=False))
        ]

        return df_metric.groupby("WEEK_NUM")["VALUE"] \
            .mean().reset_index().sort_values("WEEK_NUM")

    # =========================
    # AGREGACIÓN
    # =========================
    elif query_type == "aggregation":

        df_metric = df_filtered[
            (df_filtered["SOURCE"] == "metrics") &
            (df_filtered["METRIC"].str.contains(metric, case=False))
        ]

        df_metric = filter_week(df_metric, week)

        return df_metric.groupby("COUNTRY")["VALUE"] \
            .mean().reset_index()

    # =========================
    # MULTIVARIABLE
    # =========================
    elif query_type == "multivariable":

        df_lead = df_filtered[
            (df_filtered["SOURCE"] == "metrics") &
            (df_filtered["METRIC"].str.contains("lead", case=False))
        ]

        df_perfect = df_filtered[
            (df_filtered["SOURCE"] == "metrics") &
            (df_filtered["METRIC"].str.contains("perfect", case=False))
        ]

        df_lead = filter_week(df_lead, week)
        df_perfect = filter_week(df_perfect, week)

        merged = df_lead.merge(df_perfect, on="ZONE")

        return merged[
            (merged["VALUE_x"] > merged["VALUE_x"].mean()) &
            (merged["VALUE_y"] < merged["VALUE_y"].mean())
        ]

    # =========================
    # CRECIMIENTO REAL (WOW)
    # =========================
    elif query_type == "growth":

        df_orders = df_filtered[df_filtered["SOURCE"] == "orders"]

        pivot = df_orders.pivot_table(
            index="ZONE",
            columns="WEEK_NUM",
            values="VALUE",
            aggfunc="sum"
        )

        available_weeks = sorted(pivot.columns)

        if len(available_weeks) < 5:
            return pivot.reset_index()

        latest = min(available_weeks)  # L0
        prev = latest + 5 if (latest + 5) in available_weeks else max(available_weeks)

        pivot["growth"] = pivot[latest] - pivot[prev]

        return pivot.reset_index() \
            .sort_values("growth", ascending=False) \
            .head(5)

    return None
