"""
Aplicación Streamlit para la Evaluación de un Árbol de Decisión (Servicio de Delivery).
Calcula y compara el Valor Esperado de desarrollar un sistema propio vs. subcontratar.
"""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import tempfile
import os
import platform
from graphviz import Digraph
from PIL import Image

# Configuración de ruta para Graphviz (Ayuda a evitar errores en Windows si no está en el PATH global)
if platform.system() == "Windows":
    graphviz_path = r"C:\Program Files\Graphviz\bin"
    if os.path.exists(graphviz_path) and graphviz_path not in os.environ["PATH"]:
        os.environ["PATH"] += os.pathsep + graphviz_path

st.set_page_config(page_title="Árbol de Decisión", layout="centered")
st.title("Evaluación de Árbol de Decisión para Servicio Delivery")

# --- Entradas de la barra lateral ---
st.sidebar.header("Parámetros de Entrada")
titles = ["A1. Profesional", "A2. Freelancers", "B1. Empresa top", "B2. Empresa barata"]
key_map = {"A1": titles[0], "A2": titles[1], "B1": titles[2], "B2": titles[3]}
params = {}

for full in titles:
    st.sidebar.subheader(full)
    cost = st.sidebar.number_input(f"Costo (S/) {full}", min_value=0.0, value=5000.0, step=500.0, key=f"cost_{full}")
    months = st.sidebar.number_input(f"Meses de implementación {full}", min_value=1, value=1, step=1, key=f"months_{full}")
    p_good = st.sidebar.slider(f"Probabilidad Buena (%) {full}", 0, 100, 40, key=f"pB_{full}")
    p_mod = st.sidebar.slider(f"Probabilidad Moderada (%) {full}", 0, 100, 40, key=f"pM_{full}")
    p_poor = max(0, 100 - (p_good + p_mod))
    st.sidebar.markdown(f"Probabilidad Pobre (%) **{p_poor}**")
    
    v_good = st.sidebar.number_input(f"Ventas Buena (S/) {full}", min_value=0.0, value=15000.0, step=1000.0, key=f"vB_{full}")
    v_mod = st.sidebar.number_input(f"Ventas Moderada (S/) {full}", min_value=0.0, value=10000.0, step=1000.0, key=f"vM_{full}")
    v_poor = st.sidebar.number_input(f"Ventas Pobre (S/) {full}", min_value=0.0, value=5000.0, step=1000.0, key=f"vP_{full}")
    
    params[full] = {"cost": cost, "months": months, "p": [p_good/100, p_mod/100, p_poor/100], "v": [v_good, v_mod, v_poor]}

# --- Calcular valores esperados ---
records = []
for full, d in params.items():
    ev = sum(p * v for p, v in zip(d["p"], d["v"]))
    records.append({"Subopción": full, "Costo (S/)": d["cost"], "Meses": d["months"], "VE (S/)": ev})

df = pd.DataFrame(records)

# Mostrar tabla en la aplicación
st.subheader("Valores Esperados de cada Subopción")
st.dataframe(df.set_index("Subopción"), use_container_width=True)

# Mostrar gráfico de barras
st.subheader("Comparación de Valor Esperado")
fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(df["Subopción"], df["VE (S/)"], color='skyblue', edgecolor='black')
ax.set_ylabel("VE (S/)")
plt.xticks(rotation=45, ha='right')
st.pyplot(fig)

# Determinar las mejores opciones
best_A = df[df["Subopción"].str.startswith("A")].sort_values(by=["VE (S/)", "Meses", "Costo (S/)"] , ascending=[False, True, True]).iloc[0]
best_B = df[df["Subopción"].str.startswith("B")].sort_values(by=["VE (S/)", "Meses", "Costo (S/)"] , ascending=[False, True, True]).iloc[0]
best_global = df.sort_values(by=["VE (S/)", "Meses", "Costo (S/)"] , ascending=[False, True, True]).iloc[0]

# Mostrar recomendaciones
st.markdown("### Recomendaciones")
st.markdown(f"- **Mejor en Sistema Propio (A):** {best_A['Subopción']} (VE = S/ {best_A['VE (S/)']:.2f}, Meses = {int(best_A['Meses'])}, Costo = S/ {best_A['Costo (S/)']:.2f})")
st.markdown(f"- **Mejor al Subcontratar (B):** {best_B['Subopción']} (VE = S/ {best_B['VE (S/)']:.2f}, Meses = {int(best_B['Meses'])}, Costo = S/ {best_B['Costo (S/)']:.2f})")
st.success(f"**Decisión Óptima Global:** {best_global['Subopción']} (VE = S/ {best_global['VE (S/)']:.2f}, Meses = {int(best_global['Meses'])}, Costo = S/ {best_global['Costo (S/)']:.2f})")

