# Resultados del Modelo de Machine Learning

## Modelo campeón
- Algoritmo: **Gradient Boosted Trees (GBTClassifier)**
- Framework: Apache Spark MLlib

## Métricas

| Métrica | Valor |
|---|---:|
| Accuracy | 1.00 |
| Precision | 1.00 |
| Recall | 1.00 |
| F1 Score | 1.00 |

## Matriz de Confusión

| | Predicción No Churn | Predicción Churn |
|---|---:|---:|
| Real No Churn | 808 | 0 |
| Real Churn | 0 | 150 |

- TP: 150
- TN: 808
- FP: 0
- FN: 0

## Conclusión

El modelo clasificó correctamente los 958 registros del conjunto de prueba y sus resultados fueron exportados a MongoDB para ser consumidos por el backend FastAPI y el frontend Next.js.
