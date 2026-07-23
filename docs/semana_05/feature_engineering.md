## Semana 5 – Feature Engineering


### Proyecto Sistema de Predicción de Churn para Clientes de una Empresa de Telecomunicaciones B2B mediante Big Data y Machine Learning

1. Objetivo
El objetivo de esta fase fue realizar el proceso de Feature Engineering (Ingeniería de Variables), transformando la información obtenida durante el proceso ETL (Bronze, Silver y Gold) en un conjunto de variables predictivas que permitieran mejorar el desempeño del modelo de Machine Learning para la predicción del abandono de clientes (Churn).
En esta etapa se consolidó la información proveniente de múltiples fuentes de negocio, generando un dataset único que representa el comportamiento comercial, financiero, operativo y de atención al cliente de cada empresa.

Integrantes:
- Asto Arotinco Ana (0000-0002-2195-0764)
- Flores Condeña Javier (0000-0003-2800-5084)
- Lindo Barrientos Jhonn Viequier(0000-0001-6025-7332)
- Tito Paredes Arian (0009-0002-5717-8099)
- Quispe Poma Cristian (0009-0008-6566-3741)

2. Proceso realizado
El proceso de Ingeniería de Variables se desarrolló utilizando Apache Spark sobre Databricks Community Edition.
Las actividades realizadas fueron las siguientes:

Consolidación de información
Se integraron los datasets provenientes de:
- Empresas
- Facturación
- Consumo
- Servicios contratados
- Tickets de soporte
- Eventos de red
- Dataset de Churn
Todo ello permitió obtener una única vista por empresa.

Limpieza de datos
Durante esta etapa se realizaron las siguientes actividades:
- Eliminación de registros duplicados.
- Tratamiento de valores nulos.
- Homogeneización de tipos de datos.
- Validación de integridad de las claves (company_id).
- Normalización de formatos.

Transformación de variables
Posteriormente se construyeron variables agregadas utilizando funciones de Apache Spark.
Las agregaciones se realizaron por empresa (company_id).

3. Variables predictivas generadas
Las principales variables obtenidas fueron las siguientes:

Variable | Descripción | Tipo
--- | --- | ---
empleados | Número de colaboradores de la empresa | Numérica
facturacion_total | Facturación acumulada del cliente | Numérica
facturacion_promedio | Promedio mensual de facturación | Numérica
facturacion_maxima | Mayor facturación registrada | Numérica
dias_mora_promedio | Promedio de días de atraso en pagos | Numérica
deuda_total | Deuda acumulada | Numérica
trafico_total_gb | Consumo total de datos | Numérica
trafico_promedio_gb | Consumo promedio mensual | Numérica
ancho_banda_promedio | Ancho de banda contratado | Numérica
pico_maximo_mbps | Máximo pico de tráfico | Numérica
cantidad_servicios | Número de servicios contratados | Numérica
monto_mensual_promedio | Promedio mensual del servicio | Numérica
sla_promedio | Nivel promedio de cumplimiento del SLA | Numérica
cantidad_tickets | Número total de tickets de soporte | Numérica
tiempo_resolucion_promedio | Tiempo promedio de resolución | Numérica
tickets_escalados | Cantidad de tickets escalados | Numérica
cantidad_eventos | Número de eventos de red | Numérica
duracion_promedio_eventos | Duración promedio de incidencias | Numérica
nps | Net Promoter Score | Numérica
csat | Customer Satisfaction Score | Numérica

4. Variables categóricas transformadas
Las variables categóricas fueron convertidas a valores numéricos mediante técnicas de codificación para permitir su utilización por el algoritmo de Machine Learning.
Se transformaron las siguientes variables:

Variable Original | Variable Generada
--- | ---
sector | sector_index
region | region_index
segmento | segmento_index

Esta transformación permite que el modelo interprete correctamente la información categórica.

5. Dataset final para Machine Learning
El dataset final quedó conformado por las siguientes variables:
- company_id
- ruc
- razon_social
- sector
- region
- empleados
- segmento
- fecha_alta
- ejecutivo_comercial
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
- risk_score
- churn

Posteriormente este dataset fue utilizado para entrenar el modelo de Machine Learning.

6. Justificación de las variables creadas
Las variables seleccionadas representan los principales factores que influyen en el abandono de clientes dentro de una empresa de telecomunicaciones B2B.

Variables financieras
Permiten identificar clientes con problemas de pago o disminución en el consumo del servicio.
Ejemplos:
- facturación promedio
- deuda total
- días de mora

Variables de consumo
Representan el uso real de los servicios contratados.
Ejemplos:
- tráfico promedio
- ancho de banda
- pico máximo de utilización

Variables de soporte
Miden la experiencia del cliente respecto al servicio recibido.
Ejemplos:
- tickets
- tiempo de resolución
- tickets escalados

Variables de calidad del servicio
Permiten medir la estabilidad de la red.
Ejemplos:
- eventos de red
- duración de incidencias
- SLA promedio

Variables de satisfacción
Representan la percepción del cliente.
Ejemplos:
- NPS
- CSAT

7. Importancia para el modelo predictivo
La Ingeniería de Variables permitió transformar datos operativos en información relevante para el algoritmo de Machine Learning.
Estas variables incrementan la capacidad del modelo para identificar patrones asociados al abandono de clientes, mejorando la calidad de las predicciones y proporcionando una visión integral del comportamiento de los clientes empresariales.

8. Entregables
Durante la Semana 5 se generaron los siguientes entregables:
- Notebook de Databricks con el proceso completo de Ingeniería de Variables.
- Dataset Gold consolidado con variables predictivas.
- Documentación de las nuevas variables creadas.
- Dataset final preparado para el entrenamiento del modelo de Machine Learning.