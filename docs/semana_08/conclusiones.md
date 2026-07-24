# Informe - Semana 8

## Conclusiones del Proyecto

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

## 1. Sobre el objetivo general

Se desarrolló un sistema completo de predicción de churn para clientes B2B que integra procesamiento distribuido, modelado predictivo y visualización, cumpliendo el objetivo general planteado en la Semana 1. La solución identifica clientes en riesgo con la ventana de anticipación de 90 días definida en el alcance del proyecto.

---

## 2. Sobre el proceso de datos

- La **arquitectura Medallion** demostró ser adecuada para el problema: la separación en capas Bronze, Silver y Gold permitió aislar el dato crudo del dato analítico y mantener trazabilidad en todo el proceso.

- La integración de **siete fuentes heterogéneas** en una vista única por empresa validó la hipótesis de que el churn corporativo requiere una visión integral del cliente, y no el análisis aislado de una sola dimensión.

- El uso de **Apache Spark** permitió procesar el volumen consolidado de forma distribuida, con un pipeline que escalaría sin cambios de código ante un aumento significativo de registros.

- El dataset final consolidó **5,000 empresas** con **30 columnas**, de las cuales 23 fueron utilizadas como variables predictivas.

---

## 3. Sobre los hallazgos analíticos

- Los factores más asociados al abandono corresponden a la **calidad técnica del servicio y la experiencia de soporte** (duración de incidencias, tiempo de resolución y tickets escalados), por encima de las variables financieras y de consumo.

- Los indicadores de satisfacción (**NPS** y **CSAT**) mostraron correlación negativa fuerte con el churn, confirmando su valor como señales tempranas de riesgo.

- La tasa de churn observada fue de **16.80 %** (840 de 5,000 clientes), un desbalance moderado que exige evaluar el modelo con métricas más informativas que el Accuracy.

---

## 4. Sobre el modelo

- El algoritmo **Gradient Boosted Trees (GBTClassifier)** resultó apropiado por su capacidad de manejar variables numéricas y categóricas, y por su integración nativa con Spark MLlib.

- El modelo obtuvo **Accuracy, Precision, Recall y F1-Score de 1.00** sobre el conjunto de prueba de 958 registros, con cero falsos positivos y cero falsos negativos.

- **Estas métricas perfectas se explican por la naturaleza sintética del dataset y no por el desempeño del algoritmo.** El análisis del dataset Gold reveló que siete variables separan las clases sin ningún solapamiento; una regla trivial de un solo umbral alcanza el mismo 100 % de exactitud sin necesidad de Machine Learning. El modelo, por tanto, no ha sido validado en condiciones realistas.

- La omisión del cálculo de **ROC-AUC** dejó sin verificar uno de los indicadores de éxito comprometidos en la definición del proyecto.

---

## 5. Sobre la solución tecnológica

- La integración entre **Databricks, MongoDB Atlas, FastAPI y Next.js** demostró que es viable construir una cadena completa desde el procesamiento analítico hasta una interfaz de negocio utilizando exclusivamente herramientas gratuitas o de capa libre.

- El dashboard **Telco AI** traduce la salida técnica del modelo en información accionable, organizada por perfil de usuario y con niveles de riesgo interpretables por personal no técnico.

---

## 6. Conclusión general

El proyecto cumplió íntegramente su propósito formativo y técnico: se construyó un pipeline completo, funcional y reproducible que abarca desde la ingesta de datos crudos hasta un dashboard operativo en la nube. Ese pipeline constituye el activo real del proyecto y operaría de la misma forma con datos reales.

La principal lección metodológica obtenida es que **un resultado perfecto en un problema de negocio complejo debe tratarse como una señal de alerta y no como un logro**. La verificación de solapamiento entre clases y la revisión de correlaciones extremas con la variable objetivo deberían formar parte del protocolo estándar de validación de cualquier modelo antes de darlo por concluido.

---

*Semana 8 — Informe Final | Big Data DD283 — Universidad Autónoma del Perú*
