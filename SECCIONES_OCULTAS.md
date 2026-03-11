# Registro de Secciones Ocultas - Dashboard Tactico
Este documento sirve como inventario de las secciones que han sido ocultadas del dashboard principal para simplificar la interfaz, pero que siguen disponibles en el código para ser reactivadas.

## 1. Municipios con Necesidades de Vinculación
- **Fecha de ocultación:** 10 de Marzo, 2026
- **Ubicación en el código:** `app.py`, aproximadamente línea 1646 (dentro del bloque `ROW 3: Bottom Tables & Charts`).
- **Descripción:** Tabla que agrupa por municipio y nodo el estado de postulantes, vinculados y vacantes, filtrando solo aquellos con necesidades pendientes.
- **Cómo reactivar:** 
    1. Volver a habilitar el bloque de código comentado en `app.py`.
    2. Cambiar el layout de columnas en la línea 1643 de `st.columns(1)` a `st.columns(2)`.
    3. Mover el bloque de la sección de Asistencia de nuevo al contenedor `b2`.

---
*Nota: Este documento debe actualizarse cada vez que se oculte o elimine una sección funcional del tablero.*
