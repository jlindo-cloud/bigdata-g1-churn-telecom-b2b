# Informe - Semana 8

## Recomendaciones del Proyecto

---

## Proyecto

Sistema de Predicción de Churn para Clientes de una Empresa de Telecomunicaciones B2B utilizando Big Data y Machine Learning

---

## Integrantes:

- Asto Arotinco Ana (0000-0002-2195-0764)
- Flores Condeña Javier (0000-0003-2800-5084)
- Lindo Barrientos Jhonn Viequier (0000-0001-6025-7332)
- Tito Paredes Arian (0009-0002-5717-8099)
- Quispe Poma Cristian (0009-0008-6566-3741)

---

## 1. Prioridad alta — Validez del modelo

| Recomendación | Justificación |
|---|---|
| Validar el modelo con datos reales o con un dataset sintético que incorpore ruido y solapamiento entre clases | Es la única forma de conocer el desempeño verdadero del clasificador; los resultados actuales no son extrapolables a producción |
| Calcular e informar ROC-AUC y la curva Precision-Recall | Cierra la brecha con el indicador de éxito comprometido en la Semana 1 y describe el comportamiento del modelo ante distintos umbrales de decisión |
| Auditar el conjunto de variables de entrada y excluir explícitamente `risk_score` | Previene fuga de información (*data leakage*) desde variables derivadas de la etiqueta objetivo |
| Incorporar validación cruzada (k-fold) en lugar de una única partición Hold-Out | Reduce la dependencia del resultado respecto de una partición particular y ofrece una estimación más estable del desempeño |

---

## 2. Prioridad media — Robustez técnica

- Implementar **autenticación real con control de acceso por rol** en el dashboard, sustituyendo el modo de demostración actual.
- **Automatizar la actualización de predicciones** mediante un proceso programado, evitando la sincronización manual desde el módulo de Administración.
- Registrar el **versionado de modelos** y su historial de métricas, para detectar degradación del desempeño en el tiempo.
- Establecer **pruebas automatizadas de calidad de datos** sobre la capa Silver, con umbrales definidos de valores nulos, duplicados e integridad referencial.

---

## 3. Prioridad media — Aprovechamiento del negocio

- **Priorizar la gestión de retención cruzando el nivel de riesgo con la facturación anual** del cliente, de modo que el esfuerzo comercial se concentre donde el ingreso en juego es mayor.
- **Actuar sobre las causas identificadas en el análisis:** dado que las variables dominantes son operativas, las acciones de mayor impacto son reducir la duración de incidencias y los tiempos de resolución, más que ofrecer descuentos o incentivos comerciales.
- Definir un **protocolo de intervención por nivel de riesgo**, asignando responsables y plazos de contacto diferenciados según la criticidad del cliente.
- **Medir sistemáticamente la efectividad** de las campañas de retención mediante el indicador de conversiones exitosas ya presente en el dashboard.

---

## 4. Trabajo futuro

- Incorporar **variables temporales** que capturen la tendencia del comportamiento (variación del consumo o de la facturación en los últimos tres y seis meses) en lugar de únicamente valores agregados históricos.
- Evaluar técnicas de **interpretabilidad** como SHAP para explicar las predicciones individuales, requisito frecuente para la adopción del modelo por parte de las áreas comerciales.
- Explorar el **procesamiento en streaming** para detectar cambios de comportamiento en ventanas de tiempo más cortas.
- Ampliar el alcance hacia un **modelo de estimación del valor en riesgo**, que combine la probabilidad de abandono con el ingreso asociado a cada cliente.

---

*Semana 8 — Informe Final | Big Data DD283 — Universidad Autónoma del Perú*
