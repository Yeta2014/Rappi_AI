
import io
import streamlit as st
import matplotlib.pyplot as plt
import requests
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(page_title="Rappi AI", layout="wide")

st.title("🚀 Rappi AI Assistant")
st.markdown("Analiza métricas, zonas y crecimiento con inteligencia artificial")

st.markdown("""
<style>
[data-testid="stChatMessage"] {
    border-radius: 12px;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

API_URL = f"{os.getenv('API_URL')}/ask"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def generate_pdf(question, result_df, fig, insights):

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("📊 REPORTE RAPPI AI", styles["Title"]))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph(f"<b>Pregunta:</b> {question}", styles["Normal"]))
    elements.append(Spacer(1, 10))

    if result_df is not None and not result_df.empty:

        cols = [c for c in ["ZONE", "COUNTRY", "VALUE", "VALUE_current", "growth"] if c in result_df.columns]
        df_clean = result_df[cols].head(5)

        data = [df_clean.columns.tolist()] + df_clean.values.tolist()

        table = Table(data)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#FF441F")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ]))

        elements.append(Paragraph("📊 Resultados", styles["Heading2"]))
        elements.append(table)
        elements.append(Spacer(1, 10))

    if fig is not None:
        img_buffer = io.BytesIO()
        fig.savefig(img_buffer, format="png", dpi=120)
        img_buffer.seek(0)

        elements.append(Paragraph("📈 Visualización", styles["Heading2"]))
        elements.append(Image(img_buffer, width=320, height=200))
        elements.append(Spacer(1, 10))

    elements.append(Paragraph("🧠 Insights", styles["Heading2"]))

    for line in insights.split("\n"):
        if line.strip():
            elements.append(Paragraph(line, styles["Normal"]))

    doc.build(elements)
    buffer.seek(0)

    return buffer


def generate_chart(result):

    if result is None or result.empty:
        return None

    try:
        if "ZONE" in result.columns:

            value_col = next(
                (c for c in ["VALUE", "VALUE_current", "growth"] if c in result.columns),
                None
            )

            if value_col:
                chart_df = result.head(5)

                fig, ax = plt.subplots(figsize=(3.2, 1.8), dpi=120)

                ax.barh(chart_df["ZONE"], chart_df[value_col])
                ax.invert_yaxis()

                ax.set_title("Top Zonas", fontsize=9)
                ax.tick_params(labelsize=7)

                plt.tight_layout()
                return fig

    except:
        return None



for i, chat in enumerate(st.session_state.chat_history):

    with st.chat_message("user"):
        st.markdown(chat["question"])

    with st.chat_message("assistant"):

        if chat["result"] is not None:
            st.dataframe(chat["result"], width="stretch")

        if chat["fig"] is not None:
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                st.pyplot(chat["fig"])

        st.markdown(chat["response"])

        pdf = generate_pdf(
            chat["question"],
            chat["result"],
            chat["fig"],
            chat["response"]
        )

        st.download_button(
            label="⬇️ Descargar PDF",
            data=pdf,
            file_name=f"reporte_{i}.pdf",
            mime="application/pdf",
            key=f"download_{i}"
        )


if prompt := st.chat_input("Haz tu pregunta..."):

    try:
        res = requests.post(API_URL, json={"question": prompt})
        data = res.json()

        import pandas as pd
        result = pd.DataFrame(data["data"])

        fig = generate_chart(result)
        response = data["insights"]

    except Exception as e:
        result = None
        fig = None
        response = f"❌ Error conectando API: {e}"

    st.session_state.chat_history.append({
        "question": prompt,
        "result": result,
        "fig": fig,
        "response": response
    })

    st.rerun()

if st.button("🧹 Limpiar chat"):
    st.session_state.chat_history = []
    st.rerun()