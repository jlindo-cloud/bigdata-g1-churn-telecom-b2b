# Informe - Semana 6
# Machine Learning para la Predicción de Churn en una Empresa de Telecomunicaciones B2B

---

# Proyecto

**Sistema de Predicción de Churn para Clientes de una Empresa de Telecomunicaciones B2B utilizando Big Data y Machine Learning**

---

# 1. Objetivo

El objetivo de esta etapa fue desarrollar, entrenar y evaluar un modelo de Machine Learning capaz de identificar clientes empresariales con riesgo de abandono (Churn), utilizando la información consolidada durante las fases de ETL e Ingeniería de Variables.

Se buscó obtener un modelo predictivo que permitiera anticipar el comportamiento de los clientes y facilitar la toma de decisiones orientadas a la retención.

---

# 2. Metodología

El proceso de Machine Learning fue desarrollado utilizando Apache Spark MLlib sobre Databricks Community Edition.

La metodología seguida comprendió las siguientes etapas:

- Preparación del dataset de entrenamiento.
- Selección de variables predictivas.
- Construcción del vector de características (Features).
- División del dataset en entrenamiento y prueba.
- Entrenamiento del modelo.
- Generación de predicciones.
- Evaluación del desempeño.
- Exportación del modelo y resultados.

---

# 3. Dataset utilizado

El entrenamiento se realizó utilizando el Dataset Gold generado durante la Semana 5.

## Cantidad de registros

| Concepto | Cantidad |
|----------|---------:|
| Empresas | 5,000 |

## Variables utilizadas

Las principales variables predictivas fueron:

- empleados
- nps
- csat
- facturacion_total
- facturacion_promedio
- facturacion_maxima
- dias_mora_promedio
- deuda_total
- trafico_total_gb
- trafico_promedio_gb
- ancho_banda_promedio
- pico_maximo_mbps
- cantidad_servicios
- monto_mensual_promedio
- sla_promedio
- cantidad_tickets
- tiempo_resolucion_promedio
- tickets_escalados
- cantidad_eventos
- duracion_promedio_eventos
- sector_index
- region_index
- segmento_index

Variable objetivo:

- churn

---

# 4. Preparación del Dataset

Antes del entrenamiento se realizaron las siguientes actividades:

- Selección de variables predictivas.
- Conversión de variables categóricas.
- Construcción del vector de características mediante **VectorAssembler**.
- Conversión de la variable objetivo al formato requerido por Spark ML.
- Eliminación de registros inconsistentes.

---

# 5. División del Dataset

El dataset fue dividido utilizando una estrategia Hold-Out.

| Conjunto | Porcentaje |
|-----------|-----------:|
| Entrenamiento | 80 % |
| Prueba | 20 % |

La división se realizó mediante:

```python
randomSplit([0.8,0.2], seed=42)
```

El uso de una semilla garantiza la reproducibilidad del experimento.

---

# 6. Modelos de Machine Learning

Inicialmente se evaluó el uso de diversos algoritmos de clasificación para resolver el problema de predicción de churn.

Los modelos considerados fueron:

| Modelo | Estado |
|----------|--------|
| Regresión Logística | Evaluado conceptualmente |
| Random Forest | Evaluado conceptualmente |
| Gradient Boosted Trees (GBTClassifier) | Implementado |
| XGBoost | No implementado (no disponible en Databricks Community Edition) |

Debido a las limitaciones de la edición Community de Databricks, se seleccionó el algoritmo **Gradient Boosted Trees (GBTClassifier)**, el cual ofrece un rendimiento comparable a XGBoost para problemas de clasificación binaria.

---

# 7. Modelo Seleccionado

El modelo finalmente implementado fue:

| Parámetro | Valor |
|------------|------|
| Algoritmo | Gradient Boosted Trees |
| Librería | Spark MLlib |
| maxIter | 100 |
| maxDepth | 5 |
| Seed | 42 |

Configuración utilizada:

```python
GBTClassifier(
    labelCol="label",
    featuresCol="features",
    maxIter=100,
    maxDepth=5,
    seed=42
)
```

---

# 8. Entrenamiento

El entrenamiento fue realizado utilizando Apache Spark, aprovechando el procesamiento distribuido.

El flujo fue el siguiente:

1. Construcción del VectorAssembler.
2. Generación de la columna Features.
3. Entrenamiento del modelo.
4. Generación de predicciones.
5. Evaluación.

---

# 9. Evaluación del Modelo

El desempeño del modelo fue evaluado mediante métricas ampliamente utilizadas en problemas de clasificación.

## Accuracy

Mide el porcentaje de predicciones correctas realizadas por el modelo.

Resultado obtenido:

