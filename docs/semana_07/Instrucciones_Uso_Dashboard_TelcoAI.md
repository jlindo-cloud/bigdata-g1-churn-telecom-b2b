# Informe - Semana 7

## Dashboard y Visualización del Riesgo de Churn para Áreas Comerciales

---

## Proyecto

Sistema de Predicción de Churn para Clientes de una Empresa de Telecomunicaciones B2B utilizando Big Data y Machine Learning

---

## Objetivo

Documentar el dashboard interactivo desarrollado para la visualización del riesgo de churn en clientes B2B, describiendo su estructura, secciones, métricas e indicadores, así como las instrucciones de uso dirigidas a las áreas comerciales para la identificación y gestión proactiva de clientes en riesgo de fuga.

El dashboard fue construido como una aplicación web desplegada en la nube, utilizando **Next.js** y **Vercel** como tecnologías principales, y consume las métricas generadas por el modelo de predicción de churn desarrollado en las etapas previas del proyecto.

---

## Integrantes:

- Asto Arotinco Ana (0000-0002-2195-0764)
- Flores Condeña Javier (0000-0003-2800-5084)
- Lindo Barrientos Jhonn Viequier (0000-0001-6025-7332)
- Tito Paredes Arian (0009-0002-5717-8099)
- Quispe Poma Cristian (0009-0008-6566-3741)

---

## Plataforma documentada

| Campo | Detalle |
|-------|---------|
| **Nombre** | Telco AI — Churn Predictor |
| **URL** | https://v0-churntelco2b2.vercel.app |
| **Stack** | Next.js desplegado en Vercel |
| **Repositorio** | g1-churn-telecom-b2b |
| **Curso** | Big Data (DD283) — Universidad Autónoma del Perú |

---

## 1. Propósito del dashboard

Telco AI es una plataforma de monitoreo y predicción de churn (fuga de clientes) para el segmento **B2B de telecomunicaciones**. Su objetivo es que las áreas comerciales identifiquen, con anticipación de hasta 90 días, qué clientes empresariales tienen alta probabilidad de no renovar su contrato, para intervenir de forma proactiva antes de perderlos.

**Usuarios objetivo:** ejecutivos comerciales, account managers, gerencia de retención y equipo de datos.

---

## 2. Acceso a la plataforma

1. Ingresar a la URL de la plataforma.
2. Se muestra la pantalla **Bienvenido** con el formulario de inicio de sesión.
3. Completar **Correo Electrónico** y **Contraseña**.
4. Pulsar **Iniciar Sesión**.

> **Nota sobre el entorno actual:** la plataforma opera en modo demostración. Tal como indica la propia pantalla de login, acepta cualquier correo con una contraseña de mínimo 6 caracteres. No existe validación real de credenciales ni control de roles en esta versión.

---

## 3. Estructura general de la interfaz

La aplicación usa un layout de tres zonas constantes:

| Zona | Ubicación | Contenido |
|------|-----------|-----------|
| Menú lateral | Izquierda | Navegación entre las 6 secciones + Cerrar Sesión (al pie) |
| Barra superior | Arriba | Nombre de la sección activa, buscador global, notificaciones y perfil |
| Área de trabajo | Centro | Contenido de la sección seleccionada |

**Secciones disponibles:** Dashboard · Predicciones · Empresas · Reportes · Administración · Configuración

---

## 4. Sección: Dashboard Ejecutivo

Vista de entrada. Ofrece el monitoreo general en tiempo real de las predicciones de churn.

### 4.1 Tarjetas de indicadores (KPIs)

Cuatro tarjetas en la parte superior. Cada una muestra el valor actual y su variación porcentual respecto al periodo anterior.

| Indicador | Qué mide | Cómo leerlo |
|-----------|----------|-------------|
| **Clientes en Riesgo** | Cantidad de clientes con probabilidad de churn elevada | Un aumento exige acción comercial inmediata |
| **Tasa de Churn (90d)** | Porcentaje de fuga proyectado a 90 días | Una variación negativa es favorable: significa que el churn baja |
| **Clientes Totales** | Base total de clientes analizados | Contextualiza el volumen sobre el que operan los porcentajes |
| **Conversiones Exitosas** | Clientes en riesgo que fueron retenidos | Mide la efectividad de las campañas de retención |

> Atención al signo de la variación: en **Tasa de Churn** un valor negativo es un buen resultado, mientras que en el resto de tarjetas lo positivo es el crecimiento.

### 4.2 Tendencia de Churn (Real vs Predicción)

Gráfico de líneas que superpone el **churn predicho** por el modelo contra el **churn real** observado. Sirve para validar visualmente qué tan ajustado está el modelo: cuanto más se solapan ambas líneas, mayor es la confiabilidad de las predicciones.

### 4.3 Distribución de Riesgo

Gráfico circular que segmenta toda la cartera en tres niveles: **Bajo Riesgo**, **Riesgo Medio** y **Alto Riesgo**, con el conteo de clientes en cada uno. Permite dimensionar de un vistazo cuánta de la cartera requiere atención prioritaria.

### 4.4 Precisión Histórica del Modelo

