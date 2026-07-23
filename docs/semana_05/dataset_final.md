# Dataset Final para Machine Learning
## Proyecto: Sistema de Predicción de Churn para una Empresa de Telecomunicaciones B2B

---

# Descripción

El presente dataset corresponde al resultado final del proceso de **Feature Engineering** desarrollado durante la Semana 5 del proyecto.

Este conjunto de datos consolida información proveniente de múltiples fuentes de negocio (clientes, facturación, consumo, servicios, soporte técnico y eventos de red), permitiendo representar el comportamiento integral de cada empresa cliente.

El dataset fue construido sobre Apache Spark utilizando Databricks Community Edition y constituye la base para el entrenamiento del modelo de Machine Learning encargado de predecir el riesgo de abandono (Churn).

---

# Origen de los datos

El dataset fue generado a partir de la integración de las siguientes fuentes:

- Empresas
- Facturación
- Consumo
- Servicios
- Tickets de soporte
- Eventos de red
- Información histórica de Churn

Cada fuente fue procesada mediante la arquitectura Medallion (Bronze, Silver y Gold), garantizando la calidad e integridad de la información.

---

# Estructura del Dataset

| Variable | Tipo | Descripción |
|----------|------|-------------|
| company_id | Integer | Identificador único de la empresa |
| ruc | Long | Número de RUC de la empresa |
| razon_social | String | Nombre o razón social del cliente |
| sector | String | Sector económico al que pertenece la empresa |
| region | String | Región geográfica del cliente |
| empleados | Integer | Número de colaboradores de la empresa |
| segmento | String | Segmento comercial asignado |
| fecha_alta | Date | Fecha de incorporación como cliente |
| ejecutivo_comercial | String | Ejecutivo responsable de la cuenta |
| nps | Double | Net Promoter Score del cliente |
| csat | Double | Customer Satisfaction Score |
| facturacion_total | Double | Facturación acumulada del cliente |
| facturacion_promedio | Double | Promedio mensual de facturación |
| facturacion_maxima | Double | Mayor monto facturado durante el periodo |
| dias_mora_promedio | Double | Promedio de días de retraso en pagos |
| deuda_total | Double | Deuda acumulada del cliente |
| trafico_total_gb | Double | Consumo total de datos (GB) |
| trafico_promedio_gb | Double | Consumo promedio mensual (GB) |
| ancho_banda_promedio | Double | Promedio del ancho de banda contratado |
| pico_maximo_mbps | Double | Máximo pico de tráfico registrado |
| cantidad_servicios | Integer | Número de servicios contratados |
| monto_mensual_promedio | Double | Pago mensual promedio |
| sla_promedio | Double | Nivel promedio de cumplimiento del SLA |
| cantidad_tickets | Integer | Total de tickets de soporte registrados |
| tiempo_resolucion_promedio | Double | Tiempo promedio de resolución de incidencias |
| tickets_escalados | Integer | Cantidad de tickets escalados |
| cantidad_eventos | Integer | Total de eventos de red registrados |
| duracion_promedio_eventos | Double | Duración promedio de las incidencias |
| churn | Integer | Variable objetivo histórica (0 = No abandono, 1 = Abandono) |
| risk_score | Double | Nivel de riesgo histórico asociado al cliente |
| sector_index | Double | Codificación numérica del sector |
| region_index | Double | Codificación numérica de la región |
| segmento_index | Double | Codificación numérica del segmento |

---

# Variables Predictoras

Las siguientes variables fueron utilizadas como características (features) para el entrenamiento del modelo de Machine Learning:

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

Estas variables representan el comportamiento comercial, financiero, operativo y de calidad del servicio de cada cliente empresarial.

---

# Variable Objetivo

Durante el entrenamiento del modelo se utilizó la siguiente variable objetivo:

| Variable | Descripción |
|----------|-------------|
| churn | Indica si el cliente abandonó el servicio (1) o permaneció activo (0) |

Una vez entrenado el modelo, la aplicación utiliza únicamente la predicción generada y el **Risk Score** para identificar clientes con mayor probabilidad de abandono.

---

# Variables Exportadas al Backend

Con el objetivo de optimizar el rendimiento de la aplicación web, únicamente se exportan a MongoDB los datos necesarios para el consumo del backend.

## Colección: predictions

| Campo |
|--------|
| company_id |
| ruc |
| razon_social |
| sector |
| region |
| segmento |
| ejecutivo_comercial |
| prediction |
| risk_score |

---

# Colección: metrics

Contiene las métricas finales del modelo de Machine Learning.

| Campo |
|--------|
| accuracy |
| precision |
| recall |
| f1_score |
| true_positive |
| true_negative |
| false_positive |
| false_negative |

---

# Colección: confusion_matrix

Almacena la matriz de confusión calculada durante la evaluación del modelo.

| Campo |
|--------|
| TP |
| TN |
| FP |
| FN |
| accuracy |
| precision |
| recall |
| f1_score |
| created_at |

---

# Colección: model_info

Contiene información descriptiva del modelo entrenado.

| Campo |
|--------|
| algorithm |
| version |
| training_date |
| accuracy |
| precision |
| recall |
| f1_score |
| records |

---

# Cantidad de Registros

| Dataset | Cantidad |
|----------|---------:|
| Empresas | 5,000 |
| Facturación | 120,000 |
| Consumo | 120,000 |
| Servicios | 15,140 |
| Tickets | 102,980 |
| Eventos de Red | 273,378 |
| Dataset Gold | 5,000 registros consolidados |
| Predicciones exportadas | 5,000 |

---

# Uso del Dataset

El dataset final es utilizado para:

- Entrenamiento del modelo de Machine Learning.
- Generación de predicciones de Churn.
- Cálculo de métricas de desempeño del modelo.
- Construcción del Dashboard Ejecutivo.
- Visualización del riesgo de abandono por empresa.
- Consulta desde el Backend desarrollado en FastAPI.
- Consumo desde el Frontend desarrollado con Next.js (V0.app).

---

# Conclusión

El dataset final representa una visión integral del comportamiento de los clientes B2B de una empresa de telecomunicaciones, consolidando información comercial, financiera, operativa y de soporte técnico.

La aplicación de técnicas de Feature Engineering permitió construir un conjunto robusto de variables predictivas que sirven como base para el modelo de Machine Learning encargado de estimar el riesgo de abandono de clientes, proporcionando información estratégica para la toma de decisiones y la implementación de acciones preventivas de retención.