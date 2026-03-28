import os
from openai import OpenAI
from dotenv import load_dotenv

# =========================
# 🔐 CONFIG
# =========================
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# =========================
# 🧠 SYSTEM PROMPT
# =========================
SYSTEM_PROMPT = """
Eres un Senior Business Analyst en Rappi.

OBJETIVO:
Dar insights de negocio claros, accionables y basados en datos.

REGLAS:
- Usa SOLO la información del contexto
- NO inventes datos
- Máximo 3 insights
- Lenguaje claro y ejecutivo

CONTEXTO CONVERSACIONAL:
- Si la pregunta depende de una anterior, usa el contexto previo
- Mantén el mismo tema (no cambies de enfoque)
- Sé consistente con respuestas anteriores

FORMATO DE RESPUESTA:

🔎 Insights:
1.
2.
3.

📊 Impacto:

🚀 Recomendación:
"""


# =========================
# 🔧 BUILD MESSAGES
# =========================
def build_messages(context, question, history=None):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # 🔥 memoria conversacional
    if history:
        for h in history[-3:]:
            if "question" in h and "response" in h:
                messages.append({
                    "role": "user",
                    "content": h["question"]
                })
                messages.append({
                    "role": "assistant",
                    "content": h["response"]
                })

    # 🔥 input actual
    messages.append({
        "role": "user",
        "content": f"""
Contexto de datos:
{context}

Pregunta del usuario:
{question}
"""
    })

    return messages


# =========================
# 🤖 ASK LLM
# =========================
def ask_llm(context, question, history=None):

    try:
        messages = build_messages(context, question, history)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.2,
            max_tokens=700
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"❌ Error generando respuesta: {str(e)}"