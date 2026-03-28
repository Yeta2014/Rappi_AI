
def extract_metric(question, df):
    q = question.lower()
    metrics = df["METRIC"].unique()

    for m in metrics:
        if m.lower() in q:
            return m

    if "lead" in q:
        return "Lead Penetration"
    elif "perfect" in q:
        return "Perfect Orders"
    elif "profit" in q:
        return "Gross Profit UE"

    return None


def extract_country(question):
    q = question.lower()

    countries = {
        "mexico": "MX",
        "peru": "PE",
        "colombia": "CO",
        "brasil": "BR",
        "uruguay": "UY"
    }

    for k, v in countries.items():
        if k in q:
            return v

    return None


def detect_query_type(question):
    q = question.lower()

    if "promedio" in q:
        return "aggregation"

    if "compara" in q:
        return "comparison"

    if "evolución" in q or "tendencia" in q:
        return "trend"

    if "alto" in q and "bajo" in q:
        return "multivariable"

    if "crecimiento" in q or "crecen" in q:
        return "growth"

    return "top"