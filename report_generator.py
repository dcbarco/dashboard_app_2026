# ============================================================================
# REPORT GENERATOR — PDF REPORT ENGINE
# Generates dark-themed PDF reports mirroring the dashboard layout
# ============================================================================

import io
import os
import tempfile
import requests
from datetime import datetime
from fpdf import FPDF
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd

# ── Brand Colors (matching app.py) ──────────────────────────────────────────
BG       = "#080810"
CARD     = "#0f0f1a"
CARD2    = "#12121f"
ACCENT   = "#886FFF"
GN       = "#00FF80"
MG       = "#FF0080"
CY       = "#00D4FF"
OR       = "#FF9F1C"
TW       = "#e8e6f0"
TD       = "rgba(232,230,240,0.45)"
BDR      = "rgba(136,111,255,0.18)"
LOGO_URL = "https://ia903209.us.archive.org/35/items/id-general-textura-blanco/ID_General_Textura_Blanco.png"

# RGB tuples for fpdf
RGB_BG     = (8, 8, 16)
RGB_CARD   = (15, 15, 26)
RGB_CARD2  = (18, 18, 31)
RGB_ACCENT = (136, 111, 255)
RGB_GN     = (0, 255, 128)
RGB_MG     = (255, 0, 128)
RGB_CY     = (0, 212, 255)
RGB_OR     = (255, 159, 28)
RGB_TW     = (232, 230, 240)
RGB_TD     = (160, 158, 170)
RGB_WHITE  = (255, 255, 255)
RGB_BORDER = (50, 45, 80)


def _hex_to_rgb(hex_color):
    """Convert hex color string to RGB tuple."""
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def _download_logo(cache_dir=None):
    """Download and cache the logo image."""
    if cache_dir is None:
        cache_dir = tempfile.gettempdir()
    logo_path = os.path.join(cache_dir, "artes_logo.png")
    if not os.path.exists(logo_path):
        try:
            r = requests.get(LOGO_URL, timeout=10)
            r.raise_for_status()
            with open(logo_path, "wb") as f:
                f.write(r.content)
        except Exception:
            return None
    return logo_path


def _fig_to_png(fig, width=800, height=400):
    """Convert a Plotly figure to PNG bytes using kaleido. Returns bytes or None."""
    try:
        return pio.to_image(fig, format="png", width=width, height=height, scale=2)
    except Exception:
        return None


def _save_tmp_png(png_bytes, name="chart"):
    """Save PNG bytes to a temp file and return path."""
    if png_bytes is None:
        return None
    path = os.path.join(tempfile.gettempdir(), f"report_{name}.png")
    with open(path, "wb") as f:
        f.write(png_bytes)
    return path


