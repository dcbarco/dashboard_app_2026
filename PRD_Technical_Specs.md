# PRD: Especificaciones Técnicas - Dashboard Artes para la Paz

## 1. Stack Tecnológico
*   **Lenguaje:** Python 3.9+.
*   **Frontend Framework:** Streamlit.
*   **Data Manipulation:** Pandas.
*   **Geospatial Visualization:** PyDeck (Deck.gl).
*   **Charting:** Plotly Express.

## 2. Estructura de Datos (Backend Simulation)
El sistema leerá la hoja `DATA_MASTER` de Google Sheets.
**Columnas Críticas:**
*   `NODO` (String): Identificador del grupo (ej. "Nodo 1").
*   `DEPARTAMENTO` (String): Filtro macro.
*   `MUNICIPIO` (String): Filtro micro.
*   `EE` (String): Nombre del Establecimiento Educativo (Label del punto).
*   `ESTADO_CONTRATACION` (Columna M original):
    *   *Lógica:* Si la celda tiene contenido (texto) -> **CONTRATADO**.
    *   *Lógica:* Si la celda es `NaN` o vacía -> **VACANTE**.
*   `LATITUD` (Float): Coordenada Y (Columna O generada por fórmula).
*   `LONGITUD` (Float): Coordenada X (Columna P generada por fórmula).

## 3. Requerimientos de UI/UX (Streamlit)

### 3.1 Layout General
*   `st.set_page_config(layout="wide")`
*   **Sidebar:** Debe contener los filtros de control (Departamento, Nodo).
*   **Main Area:** Header con Logo, KPIs, Mapa Central, Gráficos inferiores.

### 3.2 Componentes Específicos
*   **KPI Cards:** Usar CSS personalizado (`st.markdown`) para crear tarjetas con efecto "Glassmorphism" (fondo semitransparente) y borde superior color `#886FFF`.
*   **Mapa (PyDeck):**
    *   Estilo de mapa: `mapbox://styles/mapbox/dark-v10`.
    *   Layer: `pdk.Layer("ScatterplotLayer")`.
    *   **Colores de Puntos:**
        *   Contratado: `[0, 255, 128, 200]` (Verde Neón).
        *   Vacante: `[255, 0, 128, 200]` (Magenta/Rojo).
    *   Radio de puntos: Dinámico o fijo (ej. 100m - 500m dependiendo del zoom).
*   **Gráfico de Barras (Plotly):**
    *   Barras horizontales: Avance por Nodo.
    *   Color de barras: `#886FFF`.
    *   Fondo del gráfico: Transparente (`paper_bgcolor='rgba(0,0,0,0)'`).

## 4. Flujo de Datos y Simulación
Dado que el entorno de desarrollo inicial no tiene acceso a la API de Google, se debe crear una función `load_data()` que:
1.  Genere un **DataFrame Mock (Falso)**.
2.  Replique exactamente las columnas mencionadas en la sección 2.
3.  Simule ~300 registros distribuidos en los departamentos de Colombia.
4.  Permita cambiar fácilmente a la conexión real (`st.connection` o `gspread`) en el futuro cambiando solo una línea de código.