# Dataset Procesado y Validado

## Objetivo

Documentar el conjunto de datos consolidado generado como resultado del proceso ETL, describiendo su estructura, origen, transformaciones realizadas y validaciones aplicadas para garantizar que la información utilizada en el entrenamiento del modelo de predicción de churn sea confiable y consistente.

El dataset fue construido utilizando una arquitectura **Medallion (Bronze, Silver y Gold)** implementada en **Databricks Community Edition**, utilizando Apache Spark y Delta Lake como tecnologías principales para el procesamiento de datos.

---

## Integrantes:
- Asto Arotinco Ana (0000-0002-2195-0764)
- Flores Condeña Javier (0000-0003-2800-5084)
- Lindo Barrientos Jhonn Viequier(0000-0001-6025-7332)
- Tito Paredes Arian (0009-0002-5717-8099)
- Quispe Poma Cristian (0009-0008-6566-3741)
---
# Arquitectura del Dataset

```text
Archivos CSV
│
├── empresas.csv
├── facturacion.csv
├── consumo.csv
├── servicios.csv
├── tickets.csv
├── eventos_red.csv
└── churn.csv
        │
        ▼
01_ingestion
        │
        ▼
Bronze
        │
        ▼
Silver
        │
        ▼
Gold
        │
        ▼
gold_dataset
        │
        ▼
EDA
        │
        ▼
Feature Engineering
        │
        ▼
dataset_ml
```

---

# Origen de los Datos

El dataset consolidado se construyó a partir de siete fuentes de información correspondientes a diferentes procesos del negocio de telecomunicaciones B2B.

| Dataset | Descripción |
|----------|-------------|
| empresas.csv | Información general de las empresas clientes |
| facturacion.csv | Historial de facturación mensual |
| consumo.csv | Consumo de servicios de telecomunicaciones |
| servicios.csv | Servicios contratados por cada empresa |
| tickets.csv | Incidentes registrados por soporte técnico |
| eventos_red.csv | Eventos e incidencias de infraestructura de red |
| churn.csv | Variable objetivo y nivel de riesgo de abandono |

Todos los archivos fueron almacenados inicialmente en el volumen:

```text
/Volumes/workspace/default/churn_b2b/Datos/
```

---

# Proceso de Construcción

## 1. Ingesta

Los archivos CSV fueron cargados utilizando PySpark, validando:

- Existencia de los archivos.
- Esquema de datos.
- Número de registros.
- Tipos de datos.

Resultado:

DataFrames independientes para cada fuente de información.

---

## 2. Capa Bronze

En esta etapa se almacenó una copia fiel de los datos originales en formato Delta Lake.

Objetivos:

- Preservar la información original.
- Mantener trazabilidad.
- Facilitar el reprocesamiento de datos.

Datasets almacenados:

- empresas
- facturacion
- consumo
- servicios
- tickets
- eventos_red
- churn

---

## 3. Capa Silver

Durante esta etapa se realizaron procesos de limpieza y normalización.

Principales actividades:

- Validación de tipos de datos.
- Eliminación de registros inválidos.
- Tratamiento de valores nulos.
- Verificación de identificadores.
- Normalización de estructuras.

El resultado fue un conjunto de datos limpio y consistente para cada fuente.

---

## 4. Capa Gold

La capa Gold integró toda la información mediante la llave de negocio:

```text
company_id
```

Se realizaron operaciones de agregación para obtener indicadores empresariales relacionados con:

- Facturación.
- Consumo.
- Servicios.
- Tickets.
- Eventos de red.
- Riesgo de abandono.

Como resultado se generó el dataset:

```text
gold_dataset
```

Ubicación:

```text
/Volumes/workspace/default/churn_b2b/Gold/gold_dataset
```

---

# Variables Integradas

El dataset consolidado contiene información proveniente de diferentes áreas del negocio.

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

---

## Indicadores Financieros

- facturacion_total
- facturacion_promedio
- facturacion_maxima
- dias_mora_promedio
- deuda_total

---

## Indicadores de Consumo

- trafico_total_gb
- trafico_promedio_gb
- ancho_banda_promedio
- pico_maximo_mbps

---

## Indicadores de Servicios

- cantidad_servicios
- monto_mensual_promedio
- sla_promedio

---

## Indicadores de Soporte