def _sanitize(text):
    """Replace Unicode characters unsupported by Helvetica with ASCII equivalents."""
    if not isinstance(text, str):
        text = str(text)
    replacements = {
        "\u2014": "-",   # em-dash
        "\u2013": "-",   # en-dash
        "\u2018": "'",   # left single quote
        "\u2019": "'",   # right single quote
        "\u201c": '"',   # left double quote
        "\u201d": '"',   # right double quote
        "\u2026": "...", # ellipsis
        "\u00b7": ".",   # middle dot
        "\u2022": "*",   # bullet
        "\u00e9": "e",   # é
        "\u00e1": "a",   # á
        "\u00ed": "i",   # í
        "\u00f3": "o",   # ó
        "\u00fa": "u",   # ú
        "\u00f1": "n",   # ñ
        "\u00c9": "E",   # É
        "\u00c1": "A",   # Á
        "\u00cd": "I",   # Í
        "\u00d3": "O",   # Ó
        "\u00da": "U",   # Ú
        "\u00d1": "N",   # Ñ
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    # Fallback: strip any remaining non-latin1 chars
    try:
        text.encode('latin-1')
    except UnicodeEncodeError:
        text = text.encode('latin-1', errors='replace').decode('latin-1')
    return text


class ReportPDF(FPDF):
    """Custom PDF class with dark theme and consistent layout."""

    def __init__(self, filter_context="", **kwargs):
        super().__init__(orientation="P", unit="mm", format="A4", **kwargs)
        self.filter_context = filter_context
        self.report_date = datetime.now().strftime("%d/%m/%Y - %I:%M %p")
        self._logo_path = _download_logo()
        self.set_auto_page_break(auto=True, margin=12)

    def _draw_bg(self):
        """Fill the entire page with the dark background color."""
        self.set_fill_color(*RGB_BG)
        self.rect(0, 0, 210, 297, "F")

    def _draw_header(self, title=""):
        """Draw a subtle header bar on non-cover pages."""
        # Header background
        self.set_fill_color(*RGB_CARD)
        self.rect(0, 0, 210, 14, "F")
        # Logo (small, fits inside header)
        if self._logo_path and os.path.exists(self._logo_path):
            self.image(self._logo_path, 6, 2, 22)
        # Title
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*RGB_TW)
        self.set_xy(32, 3)
        self.cell(0, 5, _sanitize(title), ln=False)
        # Date
        self.set_font("Helvetica", "", 7)
        self.set_text_color(*RGB_TD)
        self.set_xy(32, 8)
        self.cell(0, 5, _sanitize(self.report_date), ln=False)
        # Filter context on the right
        if self.filter_context:
            self.set_font("Helvetica", "I", 7)
            self.set_text_color(*RGB_ACCENT)
            self.set_xy(140, 3)
            self.cell(60, 5, _sanitize(self.filter_context), ln=False, align="R")

    def footer(self):
        """FPDF built-in footer — called automatically, never triggers extra pages."""
        self.set_y(-10)
        self.set_font("Helvetica", "", 6)
        self.set_text_color(*RGB_TD)
        self.cell(0, 4, _sanitize(f"Artes para la Paz - Reporte Tactico  |  Pagina {self.page_no()}"), align="C")

    def _draw_card(self, x, y, w, h, border_color=RGB_ACCENT):
        """Draw a rounded card background."""
        self.set_fill_color(*RGB_CARD)
        self.set_draw_color(*border_color)
        self.set_line_width(0.4)
        self.rect(x, y, w, h, "DF")

    def _draw_kpi_card(self, x, y, w, h, label, value, sub, color_rgb, border_top=True):
        """Draw a single KPI card with label, big value, and subtitle."""
        # Card background
        self._draw_card(x, y, w, h, border_color=RGB_BORDER)
        if border_top:
            self.set_draw_color(*color_rgb)
            self.set_line_width(0.8)
            self.line(x, y, x + w, y)
        # Label
        self.set_font("Helvetica", "B", 6)
        self.set_text_color(*color_rgb)
        self.set_xy(x + 4, y + 3)
        self.cell(w - 8, 4, _sanitize(label.upper()), ln=False)
        # Value
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(*RGB_WHITE)
        self.set_xy(x + 4, y + 8)
        self.cell(w - 8, 12, _sanitize(str(value)), ln=False)
        # Subtitle
        self.set_font("Helvetica", "", 6)
        self.set_text_color(*RGB_TD)
        self.set_xy(x + 4, y + 21)
        self.cell(w - 8, 4, _sanitize(sub), ln=False)

    def _draw_progress_bar(self, x, y, w, h, pct, color_rgb):
        """Draw a horizontal progress bar."""
        # Background track
        self.set_fill_color(30, 30, 45)
        self.rect(x, y, w, h, "F")
        # Filled portion
        fill_w = max(w * min(pct, 100) / 100, 0)
        if fill_w > 0:
            self.set_fill_color(*color_rgb)
            self.rect(x, y, fill_w, h, "F")


    # ── PAGE BUILDERS ───────────────────────────────────────────────────────

    def add_cover_page(self, title="TABLERO ESTRATEGICO", subtitle="ARTES PARA LA PAZ"):
        """Page 1: Cover page with logo, title, and date."""
        self.add_page()
        self._draw_bg()

        # Centered content
        cy = 70

        # Logo
        if self._logo_path and os.path.exists(self._logo_path):
            self.image(self._logo_path, 65, cy, 80)
            cy += 50

        # Decorative line (below logo)
        self.set_draw_color(*RGB_ACCENT)
        self.set_line_width(0.3)
        self.line(70, cy, 140, cy)
        cy += 8

        # Title
        self.set_font("Helvetica", "B", 22)
        self.set_text_color(*RGB_WHITE)
        self.set_xy(10, cy)
        self.cell(190, 12, _sanitize(title), align="C")
        cy += 14

        # Subtitle
        self.set_font("Helvetica", "", 14)
        self.set_text_color(*RGB_ACCENT)
        self.set_xy(10, cy)
        self.cell(190, 10, _sanitize(subtitle), align="C")
        cy += 18

        # Command Center label
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*RGB_TD)
        self.set_xy(10, cy)
        self.cell(190, 6, "COMMAND CENTER v4.1 - REPORTE TACTICO", align="C")
        cy += 14

        # Date
        self.set_font("Helvetica", "", 11)
        self.set_text_color(*RGB_CY)
        self.set_xy(10, cy)
        self.cell(190, 8, _sanitize(f"Generado: {self.report_date}"), align="C")
        cy += 12

        # Filter context
        if self.filter_context:
            self.set_font("Helvetica", "I", 10)
            self.set_text_color(*RGB_OR)
            self.set_xy(10, cy)
            self.cell(190, 8, _sanitize(f"Filtro: {self.filter_context}"), align="C")

    def add_kpis_page(self, kpis, extra_cards=None):
        """Page 2: Main KPI cards and secondary info cards."""
        self.add_page()
        self._draw_bg()
        self._draw_header("INDICADORES PRINCIPALES")

        y_start = 24
        # Section title
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*RGB_WHITE)
        self.set_xy(10, y_start)
        self.cell(190, 8, "INDICADORES CLAVE DE DESEMPENO", ln=True)
        y_start += 12

        # 4 KPI cards in a row (2x2 grid)
        card_w = 88
        card_h = 30
        gap = 6

        colors = [RGB_CY, RGB_GN, RGB_MG, RGB_ACCENT]
        for i, kpi in enumerate(kpis[:4]):
            col = i % 2
            row = i // 2
            cx = 12 + col * (card_w + gap)
            cy = y_start + row * (card_h + gap)
            self._draw_kpi_card(cx, cy, card_w, card_h,
                                kpi["label"], kpi["value"], kpi["sub"], colors[i])
            # Progress bar below each card
            pct = kpi.get("pct", 0)
            self._draw_progress_bar(cx + 4, cy + card_h - 5, card_w - 8, 2.5, pct, colors[i])

        y_start += 2 * (card_h + gap) + 10

        # ── Secondary cards section ──
        if extra_cards:
            # Section label
            self.set_font("Helvetica", "B", 9)
            self.set_text_color(*RGB_TD)
            self.set_xy(10, y_start)
            self.cell(190, 6, "METRICAS COMPLEMENTARIAS", ln=True)
            y_start += 8

            sec_w = 58
            sec_h = 32
            for i, card in enumerate(extra_cards[:3]):
                cx = 12 + i * (sec_w + 5)
                self._draw_card(cx, y_start, sec_w, sec_h, border_color=RGB_BORDER)
                # Top border accent
                c_color = card.get("color", RGB_ACCENT)
                self.set_draw_color(*c_color)
                self.set_line_width(0.6)
                self.line(cx, y_start, cx + sec_w, y_start)
                # Label
                self.set_font("Helvetica", "B", 6)
                self.set_text_color(*c_color)
                self.set_xy(cx + 4, y_start + 3)
                self.cell(sec_w - 8, 4, _sanitize(card["label"].upper()), ln=False)
                # Value
                self.set_font("Helvetica", "B", 14)
                self.set_text_color(*RGB_WHITE)
                self.set_xy(cx + 4, y_start + 9)
                self.cell(sec_w - 8, 8, _sanitize(str(card["value"])), ln=False)
                # Subtitle
                self.set_font("Helvetica", "", 6)
                self.set_text_color(*RGB_TD)
                self.set_xy(cx + 4, y_start + 19)
                self.cell(sec_w - 8, 4, _sanitize(card.get("sub", "")), ln=False)

    def add_charts_page(self, nodo_chart_fig=None, radar_chart_fig=None):
        """Page 3: Cobertura por Nodo + Centros de Interés radar."""
        self.add_page()
        self._draw_bg()
        self._draw_header("VISUALIZACIONES")

        y = 24

        # ── Nodo Coverage Chart ──
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*RGB_WHITE)
        self.set_xy(10, y)
        self.cell(190, 6, "COBERTURA POR NODO", ln=True)
        y += 8

        if nodo_chart_fig:
            # Set white text + dark bg for PDF export
            nodo_chart_fig.update_layout(
                paper_bgcolor=BG, plot_bgcolor=BG,
                font=dict(color=TW)
            )
            png = _fig_to_png(nodo_chart_fig, width=900, height=400)
            path = _save_tmp_png(png, "nodo_coverage")
            if path:
                self.image(path, 10, y, 190)
                y += 100
        else:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(*RGB_TD)
            self.set_xy(10, y)
            self.cell(190, 6, "Sin datos de nodo disponibles", ln=True)
            y += 10

        y += 5

        # ── Centros de Interés Radar ──
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*RGB_WHITE)
        self.set_xy(10, y)
        self.cell(190, 6, "CENTROS DE INTERES", ln=True)
        y += 8

        if radar_chart_fig:
            radar_chart_fig.update_layout(
                paper_bgcolor=BG, plot_bgcolor=BG,
                font=dict(color=TW)
            )
            png = _fig_to_png(radar_chart_fig, width=700, height=400)
            path = _save_tmp_png(png, "radar_ci")
            if path:
                self.image(path, 30, y, 150)
        else:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(*RGB_TD)
            self.set_xy(10, y)
            self.cell(190, 6, "Sin datos de radar disponibles", ln=True)

    def add_tablero_page(self, met_summary, tablero_radar_fig=None, tablero_area_fig=None):
        """Page 4: Tablero de Seguimiento metrics."""
        self.add_page()
        self._draw_bg()
        self._draw_header("TABLERO DE SEGUIMIENTO")

        y = 24

        # Section title
        self.set_draw_color(*RGB_OR)
        self.set_line_width(0.8)
        self.line(10, y, 10, y + 10)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*RGB_WHITE)
        self.set_xy(14, y)
        self.cell(180, 6, "TABLERO DE SEGUIMIENTO", ln=True)
        self.set_font("Helvetica", "", 7)
        self.set_text_color(*RGB_TD)
        self.set_xy(14, y + 6)
        self.cell(180, 4, "Metricas Unificadas - Equipos Territoriales 2026", ln=True)
        y += 16

        if met_summary:
            def _safe_fmt(v, default="-"):
                if v is None:
                    return default
                try:
                    f = float(v)
                    return f"{int(f):,}" if f == int(f) else f"{f:,.1f}"
                except:
                    return str(v)

            def _parse_pct(v):
                if v is None:
                    return 0.0
                if isinstance(v, (int, float)):
                    return float(v) * 100 if float(v) < 1 else float(v)
                s = str(v).strip().replace("%", "").replace(",", ".")
                try:
                    f = float(s)
                    return f * 100 if f < 1 and "%" not in str(v) else f
                except:
                    return 0.0

            # KPI cards column (left side)
            kpi_items = [
                ("SEDES ESTIMADAS",    _safe_fmt(met_summary.get("sedes_estimadas")),    "Total",     RGB_OR),
                ("ACUERDOS COB. EST.", _safe_fmt(met_summary.get("acuerdos_estimados")), "Estimados", RGB_OR),
                ("ACUERDOS COBERTURA", _safe_fmt(met_summary.get("acuerdos_cobertura")), "Global",    RGB_CY),
                ("FORMADORES ACTIVOS", _safe_fmt(met_summary.get("formadores_activos")), "Activos",   RGB_GN),
                ("CENTROS INT. PROY.", _safe_fmt(met_summary.get("centros_proyectados")),  "Plazas",  RGB_MG),
            ]

            card_w = 55
            card_h = 20
            for i, (label, value, sub, color) in enumerate(kpi_items):
                cy = y + i * (card_h + 3)
                self._draw_card(12, cy, card_w, card_h, border_color=RGB_BORDER)
                # Left border accent
                self.set_draw_color(*color)
                self.set_line_width(0.6)
                self.line(12, cy, 12, cy + card_h)
                # Label
                self.set_font("Helvetica", "B", 5.5)
                self.set_text_color(*color)
                self.set_xy(16, cy + 2)
                self.cell(card_w - 8, 3, _sanitize(label), ln=False)
                # Value
                self.set_font("Helvetica", "B", 13)
                self.set_text_color(*color)
                self.set_xy(16, cy + 6)
                self.cell(card_w - 8, 8, _sanitize(value), ln=False)
                # Sub
                self.set_font("Helvetica", "", 5)
                self.set_text_color(*RGB_TD)
                self.set_xy(16, cy + 15)
                self.cell(card_w - 8, 3, _sanitize(sub), ln=False)

            # Right side: radar chart + additional metrics
            chart_x = 75
            chart_y = y

            if tablero_radar_fig:
                tablero_radar_fig.update_layout(
                    paper_bgcolor=BG, plot_bgcolor=BG,
                    font=dict(color=TW)
                )
                png = _fig_to_png(tablero_radar_fig, width=600, height=420)
                path = _save_tmp_png(png, "tablero_radar")
                if path:
                    self.image(path, chart_x, chart_y, 125)

            chart_y += 72

            # Right-side extra metrics in cards
            right_metrics = [
                ("BENEF. VALIDADOS",    _safe_fmt(met_summary.get("benef_validados")),    RGB_GN),
                ("ACUERDOS PLAT.",      _safe_fmt(met_summary.get("acuerdos_plataforma")), RGB_MG),
                ("BENEF. PLATAFORMA",   _safe_fmt(met_summary.get("benef_plataforma")),   RGB_CY),
            ]
            rm_w = 38
            rm_h = 20
            for i, (label, value, color) in enumerate(right_metrics):
                rx = chart_x + 5 + i * (rm_w + 3)
                self._draw_card(rx, chart_y, rm_w, rm_h, border_color=RGB_BORDER)
                self.set_draw_color(*color)
                self.set_line_width(0.5)
                self.line(rx, chart_y, rx + rm_w, chart_y)
                self.set_font("Helvetica", "B", 5)
                self.set_text_color(*color)
                self.set_xy(rx + 2, chart_y + 2)
                self.cell(rm_w - 4, 3, _sanitize(label), ln=False)
                self.set_font("Helvetica", "B", 11)
                self.set_text_color(*RGB_WHITE)
                self.set_xy(rx + 2, chart_y + 7)
                self.cell(rm_w - 4, 7, _sanitize(value), ln=False)

            chart_y += rm_h + 5

            # % Acuerdos Cobertura progress bar
            pct_cob = _parse_pct(met_summary.get("pct_cobertura", 0))
            self._draw_card(chart_x + 5, chart_y, 120, 22, border_color=RGB_BORDER)
            self.set_draw_color(*RGB_CY)
            self.set_line_width(0.5)
            self.line(chart_x + 5, chart_y, chart_x + 5, chart_y + 22)
            self.set_font("Helvetica", "B", 5.5)
            self.set_text_color(*RGB_CY)
            self.set_xy(chart_x + 9, chart_y + 2)
            self.cell(110, 3, "% ACUERDOS COBERTURA", ln=False)
            self.set_font("Helvetica", "B", 14)
            self.set_xy(chart_x + 9, chart_y + 6)
            self.cell(50, 8, f"{pct_cob:.1f}%", ln=False)
            self._draw_progress_bar(chart_x + 9, chart_y + 16, 108, 3, pct_cob, RGB_CY)

            # Area chart below KPIs
            if tablero_area_fig:
                area_y = y + 5 * (card_h + 3) + 5
                tablero_area_fig.update_layout(
                    paper_bgcolor=BG, plot_bgcolor=BG,
                    font=dict(color=TW)
                )
                png = _fig_to_png(tablero_area_fig, width=600, height=250)
                path = _save_tmp_png(png, "tablero_area")
                if path:
                    self.image(path, 10, area_y, 120)

        else:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(*RGB_TD)
            self.set_xy(10, y)
            self.cell(190, 6, "Pendiente de conexion con fuente de datos.", ln=True)


    def add_closing_page(self):
        """Page 6: Summary footer with date and attribution."""
        self.add_page()
        self._draw_bg()

        cy = 100

        # Decorative line
        self.set_draw_color(*RGB_ACCENT)
        self.set_line_width(0.3)
        self.line(50, cy, 160, cy)
        cy += 10

        self.set_font("Helvetica", "B", 12)
        self.set_text_color(*RGB_WHITE)
        self.set_xy(10, cy)
        self.cell(190, 8, "FIN DEL REPORTE", align="C")
        cy += 14

        self.set_font("Helvetica", "", 9)
        self.set_text_color(*RGB_TD)
        self.set_xy(10, cy)
        self.cell(190, 6, _sanitize(f"Generado automaticamente el {self.report_date}"), align="C")
        cy += 8

        if self.filter_context:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(*RGB_ACCENT)
            self.set_xy(10, cy)
            self.cell(190, 6, _sanitize(f"Filtro aplicado: {self.filter_context}"), align="C")
            cy += 8

        cy += 6
        self.set_font("Helvetica", "", 7)
        self.set_text_color(*RGB_TD)
        self.set_xy(10, cy)
        self.cell(190, 5, "ARTES PARA LA PAZ - Tablero Estrategico - Command Center v4.1", align="C")
        cy += 5
        self.set_xy(10, cy)
        self.cell(190, 5, "Fuente de datos: Google Sheets (conexion en vivo)", align="C")

        # Logo at bottom
        if self._logo_path and os.path.exists(self._logo_path):
            self.image(self._logo_path, 80, cy + 15, 50)


