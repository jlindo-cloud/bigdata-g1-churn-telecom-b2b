
# Análisis de Calidad de Datos

## Objetivo

Evaluar la calidad de la información utilizada en el proyecto de predicción de churn de clientes B2B del sector telecomunicaciones, garantizando que los datos empleados durante el proceso ETL y el entrenamiento del modelo de Machine Learning sean consistentes, completos, íntegros y confiables.

El análisis de calidad de datos se realizó durante las capas **Bronze**, **Silver** y **Gold** de la arquitectura Medallion implementada en Databricks, aplicando controles automáticos sobre cada conjunto de datos antes de su consolidación.

---

Integrantes:

- Asto Arotinco Ana (0000-0002-2195-0764)
- Flores Condeña Javier (0000-0003-2800-5084)
- Lindo Barrientos Jhonn Viequier(0000-0001-6025-7332)
- Tito Paredes Arian (0009-0002-5717-8099)
- Quispe Poma Cristian (0009-0008-6566-3741)
---
# Arquitectura del Proceso de Calidad de Datos

```text
Archivos CSV
        │
        ▼
01_ingestion
        │
        ▼
Bronze
(Validación Inicial)
        │
        ▼
Silver
(Limpieza y Calidad)
        │
        ▼
Gold
(Integración y Validación)
        │
        ▼
EDA
        │
        ▼
Feature Engineering
```

---

# Dimensiones de Calidad Evaluadas

## 1. Completitud

### Objetivo

Verificar que los datos requeridos para el análisis y entrenamiento del modelo se encuentren disponibles y con un nivel mínimo de información faltante.

### Validaciones realizadas

Se evaluó:

- Cantidad de valores nulos por columna.
- Porcentaje de registros incompletos.
- Disponibilidad de las variables críticas para el modelo.

Ejemplo de validación en PySpark:

```python
from pyspark.sql.functions import col, count, when

gold_dataset.select([
    count(when(col(c).isNull(), c)).alias(c)
    for c in gold_dataset.columns
]).show()
```

### Resultado

- No se identificaron valores nulos en las variables principales del dataset consolidado.
- Los valores faltantes fueron tratados durante la capa Silver mediante imputación controlada.

**Estado:** ✅ Aprobado

---

## 2. Consistencia

### Objetivo

Garantizar que la información mantenga coherencia entre todos los conjuntos de datos utilizados.

### Validaciones realizadas

Se verificó:

- Tipos de datos.
- Formatos numéricos.
- Formatos de fechas.
- Correspondencia entre columnas relacionadas.
- Uniformidad de nombres de atributos.

Ejemplos:

| Campo | Tipo esperado |
|--------|---------------|
| company_id | Integer |
| monto_facturado | Double |
| trafico_gb | Double |
| churn | Integer |
| risk_score | Double |

Se validó el esquema mediante:

```python
df.printSchema()
```

### Resultado

Todos los datasets conservaron la estructura esperada durante el proceso ETL.

**Estado:** ✅ Consistencia Alta

---

## 3. Unicidad

### Objetivo

Verificar que los registros posean identificadores únicos y que no existan duplicados que afecten los resultados del análisis.

### Identificadores evaluados

- company_id
- factura_id
- consumo_id
- servicio_id
- ticket_id
- evento_id

### Validaciones realizadas

Se revisó la existencia de registros duplicados utilizando funciones de agrupación y conteo.

Ejemplo:

```python
df.groupBy("company_id").count()
```

### Resultado

No se detectaron duplicados en los identificadores principales utilizados durante la integración.

Los registros inconsistentes fueron eliminados durante la capa Silver.

**Estado:** ✅ Validado

---

## 4. Validez

### Objetivo

Verificar que los valores almacenados cumplan las reglas de negocio definidas para el proyecto.

### Reglas aplicadas

#### Facturación

```text
monto_facturado >= 0
```

#### Consumo

```text
trafico_gb >= 0
```

#### Mora

```text
dias_mora >= 0
```

#### Servicios

```text
monto_mensual >= 0
```

#### Churn

```text
0 = Cliente activo

1 = Cliente abandonó
```

