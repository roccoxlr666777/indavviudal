import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Advanced English Simulator", page_icon="🌐", layout="wide")

# Diseño limpio sin imágenes complejas
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    h1, h2, h3 { color: #2c3e50; font-family: 'Georgia', serif; }
    .grammar-box { background-color: #ffffff; padding: 20px; border-left: 5px solid #3498db; border-radius: 5px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    </style>
""", unsafe_allow_html=True)
# 2. SEGURIDAD (Opcional, misma mecánica)
if 'acceso_avanzado' not in st.session_state:
    st.session_state.acceso_avanzado = False

if not st.session_state.acceso_avanzado:
    st.title("🔒 Advanced English Portal")
    pwd = st.text_input("Ingresa la clave de acceso (Pista: Avanzado2026):", type="password")
    if st.button("Entrar"):
        if pwd == "Avanzado2026":
            st.session_state.acceso_avanzado = True
            st.rerun()
        else:
            st.error("Contraseña incorrecta.")
    st.stop()

# 3. CARGA DE VOCABULARIO
@st.cache_data
def cargar_vocabulario():
    archivo_csv = 'vocabulario_avanzado.csv'
    if os.path.exists(archivo_csv):
        return pd.read_csv(archivo_csv, encoding='utf-8')
    return pd.DataFrame()

df_vocab = cargar_vocabulario()

# 4. BASE DE DATOS DE EJERCICIOS (Se pueden agregar cientos aquí)
ejercicios = [
    {
        "pregunta": "Choose the correct inversion: ___ had I arrived when the phone rang.",
        "opciones": ["Hardly", "No sooner", "As soon as", "Barely"],
        "respuesta_correcta": "Hardly",
        "explicacion": "'Hardly' va seguido de 'had + sujeto + participio pasado' y se complementa con 'when'."
    },
    {
        "pregunta": "Mixed Conditional: If I had studied medicine, I ___ a doctor right now.",
        "opciones": ["would have been", "will be", "would be", "had been"],
        "respuesta_correcta": "would be",
        "explicacion": "Condición irreal en el pasado (had studied) + Resultado irreal en el presente (would be)."
    },
    {
        "pregunta": "Passive Voice: It ___ that the economy will recover soon.",
        "opciones": ["is believing", "believes", "is believed", "has believed"],
        "respuesta_correcta": "is believed",
        "explicacion": "Estructura de voz pasiva impersonal para opiniones generales: It + to be + past participle + that."
    },
    {
        "pregunta": "Vocabulary: The new policy will ___ the negative effects of the crisis.",
        "opciones": ["exacerbate", "mitigate", "delineate", "foster"],
        "respuesta_correcta": "mitigate",
        "explicacion": "'Mitigate' significa hacer algo menos severo o doloroso (Atenuar)."
    }
]

# 5. ESTRUCTURA DE LA APP
st.title("🌐 Advanced English Training C1/C2")
st.markdown("Dominio estructural, vocabulario académico y precisión gramatical.")

tab_vocab, tab_gramatica, tab_ejercicios = st.tabs(["📖 C1/C2 Vocabulary", "⚙️ Advanced Structures", "📝 Interactive Quiz"])

# --- PESTAÑA 1: VOCABULARIO ---
with tab_vocab:
    st.markdown("### Base de Datos de Vocabulario Avanzado")
    if not df_vocab.empty:
        categorias = df_vocab["Categoría Gramatical"].unique()
        cat_sel = st.selectbox("Filtrar por tipo:", categorias)
        df_mostrar = df_vocab[df_vocab["Categoría Gramatical"] == cat_sel][["Palabra en Inglés", "Traducción"]].sort_values(by="Palabra en Inglés").reset_index(drop=True)
        st.dataframe(df_mostrar, use_container_width=True, height=400)
    else:
        st.error("No se encontró el archivo CSV.")

# --- PESTAÑA 2: GRAMÁTICA AVANZADA ---
with tab_gramatica:
    st.markdown("### Estructuras de Nivel C1/C2")
    
    st.markdown("""
    <div class='grammar-box'>
        <h4>1. Inversion (Inversión Estilística)</h4>
        <p><b>Uso:</b> Para dar énfasis literario o formal. Se altera el orden de Sujeto y Verbo Auxiliar tras ciertas expresiones negativas.</p>
        <p><b>Fórmula:</b> Expresión Negativa + Auxiliar + Sujeto + Verbo</p>
        <p><b>Ejemplos:</b></p>
        <ul>
            <li><i>Normal:</i> I have never seen such a beautiful painting.</li>
            <li><i>Inversion:</i> <b>Never have I seen</b> such a beautiful painting.</li>
            <li><i>Inversion:</i> <b>Seldom does he visit</b> his hometown.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='grammar-box'>
        <h4>2. Mixed Conditionals (Condicionales Mixtos)</h4>
        <p><b>Uso:</b> Para mezclar tiempos. Usualmente, una condición irreal en el pasado que tiene un resultado en el presente.</p>
        <p><b>Fórmula:</b> If + Past Perfect (Pasado) , Sujeto + Would + Verbo base (Presente)</p>
        <p><b>Ejemplos:</b></p>
        <ul>
            <li><i>Contexto:</i> No gané la lotería ayer, así que no soy rico hoy.</li>
            <li><i>Mixto:</i> <b>If I had won</b> the lottery, <b>I would be</b> rich now.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='grammar-box'>
        <h4>3. Impersonal Passive (Voz Pasiva Impersonal)</h4>
        <p><b>Uso:</b> Común en periodismo y academia para expresar suposiciones, creencias o reportes sin especificar quién lo dice.</p>
        <p><b>Fórmula 1:</b> It is + Participio (said/believed/thought) + that...</p>
        <p><b>Fórmula 2:</b> Sujeto + is + Participio + to + verbo...</p>
        <p><b>Ejemplos:</b></p>
        <ul>
            <li><b>It is widely believed that</b> the climate is changing.</li>
            <li>The CEO <b>is expected to resign</b> tomorrow.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# --- PESTAÑA 3: EJERCICIOS INTERACTIVOS ---
with tab_ejercicios:
    st.markdown("### Test Your Knowledge")
    st.write("Selecciona la respuesta correcta y presiona 'Check Answers' al final.")
    
    # Usamos session_state para guardar las respuestas del usuario
    respuestas_usuario = {}
    
    for i, ej in enumerate(ejercicios):
        st.markdown(f"**Q{i+1}: {ej['pregunta']}**")
        respuestas_usuario[i] = st.radio("Selecciona una opción:", ej['opciones'], key=f"q_{i}", index=None)
        st.write("---")
        
    if st.button("Verificar Resultados", type="primary"):
        puntaje = 0
        for i, ej in enumerate(ejercicios):
            st.markdown(f"**Q{i+1}: {ej['pregunta']}**")
            if respuestas_usuario[i] == ej['respuesta_correcta']:
                st.success(f"✅ ¡Correcto! Tu respuesta: {respuestas_usuario[i]}")
                puntaje += 1
            else:
                st.error(f"❌ Incorrecto. Tu respuesta: {respuestas_usuario[i]} | Respuesta correcta: {ej['respuesta_correcta']}")
            
            # Muestra la explicación técnica siempre al calificar
            st.info(f"💡 Explicación: {ej['explicacion']}")
            st.write("---")
            
        st.metric(label="Puntaje Final", value=f"{puntaje} / {len(ejercicios)}")
        if puntaje == len(ejercicios):
            st.balloons()
