from fastapi import FastAPI
from pydantic import BaseModel, Field

from src.ingestion.load_data import load_excel
from src.processing.transform import normalize_dataframe
from src.analytics.query_engine import answer_question
from src.llm.chatbot import ask_llm


app = FastAPI(
    title="Rappi AI API",
    description="""
API de análisis inteligente para operaciones Rappi.

Permite:
- Consultar métricas por zona
- Detectar oportunidades y problemas
- Generar insights automáticos con IA

Casos de uso:
- Top zonas por métrica
- Comparaciones
- Tendencias
- Crecimiento
- Zonas problemáticas
""",
    version="1.0.0"
)


df = normalize_dataframe(load_excel("data/example.xlsx"))



class QueryRequest(BaseModel):
    question: str = Field(
        ...,
        example="¿Cuáles son las 5 zonas con mayor Lead Penetration esta semana?",
        description="Pregunta en lenguaje natural sobre métricas de negocio"
    )



@app.get(
    "/",
    summary="Estado del servicio",
    description="Verifica que la API está corriendo correctamente"
)
def root():
    return {
        "status": "Rappi AI API running 🚀",
        "endpoints": ["/ask"]
    }


@app.post(
    "/ask",
    summary="Consultar métricas con IA",
    description="""
Permite hacer preguntas en lenguaje natural sobre los datos.

Ejemplos de preguntas:
- Top 5 zonas con mayor Lead Penetration
- Zonas con menor Perfect Orders
- Crecimiento de órdenes últimas semanas
- Zonas problemáticas
""",
    response_description="Resultados estructurados + insights generados por IA"
)
def ask(request: QueryRequest):

    result = answer_question(df, request.question)

    context = (
        result.head(5).to_string(index=False)
        if result is not None and not result.empty
        else "Sin datos relevantes"
    )

    response = ask_llm(
        context=context,
        question=request.question,
        history=[]
    )

    return {
        "question": request.question,
        "data": result.to_dict(orient="records") if result is not None else [],
        "insights": response
    }