#### Risk Score

```text
0 <= risk_score <= 1
```

### Resultado

Los valores procesados cumplen las reglas establecidas para el modelo predictivo.

**Estado:** ✅ Validado

---

## 5. Integridad Referencial

### Objetivo

Garantizar que todas las tablas secundarias mantengan una relación válida con la tabla principal de empresas.

### Llave de negocio utilizada

```text
company_id
```

### Tablas relacionadas

- empresas
- facturacion
- consumo
- servicios
- tickets
- eventos_red
- churn

Las relaciones fueron implementadas mediante operaciones **LEFT JOIN**, preservando todas las empresas del conjunto principal.

Ejemplo:

```python
df_empresas.join(df_facturacion, "company_id", "left")
```

### Resultado

No se identificaron registros huérfanos relevantes que afecten el proceso de integración.

**Estado:** ✅ Integridad Referencial Validada

---

# Controles Implementados en Cada Capa

## Bronze

Controles aplicados:

- Verificación de lectura de archivos.
- Validación de esquemas.
- Conteo de registros.
- Almacenamiento en formato Delta.

Objetivo:

Preservar los datos originales sin modificaciones.

---

## Silver

Controles aplicados:

- Eliminación de registros inválidos.
- Tratamiento de valores nulos.
- Normalización de tipos de datos.
- Validación de identificadores.
- Estandarización de estructuras.

Objetivo:

Obtener datos limpios y consistentes.

---

## Gold

Controles aplicados:

- Validación de uniones entre tablas.
- Integración mediante `company_id`.
- Agregaciones por empresa.
- Revisión del número final de registros.
- Construcción del dataset maestro.

Objetivo:

Generar un dataset analítico listo para Machine Learning.

---

# Indicadores de Calidad

| Indicador | Resultado |
|------------|-----------|
| Completitud | 100% en variables críticas |
| Consistencia | Alta |
| Unicidad | Validada |
| Validez | Validada |
| Integridad Referencial | Validada |
| Calidad del Esquema | Validada |
| Calidad General | Aprobada |

---

# Riesgos Identificados

Durante el análisis se identificaron los siguientes riesgos potenciales:

- Posibles inconsistencias históricas en información operativa.
- Variaciones de formatos provenientes de diferentes sistemas origen.
- Valores faltantes en atributos secundarios.
- Posibles diferencias en la periodicidad de actualización entre fuentes.

Estos riesgos fueron mitigados mediante las transformaciones implementadas en la capa Silver.

---

# Acciones Correctivas Aplicadas

Durante el proceso ETL se implementaron las siguientes acciones de mejora:

- Validación automática de esquemas.
- Conversión de tipos de datos.
- Tratamiento de valores nulos.
- Eliminación de registros inconsistentes.
- Validación de claves primarias.
- Verificación de relaciones entre tablas.
- Integración mediante LEFT JOIN.
- Consolidación de indicadores por empresa.
- Generación del dataset analítico para Machine Learning.

---

# Beneficios del Proceso de Calidad

La implementación de controles de calidad permitió:

- Incrementar la confiabilidad de los datos.
- Reducir errores durante el entrenamiento del modelo.
- Mejorar la consistencia entre las distintas fuentes de información.
- Garantizar la integridad del dataset consolidado.
- Facilitar el análisis exploratorio y la generación de variables predictivas.

---

# Conclusión

El proceso de calidad de datos implementado permitió garantizar que la información utilizada en el proyecto cumple con los estándares mínimos requeridos para el desarrollo de modelos predictivos de Machine Learning.

Las validaciones realizadas durante las capas **Bronze**, **Silver** y **Gold** aseguraron que el dataset consolidado presente altos niveles de completitud, consistencia, unicidad, validez e integridad referencial.

Como resultado, el conjunto de datos generado constituye una base confiable para las siguientes etapas del proyecto, incluyendo el análisis exploratorio (EDA), la ingeniería de características (Feature Engineering), el entrenamiento del modelo predictivo de churn y su posterior despliegue mediante FastAPI, MongoDB Atlas, Railway, Vercel y Power BI.