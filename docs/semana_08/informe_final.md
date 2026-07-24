# Informe - Semana 8

## Informe Final del Proyecto

---

## Proyecto

Sistema de Predicción de Churn para Clientes de una Empresa de Telecomunicaciones B2B utilizando Big Data y Machine Learning

---

## Objetivo

Documentar de forma integral el proyecto desarrollado a lo largo de ocho semanas, consolidando la metodología aplicada, los resultados obtenidos en cada etapa, el análisis crítico del desempeño del modelo y las recomendaciones derivadas para su aplicación en un entorno de negocio real.

---

## Integrantes:

- Asto Arotinco Ana (0000-0002-2195-0764)
- Flores Condeña Javier (0000-0003-2800-5084)
- Lindo Barrientos Jhonn Viequier (0000-0001-6025-7332)
- Tito Paredes Arian (0009-0002-5717-8099)
- Quispe Poma Cristian (0009-0008-6566-3741)

---

## Datos generales

| Campo | Detalle |
|---|---|
| **Curso** | Big Data (DD283) — Ciclo VIII |
| **Docente** | Mg. Rubén Quispe Llacctarimay |
| **Semestre** | 2026-1 |
| **Entregable** | Semana 8 — Informe Final |
| **Repositorio** | github.com/jlindo-cloud/bigdata-g1-churn-telecom-b2b |
| **Dashboard** | v0-churntelco2b2.vercel.app |
| **Video de demostración** | https://drive.google.com/file/d/1SbeNbehBP5sFfGkmTlNcg1f9zYW2vYNi/view |
| **Presentación final** | https://www.canva.com/design/DAHQPKtfiLA/nGreNzr4fD-P_MBnThFVHg/edit |

---

## Entregables de la Semana 8