Gráfico de barras con la evolución del porcentaje de precisión del modelo por periodo. Al pasar el cursor sobre cada barra se muestra el valor exacto. Es la métrica de control de calidad: si la precisión cae de forma sostenida, el modelo necesita reentrenamiento.

### 4.5 Principales Empresas en Riesgo

Listado de las empresas más críticas, con su nombre, número de empleados y una etiqueta de color según el nivel de riesgo (Alto / Medio / Bajo). Es el acceso rápido a la cartera que exige gestión inmediata.

### 4.6 Botón "Generar Reporte"

Ubicado arriba a la derecha. Genera un reporte a partir de la información visible en el dashboard.

---

## 5. Sección: Predicciones

Muestra el análisis predictivo a 90 días para toda la cartera.

### 5.1 Tarjetas de estado del modelo

| Tarjeta | Contenido |
|---------|-----------|
| **Última Actualización** | Fecha y antigüedad del último cálculo de predicciones |
| **Precisión Promedio** | Precisión global del modelo y la versión en producción |
| **Clientes Analizados** | Total procesado y cuántos resultaron en riesgo |

Antes de tomar decisiones, verificar la **Última Actualización**: si los datos tienen varias horas o días, conviene sincronizar desde Administración.

### 5.2 Top 5 Clientes de Alto Riesgo

Ranking de los cinco clientes con mayor probabilidad de fuga. Cada fila incluye:

- **Nombre de la empresa** y fecha de la predicción.
- **Porcentaje de riesgo** (cifra grande a la derecha): probabilidad estimada de que el cliente abandone en los próximos 90 días.
- **Confianza:** qué tan seguro está el modelo de esa predicción. Es una métrica distinta al riesgo y debe leerse junto a él.
- **Botón "Ver Detalles":** abre el perfil completo del cliente.
- **Ícono de color** a la izquierda, que replica el semáforo de riesgo.

> **Cómo interpretar riesgo y confianza juntos:** un riesgo de 87% con confianza de 94% es una alerta sólida y accionable. Un riesgo alto con confianza baja debe validarse con el account manager antes de escalar una acción comercial.

---

## 6. Sección: Empresas

Módulo de gestión y análisis detallado de la cartera de clientes B2B.

### 6.1 Herramientas de búsqueda y filtrado

| Control | Función |
|---------|---------|
| **Buscar por nombre o ID** | Localiza una empresa puntual por texto |
| **Todos los riesgos** | Filtra la tabla por nivel de riesgo (Alto / Medio / Bajo) |
| **Ordenar por Riesgo** | Cambia el criterio de ordenamiento de la tabla |

Debajo de los controles se indica el número de resultados que cumplen el filtro activo.

### 6.2 Tabla de empresas

| Columna | Descripción |
|---------|-------------|
| **Empresa** | Razón social y número identificador del cliente |
| **Empleados** | Tamaño de la organización |
| **Ingresos Anuales** | Facturación que aporta el cliente (en miles de USD) |
| **Riesgo de Churn** | Porcentaje con indicador de color |
| **Tendencia** | Si el riesgo va *Aumentando* (flecha roja) o *Mejorando* (flecha verde) |
| **Última Act.** | Fecha del último cálculo para ese cliente |

Al pulsar la flecha del extremo derecho de cada fila se accede al detalle de la empresa.

### 6.3 Convención de colores (semáforo de riesgo)

Según el comportamiento observado en la plataforma:

| Color | Rango aproximado | Lectura |
|-------|------------------|---------|
| 🔴 Rojo | 80% a más | Riesgo alto — intervención urgente |
| 🟡 Amarillo | 50% – 79% | Riesgo medio — seguimiento cercano |
| 🟢 Verde | Menos de 50% | Riesgo bajo — mantenimiento habitual |

### 6.4 Cruce clave para priorizar

La combinación más importante de esta tabla es **Riesgo de Churn × Ingresos Anuales**. Un cliente con 91% de riesgo y facturación alta representa una pérdida potencial mucho mayor que uno con el mismo riesgo pero facturación baja. La columna **Tendencia** añade urgencia: un riesgo *Aumentando* debe atenderse antes que uno estable o *Mejorando*.

---

## 7. Sección: Reportes

Permite generar y descargar reportes de análisis.

### 7.1 Generar un nuevo reporte

1. Seleccionar el **Tipo de Reporte** en el menú desplegable.
2. Elegir el **Periodo** en el selector de fecha.
3. Pulsar **Generar Reporte**.

### 7.2 Reportes disponibles

Listado de reportes ya generados. Cada entrada muestra el título, el periodo que cubre, la fecha de generación, una etiqueta de estado (**Completado**) y la acción **Descargar**.

Los reportes contemplados son: Reporte Mensual de Churn, Análisis de Tendencias Trimestrales y Reporte de Precisión del Modelo.

---

## 8. Sección: Administración

Módulo técnico. Su uso está pensado para el equipo de datos y TI, no para el área comercial.

### 8.1 Módulos de gestión

