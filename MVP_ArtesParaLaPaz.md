# MVP: Tablero Estratégico "Artes para la Paz" - Command Center

## 1. Visión del Producto
Crear una aplicación web de visualización de datos (Dashboard) de alto impacto visual y rendimiento en tiempo real. El objetivo es monitorear la gestión territorial de 33 Nodos y 6 Departamentos en Colombia, visualizando la cobertura de contratación de Artistas Formadores.

## 2. Identidad Visual (Look & Feel)
*   **Tema:** "Smart City / Cyberpunk Clean".
*   **Modo:** Dark Mode (Fondo oscuro profundo #0E1117).
*   **Color de Marca (Acento Principal):** `#886FFF` (Violeta Estratégico).
*   **Logo:** Debe situarse en la esquina superior izquierda. URL: `https://ia903209.us.archive.org/35/items/id-general-textura-blanco/ID_General_Textura_Blanco.png`
*   **Tipografía:** Sans-serif, limpia y moderna.

## 3. Características Principales (Scope)
### A. Mapa de Inteligencia Territorial
*   Mapa navegable de Colombia oscuro.
*   Visualización de puntos (Establecimientos Educativos) con diferenciación de color por estado de contratación.
*   Tooltips informativos al pasar el mouse (Municipio, Nodo, Estado).

### B. Métricas de Alto Nivel (KPIs)
*   **Meta Global:** 803 Artistas (Cifra estática de referencia).
*   **Ejecución Real:** Conteo dinámico basado en la data.
*   **Porcentaje de Avance:** Cálculo automático.

### C. Análisis por Nodo
*   Gráfico comparativo que permita identificar rápidamente qué nodos tienen mayor o menor cobertura.

## 4. Fuente de Datos
*   **Origen:** Google Sheets.
*   **Hoja Específica:** `DATA_MASTER` (Hoja pre-procesada que contiene datos + coordenadas).
*   **Frecuencia:** Tiempo real (o caché de corta duración).

## 5. Criterios de Éxito
*   La aplicación debe cargar en menos de 3 segundos.
*   El mapa debe ser fluido al hacer zoom.
*   La estética debe coincidir con el código HEX `#886FFF`.