- cantidad_tickets
- tickets_escalados
- tiempo_resolucion_promedio

---

## Indicadores de Red

- cantidad_eventos
- duracion_promedio_eventos

---

## Variable Objetivo

- churn
- risk_score

---

# Validaciones Aplicadas

Antes de consolidar el dataset se ejecutaron diferentes controles de calidad.

## Completitud

Se verificó la existencia de valores nulos.

Resultado:

- Sin valores nulos en las variables críticas.

---

## Consistencia

Se validó:

- Tipos de datos.
- Esquemas.
- Formatos numéricos.
- Integridad de identificadores.

Resultado:

Información consistente entre todos los datasets.

---

## Integridad Referencial

Se verificó la relación entre todas las tablas utilizando:

```text
company_id
```

Resultado:

No se detectaron registros huérfanos significativos.

---

## Unicidad

Se validó la unicidad de:

- company_id
- factura_id
- consumo_id
- servicio_id
- ticket_id
- evento_id

Resultado:

No existen duplicados que afecten el análisis.

---

## Reglas de Negocio

Se validó que los datos cumplieran restricciones como:

Facturación

```text
monto_facturado >= 0
```

Consumo

```text
trafico_gb >= 0
```

Churn

```text
0 = Cliente activo

1 = Cliente abandonó
```

Risk Score

```text
0 <= risk_score <= 1
```

---

# Dataset para Machine Learning

Posteriormente se ejecutó el proceso de Feature Engineering.

Durante esta etapa se generaron nuevas variables predictoras como:

- ARPU.
- Deuda por servicio.
- Consumo por servicio.
- Tickets por servicio.
- Eventos por servicio.
- Facturación por empleado.
- Tickets por empleado.

Asimismo, las variables categóricas fueron codificadas mediante StringIndexer.

Variables transformadas:

- sector
- region
- segmento

El resultado fue un nuevo dataset denominado:

```text
dataset_ml
```

Ubicación:

```text
/Volumes/workspace/default/churn_b2b/Feature_Engineering/dataset_ml
```

Este conjunto de datos contiene únicamente variables numéricas y está preparado para el entrenamiento del modelo de Machine Learning.

---

# Características del Dataset Final

| Característica | Descripción |
|----------------|-------------|
| Formato | Delta Lake |
| Plataforma | Databricks Community Edition |
| Motor de procesamiento | Apache Spark |
| Arquitectura | Medallion (Bronze, Silver y Gold) |
| Llave principal | company_id |
| Dataset analítico | dataset_ml |
| Variables objetivo | churn |
| Destino | Entrenamiento del modelo predictivo |

---

# Uso del Dataset

El dataset generado constituye la fuente oficial para las siguientes etapas del proyecto:

- Entrenamiento del modelo predictivo.
- Evaluación del modelo.
- Registro del modelo mediante MLflow.
- Publicación mediante FastAPI.
- Consulta desde MongoDB Atlas.
- Visualización en Power BI.
- Consumo desde la aplicación desarrollada en Next.js y desplegada en Vercel.

---

# Beneficios del Dataset Consolidado

La construcción del dataset permitió:

- Integrar información proveniente de múltiples fuentes.
- Eliminar inconsistencias entre los sistemas de origen.
- Obtener indicadores consolidados por empresa.
- Reducir la complejidad del procesamiento analítico.
- Facilitar la construcción de modelos predictivos.
- Garantizar la trazabilidad de los datos mediante la arquitectura Medallion.
- Contar con una base de datos lista para proyectos de Big Data y Machine Learning.

---

# Conclusión

El proceso ETL implementado permitió construir un dataset consolidado, limpio y validado que integra información comercial, financiera, operativa, técnica y de soporte de clientes B2B del sector telecomunicaciones.

Las validaciones realizadas durante las capas **Bronze**, **Silver** y **Gold**, junto con el proceso de **Feature Engineering**, garantizaron que el conjunto de datos utilizado para el entrenamiento del modelo de Machine Learning cumpla con criterios de calidad, consistencia e integridad.

Como resultado, el dataset **dataset_ml** constituye la base oficial para el desarrollo del modelo predictivo de churn y para su integración con el backend desarrollado en FastAPI, la base de datos MongoDB Atlas, el frontend implementado en Next.js y las herramientas de análisis y visualización como Power BI.