def generate_pdf_report(data_dict):
    """
    Main entry point: generate a full PDF report.

    Parameters
    ----------
    data_dict : dict with keys:
        - filter_context : str — e.g. "NODO 3 · Manizales"
        - kpis : list of dicts with {label, value, sub, pct}
        - extra_cards : list of dicts with {label, value, sub, color}
        - nodo_chart_fig : plotly Figure or None
        - radar_chart_fig : plotly Figure or None
        - met_summary : dict with tablero metrics
        - tablero_radar_fig : plotly Figure or None
        - tablero_area_fig : plotly Figure or None
    Returns
    -------
    bytes : PDF file content
    """
    ctx = data_dict.get("filter_context", "")
    pdf = ReportPDF(filter_context=ctx)

    # Page 1: Cover
    pdf.add_cover_page()

    # Page 2: KPIs
    pdf.add_kpis_page(
        kpis=data_dict.get("kpis", []),
        extra_cards=data_dict.get("extra_cards", [])
    )

    # Page 3: Charts
    pdf.add_charts_page(
        nodo_chart_fig=data_dict.get("nodo_chart_fig"),
        radar_chart_fig=data_dict.get("radar_chart_fig")
    )

    # Page 4: Tablero de Seguimiento
    pdf.add_tablero_page(
        met_summary=data_dict.get("met_summary", {}),
        tablero_radar_fig=data_dict.get("tablero_radar_fig"),
        tablero_area_fig=data_dict.get("tablero_area_fig")
    )


    # Page 6: Closing
    pdf.add_closing_page()

    return bytes(pdf.output())
