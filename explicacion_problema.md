# Caso de Estudio: Análisis de Mejora del Servicio de Delivery

## Descripción del Problema

Una empresa del sector gastronómico ha detectado que su servicio de entregas a domicilio actual está generando demoras y reduciendo la satisfacción de los clientes. La gerencia ha decidido invertir para **mejorar el servicio de delivery** y se enfrenta a una decisión estratégica. Tienen dos alternativas principales:

1. **Opción A: Desarrollar un sistema de delivery propio.**
2. **Opción B: Subcontratar el servicio a una empresa externa.**

A su vez, cada una de estas opciones presenta dos subopciones que varían en términos de inversión de capital (costo inicial), tiempo necesario para estar operativas (meses) y los resultados financieros esperados en base al comportamiento del mercado.

### Alternativas y Subopciones

#### A. Sistema Propio
- **A1. Equipo Profesional**: Implica contratar a una agencia o desarrolladores senior. Es más estructurado, pero requiere una inversión inicial alta.
- **A2. Equipo de Freelancers**: Una alternativa más económica y tal vez más rápida, pero que podría implicar distintas probabilidades de éxito.

#### B. Subcontratar
- **B1. Empresa Top del mercado**: Garantiza calidad y cobertura, pero con un costo y/o comisiones más elevadas.
- **B2. Empresa Barata**: Menor costo, pero podría traer riesgos en la percepción del servicio por parte del cliente.

### Variables del Modelo

Para tomar una decisión matemática e informada sobre cada una de las 4 subopciones (A1, A2, B1, B2), el negocio ha estimado los siguientes parámetros:
- **Costo de Inversión (S/)**: Dinero requerido para iniciar la alternativa.
- **Meses de implementación**: Tiempo necesario para poner en marcha la solución.
- **Escenarios de Venta**: Se proyectan tres posibles respuestas por parte del mercado, cada una con su probabilidad de ocurrir y el nivel de ventas que generaría:
  - **Buena**: Probabilidad (%) y Ventas estimadas (S/).
  - **Moderada**: Probabilidad (%) y Ventas estimadas (S/).
  - **Pobre**: Probabilidad (%) y Ventas estimadas (S/).

---

## ¿Cómo resuelve este problema la aplicación `app.py`?

El problema se resuelve modelando un **Árbol de Decisión** y aplicando el criterio del **Valor Esperado (VE)**. La aplicación desarrollada en Streamlit permite automatizar y visualizar toda esta evaluación.

1. **Simulación de Escenarios (Ingreso de Datos)**
   La aplicación expone una barra lateral donde el analista de negocios puede iterar con las estimaciones. Permite ajustar dinámicamente cuánto costará, cuánto tardará y cuáles son las probabilidades de éxito para cada subopción.

2. **Cálculo del Valor Esperado (VE)**
   Para cada subopción, el script calcula matemáticamente cuánto dinero se espera ganar en promedio considerando el riesgo de los tres escenarios. La fórmula general para el Valor Esperado es la sumatoria del producto entre la probabilidad de cada evento y su ganancia/pago asociado:

$$
VE = \sum_{i=1}^{n} (P_i \times V_i)
$$

   Donde $P_i$ es la probabilidad de que ocurra el escenario $i$, y $V_i$ son las ventas proyectadas en dicho escenario.

   Aplicado a nuestro problema específico con 3 escenarios (Buena, Moderada, Pobre), la fórmula expandida que ejecuta automáticamente el sistema es:

$$
VE = (P_{Buena} \times V_{Buena}) + (P_{Moderada} \times V_{Moderada}) + (P_{Pobre} \times V_{Pobre})
$$

3. **Toma de Decisión Automatizada**
   Una vez calculados los VE de las cuatro subopciones, la aplicación ordena y determina la mejor alternativa para el "Sistema propio", la mejor para "Subcontratar" y, finalmente, la **Decisión Óptima Global**. Para evaluar la opción global, la app prioriza primero el mayor Valor Esperado, usando el menor tiempo de implementación y menor costo como criterios de desempate.

4. **Análisis Visual y Generación de Reportes**
   - **Gráfico Comparativo**: Genera un gráfico de barras para visualizar rápidamente qué opción promete mayor rentabilidad esperada.
   - **Árbol de Decisión**: Mediante la librería *Graphviz*, el sistema dibuja automáticamente el árbol mostrando las decisiones (cuadrados/nodos iniciales), los eventos probabilísticos (rutas) y los pagos en cada hoja.
   - **Exportación Profesional**: Compila todos los resultados, las recomendaciones estratégicas y los gráficos en un reporte **PDF**, lo que permite entregar una justificación analítica formal a la gerencia para respaldar la decisión final.