# Construir árbol de decisión
edges = [("Root", "A"), ("Root", "B")]
outcomes = ["Buena", "Moderada", "Pobre"]

for key, full in key_map.items():
    parent = "A" if key.startswith("A") else "B"
    edges.append((parent, key))
    for i in range(3): 
        edges.append((key, f"{key}_{i}"))

dot = Digraph(graph_attr={'rankdir':'LR'})
dot.node("Root", "Mejorar servicio delivery")
dot.node("A", "Sistema propio")
dot.node("B", "Subcontratar")

for key, full in key_map.items(): 
    dot.node(key, full.split('. ', 1)[1])

for p, c in edges: 
    dot.edge(p, c)

for key, full in key_map.items():
    for i, o in enumerate(outcomes):
        txt = f"{o}\nP={params[full]['p'][i]:.0%}\nV={params[full]['v'][i]:.0f}"
        dot.node(f"{key}_{i}", txt)

st.subheader("Árbol de Decisión")
st.graphviz_chart(dot)

# Generación del PDF
if st.button("Guardar en PDF"):
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_chart:
        chart_path = tmp_chart.name
    fig.savefig(chart_path, bbox_inches='tight')
    
    tree_png = dot.pipe(format='png')
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_tree:
        tree_path = tmp_tree.name
        tmp_tree.write(tree_png)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Página 1: Tabla y recomendación
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, 'Reporte: Árbol de Decisión Delivery', ln=True, align='C')
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, 'Valores Esperados por Subopción', ln=True)
    pdf.ln(2)
    
    col_w = [45, 35, 25, 35]
    hdr = ['Subopción', 'Costo (S/)', 'Meses', 'VE (S/)']
    pdf.set_font("Arial", 'B', 10)
    for w, h in zip(col_w, hdr): 
        pdf.cell(w, 8, h, border=1, align='C')
    pdf.ln()
    
    pdf.set_font("Arial", '', 10)
    for _, r in df.iterrows():
        pdf.cell(col_w[0], 6, str(r['Subopción']), border=1)
        pdf.cell(col_w[1], 6, f"S/ {r['Costo (S/)']:.2f}", border=1, align='R')
        pdf.cell(col_w[2], 6, str(int(r['Meses'])), border=1, align='C')
        pdf.cell(col_w[3], 6, f"S/ {r['VE (S/)']:.2f}", border=1, align='R')
        pdf.ln()
        
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, 'Recomendación Óptima', ln=True)
    pdf.set_font("Arial", '', 10)
    pdf.multi_cell(0, 6, f"{best_global['Subopción']} (VE = S/ {best_global['VE (S/)']:.2f}, Meses = {int(best_global['Meses'])}, Costo = S/ {best_global['Costo (S/)']:.2f})")
    
    # Insertar gráfico ajustado
    pdf.set_auto_page_break(False)
    img = Image.open(chart_path)
    ow, oh = img.size
    x_m, y_m = 10, pdf.get_y() + 5
    max_w, max_h = pdf.w - 2 * x_m, pdf.h - y_m - 15
    scale = min(max_w / ow, max_h / oh)
    pdf.image(chart_path, x=x_m, y=y_m, w=ow * scale, h=oh * scale)
    pdf.set_auto_page_break(True, margin=15)

    # Página 2: Árbol de decisión
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, 'Árbol de Decisión', ln=True)
    
    img2 = Image.open(tree_path)
    tw, th = img2.size
    x2, y2 = 10, 20
    mw2, mh2 = pdf.w - 2 * x2, pdf.h - y2 - 15
    sc2 = min(mw2 / tw, mh2 / th)
    pdf.image(tree_path, x=x2, y=y2, w=tw * sc2, h=th * sc2)

    # Eliminar temporales
    for p in [chart_path, tree_path]:
        try:
            os.remove(p)
        except Exception:
            pass

    # Descarga del PDF
    out = 'decision_tree_report.pdf'
    pdf.output(out)
    with open(out, 'rb') as f: 
        st.download_button('Descargar PDF', f, file_name=out, mime='application/pdf')

st.markdown('---')
st.markdown('*Ajusta los parámetros en la barra lateral y genera tu reporte en PDF.*')
