import streamlit as st
import pandas as pd
import os
import random

# ==========================================
# 1. CONFIGURACIÓN Y DISEÑO (CSS Premium)
# ==========================================
st.set_page_config(page_title="Advanced English C1/C2", page_icon="🎓", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    /* Fondo principal */
    .stApp { background-color: #f4f7f6; }
    
    /* Títulos elegantes (Grafito y Esmeralda) */
    h1, h2, h3 { color: #1a3c34 !important; font-family: 'Georgia', serif; }
    
    /* Tarjetas de gramática */
    .grammar-card {
        background-color: white;
        padding: 25px;
        border-radius: 12px;
        border-top: 5px solid #2e7d32;
        box-shadow: 0 6px 12px rgba(0,0,0,0.08);
        margin-bottom: 20px;
    }
    .grammar-card h4 { color: #2e7d32; margin-top: 0; }
    
    /* Botones estilizados */
    .stButton>button {
        background-color: #1a3c34; color: white; border-radius: 8px; font-weight: bold; border: none; transition: 0.3s;
    }
    .stButton>button:hover { background-color: #2e7d32; color: white; }
    
    /* Cabecera superior */
    .header-box {
        background-color: #1a3c34; padding: 25px; border-radius: 12px; color: white; text-align: center; margin-bottom: 30px;
    }
    .header-box h1 { color: white !important; margin: 0; font-size: 2.5rem; }
    .header-box p { font-size: 1.2rem; margin-top: 5px; opacity: 0.9; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. BASE DE DATOS GRAMATICAL (15 Temas)
# ==========================================
temas_avanzados = {
    "1. Zero Conditional": {
        "uso": "Hechos científicos, verdades universales y leyes. Situaciones que siempre son 100% reales.",
        "formula": "If + Present Simple, Present Simple",
        "ejemplo": "If you heat ice, it melts. (Si calientas hielo, se derrite.)"
    },
    "2. First Conditional": {
        "uso": "Situaciones futuras probables o reales y sus consecuencias.",
        "formula": "If + Present Simple, Will + Verbo base",
        "ejemplo": "If she studies hard, she will pass the C1 exam. (Si estudia duro, aprobará el examen C1.)"
    },
    "3. Second Conditional": {
        "uso": "Situaciones hipotéticas, irreales o muy improbables en el presente o futuro.",
        "formula": "If + Past Simple, Would + Verbo base",
        "ejemplo": "If I were the CEO, I would change the policy. (Si yo fuera el CEO, cambiaría la política.)"
    },
    "4. Third Conditional": {
        "uso": "Arrepentimientos o situaciones hipotéticas en el pasado (que ya no se pueden cambiar).",
        "formula": "If + Past Perfect, Would have + Participio Pasado",
        "ejemplo": "If they had invested earlier, they would have made a profit. (Si hubieran invertido antes, habrían tenido ganancias.)"
    },
    "5. Mixed Conditional (Past Condition / Present Result)": {
        "uso": "Una acción irreal en el pasado que tiene una consecuencia en el presente.",
        "formula": "If + Past Perfect, Would + Verbo base",
        "ejemplo": "If I had learned German (past), I would live in Berlin now (present)."
    },
    "6. Mixed Conditional (Present Condition / Past Result)": {
        "uso": "Un estado continuo irreal en el presente que afectó una acción en el pasado.",
        "formula": "If + Past Simple, Would have + Participio Pasado",
        "ejemplo": "If I weren't so afraid of flying (always), I would have gone to Japan last year (past)."
    },
    "7. Adjectivization (Creación de Adjetivos)": {
        "uso": "Formar adjetivos a partir de sustantivos o verbos usando sufijos avanzados (-able, -ive, -ous, -ic).",
        "formula": "Sustantivo/Verbo + Sufijo",
        "ejemplo": "Rely (Confiar) -> Reliable (Confiable) | Hazard (Peligro) -> Hazardous (Peligroso)."
    },
    "8. Substantivization (Nominalización)": {
        "uso": "Convertir adjetivos o verbos en sustantivos para sonar más académico o formal (Ej. 'The + Adjetivo' para grupos de personas).",
        "formula": "The + Adjetivo = Grupo social / Verbo + -tion/-ment = Sustantivo abstracto",
        "ejemplo": "The wealthy (Los ricos) should pay more taxes. / His refusal (de refuse) was unexpected."
    },
    "9. Inversion (Énfasis Formal)": {
        "uso": "Dar un tono dramático o literario alterando el orden de Sujeto y Auxiliar tras adverbios negativos.",
        "formula": "Adverbio Negativo + Auxiliar + Sujeto + Verbo",
        "ejemplo": "Never have I witnessed such a brilliant presentation. (Nunca he presenciado...)"
    },
    "10. Impersonal Passive Voice": {
        "uso": "Reportar opiniones, mitos o creencias sin especificar quién lo dice (común en noticias).",
        "formula": "It is + Participio (said/believed) + that... OR Sujeto + is + Participio + to + Verbo",
        "ejemplo": "It is believed that the market will crash. / The CEO is expected to resign."
    },
    "11. Cleft Sentences (Oraciones Hendidas)": {
        "uso": "Enfatizar una parte específica de la oración (quién lo hizo, cuándo, dónde).",
        "formula": "It is/was + [Parte a enfatizar] + who/that + resto de la oración.",
        "ejemplo": "It was the marketing department that caused the delay. (Fue el departamento de marketing el que...)"
    },
    "12. Relative Clauses (Defining & Non-Defining)": {
        "uso": "Añadir información sobre un sustantivo. Las 'Non-defining' van entre comas y se pueden omitir.",
        "formula": "Sustantivo + who/which/that/whose + Cláusula",
        "ejemplo": "My professor, who is from London, speaks very fast. (Non-defining: se puede omitir y tiene sentido)."
    },
    "13. Participle Clauses": {
        "uso": "Acortar oraciones y sonar más sofisticado uniendo dos acciones realizadas por el mismo sujeto.",
        "formula": "Present/Past Participle + Frase, Sujeto + Verbo principal",
        "ejemplo": "Having finished the report, she left the office. (Habiendo terminado el reporte...)"
    },
    "14. Causative Verbs (Have / Get something done)": {
        "uso": "Indicar que le pagaste o pediste a alguien más que hiciera un servicio por ti.",
        "formula": "Sujeto + Have/Get + Objeto + Participio Pasado",
        "ejemplo": "I had my car repaired. (Hice que me repararan el auto. Yo no lo reparé personalmente)."
    },
    "15. Subjunctive in English": {
        "uso": "Expresar urgencia, demanda o sugerencia. Se usa el verbo base sin 's' incluso para He/She/It.",
        "formula": "Verbo de demanda (suggest/insist) + that + Sujeto + Verbo base",
        "ejemplo": "The board insisted that he resign immediately. (No 'resigns')."
    }
}

# ==========================================
# 3. BANCO DE PREGUNTAS (Para el Quiz Aleatorio)
# ==========================================
banco_preguntas = [
    {"q": "___ had we started the meeting when the fire alarm went off.", "opts": ["Hardly", "No sooner", "Barely", "As soon as"], "ans": "Hardly", "exp": "Inversión: 'Hardly' se usa con 'had + sujeto' y se complementa con 'when'."},
    {"q": "Mixed Conditional: If he had taken the medicine yesterday, he ___ sick today.", "opts": ["wouldn't be", "won't be", "wouldn't have been", "isn't"], "ans": "wouldn't be", "exp": "Condición irreal pasada (had taken) con resultado presente (wouldn't be)."},
    {"q": "Impersonal Passive: The suspect ___ to have fled the country.", "opts": ["is believed", "believes", "is believing", "has believed"], "ans": "is believed", "exp": "Sujeto + is believed + to + have + participio."},
    {"q": "Substantivization: The government needs to do more to help ___.", "opts": ["the poor", "the poors", "poor people's", "poor"], "ans": "the poor", "exp": "'The + Adjetivo' se usa para referirse a un grupo social entero."},
    {"q": "Causative: I need to ___ before the wedding.", "opts": ["have my suit cleaned", "clean my suit", "have cleaned my suit", "get clean my suit"], "ans": "have my suit cleaned", "exp": "Estructura Causativa: Have + Objeto (my suit) + Participio pasado (cleaned)."},
    {"q": "Subjunctive: The manager demanded that she ___ early tomorrow.", "opts": ["arrive", "arrives", "arrived", "will arrive"], "ans": "arrive", "exp": "Subjuntivo: Tras verbos de demanda, se usa el verbo base para todos los sujetos."},
    {"q": "Cleft Sentence: ___ was John who broke the printer.", "opts": ["It", "He", "There", "That"], "ans": "It", "exp": "Estructura de énfasis: It + is/was + sujeto + who/that."},
    {"q": "Participle Clause: ___ all the money, we had to walk home.", "opts": ["Having spent", "Spent", "To spend", "Spending"], "ans": "Having spent", "exp": "Cláusula de participio para mostrar una acción que ocurrió antes que la principal."},
    {"q": "Third Conditional: If I ___ the train, I would have missed the flight.", "opts": ["hadn't caught", "didn't catch", "don't catch", "wouldn't catch"], "ans": "hadn't caught", "exp": "Estructura irreal en el pasado: If + Past Perfect."},
    {"q": "Adjectivization: Her behavior was completely ___; she wouldn't listen to reason.", "opts": ["irrational", "irrationalize", "irrationality", "irrationable"], "ans": "irrational", "exp": "Adjetivo formado a partir de la raíz 'ration' con prefijo 'ir-' y sufijo '-al'."}
]

# ==========================================
# 4. APLICACIÓN PRINCIPAL
# ==========================================
# Encabezado visual
st.markdown("""
<div class='header-box'>
    <h1>🏛️ Advanced English C1/C2</h1>
    <p>Academic Rigor • Structural Mastery • Professional Vocabulary</p>
</div>
""", unsafe_allow_html=True)

# Menú lateral elegante
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/1903/1903162.png", width=80)
st.sidebar.title("Navegación C1/C2")
menu = st.sidebar.radio("Selecciona un módulo:", ["📚 Vocabulary Database", "🧩 Advanced Grammar (15 Topics)", "📝 Randomized Quiz"])

# Cargar CSV de vocabulario (Reutilizamos la función)
@st.cache_data
def cargar_vocabulario():
    if os.path.exists('vocabulario_avanzado.csv'):
        return pd.read_csv('vocabulario_avanzado.csv', encoding='utf-8')
    return pd.DataFrame()

df_vocab = cargar_vocabulario()

# --- MÓDULO 1: VOCABULARIO ---
if menu == "📚 Vocabulary Database":
    st.markdown("### Base de Datos de Nivel Avanzado")
    if not df_vocab.empty:
        col1, col2 = st.columns([1, 2])
        with col1:
            categorias = df_vocab["Categoría Gramatical"].unique()
            cat_sel = st.selectbox("📂 Filtrar por categoría:", categorias)
        with col2:
            st.info("💡 Usa el buscador de la tabla o haz clic en las columnas para ordenar alfabéticamente.")
            
        df_mostrar = df_vocab[df_vocab["Categoría Gramatical"] == cat_sel][["Palabra en Inglés", "Traducción"]].sort_values(by="Palabra en Inglés").reset_index(drop=True)
        st.dataframe(df_mostrar, use_container_width=True, height=500)
    else:
        st.error("⚠️ Sube tu archivo 'vocabulario_avanzado.csv' a GitHub para ver la lista.")

# --- MÓDULO 2: GRAMÁTICA AVANZADA ---
elif menu == "🧩 Advanced Grammar (15 Topics)":
    colA, colB = st.columns([1, 2])
    with colA:
        st.image("https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?ixlib=rb-1.2.1&auto=format&fit=crop&w=600&q=80", use_container_width=True)
    with colB:
        st.markdown("### Mastery of Complex Structures")
        st.write("Selecciona uno de los 15 temas avanzados de la lista desplegable para analizar su estructura formal.")
        tema_seleccionado = st.selectbox("📌 Seleccionar Tema Gramatical:", list(temas_avanzados.keys()))

    datos = temas_avanzados[tema_seleccionado]
    
    st.markdown(f"""
    <div class='grammar-card'>
        <h4>{tema_seleccionado}</h4>
        <p><b>📖 Uso Contextual:</b> {datos['uso']}</p>
        <div style='background-color: #e8f5e9; padding: 15px; border-radius: 8px; margin: 15px 0;'>
            <p style='margin:0; color: #1b5e20;'><b>📐 Fórmula Estructural:</b><br>{datos['formula']}</p>
        </div>
        <p><b>💡 Ejemplo Práctico:</b><br><i>{datos['ejemplo']}</i></p>
    </div>
    """, unsafe_allow_html=True)

# --- MÓDULO 3: QUIZ ALEATORIO ---
elif menu == "📝 Randomized Quiz":
    st.markdown("### C1/C2 Proficiency Test")
    st.write("El sistema selecciona 5 preguntas al azar del banco de datos. ¡Pon a prueba tu dominio estructural!")
    
    # Motor de aleatoriedad
    if 'quiz_actual' not in st.session_state:
        # Extrae 5 preguntas al azar sin repetirse
        st.session_state.quiz_actual = random.sample(banco_preguntas, 5)
        st.session_state.calificado = False

    if st.button("🔄 Generar Nuevo Test Aleatorio"):
        st.session_state.quiz_actual = random.sample(banco_preguntas, 5)
        st.session_state.calificado = False
        st.rerun()

    respuestas_usuario = {}
    
    # Mostrar el test generado
    for i, ej in enumerate(st.session_state.quiz_actual):
        st.markdown(f"**{i+1}. {ej['q']}**")
        respuestas_usuario[i] = st.radio("Opciones:", ej['opts'], key=f"rad_{i}", index=None, label_visibility="collapsed")
        st.write("---")
        
    if st.button("✅ Calificar Examen", type="primary"):
        puntaje = 0
        for i, ej in enumerate(st.session_state.quiz_actual):
            if respuestas_usuario[i] == ej['ans']:
                st.success(f"Pregunta {i+1}: ¡Correcto! ({ej['ans']})")
                puntaje += 1
            else:
                st.error(f"Pregunta {i+1}: Incorrecto. La respuesta es **{ej['ans']}**.")
            st.caption(f"Explicación: {ej['exp']}")
            
        st.markdown(f"### 🏆 Puntaje Final: {puntaje} / 5")
        if puntaje == 5:
            st.balloons()
