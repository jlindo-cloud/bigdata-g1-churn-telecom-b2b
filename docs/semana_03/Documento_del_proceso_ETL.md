# Proceso ETL (Extract, Transform and Load)

## Objetivo

Diseñar e implementar un proceso ETL (Extract, Transform and Load) que permita integrar la información proveniente de diferentes fuentes de datos relacionadas con empresas del sector telecomunicaciones B2B, con el fin de construir un conjunto de datos confiable para el análisis y predicción del abandono de clientes (Customer Churn).

El proceso fue desarrollado utilizando **Databricks Community Edition**, aprovechando Apache Spark para el procesamiento distribuido de los datos y una arquitectura de tipo **Medallion (Bronze, Silver y Gold)**.

---

Integrantes:

- Asto Arotinco Ana (0000-0002-2195-0764)
- Flores Condeña Javier (0000-0003-2800-5084)
- Lindo Barrientos Jhonn Viequier(0000-0001-6025-7332)
- Tito Paredes Arian (0009-0002-5717-8099)
- Quispe Poma Cristian (0009-0008-6566-3741)
---

# Arquitectura ETL

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
02_bronze
        │
        ▼
Silver
        │
        ▼
03_silver
        │
        ▼
Gold
        │
        ▼
04_gold
        │
        ▼
gold_dataset
        │
        ▼
05_eda
        │
        ▼
06_feature_engineering
        │
        ▼
