# 🧠 Rappi AI Insights

Sistema de análisis inteligente de métricas y órdenes usando IA, con una arquitectura modular que integra procesamiento de datos, análisis NLP y generación de reportes.

---

## 🚀 Descripción

Este proyecto permite analizar datos de órdenes y métricas mediante un chatbot impulsado por IA. Combina:

- 📊 Procesamiento de datos
- 🧠 NLP (Natural Language Processing)
- 🤖 Generación de insights
- 🌐 API con FastAPI
- 📈 Interfaz visual con Streamlit

---

## 🏗️ Arquitectura del proyecto

RAPPI-AI-INSIGHTS/
│
├── app/ # Interfaz (Streamlit)
│ ├── streamlit_app.py
│ └── style.css
│
├── data/ # Datos de entrada
│ └── example.xlsx
│
├── src/
│ ├── analytics/ # Lógica de análisis
│ │ ├── nlp_parser.py
│ │ ├── query_engine.py
│ │ └── report_engine.py
│ │
│ ├── api/ # API (FastAPI)
│ │ └── app.py
│ │
│ ├── ingestion/ # Carga de datos
│ │ └── load_data.py
│ │
│ ├── llm/ # Chatbot / IA
│ │ └── chatbot.py
│ │
│ └── processing/ # Transformaciones
│ └── transform.py
│
├── .env # Variables de entorno (NO subir)
├── .gitignore
├── requirements.txt
└── README.md

---

## ⚙️ Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/Yeta2014/Rappi_AI.git
cd Rappi_AI
```

### 2. Crear entorno virtual

```bash
python -m venv venv
```

### 3. Activar entorno (Windows)

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 🔐 Variables de entorno

Crea un archivo `.env`:

```
OPENAI_API_KEY=tu_api_key_aqui
```

⚠️ Nunca subir este archivo

---

## ▶️ Cómo ejecutar el proyecto

### 🔹 1. Ejecutar API (FastAPI)

```bash
python -m uvicorn src.api.app:app --reload
```

Accede a:

- Swagger: http://127.0.0.1:8000/docs

---

### 🔹 2. Ejecutar interfaz (Streamlit)

En otra terminal:

```bash
streamlit run app/streamlit_app.py
```

---

## 🧠 Flujo del sistema

- 📥 Ingesta de datos (`load_data.py`)
- 🔄 Transformación (`transform.py`)
- 📊 Análisis (`query_engine.py`, `report_engine.py`)
- 🧠 Interpretación NLP (`nlp_parser.py`)
- 🤖 Chatbot IA (`chatbot.py`)
- 🌐 Exposición vía API
- 📈 Visualización en Streamlit

---

## 💡 Funcionalidades

- Consultas en lenguaje natural  
- Análisis de crecimiento (orders vs metrics)  
- Generación de insights automáticos  
- Integración con modelos de IA  
- Visualización interactiva  

---

## 🧪 Ejemplo de uso

Pregunta en el chatbot:

```
¿Cómo ha sido el crecimiento de órdenes vs métricas?
```

El sistema:

- interpreta la pregunta  
- consulta los datos  
- genera un análisis  
- devuelve un insight  

---

## 🛠️ Tecnologías usadas

- Python  
- FastAPI  
- Streamlit  
- Pandas  
- OpenAI API  
- NLP  

---

## ⚠️ Buenas prácticas implementadas

- Separación por capas (API, lógica, datos)  
- Uso de entorno virtual  
- Manejo de variables sensibles con `.env`  
- Código modular y escalable  

---

## 🚀 Mejoras futuras

- Dashboard más avanzado  
- Cacheo de consultas  
- Autenticación en API  
- Deployment en la nube  

---

## 👩‍💻 Autor

Desarrollado por **Yeimmy Tatiana Suarez**  
AI Engineer / Backend Developer  