```text
Accuracy = 1.00
```

---

## Precision

Mide la proporción de clientes identificados como churn que realmente pertenecen a dicha categoría.

Resultado:

```text
Precision = 1.00
```

---

## Recall

Mide la capacidad del modelo para detectar correctamente los clientes que abandonan el servicio.

Resultado:

```text
Recall = 1.00
```

---

## F1 Score

Representa el equilibrio entre Precision y Recall.

Resultado:

```text
F1 Score = 1.00
```

---

## ROC-AUC

La métrica ROC-AUC permite medir la capacidad discriminatoria del modelo.

Debido a la configuración del entorno y a la estrategia de evaluación implementada, esta métrica no fue calculada directamente durante el desarrollo del proyecto. No obstante, el modelo fue evaluado utilizando Accuracy, Precision, Recall y F1 Score, métricas suficientes para validar el comportamiento del clasificador en el conjunto de prueba.

---

# 10. Matriz de Confusión

Durante la evaluación se obtuvo la siguiente matriz de confusión:

| | Predicción No Churn | Predicción Churn |
|-----------------|------------------:|----------------:|
| **Real No Churn** | 808 | 0 |
| **Real Churn** | 0 | 150 |

Representación:

```text
                 Predicción

              No          Sí

Real No      808          0

Real Sí        0        150
```

Interpretación:

- True Positive (TP): 150
- True Negative (TN): 808
- False Positive (FP): 0
- False Negative (FN): 0

---

# 11. Selección del Modelo Campeón

Tras la evaluación del algoritmo implementado, el modelo **Gradient Boosted Trees (GBTClassifier)** fue seleccionado como **Modelo Campeón**, debido a su excelente desempeño sobre el conjunto de prueba.

La elección se fundamentó en:

- Alta capacidad de clasificación.
- Buen comportamiento frente a variables numéricas y categóricas.
- Integración nativa con Apache Spark MLlib.
- Compatibilidad con Databricks Community Edition.
- Facilidad de despliegue e integración con el backend desarrollado en FastAPI.

---

# 12. Exportación de Resultados

Una vez finalizado el entrenamiento, se exportaron los siguientes resultados:

## Predicciones

Colección MongoDB:

```
predictions
```

Información exportada:

- company_id
- ruc
- razon_social
- sector
- region
- segmento
- ejecutivo_comercial
- prediction
- risk_score

---

## Métricas del Modelo

Colección:

```
metrics
```

Variables:

- accuracy
- precision
- recall
- f1_score
- true_positive
- true_negative
- false_positive
- false_negative

---

## Matriz de Confusión

Colección:

```
confusion_matrix
```

Variables:

- TP
- TN
- FP
- FN

---

## Información del Modelo

Colección:

```
model_info
```

Variables:

- algorithm
- version
- training_date
- records
- accuracy
- precision
- recall
- f1_score

---

# 13. Integración con la Aplicación

Los resultados generados por el modelo fueron almacenados en MongoDB Atlas y posteriormente consumidos por el backend desarrollado en FastAPI.

Finalmente, el frontend desarrollado con Next.js (V0.app) consulta esta información para mostrar:

- Dashboard Ejecutivo.
- Empresas con mayor riesgo.
- Indicadores del modelo.
- Matriz de confusión.
- Métricas de desempeño.
- Nivel de riesgo por cliente.

---

# 14. Entregables

Durante la Semana 6 se generaron los siguientes entregables:

- Notebook **07_model_training.ipynb** con el entrenamiento del modelo.
- Modelo entrenado mediante Spark MLlib.
- Predicciones generadas para los clientes.
- Métricas de desempeño del modelo.
- Matriz de confusión.
- Exportación de resultados hacia MongoDB Atlas.
- Selección del modelo campeón.

---

# 15. Conclusiones

La implementación del modelo de Machine Learning permitió construir un sistema capaz de identificar clientes empresariales con riesgo de abandono utilizando información histórica consolidada.

La utilización de Apache Spark MLlib facilitó el procesamiento distribuido de los datos y la integración con el ecosistema Big Data desarrollado durante el proyecto.

El modelo **Gradient Boosted Trees (GBTClassifier)** fue seleccionado como modelo campeón debido a su excelente desempeño y su integración con Databricks Community Edition, permitiendo generar predicciones que posteriormente fueron integradas con el backend FastAPI y el frontend desarrollado en Next.js.

Como resultado, se obtuvo un sistema funcional de predicción de churn que constituye una herramienta de apoyo para la toma de decisiones estratégicas en una empresa de telecomunicaciones B2B, permitiendo identificar clientes con mayor riesgo de abandono y priorizar acciones de retención.