dataset_ml
```

---

# Tecnologías utilizadas

| Herramienta | Descripción |
|-------------|-------------|
| Databricks Community Edition | Plataforma para procesamiento Big Data |
| Apache Spark | Procesamiento distribuido de datos |
| PySpark | Transformación y análisis de datos |
| Delta Lake | Almacenamiento optimizado de datos |
| Unity Catalog Volumes | Administración de archivos y datasets |
| GitHub | Versionamiento del código fuente |

---

# Fase 1: Extracción (Extract)

## Objetivo

Leer los archivos CSV que contienen la información histórica de las empresas y sus operaciones.

Los archivos fueron almacenados dentro del volumen de Databricks:

```text
/Volumes/workspace/default/churn_b2b/Datos/
```

## Archivos procesados

| Archivo | Descripción |
|----------|-------------|
| empresas.csv | Información general de las empresas |
| facturacion.csv | Historial de facturación |
| consumo.csv | Consumo mensual de servicios |
| servicios.csv | Servicios contratados |
| tickets.csv | Historial de incidencias y soporte |
| eventos_red.csv | Eventos e incidencias de red |
| churn.csv | Variable objetivo del modelo |

## Actividades realizadas

- Lectura de archivos CSV mediante PySpark.
- Inferencia automática de esquemas.
- Validación de existencia de los archivos.
- Carga inicial en DataFrames Spark.

Ejemplo:

```python
df_empresas = spark.read.csv(
    "/Volumes/workspace/default/churn_b2b/Datos/empresas.csv",
    header=True,
    inferSchema=True
)
```

---

# Fase 2: Capa Bronze

## Objetivo

Almacenar una copia fiel de los datos originales sin realizar modificaciones significativas.

Esta capa representa la zona de aterrizaje (Landing Zone) del Data Lake.

## Actividades realizadas

- Validación de la estructura de los archivos.
- Verificación del número de registros.
- Almacenamiento en formato Delta Lake.

Ubicación:

```text
/Volumes/workspace/default/churn_b2b/Bronze/
```

Datasets almacenados:

- empresas
- facturacion
- consumo
- servicios
- tickets
- eventos_red
- churn

Beneficios:

- Conservación de los datos originales.
- Posibilidad de reprocesamiento.
- Trazabilidad de la información.

---

# Fase 3: Capa Silver

## Objetivo

Aplicar procesos de limpieza, normalización y estandarización de los datos antes de su integración.

## Transformaciones realizadas

### Validación de tipos de datos

Se verificó que cada columna tuviera el tipo de dato adecuado.

Ejemplo:

| Campo | Tipo |
|--------|------|
| company_id | Integer |
| monto_facturado | Double |
| trafico_gb | Double |
| churn | Integer |
| risk_score | Double |

---

### Eliminación de registros inválidos

Se eliminaron registros que presentaban inconsistencias o identificadores nulos.

Ejemplo:

```python
df = df.filter(col("company_id").isNotNull())
```

---

### Tratamiento de valores nulos

Se reemplazaron valores faltantes cuando fue necesario utilizando:

- Valor 0 para variables numéricas.
- Valores por defecto en variables categóricas cuando aplicaba.

Ejemplo:

```python
df = df.fillna(0)
```

---

### Validación de calidad

Se verificó:

- Cantidad de registros.
- Esquema de cada DataFrame.
- Valores nulos.
- Tipos de datos.

Los datasets limpios fueron almacenados en:

```text
/Volumes/workspace/default/churn_b2b/Silver/
```

---

# Fase 4: Capa Gold

## Objetivo

Integrar toda la información de negocio en un único dataset consolidado listo para análisis y Machine Learning.

## Integración de datos

La integración se realizó utilizando la llave de negocio:

```text
company_id
```

Se consolidó información proveniente de:

- Empresas
- Facturación
- Consumo
- Servicios
- Tickets
- Eventos de red
- Información de churn

Las operaciones de integración se realizaron mediante LEFT JOIN para preservar todas las empresas del conjunto principal.

---

## Agregaciones realizadas

Se calcularon indicadores de negocio por empresa.

### Facturación

- Facturación total.
- Facturación promedio.
- Facturación máxima.
- Días promedio de mora.
- Deuda total.

### Consumo

- Tráfico total.
- Consumo promedio.
- Ancho de banda promedio.
- Pico máximo.

### Servicios

- Cantidad de servicios.
- Monto mensual promedio.
- SLA promedio.

### Tickets

- Cantidad de tickets.
- Tiempo promedio de resolución.
- Tickets escalados.

### Eventos de red

- Cantidad de eventos.
- Duración promedio de eventos.

---

## Resultado

Se obtuvo un dataset denominado:

```text
gold_dataset
```

Ubicación:

```text
/Volumes/workspace/default/churn_b2b/Gold/gold_dataset
```

Este dataset contiene una vista integrada de cada empresa con indicadores comerciales, financieros, operativos y técnicos.

---

# Fase 5: Validación (EDA)

Antes de generar las variables para Machine Learning se realizó un Análisis Exploratorio de Datos (EDA).

Las principales actividades fueron:

- Revisión del esquema.
- Estadísticas descriptivas.
- Identificación de valores nulos.
- Distribución de la variable objetivo (Churn).
- Distribución por sector.
- Distribución por región.
- Análisis de variables numéricas.
- Correlación entre variables relevantes.

Este análisis permitió comprender el comportamiento de los datos y validar su calidad antes del entrenamiento del modelo.

---

# Fase 6: Feature Engineering

## Objetivo

Construir nuevas variables predictoras que incrementen la capacidad del modelo de Machine Learning para identificar empresas con riesgo de abandono.

## Variables generadas

Se crearon, entre otras, las siguientes características:

- ARPU (Average Revenue Per User).
- Deuda por servicio.
- Consumo por servicio.
- Tickets por servicio.
- Eventos por servicio.
- Facturación por empleado.
- Tickets por empleado.

Además, las variables categóricas fueron codificadas mediante **StringIndexer**.

Variables codificadas:

- sector
- región
- segmento

El resultado fue almacenado como:

```text
dataset_ml
```

Ubicación:

```text
/Volumes/workspace/default/churn_b2b/Feature_Engineering/dataset_ml
```

---

# Validaciones realizadas

Durante todo el proceso ETL se ejecutaron diferentes controles de calidad:

- Validación del esquema de cada dataset.
- Conteo de registros.
- Verificación de valores nulos.
- Consistencia de tipos de datos.
- Integridad de la llave `company_id`.
- Validación de las uniones entre tablas.
- Verificación del número final de empresas procesadas.

---

# Resultado obtenido

Como resultado del proceso ETL se generó un conjunto de datos consolidado, limpio y enriquecido que servirá como base para el entrenamiento del modelo predictivo de churn.

El dataset final integra información:

- Comercial.
- Financiera.
- Operativa.
- Técnica.
- Atención al cliente.
- Riesgo de abandono.

Este conjunto de datos constituye la base para las siguientes etapas del proyecto:

- Entrenamiento del modelo de Machine Learning.
- Registro del modelo mediante MLflow.
- Exposición del modelo mediante FastAPI.
- Visualización de indicadores en Power BI.
- Consumo desde la aplicación web desarrollada con Next.js y desplegada en Vercel.

---

# Beneficios de la arquitectura implementada

- Arquitectura Medallion (Bronze, Silver y Gold).
- Procesamiento distribuido con Apache Spark.
- Almacenamiento optimizado mediante Delta Lake.
- Escalabilidad para grandes volúmenes de datos.
- Alta trazabilidad del proceso ETL.
- Separación clara entre datos crudos, datos limpios y datos analíticos.
- Base preparada para proyectos de Big Data y Machine Learning.