# Evaluación de Árbol de Decisión para Servicio Delivery

Esta es una aplicación interactiva desarrollada en Python utilizando [Streamlit](https://streamlit.io/). La herramienta permite evaluar diferentes subopciones y sus probabilidades para tomar la mejor decisión (Sistema propio vs. Subcontratar) en un servicio de delivery, basándose en el análisis del Valor Esperado.

## Características

- **Interfaz Interactiva**: Permite ajustar los costos, meses de implementación, así como las probabilidades y ventas para distintos escenarios (Bueno, Moderado, Pobre) a través de una barra lateral.
- **Cálculo de Valores Esperados**: Calcula automáticamente el Valor Esperado (VE) para cada subopción y determina la mejor decisión de forma global (ver fórmulas y detalle matemático en [`explicacion_problema.md`](./explicacion_problema.md)).
- **Visualización Gráfica**: Muestra un gráfico de barras dinámico comparando los valores esperados de cada alternativa.
- **Árbol de Decisión Dinámico**: Genera un diagrama de árbol de decisión utilizando `Graphviz` para visualizar todas las rutas posibles.
- **Generación de Reportes PDF**: Permite exportar los resultados, recomendaciones y gráficos generados directamente a un documento PDF.

## Requisitos Previos

Para ejecutar la aplicación localmente, necesitas tener instalado Python y las siguientes librerías:

- `streamlit`
- `pandas`
- `matplotlib`
- `fpdf`
- `graphviz`
- `Pillow`

### Importante: Instalación de Graphviz
Adicionalmente a la librería de Python, esta aplicación requiere tener instalado el software real de **Graphviz** en el sistema operativo para poder generar y dibujar el árbol de decisión y exportarlo a PDF.

Si utilizas **Windows**, la forma más fácil y rápida de instalarlo es abrir una terminal (PowerShell o CMD) y ejecutar el siguiente comando:
```bash
winget install graphviz
```
*(Nota: Si lo instalas manualmente desde [su página oficial](https://graphviz.org/download/), asegúrate de agregar la ruta de instalación a tus variables de entorno o ajustar la línea correspondiente en `app.py`).*

## Instalación y Ejecución

1. Clona este repositorio o descarga el código fuente.
2. Instala las dependencias requeridas ejecutando:
   ```bash
   pip install streamlit pandas matplotlib fpdf graphviz Pillow
   ```
3. Ejecuta la aplicación de Streamlit:
   ```bash
   streamlit run app.py
   ```
4. Abre tu navegador en la URL que se indica en la consola (por lo general, `http://localhost:8501`).

## Modo de Uso

1. Utiliza la barra lateral para ajustar los **Parámetros de Entrada** según el caso que desees simular.
2. Observa cómo cambian los valores esperados y el gráfico principal en tiempo real.
3. Revisa la sección de **Recomendaciones** para identificar la decisión óptima calculada.
4. Explora el **Árbol de Decisión** generado visualmente en la parte inferior de la página.
5. Haz clic en el botón **Guardar en PDF** para generar y descargar un reporte completo con los resultados.

## Licencia

Este proyecto es de uso libre con fines educativos y analíticos.
