# Informe de Análisis Exploratorio de Datos (EDA)

## Objetivo

Realizar un Análisis Exploratorio de Datos (Exploratory Data Analysis - EDA) sobre el dataset consolidado generado en la capa Gold del proceso ETL, con el objetivo de comprender la estructura de los datos, identificar patrones de comportamiento, validar la calidad de la información y detectar variables potencialmente relevantes para la predicción de churn de clientes B2B del sector telecomunicaciones.

---

## Integrantes:
- Asto Arotinco Ana (0000-0002-2195-0764)
- Flores Condeña Javier (0000-0003-2800-5084)
- Lindo Barrientos Jhonn Viequier(0000-0001-6025-7332)
- Tito Paredes Arian (0009-0002-5717-8099)
- Quispe Poma Cristian (0009-0008-6566-3741)
---
# Dataset Analizado

Fuente:

```text
/Volumes/workspace/default/churn_b2b/Gold/gold_dataset
```

Cantidad de registros:

```text
5,000 empresas
```

Variable objetivo:

```text
churn
```

Definición:

| Valor | Descripción |
|---------|------------|
| 0 | Cliente activo |
| 1 | Cliente abandonó el servicio |

---

# Estructura General del Dataset

El dataset consolidado contiene información proveniente de diferentes áreas del negocio:

## Información General

- company_id
- razon_social
- sector
- region
- empleados
- segmento
- fecha_alta
- ejecutivo_comercial
- nps
- csat

## Indicadores Financieros

- facturacion_total
- facturacion_promedio
- facturacion_maxima
- dias_mora_promedio
- deuda_total

## Indicadores de Consumo

- trafico_total_gb
- trafico_promedio_gb
- ancho_banda_promedio
- pico_maximo_mbps

## Indicadores de Servicios

- cantidad_servicios
- monto_mensual_promedio
- sla_promedio

## Indicadores de Soporte

- cantidad_tickets
- tiempo_resolucion_promedio
- tickets_escalados

## Indicadores de Infraestructura

- cantidad_eventos
- duracion_promedio_eventos

## Variable Objetivo

- churn
- risk_score

---

# Análisis de Calidad de Datos

## Completitud

Se ejecutó una validación de valores nulos sobre todas las columnas del dataset.

Resultado:

- No se identificaron valores nulos en las variables críticas.
- Todas las columnas presentan 5,000 registros válidos.

Resultado:

```text
Completitud = 100%
```

---

# Estadísticas Descriptivas

## Tamaño promedio de empresa

| Métrica | Valor |
|----------|--------|
| Promedio de empleados | 5,001 |
| Desviación estándar | 2,887 |

Interpretación:

La base contiene empresas de distintos tamaños, lo que aporta diversidad al modelo predictivo.

---

## Satisfacción del Cliente

### NPS

| Métrica | Valor |
|----------|--------|
| Promedio | 65.58 |
| Desviación estándar | 24.81 |

### CSAT

| Métrica | Valor |
|----------|--------|
| Promedio | 3.88 / 5 |
| Desviación estándar | 0.96 |

Interpretación:

Los niveles de satisfacción son relativamente altos, aunque existe una dispersión considerable entre clientes.

---

## Facturación

| Métrica | Valor |
|----------|--------|
| Facturación total promedio | 733,580 |
| Facturación mensual promedio | 30,566 |
| Facturación máxima promedio | 57,732 |

Interpretación:

Las empresas generan niveles importantes de facturación, lo que sugiere una cartera compuesta por clientes corporativos de valor medio y alto.

---

## Mora y Deuda

| Métrica | Valor |
|----------|--------|
| Días promedio de mora | 9.23 |
| Deuda total promedio | 602,392 |

Interpretación:

Existe un nivel relevante de deuda acumulada que podría influir directamente en el riesgo de abandono.

---

## Consumo

| Métrica | Valor |
|----------|--------|
| Tráfico total promedio | 138,776 GB |
| Tráfico promedio mensual | 5,782 GB |
| Ancho de banda promedio | 231 Mbps |
| Pico máximo promedio | 822 Mbps |

Interpretación:

Los clientes presentan patrones de consumo elevados, consistentes con organizaciones que dependen fuertemente de servicios de telecomunicaciones.

---

## Servicios Contratados

| Métrica | Valor |
|----------|--------|
| Cantidad promedio de servicios | 3.03 |
| SLA promedio | 99.78% |
| Monto mensual promedio | 12,874 |

Interpretación:

La mayoría de empresas mantiene múltiples servicios contratados con altos niveles de disponibilidad comprometida.

---

## Soporte Técnico

| Métrica | Valor |
|----------|--------|
| Tickets promedio | 20.60 |
| Tiempo promedio de resolución | 41.98 horas |
| Tickets escalados promedio | 6.66 |

Interpretación:

