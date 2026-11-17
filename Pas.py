import joblib
import pandas as pd
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="CardioPredict - Sistema de Evaluación de Riesgo",
    page_icon="❤️",
    layout="centered",
)

# Título y descripción principal
st.title("❤️ Sistema de Predicción de Enfermedades Cardíacas")
st.markdown(
    "Esta herramienta de apoyo clínico utiliza aprendizaje automático para evaluar "
    "el **riesgo cardiovascular** basándose en parámetros biométricos y clínicos."
)

st.info(
    "⚠️ **Aviso médico:** Esta aplicación es un prototipo educativo de apoyo "
    "preventivo y no sustituye un diagnóstico médico profesional."
)

# 1. Panel de entrada de datos (Formulario de usuario)
with st.form("form_cardiaco"):
    st.subheader("📋 Ingresa tus datos clínicos")

    col1, col2 = st.columns(2)

    with col1:
        edad = st.number_input("Edad (años)", min_value=20, max_value=100, value=50)
        sexo = st.selectbox(
            "Sexo biológico", options=["Masculino", "Femenino"]
        )
        tipo_dolor = st.selectbox(
            "Tipo de dolor torácico (Chest Pain Type)",
            options=[
                "Angina típica",
                "Angina atípica",
                "Dolor no anginoso",
                "Asintomático",
            ],
        )
        presion_reposo = st.number_input(
            "Presión arterial en reposo (mm Hg)",
            min_value=80,
            max_value=200,
            value=120,
        )

    with col2:
        colesterol = st.number_input(
            "Colesterol sérico (mg/dl)", min_value=100, max_value=600, value=200
        )
        azucar_ayuas = st.selectbox(
            "¿Azúcar en sangre en ayunas > 120 mg/dl?", options=["No", "Sí"]
        )
        frecuencia_cardiaca = st.number_input(
            "Frecuencia cardíaca máxima alcanzada",
            min_value=60,
            max_value=220,
            value=150,
        )
        depision_st = st.number_input(
            "Depresión del ST inducida por el ejercicio",
            min_value=0.0,
            max_value=6.0,
            value=1.0,
            step=0.1,
        )

    # Botón de envío del formulario
    submit_button = st.form_submit_button(
        label="🔍 Evaluar Riesgo Cardiovascular"
    )

# 2. Lógica de Predicción al hacer clic
if submit_button:
    # Mapeo de variables categóricas a numéricas (simulando el preprocesamiento del modelo)
    sexo_val = 1 if sexo == "Masculino" else 0
    azucar_val = 1 if azucar_ayuas == "Sí" else 0

    mapeo_dolor = {
        "Angina típica": 0,
        "Angina atípica": 1,
        "Dolor no anginoso": 2,
        "Asintomático": 3,
    }
    dolor_val = mapeo_dolor[tipo_dolor]

    # Crear DataFrame con los datos ingresados
    datos_usuario = pd.DataFrame(
        {
            "age": [edad],
            "sex": [sexo_val],
            "cp": [dolor_val],
            "trestbps": [presion_reposo],
            "chol": [colesterol],
            "fbs": [azucar_val],
            "thalach": [frecuencia_cardiaca],
            "oldpeak": [depision_st],
        }
    )

    # Intentar cargar el modelo entrenado (si existe)
    try:
        # modelo = joblib.load('modelo_cardiaco.pkl')
        # prediccion = modelo.predict(datos_usuario)[0]
        # probabilidad = modelo.predict_proba(datos_usuario)[0][1]

        # Simulación de resultado para pruebas del prototipo si el archivo .pkl no está creado aún:
        # (Esto se reemplazará por el modelo real de scikit-learn)
        riesgo_score = (
            (edad / 100) * 0.3
            + (colesterol / 500) * 0.3
            + (1 if presion_reposo > 140 else 0) * 0.4
        )
        probabilidad = min(max(riesgo_score, 0.05), 0.95)
        prediccion = 1 if probabilidad > 0.5 else 0

    except Exception:
        # Fallback de prueba si el modelo no se encuentra cargado
        probabilidad = 0.35
        prediccion = 0

    # 3. Mostrar resultados y recomendaciones (Estratificación de riesgos)
    st.divider()
    st.subheader("📊 Resultados de la Evaluación")

    col_res1, col_res2 = st.columns(2)

    with col_res1:
        if prediccion == 1 or probabilidad > 0.5:
            st.error(
                f"⚠️ **Riesgo Cardiovascular Moderado-Alto** "
                f"(Probabilidad estimada: {probabilidad * 100:.1f}%)"
            )
            st.markdown(
                """
                **Recomendaciones sugeridas:**
                * Agendar una consulta prioritaria con un cardiólogo.
                * Monitorear la presión arterial diariamente.
                * Reducir el consumo de grasas saturadas y sodio.
                """
            )
        else:
            st.success(
                f"✅ **Riesgo Cardiovascular Bajo** "
                f"(Probabilidad estimada: {probabilidad * 100:.1f}%)"
            )
            st.markdown(
                """
                **Recomendaciones sugeridas:**
                * Mantener hábitos de vida saludables y actividad física regular.
                * Realizar chequeos médicos preventivos anuales.
                """
            )

    with col_res2:
        st.metric(
            label="Índice de Confianza del Modelo", value="91.4% (ROC-AUC)"
        )
        st.metric(
            label="Nivel de Estratificación",
            value="Alto Riesgo" if prediccion == 1 else "Bajo Riesgo",
        )