| Entregable | Archivo / Enlace |
|---|---|
| Informe final (PDF) | `docs/semana_08/informe_final.pdf` |
| Informe final (Markdown) | `docs/semana_08/informe_final.md` |
| Conclusiones | `docs/semana_08/conclusiones.md` |
| Recomendaciones | `docs/semana_08/recomendaciones.md` |
| Presentación final (Canva / PPTX) | [Ver presentación](https://www.canva.com/design/DAHQPKtfiLA/nGreNzr4fD-P_MBnThFVHg/edit) |
| Video de demostración del modelo y dashboard | [Ver video](https://drive.google.com/file/d/1SbeNbehBP5sFfGkmTlNcg1f9zYW2vYNi/view) |

---

# 1. Resumen ejecutivo

El presente informe documenta el desarrollo completo de un sistema de predicción de churn (abandono de clientes) para el segmento corporativo B2B de una empresa de telecomunicaciones, construido a lo largo de ocho semanas mediante tecnologías de Big Data y Machine Learning.

El proyecto integró siete fuentes de datos independientes —información maestra de empresas, servicios contratados, consumo, facturación, tickets de soporte, eventos de red y registro histórico de churn— en un dataset consolidado de **5,000 clientes empresariales** y 30 variables, aplicando una arquitectura **Medallion (Bronze, Silver y Gold)** sobre Apache Spark en Databricks Community Edition.

Sobre ese dataset se entrenó un modelo de clasificación binaria **Gradient Boosted Trees (GBTClassifier)** de Spark MLlib, cuyas predicciones fueron persistidas en MongoDB Atlas y expuestas mediante un backend en FastAPI hacia un dashboard web desarrollado en Next.js y desplegado en Vercel, denominado **Telco AI**.

El modelo alcanzó un desempeño de 100 % en Accuracy, Precision, Recall y F1-Score sobre el conjunto de prueba. Como se analiza en detalle en la **Sección 7**, este resultado no debe interpretarse como evidencia de un modelo excepcional, sino como consecuencia directa de la naturaleza sintética del conjunto de datos empleado, en el que varias variables separan las clases de forma perfecta. El informe documenta este hallazgo de manera transparente y propone las acciones correctivas correspondientes.

## Resultados en una mirada

| Dimensión | Resultado obtenido |
|---|---|
| Clientes analizados | 5,000 empresas |
| Variables consolidadas | 30 (23 predictivas tras la ingeniería de variables) |
| Tasa de churn en la base | 16.80 % (840 de 5,000 clientes) |
| Modelo campeón | Gradient Boosted Trees (Spark MLlib) |
| Conjunto de prueba | 958 registros (808 no churn / 150 churn) |
| Métricas obtenidas | Accuracy, Precision, Recall y F1-Score = 1.00 |
| Producto final | Dashboard web Telco AI operativo en la nube |

---

# 2. Introducción y planteamiento del problema

## 2.1 Contexto

Las empresas de telecomunicaciones que atienden clientes corporativos enfrentan de forma permanente el riesgo de pérdida de cartera por factores como deterioro de la calidad del servicio, incidencias recurrentes de red, disminución del consumo, insatisfacción con la atención recibida y ofertas de la competencia. A diferencia del segmento masivo, la pérdida de un solo cliente corporativo tiene un impacto económico considerable, dado que estos clientes suelen mantener múltiples servicios contratados y generar facturación recurrente de alto valor.

## 2.2 Problema identificado

La organización no dispone de un mecanismo que permita identificar de forma anticipada qué clientes empresariales presentan riesgo de abandonar los servicios contratados. La detección tardía impide ejecutar estrategias de retención efectivas y se traduce en pérdidas económicas asociadas a la cancelación de contratos.

## 2.3 Pregunta de investigación

> ¿Es posible predecir con al menos 90 días de anticipación qué clientes corporativos presentan una alta probabilidad de churn, utilizando técnicas de Big Data y Machine Learning?

## 2.4 Objetivos

### Objetivo general

Desarrollar un modelo predictivo basado en Big Data y Machine Learning que permita identificar clientes B2B con riesgo de abandono con una anticipación mínima de 90 días.

### Objetivos específicos

1. Integrar información proveniente de múltiples fuentes relacionadas con clientes, servicios, consumo, facturación, tickets de soporte e incidencias de red.
2. Ejecutar procesos de limpieza, transformación y validación que garanticen la calidad de los datos.
3. Analizar los factores que influyen en el churn mediante análisis exploratorio de datos.
4. Construir variables predictivas que representen el comportamiento histórico de los clientes.
5. Entrenar y evaluar modelos de Machine Learning para la predicción de churn.
6. Comparar algoritmos de clasificación y seleccionar el de mejor desempeño.
7. Diseñar un dashboard que permita visualizar los clientes en riesgo y apoyar la toma de decisiones.

## 2.5 Alcance y exclusiones

| Incluido en el alcance | Excluido del alcance |
|---|---|
| Integración de siete fuentes de datos empresariales | Implementación en ambiente productivo |
| Procesamiento, limpieza y validación de información | Integración con sistemas transaccionales reales |
| Análisis exploratorio y construcción de variables | Automatización de campañas comerciales |
| Entrenamiento y evaluación de modelos de clasificación | Procesamiento en tiempo real (streaming) |
| Generación de indicadores de riesgo y dashboard | Reentrenamiento automático del modelo |

---

# 3. Metodología

El proyecto se desarrolló siguiendo un enfoque incremental de ocho semanas, en el que cada etapa produjo entregables verificables que alimentaron la siguiente. La metodología se apoyó en el ciclo estándar de un proyecto analítico: comprensión del negocio, comprensión y preparación de los datos, modelado, evaluación y despliegue.

## 3.1 Plan de trabajo ejecutado

| Semana | Etapa | Entregable principal |
|---|---|---|
| 1 | Definición del problema | Problema de negocio, objetivos, alcance y cronograma |
| 2 | Diseño de datos | Fuentes documentadas, modelo relacional y diccionario de datos |
| 3 | ETL y calidad de datos | Proceso ETL Medallion, informe de calidad, dataset validado |
| 4 | Análisis exploratorio | Notebook de EDA, visualizaciones y variables relevantes |
| 5 | Ingeniería de variables | Catálogo de features y dataset final para modelado |
| 6 | Machine Learning | Modelo entrenado, métricas y selección del modelo campeón |
| 7 | Dashboard y visualización | Dashboard Telco AI, capturas e instrucciones de uso |
| 8 | Informe final | Documentación integral, resultados y recomendaciones |

## 3.2 Fuentes de datos

Se utilizaron siete conjuntos de datos que representan dimensiones complementarias del comportamiento del cliente empresarial, permitiendo construir una visión integral de cada cuenta:

| Fuente | Dimensión del negocio | Aporte al modelo |
|---|---|---|
| `empresas.csv` | Información maestra | Variables demográficas y de segmentación |
| `servicios.csv` | Vinculación comercial | Cantidad y tipo de servicios contratados |
| `consumo.csv` | Uso del servicio | Consumo promedio, variación y tendencias |
| `facturacion.csv` | Comportamiento financiero | Facturación, morosidad y variación de ingresos |
| `tickets.csv` | Experiencia del cliente | Volumen de tickets, criticidad y tiempo de resolución |
| `eventos_red.csv` | Calidad técnica del servicio | Incidentes, indisponibilidad y frecuencia de fallas |
| `churn.csv` | Variable objetivo | Etiqueta de cliente activo (0) o con churn (1) |

## 3.3 Arquitectura del proceso ETL

El procesamiento se implementó sobre **Databricks Community Edition**, empleando Apache Spark y una arquitectura **Medallion** de tres capas, que separa con claridad el dato crudo del dato listo para el negocio:

| Capa | Propósito | Notebook |
|---|---|---|
| **Bronze** | Ingesta del dato crudo tal como llega desde los archivos de origen, sin transformación | `01_ingestion` / `02_bronze` |
| **Silver** | Limpieza, tipado, eliminación de duplicados, tratamiento de nulos y validación de integridad referencial por `company_id` | `03_silver` |
| **Gold** | Consolidación en una vista única por empresa con variables agregadas listas para análisis y modelado | `04_gold` |

```text
Archivos CSV → 01_ingestion → Bronze → 02_bronze → Silver → 03_silver
             → Gold → 04_gold → gold_dataset → 05_eda → feature_engineering → dataset_ml
```

> La ventaja de esta separación es la trazabilidad: ante cualquier inconsistencia detectada en el análisis, la capa Bronze conserva el dato original íntegro, lo que permite reprocesar sin pérdida de información.

## 3.4 Ingeniería de variables

A partir de la capa Gold se construyeron variables agregadas por empresa mediante funciones de agregación de Spark. El resultado fue un conjunto de 23 variables predictivas agrupadas en cinco dimensiones:

| Dimensión | Variables generadas |
|---|---|
| Perfil de la empresa | `empleados`, `sector_index`, `region_index`, `segmento_index` |
| Satisfacción | `nps`, `csat` |
| Financiera | `facturacion_total`, `facturacion_promedio`, `facturacion_maxima`, `dias_mora_promedio`, `deuda_total` |
| Consumo y servicios | `trafico_total_gb`, `trafico_promedio_gb`, `ancho_banda_promedio`, `pico_maximo_mbps`, `cantidad_servicios`, `monto_mensual_promedio`, `sla_promedio` |
| Soporte y red | `cantidad_tickets`, `tiempo_resolucion_promedio`, `tickets_escalados`, `cantidad_eventos`, `duracion_promedio_eventos` |

Las variables categóricas (sector, región y segmento) fueron convertidas a representación numérica mediante indexación, requisito para su procesamiento por el algoritmo de clasificación.

## 3.5 Modelado

Se evaluaron conceptualmente varios algoritmos de clasificación binaria y se implementó Gradient Boosted Trees. La decisión estuvo condicionada por el entorno de ejecución: XGBoost no se encuentra disponible en Databricks Community Edition, por lo que se optó por GBTClassifier de Spark MLlib, que ofrece un enfoque de boosting equivalente con integración nativa en el ecosistema Spark.

| Algoritmo | Estado en el proyecto |
|---|---|
| Regresión Logística | Evaluado conceptualmente, no implementado |
| Random Forest | Evaluado conceptualmente, no implementado |
| **Gradient Boosted Trees (GBTClassifier)** | **Implementado y seleccionado como modelo campeón** |
| XGBoost | Descartado por indisponibilidad en Databricks Community Edition |

### Configuración del entrenamiento

| Parámetro | Valor |
|---|---|
| Algoritmo | GBTClassifier (Spark MLlib) |
| Número de iteraciones (`maxIter`) | 100 |
| Profundidad máxima (`maxDepth`) | 5 |
| Semilla (`seed`) | 42 |
| Estrategia de partición | Hold-Out mediante `randomSplit` |
| Proporción entrenamiento / prueba | 80 % / 20 % |
| Construcción de features | `VectorAssembler` |

```python
GBTClassifier(
    labelCol="label",
    featuresCol="features",
    maxIter=100,
    maxDepth=5,
    seed=42
)
```

> El uso de una semilla fija garantiza la reproducibilidad del experimento: cualquier ejecución posterior sobre el mismo dataset producirá idéntica partición y resultados.

---

# 4. Resultados del procesamiento de datos

## 4.1 Dataset consolidado

| Indicador | Valor |
|---|---|
| Registros (empresas únicas) | 5,000 |
| Columnas totales | 30 |
| Variables predictivas utilizadas | 23 |
| Variable objetivo | `churn` (0 = activo, 1 = abandono) |
| Clientes activos | 4,160 (83.20 %) |
| Clientes con churn | 840 (16.80 %) |
| Formatos de persistencia | Parquet y CSV |

La distribución de la variable objetivo presenta un desbalance moderado de aproximadamente 5 a 1. Se trata de una proporción habitual en problemas de churn y no requiere necesariamente técnicas de remuestreo, aunque sí obliga a evaluar el modelo con métricas distintas al Accuracy, ya que un clasificador que prediga siempre la clase mayoritaria alcanzaría un 83.20 % de aciertos sin aportar valor alguno.

## 4.2 Hallazgos del análisis exploratorio

El análisis de correlación entre las variables predictivas y la variable objetivo arrojó los siguientes coeficientes, ordenados por magnitud:

| Variable | Correlación con churn | Interpretación |
|---|---:|---|
| `duracion_promedio_eventos` | 0.998 | A mayor duración de incidencias, mayor abandono |
| `tiempo_resolucion_promedio` | 0.992 | Demoras en resolver tickets impulsan el churn |
| `dias_mora_promedio` | 0.955 | La morosidad anticipa la salida del cliente |
| `tickets_escalados` | 0.941 | Escalamientos reflejan insatisfacción acumulada |
| `cantidad_eventos` | 0.905 | Frecuencia de fallas técnicas |
| `csat` | -0.879 | Menor satisfacción, mayor riesgo |
| `cantidad_tickets` | 0.858 | Volumen de incidencias reportadas |
| `nps` | -0.825 | Menor recomendación, mayor riesgo |
| `trafico_promedio_gb` | -0.295 | Caída de consumo asociada al abandono |

Desde la perspectiva del negocio, la lectura es consistente y accionable: **la calidad técnica del servicio y la experiencia de soporte son los factores dominantes del abandono**, por encima de las variables financieras o de consumo. Las cinco correlaciones más altas corresponden a incidencias de red y atención al cliente, lo que sugiere que las acciones de retención deberían priorizar la mejora operativa antes que los incentivos comerciales.

---

# 5. Resultados del modelo predictivo

## 5.1 Métricas de desempeño

El modelo fue evaluado sobre el conjunto de prueba, compuesto por 958 registros no vistos durante el entrenamiento:

| Métrica | Valor obtenido | Qué mide |
|---|---:|---|
| Accuracy | 1.00 | Proporción total de predicciones correctas |
| Precision | 1.00 | De los clientes marcados como churn, cuántos lo eran realmente |
| Recall | 1.00 | De los clientes que abandonaron, cuántos fueron detectados |
| F1-Score | 1.00 | Media armónica entre Precision y Recall |
| ROC-AUC | No calculada | Capacidad discriminatoria del clasificador |

## 5.2 Matriz de confusión

| | Predicción: No churn | Predicción: Churn |
|---|---:|---:|
| **Real: No churn** | 808 (VN) | 0 (FP) |
| **Real: Churn** | 0 (FN) | 150 (VP) |

Verdaderos positivos: 150 · Verdaderos negativos: 808 · Falsos positivos: 0 · Falsos negativos: 0

## 5.3 Cumplimiento de los indicadores de éxito

| Indicador comprometido | Meta | Resultado | Estado |
|---|---|---|---|
| ROC-AUC | ≥ 0.80 | No calculada | No verificado |
| Recall | ≥ 75 % | 100 % | Cumplido (ver Sección 7) |
| Anticipación de la predicción | 90 días | Ventana implementada | Cumplido |
| Dashboard operativo | Sí | Telco AI desplegado | Cumplido |

> La ausencia del cálculo de ROC-AUC constituye una brecha respecto de lo comprometido inicialmente. Se recomienda incorporarla, dado que es la métrica que mejor describe la capacidad discriminatoria de un clasificador ante distintos umbrales de decisión y resulta especialmente informativa en escenarios con clases desbalanceadas.

---

# 6. Solución tecnológica implementada

## 6.1 Arquitectura de la solución

| Capa | Tecnología | Función |
|---|---|---|
| Almacenamiento y procesamiento | Databricks Community Edition, Apache Spark, Delta Lake | Ejecución del ETL Medallion sobre los archivos de origen |
| Modelado | Spark MLlib (GBTClassifier) | Entrenamiento del modelo y generación de predicciones |
| Persistencia de resultados | MongoDB Atlas | Colecciones `predictions`, `metrics`, `confusion_matrix` y `model_info` |
| Servicios (backend) | FastAPI, Docker, Railway | Exposición de endpoints de autenticación, empresas, dashboard, métricas, predicciones y auditoría |
| Interfaz (frontend) | Next.js, Vercel | Dashboard Telco AI para consulta del área comercial |

## 6.2 Flujo de datos extremo a extremo

```text
Archivos CSV de origen
  → Ingesta (Bronze)
  → Limpieza y validación (Silver)
  → Consolidación por empresa (Gold)
  → Análisis exploratorio
  → Ingeniería de variables
  → Entrenamiento del modelo
  → Persistencia de predicciones en MongoDB Atlas
  → API REST en FastAPI
  → Dashboard web Telco AI
```

## 6.3 Dashboard Telco AI

El dashboard organiza la información en seis secciones orientadas a distintos perfiles de usuario:

| Sección | Contenido y propósito |
|---|---|
| **Dashboard** | Indicadores ejecutivos: clientes en riesgo, tasa de churn a 90 días, base total, conversiones exitosas, tendencia real frente a predicción, distribución de riesgo y precisión histórica del modelo |
| **Predicciones** | Análisis predictivo a 90 días, estado y versión del modelo, y ranking de clientes de alto riesgo con su nivel de confianza |
| **Empresas** | Cartera completa con buscador, filtros por nivel de riesgo, facturación anual y tendencia del riesgo por cliente |
| **Reportes** | Generación y descarga de reportes mensuales, trimestrales y de precisión del modelo |
| **Administración** | Gestión de usuarios, sincronización de datos, reentrenamiento del modelo y monitoreo del estado del sistema |
| **Configuración** | Perfil del usuario, alertas de alto riesgo, reportes semanales y preferencias de visualización |

> Los siete registros gráficos del dashboard se encuentran en la carpeta `docs/semana_07/Capturas_Dashboard` del repositorio, junto con el documento de instrucciones de uso dirigido a las áreas comerciales.

---

# 7. Análisis crítico de los resultados

> ### Hallazgo principal de la evaluación
>
> Las métricas perfectas obtenidas (100 % en Accuracy, Precision, Recall y F1-Score, con cero falsos positivos y cero falsos negativos) no reflejan la calidad del modelo, sino la estructura del conjunto de datos utilizado. El análisis del dataset Gold revela que **siete variables predictivas separan las clases de forma perfecta, sin ningún solapamiento entre clientes con churn y sin churn**.

## 7.1 Evidencia de la separabilidad perfecta

Al examinar los rangos de valores que toma cada variable en cada clase, se observa que no existe intersección alguna entre ambos grupos:

| Variable | Rango en clientes sin churn | Rango en clientes con churn | Solapamiento |
|---|---|---|---|
| `duracion_promedio_eventos` | 19.19 – 41.47 | 217.57 – 295.16 | Ninguno |
| `tiempo_resolucion_promedio` | 8.20 – 39.20 | 104.80 – 156.03 | Ninguno |
| `dias_mora_promedio` | 2.38 – 6.71 | 11.42 – 59.21 | Ninguno |
| `tickets_escalados` | 0 – 5 | 14 – 66 | Ninguno |
| `csat` | 3.50 – 5.00 | 1.00 – 3.00 | Ninguno |
| `nps` | 50 – 99 | 0 – 39 | Ninguno |
| `risk_score` | 0.01 – 59.94 | 70.01 – 99.99 | Ninguno |

La consecuencia es directa y verificable: una regla trivial de un solo umbral, sin ningún algoritmo de aprendizaje, alcanza el mismo 100 % de exactitud. Por ejemplo, clasificar como churn a todo cliente cuya duración promedio de eventos supere 129.52 minutos produce una exactitud del 100 % sobre los 5,000 registros. Si un umbral manual iguala el desempeño de un modelo de boosting con 100 iteraciones, el mérito no está en el modelo.

## 7.2 Causa e interpretación

El conjunto de datos empleado es **sintético**, generado para fines académicos a partir de reglas deterministas: los valores de las variables de soporte, red y satisfacción fueron asignados en función de la etiqueta de churn, y no al revés. Esto explica tanto las correlaciones extraordinariamente altas observadas en el EDA (0.998, 0.992, 0.955) como el desempeño perfecto del clasificador.

La variable **`risk_score`** merece una mención aparte: presenta separación perfecta con un salto abrupto entre 59.94 y 70.01, lo que indica que fue derivada de la propia etiqueta. Su inclusión entre las variables predictivas constituiría un caso claro de fuga de información (*data leakage*). Aunque la documentación de la Semana 6 no la lista entre las variables de entrada del modelo, se recomienda verificar explícitamente su exclusión en el notebook de entrenamiento.

## 7.3 Implicancias

Reconocer esta limitación no invalida el trabajo realizado. El proyecto cumplió íntegramente su propósito formativo y técnico: se construyó un pipeline completo, funcional y reproducible que abarca desde la ingesta de datos crudos hasta un dashboard operativo en la nube. Ese pipeline es el activo real del proyecto y funcionaría igual con datos reales.

Lo que no puede afirmarse es que el modelo alcance un 100 % de exactitud con datos productivos. En un escenario real, un modelo de churn bien construido suele situarse en rangos de ROC-AUC entre 0.75 y 0.90; valores superiores al 0.95 son motivo de sospecha de fuga de información antes que de celebración.

> ### Lección metodológica
>
> Un resultado perfecto en un problema de negocio complejo debe tratarse siempre como una señal de alerta y no como un logro. La verificación de solapamiento entre clases y la revisión de correlaciones extremas con la variable objetivo deberían formar parte del protocolo estándar de validación antes de dar por concluido cualquier modelo.

---

# 8. Conclusiones

## 8.1 Sobre el objetivo general

Se desarrolló un sistema completo de predicción de churn para clientes B2B que integra procesamiento distribuido, modelado predictivo y visualización, cumpliendo el objetivo general planteado. La solución identifica clientes en riesgo con la ventana de anticipación de 90 días definida en el alcance.

## 8.2 Sobre el proceso de datos

- La arquitectura Medallion demostró ser adecuada para el problema: la separación en capas Bronze, Silver y Gold permitió aislar el dato crudo del dato analítico y mantener trazabilidad en todo el proceso.
- La integración de siete fuentes heterogéneas en una vista única por empresa validó la hipótesis de que el churn corporativo requiere una visión integral del cliente, y no el análisis aislado de una sola dimensión.
- El uso de Apache Spark permitió procesar el volumen consolidado de forma distribuida con un pipeline que escalaría sin cambios ante un aumento significativo de registros.

## 8.3 Sobre los hallazgos analíticos

- Los factores más asociados al abandono corresponden a la calidad técnica del servicio y a la experiencia de soporte —duración de incidencias, tiempo de resolución y escalamientos— por encima de las variables financieras y de consumo.
- Los indicadores de satisfacción (NPS y CSAT) mostraron correlación negativa fuerte con el churn, confirmando su valor como señales tempranas de riesgo.
- La tasa de churn observada del 16.80 % representa un desbalance moderado que exige evaluar el modelo con métricas más informativas que el Accuracy.

## 8.4 Sobre el modelo

- El algoritmo Gradient Boosted Trees resultó apropiado para el problema por su capacidad de manejar variables numéricas y categóricas y su integración nativa con Spark MLlib.
- Las métricas perfectas obtenidas se explican por la naturaleza sintética del dataset y no por el desempeño del algoritmo; el modelo no ha sido validado en condiciones realistas.
- La omisión del cálculo de ROC-AUC dejó sin verificar uno de los indicadores de éxito comprometidos en la definición del proyecto.

## 8.5 Sobre la solución tecnológica

- La integración entre Databricks, MongoDB Atlas, FastAPI y Next.js demostró que es viable construir una cadena completa desde el procesamiento analítico hasta una interfaz de negocio utilizando exclusivamente herramientas gratuitas o de capa libre.
- El dashboard Telco AI traduce la salida técnica del modelo en información accionable, organizada por perfil de usuario y con niveles de riesgo interpretables por personal no técnico.

---

# 9. Recomendaciones

## 9.1 Prioridad alta — validez del modelo

| Recomendación | Justificación |
|---|---|
| Validar el modelo con datos reales o con un dataset sintético que incorpore ruido y solapamiento entre clases | Es la única forma de conocer el desempeño verdadero del clasificador; los resultados actuales no son extrapolables |
| Calcular e informar ROC-AUC y la curva Precision-Recall | Cierra la brecha con el indicador de éxito comprometido y describe el comportamiento del modelo ante distintos umbrales |
| Auditar el conjunto de variables de entrada y excluir explícitamente `risk_score` | Previene fuga de información desde variables derivadas de la etiqueta objetivo |
| Incorporar validación cruzada (k-fold) en lugar de una única partición Hold-Out | Reduce la dependencia del resultado respecto de una partición particular y ofrece una estimación más estable |

## 9.2 Prioridad media — robustez técnica

- Implementar autenticación real con control de acceso por rol en el dashboard, sustituyendo el modo de demostración actual.
- Automatizar la actualización de predicciones mediante un proceso programado, evitando la sincronización manual.
- Registrar el versionado de modelos y su historial de métricas para detectar degradación en el tiempo.
- Establecer pruebas automatizadas de calidad de datos sobre la capa Silver, con umbrales de nulos, duplicados e integridad referencial.

## 9.3 Prioridad media — aprovechamiento del negocio

- Priorizar la gestión de retención cruzando el nivel de riesgo con la facturación anual del cliente, de modo que el esfuerzo comercial se concentre donde el ingreso en juego es mayor.
- Actuar sobre las causas identificadas en el análisis: dado que las variables dominantes son operativas, las acciones de mayor impacto son reducir la duración de incidencias y los tiempos de resolución, más que ofrecer descuentos.
- Definir un protocolo de intervención por nivel de riesgo, asignando responsables y plazos de contacto diferenciados.
- Medir sistemáticamente la efectividad de las campañas mediante el indicador de conversiones exitosas ya presente en el dashboard.

## 9.4 Trabajo futuro

- Incorporar variables temporales que capturen la tendencia del comportamiento (variación del consumo o de la facturación en los últimos tres y seis meses) en lugar de únicamente valores agregados.
- Evaluar técnicas de interpretabilidad como SHAP para explicar las predicciones individuales, requisito frecuente para la adopción del modelo por parte de las áreas comerciales.
- Explorar el procesamiento en streaming para detectar cambios de comportamiento en ventanas más cortas.
- Ampliar el alcance hacia un modelo de estimación del valor en riesgo, que combine la probabilidad de abandono con el ingreso asociado a cada cliente.

---

# 10. Anexos

## 10.1 Estructura del repositorio

| Ruta | Contenido |
|---|---|
| `data/raw/` | Siete archivos CSV de origen |
| `data/processed/` | Dataset Gold consolidado en formatos Parquet y CSV |
| `notebooks/Semana02-Ingesta/` | `01_ingestion.ipynb` |
| `notebooks/Semana03-ETL/` | `02_bronze.ipynb`, `03_silver.ipynb`, `04_gold.ipynb` |
| `notebooks/Semana04-EDA/` | `05_eda.ipynb` |
| `notebooks/Semana05-Feature/` | `feature_engineering.ipynb` |
| `notebooks/Semana06-ML/` | `07_model_training.ipynb` |
| `src/churn_backend/` | API REST en FastAPI con routers de autenticación, empresas, dashboard, métricas, predicciones y auditoría |
| `src/churntelecomb2b/` | Aplicación web Next.js del dashboard Telco AI |
| `docs/semana_01 … semana_08/` | Documentación e informes de cada etapa, con evidencias gráficas |

## 10.2 Documentos de respaldo por etapa

| Etapa | Documentos |
|---|---|
| Semana 1 | `problema_negocio.md`, `objetivos.md`, `alcance.md`, `cronograma.md` |
| Semana 2 | `fuentes_datos.md`, `diccionario_datos.xlsx`, `Modelo_Relacional.png` |
| Semana 3 | `Documento_del_proceso_ETL.md`, `Informe_de_calidad_de_datos.md`, `Dataset_procesado_y_validado.md` |
| Semana 4 | `Informe_Analisis_Exploratorio_de_Datos(EDA).md` y evidencias gráficas |
| Semana 5 | `feature_engineering.md`, `dataset_final.md`, `catalogo_features.xlsx` |
| Semana 6 | `Machine Learning.md`, `resultados_modelo.md`, `metricas_modelo.xlsx` |
| Semana 7 | `Instrucciones_Uso_Dashboard_TelcoAI.md` y siete capturas del dashboard |
| Semana 8 | `informe_final.pdf`, `informe_final.md`, `conclusiones.md`, `recomendaciones.md`, `presentacion_final.pptx` |

## 10.3 Glosario

| Término | Definición |
|---|---|
| **Churn** | Abandono del servicio por parte de un cliente; en el segmento B2B, la no renovación del contrato |
| **Arquitectura Medallion** | Patrón de organización de datos en capas Bronze (crudo), Silver (limpio) y Gold (listo para negocio) |
| **Data leakage** | Fuga de información desde la variable objetivo hacia las variables predictoras, que produce métricas artificialmente altas |
| **Hold-Out** | Estrategia de validación que divide el dataset en una partición de entrenamiento y otra de prueba |
| **GBTClassifier** | Clasificador de árboles potenciados por gradiente de la librería Spark MLlib |
| **Recall** | Proporción de clientes que efectivamente abandonaron y fueron correctamente detectados por el modelo |
| **ROC-AUC** | Área bajo la curva ROC; mide la capacidad del modelo para discriminar entre clases |
| **NPS / CSAT** | Indicadores de recomendación y satisfacción del cliente |

---

*Informe Final — Semana 8 · Proyecto de Predicción de Churn B2B · Big Data (DD283) · Universidad Autónoma del Perú · 2026-1*