| Módulo | Acción | Para qué sirve |
|--------|--------|----------------|
| **Gestión de Usuarios** | Administrar Usuarios | Alta, baja y permisos de los usuarios de la plataforma |
| **Gestión de Base de Datos** | Sincronizar Datos | Actualiza la información desde las fuentes externas |
| **Entrenamiento del Modelo** | Entrenar Modelo | Reentrena y valida el modelo de predicción |
| **Configuración del Sistema** | Configurar Sistema | Parámetros avanzados de la plataforma |

> **Precaución:** *Entrenar Modelo* y *Sincronizar Datos* afectan a toda la plataforma. Ejecutarlos únicamente con autorización del responsable técnico y fuera de horario crítico, ya que las predicciones pueden variar tras el reentrenamiento.

### 8.2 Estado del Sistema

Tres indicadores de salud que deben revisarse antes de confiar en los datos mostrados:

- **API Status** → debe figurar como *Operativo*
- **Base de Datos** → debe figurar como *Conectada*
- **Modelo ML** → debe figurar como *Activo*

Si alguno aparece en estado distinto, la información del dashboard puede estar desactualizada o incompleta.

---

## 9. Sección: Configuración

Personalización de la experiencia del usuario.

### 9.1 Información de Perfil
Campos de Nombre Completo, Email y Rol. Los cambios se aplican con **Guardar Cambios**.

### 9.2 Notificaciones

| Notificación | Qué envía |
|--------------|-----------|
| **Alertas de Alto Riesgo** | Aviso cuando una empresa entra en riesgo alto |
| **Reportes Semanales** | Resumen semanal del análisis |
| **Actualizaciones del Sistema** | Avisos de mantenimiento y nuevas versiones |

Se recomienda mantener activas las **Alertas de Alto Riesgo** para el personal comercial: es el mecanismo que convierte el dashboard en una herramienta proactiva en lugar de una consulta pasiva.

### 9.3 Visualización
Permite alternar el **Modo Oscuro** y seleccionar el **Idioma** de la interfaz.

### 9.4 Cerrar Sesión
Disponible al pie del menú lateral izquierdo.

---

## 10. Flujo de trabajo sugerido para el área comercial

**Rutina diaria (5 minutos)**
1. Abrir **Dashboard** y revisar la tarjeta *Clientes en Riesgo* y su variación.
2. Comprobar en *Principales Empresas en Riesgo* si hay nombres nuevos respecto al día anterior.

**Rutina semanal (20 minutos)**
1. Entrar a **Predicciones** y verificar la fecha de *Última Actualización*.
2. Revisar el *Top 5 de Alto Riesgo* y abrir **Ver Detalles** de cada uno.
3. Pasar a **Empresas**, filtrar por riesgo Alto y ordenar por riesgo.
4. Priorizar la gestión cruzando el porcentaje de riesgo con los **Ingresos Anuales** y la **Tendencia**.
5. Asignar cada cuenta crítica a su account manager con una acción de retención concreta.

**Rutina mensual**
1. Generar el *Reporte Mensual de Churn* desde **Reportes**.
2. Contrastar el KPI de *Conversiones Exitosas* con las acciones ejecutadas el mes anterior para medir la efectividad de la retención.
3. Revisar la *Precisión Histórica del Modelo*; si muestra caída sostenida, solicitar reentrenamiento al equipo técnico.

---

## 11. Glosario de métricas

| Término | Definición |
|---------|------------|
| **Churn** | Fuga o abandono de un cliente; en B2B, la no renovación del contrato |
| **Riesgo de Churn** | Probabilidad (0–100%) de que un cliente abandone en la ventana de predicción |
| **Confianza** | Grado de certeza del modelo sobre una predicción concreta. Es independiente del riesgo |
| **Precisión del Modelo** | Porcentaje de predicciones que resultaron correctas al contrastarse con la realidad |
| **Tasa de Churn (90d)** | Porcentaje de la cartera proyectado a fugarse en los próximos 90 días |
| **Conversiones Exitosas** | Clientes que estaban en riesgo y fueron retenidos tras la gestión comercial |
| **Tendencia** | Dirección del riesgo de un cliente: *Aumentando* (empeora) o *Mejorando* |
| **Modelo v2.1** | Versión del modelo predictivo actualmente en producción |

---

## 12. Limitaciones conocidas de la versión actual

Se documentan de forma transparente para delimitar el alcance de esta entrega:

1. **Autenticación en modo demo:** no hay validación real de credenciales ni diferenciación efectiva de roles. Para producción se requiere un proveedor de autenticación real y control de acceso por rol.
2. **Datos de demostración:** la plataforma opera con un conjunto acotado de clientes y valores de ejemplo, no con la carga completa de producción.
3. **Sin conexión en vivo al pipeline:** las predicciones mostradas no se recalculan automáticamente desde la capa Gold del pipeline ETL; requieren sincronización manual desde Administración.

**Siguientes pasos propuestos:** conectar la plataforma al modelo entrenado del proyecto mediante una API, implementar autenticación real con roles diferenciados (comercial / analista / administrador) y habilitar la exportación efectiva de los reportes.

---

*Semana 7 — Dashboard y Visualización | Proyecto g1-churn-telecom-b2b*
*Big Data DD283 — Universidad Autónoma del Perú*