Los tickets representan una fuente importante de información para explicar posibles casos de churn.

---

## Eventos de Red

| Métrica | Valor |
|----------|--------|
| Eventos promedio | 54.68 |
| Duración promedio | 67.72 minutos |

Interpretación:

La calidad técnica de la red puede convertirse en un factor relevante para la satisfacción y permanencia de los clientes.

---

# Distribución de la Variable Objetivo

## Distribución de Churn

| Estado | Empresas |
|----------|-----------|
| Activas (0) | 4,160 |
| Churn (1) | 840 |

Porcentaje:

| Estado | % |
|----------|-----|
| Activas | 83.2% |
| Churn | 16.8% |

Interpretación:

Existe un desbalance moderado de clases.

```text
83.2% clientes activos
16.8% clientes churn
```

Este comportamiento es común en problemas de abandono de clientes.

---

# Distribución por Sector

| Sector | Empresas |
|----------|---------|
| Agroindustria | 541 |
| Manufactura | 538 |
| Educación | 511 |
| Telecomunicaciones | 503 |
| Construcción | 502 |
| Transporte | 496 |
| Salud | 482 |
| Tecnología | 481 |
| Retail | 479 |
| Finanzas | 467 |

Hallazgo:

La distribución sectorial es bastante equilibrada, reduciendo posibles sesgos durante el entrenamiento del modelo.

---

# Distribución por Región

| Región | Empresas |
|----------|---------|
| Huancayo | 535 |
| Ica | 527 |
| Trujillo | 525 |
| Chiclayo | 515 |
| Piura | 510 |
| Lima | 495 |
| Tacna | 487 |
| Cusco | 472 |
| Arequipa | 471 |
| Cajamarca | 463 |

Hallazgo:

La cobertura geográfica se encuentra distribuida entre diversas regiones del país.

---

# Churn por Sector

Se analizaron las empresas que abandonaron el servicio por sector.

Sectores con mayor número de casos de churn:

| Sector | Casos |
|----------|-------|
| Manufactura | 96 |
| Construcción | 95 |
| Telecomunicaciones | 93 |
| Educación | 90 |
| Agroindustria | 86 |

Sectores con menor cantidad de churn:

| Sector | Casos |
|----------|-------|
| Retail | 64 |
| Finanzas | 75 |
| Transporte | 76 |

Interpretación:

Algunos sectores muestran una mayor propensión al abandono, lo que podría indicar diferencias en comportamiento o necesidades operativas.

---

# Churn por Segmento

| Segmento | Activos | Churn |
|-----------|----------|--------|
| Enterprise | 1,396 | 292 |
| Mid-Market | 1,393 | 288 |
| SMB | 1,371 | 260 |

Tasa aproximada de churn:

| Segmento | Tasa |
|-----------|------|
| Enterprise | 17.3% |
| Mid-Market | 17.1% |
| SMB | 15.9% |

Interpretación:

El churn se distribuye de forma relativamente homogénea entre los diferentes segmentos empresariales.

---

# Correlaciones Analizadas

## Facturación vs Deuda

Coeficiente de correlación:

```text
0.787
```

Interpretación:

Existe una correlación positiva fuerte entre la facturación y la deuda acumulada.

Esto indica que las empresas con mayores niveles de facturación también tienden a mantener mayores niveles de deuda.

---

# Hallazgos Relevantes

## Hallazgo 1

El dataset presenta una calidad adecuada para Machine Learning:

- Sin valores nulos críticos.
- Sin inconsistencias estructurales.
- Integridad referencial validada.

---

## Hallazgo 2

La tasa de churn es del:

```text
16.8%
```

lo que representa un problema de clasificación binaria con desbalance moderado.

---

## Hallazgo 3

Las variables financieras muestran alta variabilidad entre empresas.

Esto podría aportar capacidad predictiva al modelo.

---

## Hallazgo 4

Las métricas de soporte técnico y eventos de red presentan diferencias importantes entre empresas, convirtiéndose en potenciales predictores de churn.

---

## Hallazgo 5

La distribución de sectores y regiones es relativamente uniforme, lo que favorece la generalización del modelo.

---

# Conclusiones

El análisis exploratorio permitió validar la calidad y consistencia del dataset consolidado generado en la capa Gold.

Los resultados muestran que la información se encuentra preparada para la fase de Feature Engineering y entrenamiento del modelo predictivo.

Las variables relacionadas con:

- Facturación.
- Deuda.
- Consumo.
- Tickets de soporte.
- Eventos de red.
- Satisfacción del cliente.

presentan potencial para explicar el comportamiento de abandono de clientes.

Finalmente, la tasa de churn observada del 16.8% confirma la necesidad de desarrollar un modelo de Machine Learning capaz de identificar tempranamente empresas con alto riesgo de abandono y facilitar estrategias de retención.