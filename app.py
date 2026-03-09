# ============================================================================
# TABLERO ESTRATÉGICO — ARTES PARA LA PAZ — COMMAND CENTER v4.1
# ============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import pydeck as pdk
import os, glob, re
from streamlit_gsheets import GSheetsConnection
from report_generator import generate_pdf_report

# ── BRAND ───────────────────────────────────────────────────────────────────
ACCENT      = "#886FFF"
BG          = "#080810"
CARD        = "#0f0f1a"
CARD2       = "#12121f"
GLOW        = "rgba(136,111,255,0.15)"
TW          = "#e8e6f0"
TD          = "rgba(232,230,240,0.45)"
BDR         = "rgba(136,111,255,0.18)"
GN          = "#00FF80"
MG          = "#FF0080"
CY          = "#00D4FF"
OR          = "#FF9F1C"
LOGO        = "https://ia903209.us.archive.org/35/items/id-general-textura-blanco/ID_General_Textura_Blanco.png"
META        = 804
TOTAL_EE    = 549
CI_CATS     = ["MÚSICA","DANZA","ESCRITURA CREATIVA","TEATRO","AUDIOVISUAL"]

COORDS = {
    "Manizales":(5.0689,-75.5174),"Villamaria":(5.0427,-75.5124),
    "Chinchina":(4.9833,-75.6061),"Neira":(5.1667,-75.5167),
    "Palestina":(5.0647,-75.6267),"Aranzazu":(5.2667,-75.4833),
    "Salamina":(5.4041,-75.4903),"Filadelfia":(5.2975,-75.5617),
    "Pacora":(5.5289,-75.4614),"Aguadas":(5.6106,-75.4567),
    "La Dorada":(5.4528,-74.6617),"Manzanares":(5.2539,-75.1547),
    "Marquetalia":(5.3000,-75.0614),"Pensilvania":(5.3833,-75.1583),
    "Norcasia":(5.5722,-74.8886),"Samana":(5.4125,-74.9903),
    "Victoria":(5.3197,-74.9367),"Viterbo":(5.0622,-75.8736),
    "Belalcazar":(4.9764,-75.8144),"Risaralda":(5.1500,-75.7667),
    "Anserma":(5.2072,-75.7878),"San Jose":(5.0833,-75.7833),
    "Riosucio":(5.4225,-75.7022),"Supia":(5.4539,-75.6483),
    "Marmato":(5.4833,-75.5972),"La Merced":(5.3167,-75.5500),
    "Pereira":(4.8133,-75.6961),"Dosquebradas":(4.8372,-75.6722),
    "Santa Rosa De Cabal":(4.8694,-75.6219),"Marsella":(4.9386,-75.7383),
    "La Virginia":(4.8994,-75.8828),"Balboa":(4.9208,-75.9483),
    "Santuario":(5.0700,-75.9583),"Apia":(5.1039,-75.9444),
    "Belen De Umbria":(5.2028,-75.8667),"Quinchia":(5.3372,-75.7297),
    "Guatica":(5.3194,-75.7903),"Mistrato":(5.3653,-75.8833),
    "Pueblo Rico":(5.2708,-76.0372),"La Celia":(5.0000,-76.0000),
    "Armenia":(4.5339,-75.6811),"Calarca":(4.5247,-75.6417),
    "Montenegro":(4.5658,-75.7508),"Circasia":(4.6183,-75.6383),
    "La Tebaida":(4.4522,-75.7931),"Quimbaya":(4.6300,-75.7650),
    "Filandia":(4.6747,-75.6597),"Salento":(4.6378,-75.5708),
    "Buenavista":(4.3608,-75.7383),"Cordoba":(4.3958,-75.6833),
    "Genova":(4.2286,-75.7861),"Pijao":(4.3339,-75.7028),
    "Ibagud":(4.4389,-75.2322),"Ibague":(4.4389,-75.2322),
    "Espinal":(4.1486,-74.8842),"Honda":(5.2061,-74.7369),
    "Mariquita":(5.2014,-74.8944),"Flandes":(4.2833,-74.8167),
    "Melgar":(4.2047,-74.6453),"Chaparral":(3.7233,-75.4861),
    "Planadas":(3.1972,-75.6472),"Rioblanco":(3.5333,-75.6500),
    "Ataco":(3.5956,-75.3867),"San Antonio":(3.9333,-75.4833),
    "Ortega":(3.9333,-75.2500),"Coyaima":(3.7969,-75.1969),
    "Natagaima":(3.6250,-75.0972),"Purificacion":(3.8583,-74.9333),
    "Prado":(3.7500,-74.9333),"Dolores":(3.5333,-74.9000),
    "Alpujarra":(3.3833,-74.9833),"Villarrica":(3.6333,-74.5833),
    "Cunday":(4.0833,-74.6833),"Icononzo":(4.1667,-74.5333),
    "Carmen De Apicala":(4.1500,-74.7333),"Suarez":(4.0500,-74.8167),
    "Guamo":(4.0333,-74.9667),"Saldana":(3.9333,-75.0167),
    "San Luis":(3.8333,-75.0833),"Lerida":(4.8667,-74.9167),
    "Ambalema":(4.7833,-74.7667),"Venadillo":(4.6833,-74.9333),
    "Alvarado":(4.5667,-74.9500),"Piedras":(4.5500,-74.8833),
    "Coello":(4.2833,-74.9500),"Cajamarca":(4.4333,-75.4333),
    "Rovira":(4.2333,-75.2333),"Valle De San Juan":(4.2000,-75.1167),
    "San Luis Tolima":(3.8333,-75.0833),"Herveo":(5.0833,-75.1667),
    "Casabianca":(5.0833,-75.1333),"Villahermosa":(5.0167,-75.1167),
    "Murillo":(4.8833,-75.1667),"Libano":(4.9167,-75.0667),
    "Fresno":(5.1500,-75.0333),"Palocabildo":(5.1167,-75.0167),
    "Falan":(5.1333,-74.9500),
    "Bogota D.C.":(4.7110,-74.0721),"Bogota":(4.7110,-74.0721),
    "Soacha":(4.5867,-74.2167),"Zipaquirá":(5.0333,-73.9833),
    "Chia":(4.8667,-74.0500),"Sopó":(4.9000,-73.9500),
    "Cajicá":(4.9167,-74.0333),"Chía":(4.8667,-74.0500),
    "Cali":(3.4516,-76.5320),"Buenaventura":(3.8801,-77.0311),
    "Palmira":(3.5394,-76.3036),"Tulua":(4.0847,-76.2000),
    "Cartago":(4.7464,-75.9117),"Buga":(3.9008,-76.3000),
    "Yumbo":(3.5847,-76.4950),"Jamundi":(3.2611,-76.5406),
    "Candelaria":(3.4075,-76.3497),"Florida":(3.3247,-76.2378),
    "Pradera":(3.4206,-76.2433),"El Cerrito":(3.6833,-76.3167),
    "Dagua":(3.6583,-76.6917),"Vijes":(3.6833,-76.4333),
    "La Cumbre":(3.6500,-76.5667),"Restrepo":(3.8167,-76.5167),
    "Alcala":(4.6750,-75.7833),"Ansermanuevo":(4.7917,-75.8333),
    "El Aguila":(4.9000,-76.0500),"El Cairo":(4.7500,-76.2167),
    "El Dovio":(4.5167,-76.2333),"Roldanillo":(4.4167,-76.1500),
    "Bolivar":(4.3333,-76.2333),"La Union":(4.5333,-76.1000),
    "Toro":(4.6167,-76.0833),"Versalles":(4.5833,-76.1833),
    "Sevilla":(4.2667,-75.9333),"Caicedonia":(4.3167,-75.8333),
    "Andalucia":(4.1667,-76.1667),"Bugalagrande":(4.2167,-76.1500),
    "San Pedro":(3.9833,-76.2333),"Trujillo":(4.2333,-76.3333),
    "Riofrio":(4.1500,-76.2833),"Obando":(4.5833,-75.9833),
    "Ulloa":(4.6833,-75.7500),"Zarzal":(4.3833,-76.0667),
    "Yotoco":(3.8667,-76.3833),"Dos Quebradas":(4.8372,-75.6722)
}

def nkey(t):
    return [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', str(t))]

def _normalize_id(val):
    """Normalize an ID value to a clean string (remove .0, strip whitespace)."""
    if pd.isna(val) or str(val).strip().lower() == 'nan':
        return ""
    s = str(val).strip()
    if s.endswith(".0"):
        s = s[:-2]
    return s

# ── DATA ────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def load_data():
    URL_M = "https://docs.google.com/spreadsheets/d/1KZjWD3be_UWojwc4iW2ldBK9s-7Bi8qt5KDfx96T4Zw/edit?gid=763041618#gid=763041618"
    URL_A = "https://docs.google.com/spreadsheets/d/1KICfAFKO2plg23CbybCGtMkbmg0tsV8lNq5kO4MPPpQ/edit?gid=73107221#gid=73107221"
    URL_AF = "https://docs.google.com/spreadsheets/d/1M86Wf2lGooAglf-GrvF7QcZaJiWXTfKSoxYrStrJ3ak/edit?gid=116204322#gid=116204322"
    URL_MET = "https://docs.google.com/spreadsheets/d/1uABbGRiPuM9Hg6SMQydmtsMLL6j6izBlk7hg0uSetm8/edit?usp=sharing"
    err = None; dm = pd.DataFrame(); da = pd.DataFrame(); df_foc = pd.DataFrame(); df_af = pd.DataFrame(); df_met_raw = pd.DataFrame(); src = "MOCK"
    try:
        # Check if secrets are available without triggering auto-error
        secrets_available = False
        if "connections" in st.secrets:
            if "gsheets" in st.secrets.connections:
                secrets_available = True
        
        if not secrets_available:
            raise Exception("Secrets Missing")
            
        conn = st.connection("gsheets", type=GSheetsConnection)
        try: dm = conn.read(spreadsheet=URL_M, worksheet="DATA_MASTER")
        except:
            try: dm = conn.read(spreadsheet=URL_M)
            except: pass
        try: da = conn.read(spreadsheet=URL_A, worksheet="RESPUESTAS_ASISTENCIA")
        except:
            try: da = conn.read(spreadsheet=URL_A)
            except: pass
        # Load full EE universe from FOCALIZACIONXNODO 2026
        try: df_foc = conn.read(spreadsheet=URL_M, worksheet="FOCALIZACIONXNODO 2026")
        except: pass
        # Load ARTISTAS FORMADORES 2026 (new CONTRATADOS source)
        try: df_af = conn.read(spreadsheet=URL_AF, worksheet="ARTISTAS FORMADORES 2026")
        except:
            try: df_af = conn.read(spreadsheet=URL_AF)
            except: pass
        # Load TABLERO METRICAS UNIFICADAS (placeholder — will use new source later)
        try: df_met_raw = conn.read(spreadsheet=URL_MET, worksheet="TABLERO_METRICAS_UNIFICADAS", header=None)
        except:
            try: df_met_raw = conn.read(spreadsheet=URL_MET, header=None)
            except: pass
        if not dm.empty: src = "LIVE"
    except Exception as e:
        err = str(e)
    if dm.empty:
        csvs = glob.glob(os.path.join(os.path.dirname(__file__), "*.csv"))
        if csvs:
            try: dm = pd.read_csv(csvs[0], encoding="latin-1"); src = "CSV"
            except: pass
    if dm.empty:
        dm = _mock(); src = "MOCK"
    
    # Parse METRICAS UNIFICADAS — 9 macro metrics from rows 6-14
    met_summary = {}
    df_met_nodos = pd.DataFrame()
    if not df_met_raw.empty:
        try:
            # Helper: search for a row containing a label fragment in column 0
            def _find_row(df, label_part):
                for idx in df.index:
                    cell = str(df.at[idx, df.columns[0]])
                    if label_part.lower() in cell.lower():
                        return idx
                return None

            # Helper: safely read a numeric value from a cell
            def _safe_cell(df, row_idx, col_idx):
                if row_idx is None: return None
                try:
                    v = df.at[row_idx, df.columns[col_idx]]
                    if pd.isna(v) or str(v).strip() in ("", "-", "nan"):
                        return None
                    return pd.to_numeric(str(v).replace(",", "").replace("%", "").strip(), errors="coerce")
                except:
                    return None

            # Helper: read raw cell as string (for percentages)
            def _raw_cell(df, row_idx, col_idx):
                if row_idx is None: return None
                try:
                    v = df.at[row_idx, df.columns[col_idx]]
                    if pd.isna(v) or str(v).strip() in ("", "-", "nan"):
                        return None
                    return str(v).strip()
                except:
                    return None

            # Find rows by label text (column A = index 0)
            r_sedes      = _find_row(df_met_raw, "Sedes estimadas")
            r_ac_est     = _find_row(df_met_raw, "Acuerdos cobertura estimados")
            r_ac_cob     = _find_row(df_met_raw, "Acuerdos cobertura (global)")
            r_pct_cob    = _find_row(df_met_raw, "% acuerdos cobertura (global)")
            r_formad     = _find_row(df_met_raw, "Formadores activos")
            r_benef_val  = _find_row(df_met_raw, "Beneficiarios validados")
            r_centros    = _find_row(df_met_raw, "Centros interes proyectados")
            r_acplat     = _find_row(df_met_raw, "Acuerdos cargados plataforma")
            r_benef_plat = _find_row(df_met_raw, "Beneficiarios cargados plataforma")

            # Try reading from both Column C (idx 2) or Column D/G (depending on structure)
            def _get_val(row, default_col=2):
                if row is None: return None
                v = _safe_cell(df_met_raw, row, default_col)
                if v is None and default_col == 2: # Try fallback to col 3 or 4 if col 2 is empty
                     v = _safe_cell(df_met_raw, row, 3) or _safe_cell(df_met_raw, row, 4)
                return v

            met_summary["sedes_estimadas"]      = _get_val(r_sedes, 2)
            met_summary["acuerdos_estimados"]   = _get_val(r_ac_est, 2) or _get_val(r_sedes, 6)
            met_summary["acuerdos_cobertura"]   = _get_val(r_ac_cob, 2)
            met_summary["pct_cobertura"]        = _raw_cell(df_met_raw, r_pct_cob, 2) or _raw_cell(df_met_raw, r_ac_cob, 6)
            met_summary["formadores_activos"]   = _get_val(r_formad, 2)
            met_summary["benef_validados"]      = _get_val(r_benef_val, 2) or _get_val(r_formad, 6)
            met_summary["centros_proyectados"]  = _get_val(r_centros, 2)
            met_summary["acuerdos_plataforma"]  = _get_val(r_acplat, 2)
            met_summary["benef_plataforma"]     = _get_val(r_benef_plat, 2) or _get_val(r_acplat, 6)

            # Clean: remove None entries
            met_summary = {k: v for k, v in met_summary.items() if v is not None}

            # Per-NODO table: find header row containing "ESTIMADOS"
            r_header = _find_row(df_met_raw, "ESTIMADOS")
            if r_header is not None:
                header_iloc = df_met_raw.index.get_loc(r_header)
                nodo_header = df_met_raw.iloc[header_iloc].tolist()
                nodo_data = df_met_raw.iloc[header_iloc+1:].copy()
                nodo_data.columns = nodo_header
                nodo_data = nodo_data.dropna(subset=[nodo_header[0]])
                nodo_data = nodo_data[nodo_data.iloc[:,0].astype(str).str.strip().str.upper().str.startswith("NODO")]
                df_met_nodos = nodo_data.reset_index(drop=True)
        except:
            pass
    
    return _proc(dm, da, df_foc, df_af, src, err, met_summary, df_met_nodos)

def _proc(dm, da, df_foc, df_af, src, err, met_summary=None, df_met_nodos=None):
    dm.columns = dm.columns.str.strip()
    dm = dm.loc[:, ~dm.columns.str.startswith("Unnamed")]

    # ── Process ARTISTAS FORMADORES (new CONTRATADOS source) ──
    # Match by CEDULA: AF has CEDULA + ESTADO CONTRATACIÓN, DM has CEDULA + DANE + EE
    af_contratado_cedulas = set()
    
    def _normalize_id(val):
        """Normalize IDs (CEDULA, DANE) to clean strings (handle int, float, str)."""
        if pd.isna(val): return None
        s = str(val).strip()
        if s.endswith(".0"): s = s[:-2]
        return s if s and s.lower() != "nan" else None

    # ── Extract contratacion summary from raw df_af (before cleanup) ──
    af_contrat_summary = {}
    if not df_af.empty:
        df_af.columns = df_af.columns.str.strip()
        # Scan ALL cells (including Unnamed cols) for summary labels
        all_totals = []  # collect all TOTAL: values found
        for col_idx, col in enumerate(df_af.columns):
            if col_idx + 1 >= len(df_af.columns):
                continue
            next_col = df_af.columns[col_idx + 1]
            for row_idx in df_af.index:
                cell = str(df_af.at[row_idx, col]).strip().upper()
                if "LEGALIZADOS Y DECLINADOS" in cell:
                    try:
                        af_contrat_summary["declinados"] = int(float(df_af.at[row_idx, next_col]))
                    except: pass
                elif "LEGALIZADOS Y CONTRATADOS" in cell:
                    try:
                        af_contrat_summary["legalizados"] = int(float(df_af.at[row_idx, next_col]))
                    except: pass
                elif cell == "TOTAL:":
                    try:
                        v = int(float(df_af.at[row_idx, next_col]))
                        all_totals.append(v)
                    except: pass
        # Compute derived values
        if "legalizados" in af_contrat_summary and "declinados" in af_contrat_summary:
            af_contrat_summary["total_legal"] = af_contrat_summary["legalizados"] + af_contrat_summary["declinados"]
        # Resoluciones = the largest TOTAL: found (695 > 595)
        if all_totals:
            af_contrat_summary["resoluciones"] = max(all_totals)
        # Now clean unnamed columns
        df_af = df_af.loc[:, ~df_af.columns.str.startswith("Unnamed")]
        # Find "Estado CONTRATACIÓN" column (column V)
        af_q_col = None
        for c in df_af.columns:
            if "ESTADO" in c.upper() and "CONTRAT" in c.upper():
                af_q_col = c
                break
        # Find CEDULA column in ARTISTAS FORMADORES
        af_ced_col = None
        for c in df_af.columns:
            if "CEDULA" in c.upper() or "DOCUMENTO" in c.upper() or "IDENTIFICACI" in c.upper():
                af_ced_col = c
                break
        if af_q_col and af_ced_col:
            df_af["AF_CONTRATADO"] = df_af[af_q_col].astype(str).str.strip().str.upper() == "CONTRATADO"
            df_af["_CED_NORM"] = df_af[af_ced_col].apply(_normalize_id)
            af_contratado_cedulas = set(df_af[df_af["AF_CONTRATADO"]]["_CED_NORM"].dropna().unique())

    # ── Determine STATUS in DATA_MASTER ──
    # First: old logic for POSTULANTE (SELECCIONADO)
    if "ESTADO" in dm.columns:
        dm["HAS_M"] = dm["ESTADO"].apply(lambda x: pd.notna(x) and str(x).strip() != "")
    elif "VACANTE" in dm.columns:
        dm["HAS_M"] = dm["VACANTE"].fillna("NO").str.strip().str.upper().apply(lambda x: x != "SI")
    else:
        dm["HAS_M"] = False

    # Find DANE column in DATA_MASTER
    dm_dane_col = None
    for c in dm.columns:
        if "DANE" in c.upper():
            dm_dane_col = c
            break

    # Find CEDULA column in DATA_MASTER
    dm_ced_col = None
    for c in dm.columns:
        if "CEDULA" in c.upper() or "DOCUMENTO" in c.upper() or "IDENTIFICACI" in c.upper():
            dm_ced_col = c
            break

    # NEW: CONTRATADO = CEDULA from DATA_MASTER matches a CONTRATADO CEDULA from AF
    dm["HAS_Q"] = False
    if dm_ced_col and af_contratado_cedulas:
        dm["_CED_NORM"] = dm[dm_ced_col].apply(_normalize_id)
        dm["HAS_Q"] = dm["_CED_NORM"].apply(lambda x: x in af_contratado_cedulas if x else False)

    # Also keep Q_CLEAN from DATA_MASTER for tooltip (En Proceso / Declinado)
    if "ESTADO CONTRATACIÓN" in dm.columns or "ESTADO CONTRATACION" in dm.columns:
        q_col = "ESTADO CONTRATACIÓN" if "ESTADO CONTRATACIÓN" in dm.columns else "ESTADO CONTRATACION"
        dm["Q_CLEAN"] = dm[q_col].astype(str).str.strip().str.upper().replace("NAN","")
    else:
        dm["Q_CLEAN"] = ""

    # Priority: Q (CONTRATADO from AF) > M (SELECCIONADO) > VACANTE
    dm["STATUS"] = "VACANTE"
    dm.loc[dm["HAS_M"], "STATUS"] = "POSTULANTE"
    dm.loc[dm["HAS_Q"], "STATUS"] = "CONTRATADO"
    dm["MUN"] = dm["MUNICIPIO"].astype(str).str.strip().str.title()
    coords = dm["MUN"].map(lambda m: COORDS.get(m, (None, None)))
    dm["LAT"] = coords.apply(lambda x: x[0])
    dm["LON"] = coords.apply(lambda x: x[1])
    # Normalize Centro de Interes
    if "CENTRO DE INTERES" in dm.columns:
        dm["CI"] = dm["CENTRO DE INTERES"].astype(str).str.strip().str.upper()
    else:
        dm["CI"] = "SIN DATO"

    # Process focalizacion data to extract full DANE universe
    if not df_foc.empty:
        df_foc.columns = df_foc.columns.str.strip()
        df_foc = df_foc.loc[:, ~df_foc.columns.str.startswith("Unnamed")]

    if not da.empty:
        da.columns = da.columns.str.strip()
        tcol = next((c for c in da.columns if any(k in c.lower() for k in ["asistentes","estudiantes","beneficiarios"])), None)
        da["Asistentes"] = pd.to_numeric(da[tcol], errors="coerce").fillna(0) if tcol else 1
        # Normalize Fase & Estacionalidad
        if "Fase" in da.columns:
            da["Fase"] = da["Fase"].astype(str).str.strip()
        if "Estacionalidad" in da.columns:
            da["Estacionalidad"] = da["Estacionalidad"].astype(str).str.strip()
        # Centro Interés from attendance
        ci_col = next((c for c in da.columns if "centro" in c.lower() and "inter" in c.lower()), None)
        if ci_col:
            da["CI_ATT"] = da[ci_col].astype(str).str.strip().str.upper()
        
        # Pre-process time for the pulse feed
        if "Marca Temporal" in da.columns:
            da["Marca Temporal"] = pd.to_datetime(da["Marca Temporal"], errors="coerce")
            da = da.sort_values("Marca Temporal", ascending=False)
    return dm, da, df_foc, df_af, src, err, met_summary or {}, df_met_nodos if df_met_nodos is not None else pd.DataFrame(), af_contrat_summary

def _mock(n=300):
    rng = np.random.default_rng(42); ms = list(COORDS.keys())
    return pd.DataFrame([{
        "NODO":f"NODO {rng.integers(1,15)}","MUNICIPIO":rng.choice(ms),
        "EE":f"IE {rng.choice(ms)}","CENTRO DE INTERES":rng.choice(CI_CATS),
        "ESTADO":"OK" if rng.random()>0.3 else np.nan,
        "ESTADO CONTRATACIÓN":"CONTRATADO" if rng.random()>0.6 else np.nan
    } for _ in range(n)])

# ── PLOTLY HELPERS ──────────────────────────────────────────────────────────
def _dark_layout(h=280, **kw):
    d = dict(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=5,r=5,t=10,b=5),height=h,
        font=dict(family="Inter",color=TD,size=11),showlegend=False)
    d.update(kw)
    return d

def gauge_chart(value, total, h=220):
    pct = min(value/total*100, 100) if total else 0
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=pct,
        number={"suffix":"%","font":{"size":28,"color":"#fff","family":"JetBrains Mono"}},
        gauge={
            "axis":{"range":[0,100],"tickwidth":0,"tickcolor":"rgba(0,0,0,0)","dtick":50,
                    "tickfont":{"size":9,"color":TD}},
            "bar":{"color":ACCENT,"thickness":0.7},
            "bgcolor":"rgba(255,255,255,0.03)",
            "borderwidth":0,
            "steps":[
                {"range":[0,50],"color":"rgba(255,0,128,0.08)"},
                {"range":[50,80],"color":"rgba(255,159,28,0.08)"},
                {"range":[80,100],"color":"rgba(0,255,128,0.08)"}
            ],
            "threshold":{"line":{"color":GN,"width":3},"thickness":0.8,"value":100}
        }
    ))
    fig.update_layout(**_dark_layout(h, margin=dict(l=10,r=10,t=30,b=0)))
    return fig

def single_gauge(value, total, color, label, h=160):
    """Single semi-circle gauge with percentage and label."""
    pct = min(value/total*100, 100) if total else 0
    fig = go.Figure(go.Indicator(
        mode="gauge",
        value=pct,
        gauge={
            "axis":{"range":[0,100],"tickwidth":0,"tickcolor":"rgba(0,0,0,0)","dtick":50,
                    "tickfont":{"size":8,"color":TD}},
            "bar":{"color":color,"thickness":0.75},
            "bgcolor":"rgba(255,255,255,0.04)",
            "borderwidth":0,
        }
    ))
    fig.add_annotation(x=0.5, y=0.32,
        text=f"<b>{pct:.1f}%</b>",
        showarrow=False, font=dict(size=22, color=color, family="JetBrains Mono"))
    fig.add_annotation(x=0.5, y=0.12,
        text=label,
        showarrow=False, font=dict(size=9, color=color, family="Inter"))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=15, b=0), height=h, font=dict(family="Inter")
    )
    return fig

def radar_chart(dm_filtered, h=320):
    if dm_filtered.empty:
        return go.Figure()
    
    # Pre-calculate counts efficiently
    ci_series = dm_filtered["CI"].fillna("").str.upper()
    counts = []
    for cat in CI_CATS:
        # Match using first 4 characters to maintain the logic but more efficiently
        pattern = cat[:4].upper()
        counts.append(ci_series.str.contains(pattern, regex=False).sum())
    
    counts.append(counts[0])  # close polygon
    cats = CI_CATS + [CI_CATS[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=counts, theta=cats, fill='toself',
        fillcolor="rgba(136,111,255,0.15)",
        line=dict(color=ACCENT, width=2),
        marker=dict(size=6, color=ACCENT)
    ))
    fig.update_layout(
        **_dark_layout(h),
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, showline=False, gridcolor="rgba(255,255,255,0.06)",
                           tickfont=dict(size=9,color=TD)),
            angularaxis=dict(gridcolor="rgba(255,255,255,0.06)",
                            tickfont=dict(size=10,color=TW))
        )
    )
    return fig

# Patterns that identify ID/code columns (should display as integers, not floats)
_ID_PATTERNS = ["DANE", "CÉDULA", "CEDULA", "CC", "DOCUMENTO", "IDENTIFICACI", "CÓDIGO", "CODIGO", "NIT"]

def _is_id_column(col_name):
    """Check if a column name looks like an ID/code that should be displayed as integer."""
    upper = col_name.strip().upper()
    return any(p in upper for p in _ID_PATTERNS)

def _format_id_value(val):
    """Format an ID value: remove trailing .0 from floats, keep as clean string."""
    if pd.isna(val) or str(val).strip().lower() == 'nan':
        return ""
    s = str(val).strip()
    # Remove trailing .0 (pandas int→float conversion artifact)
    if s.endswith(".0"):
        s = s[:-2]
    return s

def dark_table(df, max_h=350, num_cols=None, color_map=None, id_cols=None):
    """Render a DataFrame as a fully dark HTML table."""
    if df.empty:
        return "<div style='color:rgba(232,230,240,0.45);font-size:.8rem;padding:12px;'>Sin datos disponibles</div>"
    if num_cols is None:
        num_cols = list(df.select_dtypes(include='number').columns)
    if color_map is None:
        color_map = {}
    # Auto-detect ID columns by name pattern + merge with explicit id_cols
    auto_id_cols = {c for c in df.columns if _is_id_column(c)}
    if id_cols:
        auto_id_cols.update(id_cols)
    # ID columns should NOT be treated as numeric (no comma formatting)
    num_cols = [c for c in num_cols if c not in auto_id_cols]

    # Build header
    hdr_parts = []
    for c in df.columns:
        ta = "right" if c in num_cols else "left"
        hdr_parts.append(
            f"<th style='background:{CARD2};color:{TD};padding:10px 14px;"
            f"font-size:.7rem;text-transform:uppercase;letter-spacing:1px;"
            f"border-bottom:1px solid {BDR};text-align:{ta};white-space:nowrap;'>{c}</th>"
        )
    hdr = "".join(hdr_parts)

    # Build rows
    rows = ""
    for _, row in df.iterrows():
        cells = ""
        for c in df.columns:
            val = row[c]
            is_num = c in num_cols
            is_id = c in auto_id_cols
            clr = color_map.get(c, GN if is_num else TW)
            align = "right" if is_num else "left"
            if is_id:
                display = _format_id_value(val)
                fw = "600"
            elif is_num and pd.notna(val):
                display = f"{val:,.0f}"
                fw = "700"
            else:
                display = str(val) if pd.notna(val) and str(val).lower() != 'nan' else ""
                fw = "400"
            
            cells += (
                f"<td style='padding:10px 14px;border-bottom:1px solid rgba(255,255,255,0.04);"
                f"color:{clr};text-align:{align};font-size:.82rem;font-weight:{fw};"
                f"white-space:nowrap;'>{display}</td>"
            )
        rows += (
            f"<tr class='dt-row'>{cells}</tr>"
        )

    return (
        f"<div style='max-height:{max_h}px;overflow-y:auto;border:1px solid {BDR};"
        f"border-radius:12px;background:{CARD};'>"
        f"<table style='width:100%;border-collapse:collapse;'>"
        f"<thead style='position:sticky;top:0;z-index:1;'><tr>{hdr}</tr></thead>"
        f"<tbody>{rows}</tbody>"
        f"</table></div>"
    )


# ── CSS ─────────────────────────────────────────────────────────────────────
def inject_css():
    st.markdown(f"""<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap');

    header,#MainMenu,footer {{visibility:hidden;}}
    html,body,[class*="css"] {{font-family:'Inter',sans-serif!important;color:{TW}!important;}}
    .stApp {{background:{BG}!important;}}
    .block-container {{padding:1.2rem 2rem 2rem 2rem!important;max-width:100%!important;}}

    /* Sidebar */
    section[data-testid="stSidebar"] {{background:{BG}!important;border-right:1px solid {BDR};}}
    section[data-testid="stSidebar"] * {{color:{TW}!important;}}

    /* Selectbox */
    div[data-testid="stSelectbox"] [data-baseweb="select"] {{
        background-color:{CARD}!important;border:1px solid {BDR}!important;border-radius:12px!important;color:{TW}!important;
    }}
    div[data-testid="stSelectbox"] [data-baseweb="select"]:hover {{border-color:{ACCENT}!important;}}
    div[data-testid="stSelectbox"] [data-baseweb="select"] > div {{
        background-color:transparent!important;color:{TW}!important;border:none!important;
    }}
    div[data-testid="stSelectbox"] [data-baseweb="select"] svg {{fill:{TW}!important;}}
    ul[data-testid="stSelectboxVirtualDropdown"] {{background-color:{CARD}!important;border:1px solid {BDR}!important;}}
    ul[data-testid="stSelectboxVirtualDropdown"] li {{color:{TW}!important;transition:background-color 0.2s;}}
    ul[data-testid="stSelectboxVirtualDropdown"] li:hover {{background-color:{GLOW}!important;}}

    /* Scrollbar */
    ::-webkit-scrollbar {{width:5px;}} ::-webkit-scrollbar-track {{background:transparent;}} ::-webkit-scrollbar-thumb {{background:{BDR};border-radius:3px;}}

    /* Sidebar: no scroll */
    section[data-testid="stSidebar"] > div {{overflow:hidden;}}

    /* Cards */
    .dc {{background:{CARD};border:1px solid {BDR};border-radius:16px;padding:22px;transition:all .2s;}}
    .dc:hover {{border-color:{ACCENT};box-shadow:0 0 20px {GLOW};}}
    .dc-sm {{background:{CARD};border:1px solid {BDR};border-radius:12px;padding:16px;transition:all .2s;}}

    .kl {{font-size:.7rem;text-transform:uppercase;letter-spacing:1.5px;color:{TD};font-weight:600;}}
    .kv {{font-family:'JetBrains Mono';font-weight:800;line-height:1;color:#fff;}}

    /* Pulse Carousel */
    .pulse-wrap {{height:480px;overflow:hidden;position:relative;
        mask-image:linear-gradient(to bottom,transparent 0%,black 6%,black 94%,transparent 100%);
        -webkit-mask-image:linear-gradient(to bottom,transparent 0%,black 6%,black 94%,transparent 100%);}}
    .pulse-track {{display:flex;flex-direction:column;gap:10px;animation:scrollUp 120s linear infinite;}}
    .pulse-track:hover {{animation-play-state:paused;}}
    @keyframes scrollUp {{0%{{transform:translateY(0)}}100%{{transform:translateY(-50%)}}}}
    .pc {{background:{CARD2};border-left:3px solid {ACCENT};padding:12px 14px;border-radius:6px;flex-shrink:0;transition:background .2s;display:flex;align-items:flex-start;justify-content:space-between;gap:8px;}}
    .pc:hover {{background:rgba(136,111,255,0.08);}}
    .pc-body {{flex:1;min-width:0;}}
    .pc-t {{font-size:.62rem;color:{TD};margin-bottom:3px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}}
    .pc-e {{font-size:.8rem;font-weight:700;color:#fff;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}}
    .pc-l {{font-size:.7rem;color:{TD};}}
    .pc-n {{font-family:'JetBrains Mono';font-weight:700;font-size:.9rem;white-space:nowrap;flex-shrink:0;text-align:right;padding-top:2px;}}
    .pc-ng {{color:{GN};}} .pc-badge {{display:inline-block;font-size:.6rem;color:{ACCENT};border:1px solid {ACCENT};padding:1px 7px;border-radius:4px;font-weight:600;}}

    /* Status */
    .dot {{width:8px;height:8px;border-radius:50%;display:inline-block;margin-right:8px;}}
    .dot-g {{background:{GN};box-shadow:0 0 8px {GN};animation:blink 2s infinite;}}
    .dot-x {{background:#555;}}
    @keyframes blink {{0%{{opacity:1}}50%{{opacity:.35}}100%{{opacity:1}}}}

    /* Dark table scrollbar inside containers */
    div[style*="overflow-y"] {{scrollbar-width:thin;scrollbar-color:{BDR} transparent;}}

    /* Expander */
    details, .streamlit-expanderHeader {{background:{CARD}!important;border:1px solid {BDR}!important;border-radius:12px!important;color:{TW}!important;}}
    summary span {{color:{TW}!important;}}

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{background:transparent!important;border-bottom:1px solid {BDR}!important;}}
    .stTabs [data-baseweb="tab"] {{color:{TD}!important;font-weight:500;}}
    .stTabs [aria-selected="true"] {{color:{ACCENT}!important;border-bottom:2px solid {ACCENT}!important;}}
    .stTabs [data-baseweb="tab-panel"] {{background:transparent!important;}}

    /* Dialog/Modal Dark Theme */
    div[role="dialog"] {{background:{BG}!important;border:1px solid {BDR}!important;border-radius:16px!important;color:{TW}!important;}}
    div[role="dialog"] button[kind="secondary"] {{color:{TW}!important;}}
    div[data-testid="stModal"] > div {{background:rgba(0,0,0,0.75)!important;}}

    /* Dark table hover */
    .dt-row {{transition:background .15s;}}
    .dt-row:hover {{background:rgba(136,111,255,0.08)!important;}}

    /* Text input in dialogs */
    div[role="dialog"] input {{background:{CARD}!important;color:{TW}!important;border:1px solid {BDR}!important;border-radius:8px!important;}}

    /* Beneficiarios Validados — compact accent card */
    .kpi-benef {{
        background: linear-gradient(135deg, rgba(0,255,128,0.07) 0%, {CARD} 60%);
        border: 1px solid rgba(0,255,128,0.30);
        border-left: 3px solid {GN};
        border-radius: 12px;
        padding: 14px 16px;
        margin-bottom: 8px;
        position: relative;
        overflow: hidden;
        transition: all .25s ease;
    }}
    .kpi-benef:hover {{
        border-color: {GN};
        box-shadow: 0 0 18px rgba(0,255,128,0.15);
    }}
    .kpi-benef::after {{
        content: '👥';
        position: absolute;
        right: 10px; top: 50%; transform: translateY(-50%);
        font-size: 1.6rem; opacity: 0.10;
    }}
    @keyframes kpiBenefPulse {{
        0%   {{ box-shadow: 0 0 0 0 rgba(0,255,128,0.5); }}
        70%  {{ box-shadow: 0 0 0 5px rgba(0,255,128,0); }}
        100% {{ box-shadow: 0 0 0 0 rgba(0,255,128,0); }}
    }}
    .kpi-benef-dot {{
        width: 7px; height: 7px; border-radius: 50%;
        background: {GN}; display: inline-block;
        animation: kpiBenefPulse 2s infinite;
        margin-right: 5px; vertical-align: middle;
    }}

    /* Details/Summary expandable */
    details summary {{-webkit-appearance:none;}}
    details summary::-webkit-details-marker {{display:none;}}
    details[open] summary .expand-icon {{transform:rotate(90deg);}}
    details summary:hover {{opacity:0.85;}}
    </style>""", unsafe_allow_html=True)


# ── DIALOGS ─────────────────────────────────────────────────────────────────
@st.dialog("✅ Detalle de Contratados", width="large")
def show_detail_contratados(mf_data, df_af_filtered=None):
    # Use ARTISTAS FORMADORES as primary source (same as the metric card)
    # Fall back to DATA_MASTER cross-reference if AF data is not available
    use_af = (df_af_filtered is not None and not df_af_filtered.empty
              and "AF_CONTRATADO" in df_af_filtered.columns)

    if use_af:
        contr_df = df_af_filtered[df_af_filtered["AF_CONTRATADO"]].copy()
    else:
        contr_df = mf_data[mf_data["STATUS"]=="CONTRATADO"]

    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown(f"<div class='kl' style='margin-bottom:8px;color:{GN};'>LISTADO COMPLETO — {len(contr_df)} CONTRATADOS</div>", unsafe_allow_html=True)
    with c2:
        search = st.text_input("🔍", placeholder="Buscar", label_visibility="collapsed", key="search_contr")

    if not contr_df.empty:
        if use_af:
            # Detect best columns from ARTISTAS FORMADORES
            af_ee_col = next((c for c in contr_df.columns if c.strip().upper() == "EE"
                              or "ESTABLECIMIENTO" in c.upper()
                              or ("NOMBRE" in c.upper() and "EE" in c.upper())), None)
            af_dane_col = next((c for c in contr_df.columns if "DANE" in c.upper()), None)
            af_mun_col = next((c for c in contr_df.columns if c.strip().upper() == "MUNICIPIO"), None)
            af_nodo_col = next((c for c in contr_df.columns if c.strip().upper() == "NODO"
                                or c.strip().upper().startswith("NODO")), None)
            af_ci_col = next((c for c in contr_df.columns if "CENTRO" in c.upper()
                              and "INTER" in c.upper()), None)
            af_ced_col = next((c for c in contr_df.columns if "CEDULA" in c.upper()
                               or "DOCUMENTO" in c.upper()
                               or "IDENTIFICACI" in c.upper()), None)

            # If AF doesn't have EE column, enrich from DATA_MASTER via cédula
            if not af_ee_col and af_ced_col:
                dm_ced_col = next((c for c in mf_data.columns if "CEDULA" in c.upper()
                                   or "DOCUMENTO" in c.upper()
                                   or "IDENTIFICACI" in c.upper()), None)
                if dm_ced_col and "EE" in mf_data.columns:
                    contr_df["_CED_JOIN"] = contr_df[af_ced_col].apply(_normalize_id)
                    dm_lookup = mf_data[[dm_ced_col, "EE"]].copy()
                    dm_lookup["_CED_JOIN"] = dm_lookup[dm_ced_col].apply(_normalize_id)
                    dm_lookup = dm_lookup.drop_duplicates(subset=["_CED_JOIN"])
                    contr_df = contr_df.merge(dm_lookup[["_CED_JOIN", "EE"]], on="_CED_JOIN", how="left")
                    contr_df.drop(columns=["_CED_JOIN"], inplace=True)
                    af_ee_col = "EE"

            # If AF doesn't have DANE column, enrich from DATA_MASTER via cédula
            if not af_dane_col and af_ced_col:
                dm_ced_col = next((c for c in mf_data.columns if "CEDULA" in c.upper()
                                   or "DOCUMENTO" in c.upper()
                                   or "IDENTIFICACI" in c.upper()), None)
                dm_dane_col_local = next((c for c in mf_data.columns if "DANE" in c.upper()), None)
                if dm_ced_col and dm_dane_col_local:
                    if "_CED_JOIN" not in contr_df.columns:
                        contr_df["_CED_JOIN"] = contr_df[af_ced_col].apply(_normalize_id)
                    dm_lookup2 = mf_data[[dm_ced_col, dm_dane_col_local]].copy()
                    dm_lookup2["_CED_JOIN"] = dm_lookup2[dm_ced_col].apply(_normalize_id)
                    dm_lookup2 = dm_lookup2.drop_duplicates(subset=["_CED_JOIN"])
                    dm_lookup2 = dm_lookup2.rename(columns={dm_dane_col_local: "DANE"})
                    contr_df = contr_df.merge(dm_lookup2[["_CED_JOIN", "DANE"]], on="_CED_JOIN", how="left")
                    if "_CED_JOIN" in contr_df.columns:
                        contr_df.drop(columns=["_CED_JOIN"], inplace=True)
                    af_dane_col = "DANE"

            cols_show = []
            rename_map = {}
            if af_ced_col:
                cols_show.append(af_ced_col)
                rename_map[af_ced_col] = "CÉDULA"
            if af_ee_col:
                cols_show.append(af_ee_col)
                rename_map[af_ee_col] = "EE"
            if af_dane_col:
                cols_show.append(af_dane_col)
                rename_map[af_dane_col] = "DANE"
            if af_mun_col:
                cols_show.append(af_mun_col)
                rename_map[af_mun_col] = "MUNICIPIO"
            if af_nodo_col:
                cols_show.append(af_nodo_col)
                rename_map[af_nodo_col] = "NODO"
            if af_ci_col:
                cols_show.append(af_ci_col)
                rename_map[af_ci_col] = "CENTRO INTERÉS"

            if not cols_show:
                # Fallback: show all non-internal columns
                cols_show = [c for c in contr_df.columns
                             if not c.startswith("_") and c != "AF_CONTRATADO"]

            tbl = contr_df[cols_show].copy()
            tbl = tbl.rename(columns=rename_map)
        else:
            cols_show = ["EE","MUNICIPIO","NODO","CI"]
            cols_show = [c for c in cols_show if c in contr_df.columns]
            tbl = contr_df[cols_show].copy()
            tbl.columns = [c.replace("CI","CENTRO INTERÉS") for c in tbl.columns]

        if search:
            mask = tbl.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)
            tbl = tbl[mask]

        st.markdown(dark_table(tbl, max_h=500, num_cols=[],
            color_map={"EE":"#fff","CÉDULA":GN,"DANE":ACCENT,"MUNICIPIO":TD,"NODO":ACCENT,"CENTRO INTERÉS":GN}), unsafe_allow_html=True)
        st.caption(f"Mostrando {len(tbl)} registros")
    else:
        st.info("No hay contratados aún.")

@st.dialog("🏫 Detalle de EE Impactados", width="large")
def show_detail_ee_impactados(mf_data, df_foc=None):
    """Show list of EE that have at least one CONTRATADO."""
    dane_col = None
    for c in mf_data.columns:
        if "DANE" in c.upper():
            dane_col = c
            break
    
    c1, c2 = st.columns([2, 1])
    with c2:
        search = st.text_input("�", placeholder="Buscar", label_visibility="collapsed", key="search_ee_imp")
    
    if dane_col:
        def _nd(v):
            if pd.isna(v): return None
            s = str(v).strip()
            if s.endswith(".0"): s = s[:-2]
            return s if s and s.lower() != "nan" else None
        impactados_df = mf_data[mf_data["HAS_M"] == True]
        covered_danes = set(impactados_df[dane_col].dropna().apply(_nd).dropna().unique())
        
        # Use FOCALIZACION if available to get EE details
        foc_dane_col = None
        if df_foc is not None and not df_foc.empty:
            for c in df_foc.columns:
                if "DANE" in c.upper():
                    foc_dane_col = c
                    break
        
        if foc_dane_col:
            df_foc["_DANE_NORM"] = df_foc[foc_dane_col].apply(_nd)
            ee_df = df_foc[df_foc["_DANE_NORM"].isin(covered_danes)].drop_duplicates(subset=[foc_dane_col])
        else:
            ee_df = mf_data[mf_data[dane_col].isin(covered_danes)].drop_duplicates(subset=[dane_col])
        
        with c1:
            st.markdown(f"<div class='kl' style='margin-bottom:8px;color:{ACCENT};'>EE IMPACTADOS — {len(ee_df)} ESTABLECIMIENTOS</div>", unsafe_allow_html=True)
        
        if not ee_df.empty:
            show_dane = foc_dane_col if foc_dane_col else dane_col
            ee_col = next((c for c in ee_df.columns if "NOMBRE" in c.upper() or (c.upper() == "EE")), None)
            mun_col = next((c for c in ee_df.columns if c.strip().upper() == "MUNICIPIO"), None)
            nodo_col = next((c for c in ee_df.columns if c.strip().upper() == "NODO" or c.strip().upper().startswith("NODO")), None)
            ci_col_e = next((c for c in ee_df.columns if "CENTRO" in c.upper() and "INTER" in c.upper()), None)
            
            cols_show = [show_dane]
            if ee_col: cols_show.append(ee_col)
            if mun_col: cols_show.append(mun_col)
            if nodo_col: cols_show.append(nodo_col)
            if ci_col_e: cols_show.append(ci_col_e)
            cols_show = [c for c in cols_show if c in ee_df.columns]
            
            tbl = ee_df[cols_show].copy()
            tbl.columns = [c.upper().replace("CÓDIGO DANE","DANE").replace("CODIGO DANE","DANE")[:15] for c in tbl.columns]
            if search:
                mask = tbl.apply(lambda r: r.astype(str).str.contains(search, case=False, na=False).any(), axis=1)
                tbl = tbl[mask]
            st.markdown(dark_table(tbl, max_h=450, color_map={
                tbl.columns[0]: ACCENT,
            }), unsafe_allow_html=True)
            st.caption(f"Mostrando {len(tbl)} registros")
        else:
            st.info("No hay EE impactados aún.")
    else:
        st.warning("No se encontró columna DANE.")

@st.dialog("�🚨 Detalle de Vacantes Críticas", width="large")
def show_detail_vacantes(mf_data, df_foc=None):
    # Vacantes críticas: DANE codes from FOCALIZACION that have NO CONTRATADO in DATA_MASTER
    dane_col = None
    for c in mf_data.columns:
        if "DANE" in c.upper():
            dane_col = c
            break
    
    c1, c2 = st.columns([2, 1])
    with c2:
        search = st.text_input("🔍", placeholder="Buscar", label_visibility="collapsed", key="search_vac")

    if dane_col:
        # Covered = DANE codes where ESTADO is not empty (HAS_M = True)
        def _nd(v):
            if pd.isna(v): return None
            s = str(v).strip()
            if s.endswith(".0"): s = s[:-2]
            return s if s and s.lower() != "nan" else None
        impactados_df = mf_data[mf_data["HAS_M"] == True]
        covered_danes = set(impactados_df[dane_col].dropna().apply(_nd).dropna().unique())
        
        # Use FOCALIZACION as full universe if available
        foc_dane_col = None
        if df_foc is not None and not df_foc.empty:
            for c in df_foc.columns:
                if "DANE" in c.upper():
                    foc_dane_col = c
                    break
        
        if foc_dane_col:
            all_foc_danes = set(df_foc[foc_dane_col].dropna().apply(_nd).dropna().unique())
            uncovered_danes = all_foc_danes - covered_danes
            # Build table from FOCALIZACION sheet for uncovered EE
            df_foc["_DANE_NORM"] = df_foc[foc_dane_col].apply(_nd)
            vac_df = df_foc[df_foc["_DANE_NORM"].isin(uncovered_danes)].drop_duplicates(subset=[foc_dane_col])
        else:
            # Fallback to DATA_MASTER
            all_danes = mf_data[dane_col].dropna().unique()
            uncovered_danes = [d for d in all_danes if d not in covered_danes]
            vac_df = mf_data[mf_data[dane_col].isin(uncovered_danes)].drop_duplicates(subset=[dane_col])
        
        with c1:
            st.markdown(f"<div class='kl' style='margin-bottom:8px;color:{MG};'>EE CON VACANTES — {len(vac_df)} VACANTES CRÍTICAS</div>", unsafe_allow_html=True)

        if not vac_df.empty:
            # Find best columns to show
            show_dane = foc_dane_col if foc_dane_col else dane_col
            # Try to find EE name and location columns
            ee_col = next((c for c in vac_df.columns if "NOMBRE" in c.upper() or (c.upper() == "EE")), None)
            # Prefer exact MUNICIPIO, exclude CÓDIGO MUNICIPIO
            mun_col = next((c for c in vac_df.columns if c.strip().upper() == "MUNICIPIO"), None)
            if not mun_col:
                mun_col = next((c for c in vac_df.columns if "MUNICIPIO" in c.upper() and "CÓDIGO" not in c.upper() and "CODIGO" not in c.upper()), None)
            nodo_col = next((c for c in vac_df.columns if c.strip().upper() == "NODO" or c.strip().upper().startswith("NODO")), None)
            ci_col_v = next((c for c in vac_df.columns if "CENTRO" in c.upper() and "INTER" in c.upper()), None)
            
            cols_show = [show_dane]
            if ee_col: cols_show.append(ee_col)
            if mun_col: cols_show.append(mun_col)
            if nodo_col: cols_show.append(nodo_col)
            if ci_col_v: cols_show.append(ci_col_v)
            cols_show = [c for c in cols_show if c in vac_df.columns]
            tbl = vac_df[cols_show].copy()
            
            if search:
                mask = tbl.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)
                tbl = tbl[mask]

            color_map = {}
            if show_dane in tbl.columns: color_map[show_dane] = MG
            if ee_col and ee_col in tbl.columns: color_map[ee_col] = "#fff"
            if mun_col and mun_col in tbl.columns: color_map[mun_col] = TD
            if nodo_col and nodo_col in tbl.columns: color_map[nodo_col] = ACCENT
            if ci_col_v and ci_col_v in tbl.columns: color_map[ci_col_v] = CY
            
            st.markdown(dark_table(tbl, max_h=500, num_cols=[], color_map=color_map), unsafe_allow_html=True)
            st.caption(f"Mostrando {len(tbl)} registros")
        else:
            st.success("¡Todas las EE tienen AF contratado! 🎉")
    else:
        with c1:
            st.markdown(f"<div class='kl' style='margin-bottom:8px;color:{MG};'>VACANTES CRÍTICAS</div>", unsafe_allow_html=True)
        st.warning("Columna CODIGO DANE no encontrada")

@st.dialog("📋 Detalle de Seleccionados", width="large")
def show_detail_postulantes(mf_data):
    post_df = mf_data[mf_data["STATUS"]=="POSTULANTE"]
    
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown(f"<div class='kl' style='margin-bottom:8px;color:{CY};'>LISTADO COMPLETO — {len(post_df)} SELECCIONADOS</div>", unsafe_allow_html=True)
    with c2:
        search = st.text_input("🔍", placeholder="Buscar", label_visibility="collapsed", key="search_post")

    if not post_df.empty:
        cols_show = ["EE","MUNICIPIO","NODO","CI"]
        cols_show = [c for c in cols_show if c in post_df.columns]
        tbl = post_df[cols_show].copy()
        tbl.columns = [c.replace("CI","CENTRO INTERÉS") for c in tbl.columns]
        
        if search:
            mask = tbl.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)
            tbl = tbl[mask]

        st.markdown(dark_table(tbl, max_h=500, num_cols=[],
            color_map={"EE":"#fff","MUNICIPIO":TD,"NODO":ACCENT,"CENTRO INTERÉS":CY}), unsafe_allow_html=True)
        st.caption(f"Mostrando {len(tbl)} registros")
    else:
        st.info("No hay seleccionados aún.")

# ── CHART: Nodo Coverage ────────────────────────────────────────────────────
def nodo_coverage_chart(dm_filtered, h=300):
    """Horizontal stacked bar: Seleccionados / Contratados / Vacantes per Nodo."""
    if "NODO" not in dm_filtered.columns or dm_filtered.empty:
        return None
    nd = dm_filtered.groupby("NODO").agg(
        Postulantes=("STATUS", lambda x: (x=="POSTULANTE").sum()),
        Contratados=("STATUS", lambda x: (x=="CONTRATADO").sum()),
        Vacantes=("STATUS", lambda x: (x=="VACANTE").sum())
    ).reset_index()
    nd["_n"] = nd["NODO"].apply(lambda x: int(re.search(r'\d+', str(x)).group()) if re.search(r'\d+', str(x)) else 0)
    nd = nd.sort_values("_n", ascending=True).drop(columns="_n")
    fig = go.Figure()
    fig.add_trace(go.Bar(y=nd["NODO"], x=nd["Contratados"], name="Contratados",
        orientation="h", marker_color=GN, text=nd["Contratados"],
        textposition="inside", textfont=dict(size=10, color="#111")))
    fig.add_trace(go.Bar(y=nd["NODO"], x=nd["Postulantes"], name="Seleccionados",
        orientation="h", marker_color=CY, text=nd["Postulantes"],
        textposition="inside", textfont=dict(size=10, color="#fff")))
    fig.add_trace(go.Bar(y=nd["NODO"], x=nd["Vacantes"], name="Vacantes",
        orientation="h", marker_color=MG, text=nd["Vacantes"],
        textposition="inside", textfont=dict(size=10, color="#fff")))
    fig.update_layout(
        **_dark_layout(h, margin=dict(l=5, r=10, t=10, b=5), showlegend=True),
        barmode="stack",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                    font=dict(size=11, color=TW), bgcolor="rgba(0,0,0,0)"),
        yaxis=dict(showgrid=False, tickfont=dict(size=10, color=TW)),
        xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", title=None,
                   tickfont=dict(size=9, color=TD))
    )
    return fig


# ── MAIN ────────────────────────────────────────────────────────────────────
def main():
    # SVG icon for a chart to avoid twemoji external fetches
    ICON_SVG = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0naHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmcnIHZpZXdCb3g9JzAgMCAyNCAyNCcgZmlsbD0nIzg4NkZGRic+PHBhdGggZD0nTTMuNSAxOC40OWw2LTYuMDEgNCA0TDIyIDYuOTJsLTEuNDEtMS40MS03LjA5IDcuOTctNC00TDIgMTcuMDhsMS41IDEuNDF6Jy8+PC9zdmc+"
    st.set_page_config(page_title="Artes Dashboard v4.1", layout="wide", page_icon=ICON_SVG)
    inject_css()

    # ── AUTHENTICATION GATE ─────────────────────────────────────────────────
    import hashlib, hmac

    def _check_credentials(user, pwd):
        """Verify credentials against hashed values in secrets (timing-safe)."""
        try:
            expected_user = st.secrets["auth"]["username"]
            expected_hash = st.secrets["auth"]["password_hash"]
        except Exception:
            return False
        user_ok = hmac.compare_digest(user.strip(), expected_user)
        pwd_hash = hashlib.sha256(pwd.encode()).hexdigest()
        pwd_ok = hmac.compare_digest(pwd_hash, expected_hash)
        return user_ok and pwd_ok

    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        # ── Hide sidebar on login screen ──
        st.markdown("""<style>
            section[data-testid="stSidebar"] { display: none; }
            header { visibility: hidden; }
        </style>""", unsafe_allow_html=True)

        # ── Centered Login Card ──
        st.markdown("<div style='height: 60px'></div>", unsafe_allow_html=True)
        col_l, col_c, col_r = st.columns([1.2, 2, 1.2])
        with col_c:
            st.markdown(f"""<div style='text-align:center;margin-bottom:24px;'>
                <img src="{LOGO}" width="220" style="margin-bottom:18px;"/>
                <div style='font-size:.78rem;color:{TD};letter-spacing:1.5px;
                    text-transform:uppercase;'>ACCESO RESTRINGIDO</div>
            </div>""", unsafe_allow_html=True)

            # Decorative line
            st.markdown(f"<div style='width:60%;margin:0 auto 28px auto;height:1px;"
                        f"background:linear-gradient(90deg,transparent,{ACCENT},transparent);'></div>",
                        unsafe_allow_html=True)

            with st.form("login_form"):
                user_input = st.text_input("Usuario", placeholder="Ingresa tu usuario")
                pwd_input = st.text_input("Contraseña", type="password", placeholder="Ingresa tu contraseña")
                # Ensure the button is independent and clearly visible to the runner
                submit = st.form_submit_button("🔐  Iniciar Sesión", use_container_width=True, type="primary")

            if submit:
                if _check_credentials(user_input, pwd_input):
                    st.session_state["authenticated"] = True
                    st.rerun()
                else:
                    st.error("❌ Usuario o contraseña incorrectos", icon="🔒")

            st.markdown(f"<div style='text-align:center;margin-top:20px;font-size:.65rem;"
                        f"color:{TD};letter-spacing:1px;'>ARTES PARA LA PAZ — TABLERO ESTRATÉGICO</div>",
                        unsafe_allow_html=True)
        st.stop()

    # ── LOGOUT BUTTON (will be placed in sidebar later) ──
    dm, da, df_foc, df_af, src, err, met_summary, df_met_nodos, af_contrat_summary = load_data()

    # ── SIDEBAR ──
    with st.sidebar:
        st.image(LOGO, width=170)
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        dot = "dot-g" if src=="LIVE" else "dot-x"
        st.markdown(f"""<div class='dc-sm' style='display:flex;align-items:center;gap:10px;'>
            <span class='dot {dot}'></span><span style='font-size:.8rem;font-weight:700;'>{src} MODE</span>
        </div>""", unsafe_allow_html=True)
        if err: st.error(err, icon="⚠️")
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"<div class='kl'>FILTROS TÁCTICOS</div>", unsafe_allow_html=True)

        nodos = ["📍 Todos los Nodos"] + sorted(dm["NODO"].dropna().unique().astype(str).tolist(), key=nkey)
        sel_n = st.selectbox("NODO", nodos, label_visibility="collapsed")
        mf = dm.copy(); af = da.copy()
        if sel_n != "📍 Todos los Nodos":
            mf = mf[mf["NODO"]==sel_n]
            if not af.empty and "Nodo" in af.columns:
                af = af[af["Nodo"].astype(str).str.strip().str.upper()==sel_n.strip().upper()]

        muns = ["Todos los Municipios"] + sorted(mf["MUNICIPIO"].dropna().unique().tolist())
        sel_m = st.selectbox("MUNICIPIO", muns, label_visibility="collapsed")
        if sel_m != "Todos los Municipios":
            mf = mf[mf["MUNICIPIO"]==sel_m]

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Actualizar Datos", use_container_width=True, type="primary"):
            st.cache_data.clear()
            # Also clear cached PDF so it regenerates with fresh data
            for k in list(st.session_state.keys()):
                if k.startswith("_pdf_cache_"):
                    del st.session_state[k]
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        # Report download button placeholder — filled at end of main() after all data is ready
        report_placeholder = st.empty()

        # ── LOGOUT ──
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("🚪 Cerrar Sesión", use_container_width=True):
            st.session_state["authenticated"] = False
            for k in list(st.session_state.keys()):
                if k.startswith("_pdf_cache_"):
                    del st.session_state[k]
            st.rerun()
    # ── METRICS ──
    post  = len(mf[mf["STATUS"]=="POSTULANTE"])

    # CONTRATADOS count comes directly from ARTISTAS FORMADORES (source of truth)
    if not df_af.empty and "AF_CONTRATADO" in df_af.columns:
        af_filtered = df_af.copy()
        # Apply same NODO/MUNICIPIO filters to AF data
        if sel_n != "📍 Todos los Nodos":
            af_nodo_col = next((c for c in af_filtered.columns if c.strip().upper() == "NODO"), None)
            if af_nodo_col:
                af_filtered = af_filtered[af_filtered[af_nodo_col].astype(str).str.strip() == sel_n.strip()]
        if sel_m != "Todos los Municipios":
            af_mun_col = next((c for c in af_filtered.columns if c.strip().upper() == "MUNICIPIO"), None)
            if af_mun_col:
                af_filtered = af_filtered[af_filtered[af_mun_col].astype(str).str.strip() == sel_m.strip()]
        contr = int(af_filtered["AF_CONTRATADO"].sum())
    else:
        contr = len(mf[mf["STATUS"]=="CONTRATADO"])

    post_total = post + contr  # Seleccionados incluyen contratados
    filled = post + contr  # total filled positions (for gauge)
    vac   = len(mf[mf["STATUS"]=="VACANTE"])
    benef = int(af["Asistentes"].sum()) if not af.empty else 0
    sesiones = len(af)
    pct = round(filled/META*100,1) if META else 0
    pct_post = min(round(post_total/META*100,1), 100) if META else 0
    pct_contr = min(round(contr/META*100,1), 100) if META else 0

    # EE Impactados & Vacantes Críticas using FOCALIZACION as canonical source
    ee_impacted = 0
    vac_criticas = 0
    dane_col = None
    # Find DANE column in DATA_MASTER
    for c in mf.columns:
        if "DANE" in c.upper():
            dane_col = c
            break

    # --- DYNAMIC TOTAL EE CALCULATION (GLOBAL) ---
    dynamic_total_ee = TOTAL_EE # Fallback
    if not df_foc.empty:
        df_f_d_col = next((c for c in df_foc.columns if "DANE" in c.upper()), None)
        if df_f_d_col:
            dynamic_total_ee = len(df_foc[df_f_d_col].dropna().unique())
    # ---------------------------------------------

    # Find DANE column in FOCALIZACION sheet and filter by same NODO/MUNICIPIO
    foc_dane_col = None
    all_foc_danes = set()
    foc_filtered = df_foc.copy() if not df_foc.empty else pd.DataFrame()

    # Reusable DANE normalizer
    def _norm_dane_val(v):
        if pd.isna(v): return None
        s = str(v).strip()
        if s.endswith(".0"): s = s[:-2]
        return s if s and s.lower() != "nan" else None

    if not foc_filtered.empty:
        for c in foc_filtered.columns:
            if "DANE" in c.upper():
                foc_dane_col = c
                break
        # Apply same filters as sidebar to FOCALIZACION
        if sel_n != "📍 Todos los Nodos":
            foc_nodo_col = next((c for c in foc_filtered.columns if c.upper() == "NODO"), None)
            if foc_nodo_col:
                foc_filtered = foc_filtered[foc_filtered[foc_nodo_col].astype(str).str.strip() == sel_n.strip()]
        if sel_m != "Todos los Municipios":
            foc_mun_col = next((c for c in foc_filtered.columns if "MUNICIPIO" in c.upper()), None)
            if foc_mun_col:
                foc_filtered = foc_filtered[foc_filtered[foc_mun_col].astype(str).str.strip() == sel_m.strip()]
        if foc_dane_col:
            all_foc_danes = set(foc_filtered[foc_dane_col].dropna().apply(_norm_dane_val).dropna().unique())

    # EE Impactados = unique DANE codes where ESTADO is not empty (HAS_M = True)
    covered_danes = set()
    if dane_col:
        impactados_df = mf[mf["HAS_M"] == True]
        covered_danes = set(impactados_df[dane_col].dropna().apply(_norm_dane_val).dropna().unique())

    if all_foc_danes:
        ee_impacted = len(covered_danes & all_foc_danes)  # only count if DANE also exists in FOCALIZACION
    elif dane_col:
        ee_impacted = len(covered_danes)
    
    # Vacantes = Total EE (from FOCALIZACION) - EE Impactados
    actual_total_ee = len(all_foc_danes) if all_foc_danes else dynamic_total_ee
    vac_criticas = max(actual_total_ee - ee_impacted, 0)
    pct_ee = min(round(ee_impacted / actual_total_ee * 100, 1), 100) if actual_total_ee else 0
    pct_vc = min(round(vac_criticas / actual_total_ee * 100, 1), 100) if actual_total_ee else 0

    # Top EE
    top_ee, top_num, top_loc = "Sin datos", 0, ""
    if not af.empty and "EE" in af.columns:
        g = af.groupby("EE")["Asistentes"].sum().reset_index().sort_values("Asistentes",ascending=False)
        if not g.empty:
            top_ee=g.iloc[0]["EE"]; top_num=int(g.iloc[0]["Asistentes"])
            try:
                r=af[af["EE"]==top_ee].iloc[0]; top_loc=f"{r.get('Municipio','')} · {r.get('Nodo','')}"
            except: pass

    # ═══════════════════════════════════════════════════════════════════════
    # ROW 1: Main KPI Cards — Seleccionados | Contratados | V.Críticas | EE Impactados | Cobertura
    # ═══════════════════════════════════════════════════════════════════════
    c1,c2,c3,c4 = st.columns([1,1,1,1], gap="medium")
    _card_h = "min-height:120px;"
    with c1:
        st.markdown(f"""<div class='dc' style='border-top:3px solid {CY};{_card_h}'>
            <div class='kl' style='color:{CY};'>SELECCIONADOS</div>
            <div style='display:flex;align-items:baseline;gap:8px;margin-top:8px;'>
                <div class='kv' style='font-size:2rem;color:{CY};'>{post_total}</div>
                <span style='font-size:.7rem;color:{TD};'>/ {META} AF · {pct_post}%</span>
            </div>
            <div style='margin-top:8px;height:5px;background:rgba(255,255,255,0.06);border-radius:3px;overflow:hidden;'>
                <div style='width:{pct_post}%;height:100%;background:{CY};border-radius:3px;transition:width .4s;'></div>
            </div>
        </div>""", unsafe_allow_html=True)
        if st.button("Ver detalle", key="btn_post_detail", use_container_width=True):
            show_detail_postulantes(mf)
    with c2:
        _af_dec = af_contrat_summary.get("declinados", 0)
        _af_tot = af_contrat_summary.get("total_legal", contr + _af_dec)
        _af_res = af_contrat_summary.get("resoluciones", 0)
        # Build resoluciones badge HTML separately
        _resol_html = ""
        if _af_res:
            _resol_html = (
                f"<div style='margin-top:10px;background:rgba(136,111,255,0.10);border:1px solid rgba(136,111,255,0.30);"
                f"border-radius:8px;padding:7px 10px;display:flex;align-items:center;justify-content:space-between;'>"
                f"<div style='font-size:.48rem;color:{ACCENT};letter-spacing:.3px;line-height:1.3;max-width:65%;"
                f"text-transform:uppercase;font-weight:600;'>Resoluciones emitidas a<br/>personas que cumplen requisitos</div>"
                f"<div style='font-family:JetBrains Mono;font-size:1.3rem;font-weight:800;color:{ACCENT};"
                f"text-shadow:0 0 12px rgba(136,111,255,0.4);'>{_af_res:,}</div>"
                f"</div>"
            )
        st.markdown(f"""<div class='dc' style='border-top:3px solid {GN};{_card_h}'>
            <div class='kl' style='color:{GN};'>CONTRATADOS</div>
            <div style='display:flex;align-items:baseline;gap:8px;margin-top:8px;'>
                <div class='kv' style='font-size:2rem;'>{contr}</div>
                <span style='font-size:.7rem;color:{TD};'>/ {META} AF · {pct_contr}%</span>
            </div>
            <div style='margin-top:8px;height:5px;background:rgba(255,255,255,0.06);border-radius:3px;overflow:hidden;'>
                <div style='width:{pct_contr}%;height:100%;background:{GN};border-radius:3px;transition:width .4s;'></div>
            </div>
            <details style='margin-top:10px;'>
                <summary style='font-size:.6rem;color:{ACCENT};cursor:pointer;letter-spacing:.5px;
                    list-style:none;display:flex;align-items:center;gap:4px;'>
                    <span style='font-size:.7rem;'>ℹ️</span> DESGLOSE CONTRATACIÓN
                </summary>
                <div style='margin-top:8px;padding:8px 0 0 0;border-top:1px solid rgba(255,255,255,0.06);'>
                    <div style='display:flex;justify-content:space-between;font-size:.62rem;color:{TD};margin-bottom:4px;'>
                        <span>Declinados</span>
                        <span style='font-family:JetBrains Mono;color:{MG};font-weight:700;'>{_af_dec:,}</span>
                    </div>
                    <div style='display:flex;justify-content:space-between;font-size:.65rem;color:#fff;font-weight:700;
                        padding-top:4px;border-top:1px solid rgba(255,255,255,0.06);'>
                        <span>Total (Leg. + Dec.)</span>
                        <span style='font-family:JetBrains Mono;'>{_af_tot:,}</span>
                    </div>
                </div>
            </details>
            {_resol_html}
        </div>""", unsafe_allow_html=True)
        if st.button("Ver detalle", key="btn_contr_detail", use_container_width=True):
            show_detail_contratados(mf, af_filtered if not df_af.empty and "AF_CONTRATADO" in df_af.columns else None)
    with c3:
        st.markdown(f"""<div class='dc' style='border-top:3px solid {MG};{_card_h}'>
            <div class='kl' style='color:{MG};'>VACANTES CRÍTICAS</div>
            <div style='display:flex;align-items:baseline;gap:8px;margin-top:8px;'>
                <div class='kv' style='font-size:2rem;color:{MG};'>{vac_criticas}</div>
                <span style='font-size:.7rem;color:{TD};'>/ {actual_total_ee} EE · {pct_vc}%</span>
            </div>
            <div style='margin-top:8px;height:5px;background:rgba(255,255,255,0.06);border-radius:3px;overflow:hidden;'>
                <div style='width:{pct_vc}%;height:100%;background:{MG};border-radius:3px;transition:width .4s;'></div>
            </div>
        </div>""", unsafe_allow_html=True)
        if st.button("Ver detalle", key="btn_vac_detail", use_container_width=True):
            show_detail_vacantes(mf, foc_filtered)
    with c4:
        st.markdown(f"""<div class='dc' style='border-top:3px solid {ACCENT};{_card_h}'>
            <div class='kl' style='color:{ACCENT};'>EE IMPACTADOS</div>
            <div style='display:flex;align-items:baseline;gap:8px;margin-top:8px;'>
                <div class='kv' style='font-size:2rem;color:{ACCENT};'>{ee_impacted}</div>
                <span style='font-size:.7rem;color:{TD};'>/ {actual_total_ee} · {pct_ee}%</span>
            </div>
            <div style='margin-top:8px;height:5px;background:rgba(255,255,255,0.06);border-radius:3px;overflow:hidden;'>
                <div style='width:{pct_ee}%;height:100%;background:linear-gradient(90deg,{ACCENT},#a78bfa);border-radius:3px;transition:width .4s;'></div>
            </div>
        </div>""", unsafe_allow_html=True)
        if st.button("Ver detalle", key="btn_ee_detail", use_container_width=True):
            show_detail_ee_impactados(mf, foc_filtered)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════
    # ROW 2: Pulse + Map (Left) | Info Cards + Radar (Right)
    # ═══════════════════════════════════════════════════════════════════════
    cLeft, cRight = st.columns([3, 1], gap="medium")

    with cLeft:
        # Nested columns for Pulse and Map
        cP, cM = st.columns([1, 2], gap="medium")
        
        # ── PULSE FEED ──
        with cP:
            st.markdown(f"""<div class='dc' style='padding:14px;'>
            <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;'>
                <span style='font-size:.72rem;font-weight:700;letter-spacing:1px;'>📡 Pulso en Vivo</span>
                <span class='badge-live' style='font-size:.55rem;padding:2px 8px;background:rgba(136,111,255,0.15);border:1px solid {ACCENT};border-radius:10px;color:{ACCENT};'>EN VIVO</span>
            </div>""", unsafe_allow_html=True)
            if not af.empty and "Marca Temporal" in af.columns:
                html_items = ""
                for _, row in af.head(25).iterrows():
                    ts = row.get("Marca Temporal", pd.NaT)
                    ts_str = ts.strftime("%d/%m %I:%M %p") if pd.notna(ts) and hasattr(ts, 'strftime') else "Reciente"
                    ee = str(row.get("EE","")).strip()[:30]
                    nodo = str(row.get("Nodo",""))
                    b = int(row.get("Asistentes", 0))
                    ci = str(row.get("CI_ATT","")) if "CI_ATT" in af.columns else ""
                    ci_str = f" · {ci}" if ci and ci != "nan" else ""
                    html_items += f"""<div class='pc'>
                        <div class='pc-body'>
                            <div class='pc-t'>⏱ {ts_str}{ci_str}</div>
                            <div class='pc-e'>{ee}</div>
                            <div class='pc-l'>{nodo}</div>
                        </div>
                        <div class='pc-n' style='text-align:right;flex-shrink:0;'>
                            <div style='font-weight:800;color:{GN};font-size:.95rem;'>+{b}</div>
                            <div style='font-size:.55rem;color:{TD};'>BENEF.</div>
                        </div>
                    </div>"""
                st.markdown(f"<div class='pulse-wrap'><div class='pulse-track'>{html_items}{html_items}</div></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='color:{TD};padding:20px;text-align:center;'>Esperando registros...</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # ── MAP ──
        with cM:
            st.markdown(f"<div class='kl' style='margin-bottom:8px;'>🗺️ DESPLIEGUE TERRITORIAL</div>", unsafe_allow_html=True)
            
            GEOJSON_URL = "https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/colombia.geo.json"
            
            geo = mf.dropna(subset=["LAT","LON"]).copy()
            s_post = st.session_state.get("tog_p", True)
            s_contr = st.session_state.get("tog_c", True)
            s_vac = st.session_state.get("tog_v", True)

            if not geo.empty:
                agg = geo.groupby(["MUN","LAT","LON","NODO"]).agg(
                    TOT=("STATUS","count"),
                    POS=("STATUS",lambda x:((x=="POSTULANTE") | (x=="CONTRATADO")).sum()),
                    CON=("STATUS",lambda x:(x=="CONTRATADO").sum()),
                    VAC=("STATUS",lambda x:(x=="VACANTE").sum())
                ).reset_index()

                # Compute VAC_CRIT per municipality using FOCALIZACION (same logic as dialog)
                agg["VAC_CRIT"] = 0
                if dane_col and dane_col in geo.columns and not df_foc.empty:
                    # Find foc DANE and MUNICIPIO columns
                    _foc_dc = next((c for c in df_foc.columns if "DANE" in c.upper()), None)
                    _foc_mc = next((c for c in df_foc.columns if c.strip().upper() == "MUNICIPIO"), None)
                    if not _foc_mc:
                        _foc_mc = next((c for c in df_foc.columns if "MUNICIPIO" in c.upper()), None)
                    if _foc_dc and _foc_mc:
                        # Global covered DANEs: ESTADO not empty (HAS_M = True), normalized
                        _map_covered = set(mf[mf["HAS_M"] == True][dane_col].dropna().apply(_norm_dane_val).dropna().unique())
                        # All FOCALIZACION DANEs, normalized
                        _all_foc = set(df_foc[_foc_dc].dropna().apply(_norm_dane_val).dropna().unique())
                        # Global uncovered
                        _all_uncovered = _all_foc - _map_covered

                        # Per-municipality breakdown
                        df_foc["_DN"] = df_foc[_foc_dc].apply(_norm_dane_val)
                        _uncov_df = df_foc[df_foc["_DN"].isin(_all_uncovered)].drop_duplicates(subset=[_foc_dc])
                        if not _uncov_df.empty and _foc_mc in _uncov_df.columns:
                            _vc_counts = _uncov_df.groupby(_foc_mc).size().reset_index(name="VAC_CRIT")
                            _vc_counts["MUN"] = _vc_counts[_foc_mc].astype(str).str.strip().str.title()
                            _vc_counts = _vc_counts.groupby("MUN")["VAC_CRIT"].sum().reset_index()
                            agg = agg.drop(columns=["VAC_CRIT"])
                            agg = agg.merge(_vc_counts[["MUN","VAC_CRIT"]], on="MUN", how="left")
                            agg["VAC_CRIT"] = agg["VAC_CRIT"].fillna(0).astype(int)

                if not af.empty and "Municipio" in af.columns:
                    att_mun = af.groupby(af["Municipio"].str.strip().str.title())["Asistentes"].agg(["sum","count"]).reset_index()
                    att_mun.columns = ["MUN","BENEF","SES"]
                    agg = agg.merge(att_mun, on="MUN", how="left")
                    agg["BENEF"] = agg["BENEF"].fillna(0).astype(int)
                    agg["SES"] = agg["SES"].fillna(0).astype(int)
                else:
                    agg["BENEF"] = 0; agg["SES"] = 0

                mask = pd.Series(False, index=agg.index)
                if s_post: mask = mask | (agg["POS"] > 0)
                if s_contr: mask = mask | (agg["CON"] > 0)
                if s_vac: mask = mask | (agg["VAC_CRIT"] > 0)
                agg = agg[mask]

                agg["R"], agg["G"], agg["B"], agg["A"] = 136, 111, 255, 160
                if s_post:
                    agg.loc[agg["POS"] > 0, ["R","G","B"]] = [0, 212, 255]
                if s_contr:
                    agg.loc[agg["CON"] > 0, ["R","G","B"]] = [0, 255, 128]
                if s_vac:
                    agg.loc[agg["VAC_CRIT"] > 0, ["R","G","B"]] = [255, 0, 128]
                
                agg["RAD"] = agg["TOT"].clip(1, 40) * 350 + 2500

                border_layer = pdk.Layer(
                    "GeoJsonLayer", GEOJSON_URL,
                    stroked=True, filled=False,
                    get_line_color=[136, 111, 255, 60], get_line_width=1500, line_width_min_pixels=1,
                )
                point_layer = pdk.Layer(
                    "ScatterplotLayer", data=agg,
                    get_position=["LON","LAT"], get_fill_color=["R","G","B","A"],
                    get_radius="RAD", radius_min_pixels=6, radius_max_pixels=25,
                    pickable=True, auto_highlight=True
                ) if not agg.empty else None

                view = pdk.ViewState(latitude=4.8, longitude=-75.5, zoom=6.6, pitch=0)
                tooltip = {"html": """<div style='font-family:Inter;padding:8px;min-width:180px;'>
                    <b style='font-size:14px;color:#fff;'>{MUN}</b><br/><span style='color:rgba(232,230,240,0.6);font-size:11px;'>{NODO}</span>
                    <hr style='border:0;border-top:1px solid rgba(255,255,255,0.1);margin:6px 0;'/>
                    <div style='display:flex;justify-content:space-between;'><span>📋 Seleccionados:</span><b>{POS}</b></div>
                    <div style='display:flex;justify-content:space-between;'><span>✅ Contratados:</span><b>{CON}</b></div>
                    <div style='display:flex;justify-content:space-between;'><span>🚨 V. Críticas:</span><b>{VAC_CRIT}</b></div>
                    <div style='display:flex;justify-content:space-between;border-top:1px solid rgba(255,255,255,0.05);margin-top:4px;padding-top:4px;'><span>📊 Beneficiarios:</span><b>{BENEF}</b></div>
                </div>""", "style": {"background": "#0f0f1a", "color": "#fff", "border": f"1px solid {BDR}", "border-radius": "12px"}}

                layers = [border_layer]
                if point_layer: layers.append(point_layer)
                st.pydeck_chart(pdk.Deck(layers=layers, initial_view_state=view, map_style="dark", tooltip=tooltip), use_container_width=True)
            else:
                st.warning("Sin coordenadas para mostrar en el mapa")

        # ── Nodo Coverage Chart (Spans full cLeft width) ──
        st.markdown(f"""<div style='display:flex;justify-content:space-between;align-items:center;margin-top:12px;margin-bottom:4px;'>
            <div class='kl'>📊 COBERTURA POR NODO</div>
            <div style='font-family:JetBrains Mono;font-size:1.1rem;font-weight:800;color:{ACCENT};'>{filled}/{META}</div>
        </div>""", unsafe_allow_html=True)
        nc = nodo_coverage_chart(mf, h=300)
        if nc:
            st.plotly_chart(nc, use_container_width=True, config={"displayModeBar": False})
        else:
            st.caption("Sin datos de nodo")

    # ── RIGHT COLUMN: Map Toggles + Info Cards + Radar ──
    with cRight:
        # Gauges side by side at the top
        gL, gR = st.columns(2, gap="small")
        with gL:
            st.plotly_chart(single_gauge(post_total, META, CY, "SELECCIONADOS", h=160), use_container_width=True, config={"displayModeBar":False})
        with gR:
            st.plotly_chart(single_gauge(contr, META, GN, "CONTRATADOS", h=160), use_container_width=True, config={"displayModeBar":False})

        # Map filter toggles
        st.markdown(f"""<div style='font-family:Inter;font-size:.72rem;font-weight:700;letter-spacing:1.5px;
            color:{TD};margin-bottom:8px;'>FILTROS DE MAPA</div>""", unsafe_allow_html=True)
        fc1, fc2, fc3 = st.columns(3, gap="small")
        with fc1:
            st.toggle("Seleccionados", value=True, key="tog_p", label_visibility="collapsed")
            _on_p = st.session_state.get("tog_p", True)
            st.markdown(f"""<div style='text-align:center;margin-top:-8px;opacity:{"1" if _on_p else "0.3"};'>
                <div style='width:28px;height:28px;border-radius:50%;background:rgba(0,212,255,0.15);border:2px solid {CY};
                    display:inline-flex;align-items:center;justify-content:center;'>
                    <div style='width:10px;height:10px;border-radius:50%;background:{CY};'></div>
                </div>
                <div style='font-size:.68rem;font-weight:600;color:{CY};margin-top:4px;letter-spacing:.5px;'>Selec.</div>
            </div>""", unsafe_allow_html=True)
        with fc2:
            st.toggle("Contratados", value=True, key="tog_c", label_visibility="collapsed")
            _on_c = st.session_state.get("tog_c", True)
            st.markdown(f"""<div style='text-align:center;margin-top:-8px;opacity:{"1" if _on_c else "0.3"};'>
                <div style='width:28px;height:28px;border-radius:50%;background:rgba(0,255,128,0.15);border:2px solid {GN};
                    display:inline-flex;align-items:center;justify-content:center;'>
                    <div style='width:10px;height:10px;border-radius:50%;background:{GN};'></div>
                </div>
                <div style='font-size:.68rem;font-weight:600;color:{GN};margin-top:4px;letter-spacing:.5px;'>Contr.</div>
            </div>""", unsafe_allow_html=True)
        with fc3:
            st.toggle("Vacantes", value=True, key="tog_v", label_visibility="collapsed")
            _on_v = st.session_state.get("tog_v", True)
            st.markdown(f"""<div style='text-align:center;margin-top:-8px;opacity:{"1" if _on_v else "0.3"};'>
                <div style='width:28px;height:28px;border-radius:50%;background:rgba(255,0,128,0.15);border:2px solid {MG};
                    display:inline-flex;align-items:center;justify-content:center;'>
                    <div style='width:10px;height:10px;border-radius:50%;background:{MG};'></div>
                </div>
                <div style='font-size:.68rem;font-weight:600;color:{MG};margin-top:4px;letter-spacing:.5px;'>V.Crít.</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

        # -- BENEFICIARIOS card --
        st.markdown(f"""<div class='dc-sm' style='text-align:center;padding:14px;'>
            <div class='kl'>📊 Reporte de Asistencias</div>
            <div class='kv' style='font-size:2rem;margin-top:6px;'>{benef:,}</div>
            <div style='color:{TD};font-size:.72rem;'>Total Nacional</div>
        </div>""", unsafe_allow_html=True)

        # -- EE MAYOR IMPACTO card --
        st.markdown(f"""<div class='dc-sm' style='padding:14px;border-top:2px solid {GN};'>
            <div class='kl' style='color:{GN};'>🏆 EE MAYOR IMPACTO</div>
            <div style='margin-top:6px;font-size:.78rem;font-weight:700;color:#fff;'>{str(top_ee)[:35]}</div>
            <div style='font-size:.68rem;color:{TD};margin-top:2px;'>📍 {top_loc}</div>
            <div style='font-family:JetBrains Mono;font-size:1rem;color:{GN};font-weight:800;margin-top:4px;'>{top_num:,} Benef.</div>
        </div>""", unsafe_allow_html=True)

        # -- SESIONES card --
        st.markdown(f"""<div class='dc-sm' style='text-align:center;padding:14px;border-top:2px solid {OR};'>
            <div class='kl' style='color:{OR};'>📅 Momentos Pedagógicos</div>
            <div class='kv' style='font-size:2rem;margin-top:6px;color:{OR};'>{sesiones}</div>
            <div style='color:{TD};font-size:.72rem;'>Registros en BD</div>
        </div>""", unsafe_allow_html=True)

        # Radar Chart
        st.markdown(f"<div class='kl' style='margin-bottom:6px;margin-top:10px;'>🎯 CENTROS DE INTERÉS</div>", unsafe_allow_html=True)
        st.plotly_chart(radar_chart(mf, h=240), use_container_width=True, config={"displayModeBar":False})

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════
    # ROW 3: Bottom Tables & Charts
    # ═══════════════════════════════════════════════════════════════════════
    b1, b2 = st.columns(2, gap="medium")

    with b1:
        with st.expander("⚠️ Municipios con Necesidades de Contratación", expanded=True):
            if vac > 0:
                vt = mf.groupby(["MUNICIPIO","NODO"]).agg(
                    POSTULANTES=("STATUS",lambda x:(x=="POSTULANTE").sum()),
                    CONTRATADOS=("STATUS",lambda x:(x=="CONTRATADO").sum()),
                    VACANTES=("STATUS",lambda x:(x=="VACANTE").sum())
                ).reset_index()
                vt = vt[vt["VACANTES"]>0].sort_values("VACANTES",ascending=False)
                vt["ESTADO"] = "🔴 Necesita"
                st.markdown(dark_table(vt, max_h=350, num_cols=["POSTULANTES","CONTRATADOS","VACANTES"],
                    color_map={"POSTULANTES":CY,"CONTRATADOS":GN,"VACANTES":MG,"MUNICIPIO":"#fff","NODO":ACCENT,"ESTADO":MG}), unsafe_allow_html=True)
            else:
                st.success("¡Todo cubierto! 🎉")

    with b2:
        # Fase & Estacionalidad from attendance
        with st.expander("📊 Asistencia: Fase y Estacionalidad", expanded=True):
            if not af.empty:
                sub_tabs = []
                if "Fase" in af.columns: sub_tabs.append("Por Fase")
                if "Estacionalidad" in af.columns: sub_tabs.append("Por Estacionalidad")
                sub_tabs.append("Top 5 EE")
                tabs = st.tabs(sub_tabs)
                idx = 0
                if "Fase" in af.columns:
                    with tabs[idx]:
                        fd = af.groupby("Fase")["Asistentes"].agg(["sum","count"]).reset_index()
                        fd.columns = ["FASE","BENEFICIARIOS","SESIONES"]
                        fd = fd[fd["FASE"]!="nan"].sort_values("BENEFICIARIOS",ascending=False)
                        st.markdown(dark_table(fd, max_h=250, num_cols=["BENEFICIARIOS","SESIONES"],
                            color_map={"FASE":"#fff"}), unsafe_allow_html=True)
                    idx += 1
                if "Estacionalidad" in af.columns:
                    with tabs[idx]:
                        ed = af.groupby("Estacionalidad")["Asistentes"].agg(["sum","count"]).reset_index()
                        ed.columns = ["ESTACIONALIDAD","BENEFICIARIOS","SESIONES"]
                        ed = ed[ed["ESTACIONALIDAD"]!="nan"].sort_values("BENEFICIARIOS",ascending=False)
                        st.markdown(dark_table(ed, max_h=250, num_cols=["BENEFICIARIOS","SESIONES"],
                            color_map={"ESTACIONALIDAD":"#fff"}), unsafe_allow_html=True)
                    idx += 1
                with tabs[idx]:
                    if "EE" in af.columns:
                        cols_n = ["EE"]
                        if "Municipio" in af.columns: cols_n.append("Municipio")
                        rk = af.groupby(cols_n)["Asistentes"].sum().reset_index().sort_values("Asistentes",ascending=False).head(5)
                        rk.columns = [c.upper() for c in rk.columns]
                        st.markdown(dark_table(rk, max_h=250, num_cols=["ASISTENTES"],
                            color_map={"EE":"#fff","MUNICIPIO":TD}), unsafe_allow_html=True)
            else:
                st.caption("Sin datos de asistencia")

    # ═══════════════════════════════════════════════════════════════════════
    # ROW 4: TABLERO DE SEGUIMIENTO — MÉTRICAS UNIFICADAS
    # ═══════════════════════════════════════════════════════════════════════
    st.markdown(f"""<div style='margin-top:24px;margin-bottom:12px;'>
        <div style='display:flex;align-items:center;gap:12px;'>
            <div style='width:4px;height:28px;background:linear-gradient(180deg,{OR},{MG});border-radius:2px;'></div>
            <div>
                <div style='font-size:1rem;font-weight:800;letter-spacing:1.5px;color:#fff;'>TABLERO DE SEGUIMIENTO</div>
                <div style='font-size:.62rem;color:{TD};margin-top:2px;'>Métricas Unificadas — Equipos Territoriales 2026</div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)




    if met_summary:
        # Safe conversion helpers
        def _safe_int(v, default=0):
            try:
                f = float(v)
                return int(f) if pd.notna(f) else default
            except: return default

        def _safe_fmt(v, default="-"):
            """Format a numeric value: int if whole, otherwise 1 decimal, with comma separators."""
            if v is None: return default
            try:
                f = float(v)
                if pd.isna(f): return default
                return f"{int(f):,}" if f == int(f) else f"{f:,.1f}"
            except: return default

        def _parse_pct(v):
            """Parse a percentage value to float (0-100 range)."""
            if v is None: return 0.0
            if isinstance(v, (int, float)): return float(v) * 100 if float(v) < 1 else float(v)
            s_orig = str(v).strip()
            has_pct = "%" in s_orig
            s = s_orig.replace("%","").replace(",",".").strip()
            try:
                f = float(s)
                # Bare decimal without % sign (e.g. 0.0365 → 3.65%)
                if f < 1 and not has_pct:
                    return f * 100
                return f
            except: return 0.0

        # Extract all 9 metrics
        _sedes_est     = _safe_fmt(met_summary.get("sedes_estimadas"))
        _acuerdos_est  = _safe_fmt(met_summary.get("acuerdos_estimados"))
        _acuerdos_cob  = _safe_fmt(met_summary.get("acuerdos_cobertura"))
        _pct_cob       = _parse_pct(met_summary.get("pct_cobertura", 0))
        _formadores    = _safe_fmt(met_summary.get("formadores_activos"))
        _benef_val     = _safe_fmt(met_summary.get("benef_validados"))
        _acuerdos_plat = _safe_fmt(met_summary.get("acuerdos_plataforma"))
        _benef_plat    = _safe_fmt(met_summary.get("benef_plataforma"))
        _centros_proy  = _safe_fmt(met_summary.get("centros_proyectados"))

        # Numeric values for radar & area charts
        _sedes_num     = _safe_int(met_summary.get("sedes_estimadas"))
        _acuerdos_num  = _safe_int(met_summary.get("acuerdos_cobertura"))
        _centros_num   = _safe_int(met_summary.get("centros_proyectados"))
        _formad_num    = _safe_int(met_summary.get("formadores_activos"))
        _benef_v_num   = _safe_int(met_summary.get("benef_validados"))
        _acplat_num    = _safe_int(met_summary.get("acuerdos_plataforma"))
        _benef_p_num   = _safe_int(met_summary.get("benef_plataforma"))

        # ── MAIN LAYOUT: Left KPI column + Right charts column ──
        col_kpi, col_charts = st.columns([1, 2.5], gap="medium")

        # ── LEFT: Beneficiarios Validados (featured) + 5 stacked KPI cards ──
        with col_kpi:
            # ★ Beneficiarios Validados — compact accent card at the top
            st.markdown(f"""<div class='kpi-benef'>
                <div style='display:flex;align-items:center;'>
                    <span class='kpi-benef-dot'></span>
                    <span class='kl' style='color:{GN};font-size:.62rem;'>Beneficiarios en Acuerdos de Cobertura</span>
                </div>
                <div class='kv' style='font-size:1.8rem;color:{GN};margin-top:4px;
                    text-shadow:0 0 16px rgba(0,255,128,0.25);'>{_benef_val}</div>
                <div style='font-size:.55rem;color:{TD};margin-top:2px;'>Cifra acumulada nacional</div>
            </div>""", unsafe_allow_html=True)

            _kpi_data = [
                ("SEDES ESTIMADAS",    _sedes_est,    OR, "Total"),
                ("ACUERDOS COB. EST.", _acuerdos_est, OR, "Estimados"),
                ("ACUERDOS COBERTURA", _acuerdos_cob, CY, "Global"),
                ("FORMADORES ACTIVOS", _formadores,   GN, "Activos"),
                ("CENTROS INT. PROY.", _centros_proy,  MG, "Plazas"),
            ]
            for _label, _value, _color, _sub in _kpi_data:
                st.markdown(f"""<div class='dc' style='border-left:3px solid {_color};
                    padding:14px 16px;margin-bottom:8px;'>
                    <div class='kl' style='color:{_color};font-size:.62rem;'>{_label}</div>
                    <div class='kv' style='font-size:1.8rem;color:{_color};margin-top:4px;'>{_value}</div>
                    <div style='font-size:.58rem;color:{TD};margin-top:2px;'>{_sub}</div>
                </div>""", unsafe_allow_html=True)

        # ── RIGHT: Radar on top, Area chart + Progress bar on bottom ──
        with col_charts:
            # ── RADAR / SPIDER CHART ──
            radar_axes = ["Sedes", "Acuerdos", "Centros", "Formadores", "Beneficiarios"]
            radar_raw  = [_sedes_num, _acuerdos_num, _centros_num, _formad_num, _benef_v_num]

            # Normalize to 0–100 for comparable display
            _max_val = max(radar_raw) if max(radar_raw) > 0 else 1
            radar_norm = [round(v / _max_val * 100, 1) for v in radar_raw]

            # Close the polygon
            radar_axes_c = radar_axes + [radar_axes[0]]
            radar_norm_c = radar_norm + [radar_norm[0]]
            radar_raw_c  = radar_raw  + [radar_raw[0]]

            fig_radar = go.Figure()

            # Trace 1: Main values (orange fill)
            fig_radar.add_trace(go.Scatterpolar(
                r=radar_norm_c, theta=radar_axes_c, fill='toself',
                fillcolor="rgba(255,159,28,0.12)",
                line=dict(color=OR, width=2),
                marker=dict(size=6, color=OR),
                name="Cobertura",
                customdata=radar_raw_c,
                hovertemplate="%{theta}: %{customdata:,}<extra></extra>"
            ))

            # Trace 2: Plataforma overlay (cyan)
            plat_raw  = [0, _acplat_num, 0, 0, _benef_p_num]
            plat_norm = [round(v / _max_val * 100, 1) for v in plat_raw]
            plat_raw_c  = plat_raw  + [plat_raw[0]]
            plat_norm_c = plat_norm + [plat_norm[0]]
            fig_radar.add_trace(go.Scatterpolar(
                r=plat_norm_c, theta=radar_axes_c, fill='toself',
                fillcolor="rgba(0,212,255,0.08)",
                line=dict(color=CY, width=1.5, dash='dot'),
                marker=dict(size=4, color=CY),
                name="Plataforma",
                customdata=plat_raw_c,
                hovertemplate="%{theta}: %{customdata:,}<extra></extra>"
            ))

            # Trace 3: Target ring (green dashed, 100%)
            fig_radar.add_trace(go.Scatterpolar(
                r=[100]*6, theta=radar_axes_c,
                fill='none', line=dict(color=GN, width=1, dash='dash'),
                marker=dict(size=0), name="Meta", opacity=0.35,
                hoverinfo='skip'
            ))

            fig_radar.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=40, r=40, t=25, b=10), height=310,
                font=dict(family="Inter", color=TD, size=11),
                showlegend=True,
                hoverlabel=dict(bgcolor=CARD, font_size=12, font_family="Inter", font_color="#fff"),
                legend=dict(font=dict(size=9, color=TD), orientation="h",
                            x=0.5, xanchor="center", y=-0.05,
                            bgcolor="rgba(0,0,0,0)"),
                polar=dict(
                    bgcolor="rgba(0,0,0,0)",
                    radialaxis=dict(visible=True, showline=False,
                                    gridcolor="rgba(255,255,255,0.06)",
                                    tickfont=dict(size=8, color=TD), range=[0, 110]),
                    angularaxis=dict(gridcolor="rgba(255,255,255,0.08)",
                                     tickfont=dict(size=10, color=TW))
                )
            )
            st.plotly_chart(fig_radar, use_container_width=True, config={"displayModeBar": False})

            # ── BOTTOM ROW: Area chart + % Progress bar ──
            sub_left, sub_right = st.columns([1.6, 1], gap="small")

            with sub_left:
                # Area chart — Benef Validados, Acuerdos Plataforma, Benef Plataforma
                area_cats   = ["Benef. Valid.", "Acuerdos Plat.", "Benef. Plat."]
                area_vals   = [_benef_v_num, _acplat_num, _benef_p_num]
                area_colors = [GN, MG, "#CC0066"]

                fig_area = go.Figure()
                for i, (cat, val, clr) in enumerate(zip(area_cats, area_vals, area_colors)):
                    fig_area.add_trace(go.Scatter(
                        x=[0, 1, 2], y=[0, val, val * 0.85],
                        mode='lines', fill='tozeroy',
                        fillcolor=f"rgba({int(clr[1:3],16)},{int(clr[3:5],16)},{int(clr[5:7],16)},0.12)",
                        line=dict(color=clr, width=2),
                        name=cat
                    ))

                fig_area.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=5, r=5, t=10, b=5), height=180,
                    font=dict(family="Inter", color=TD, size=10),
                    showlegend=True,
                    hoverlabel=dict(bgcolor=CARD2, font_size=12, font_family="Inter", font_color="#fff"),
                    legend=dict(font=dict(size=8, color=TD), orientation="h",
                                x=0.5, xanchor="center", y=-0.15,
                                bgcolor="rgba(0,0,0,0)"),
                    xaxis=dict(visible=False),
                    yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)",
                               zeroline=False, tickfont=dict(size=8, color=TD))
                )
                st.plotly_chart(fig_area, use_container_width=True, config={"displayModeBar": False})

            with sub_right:
                # Neon progress bar — % Acuerdos Cobertura
                _pct_display = min(_pct_cob, 100)
                st.markdown(f"""<div class='dc' style='border-left:3px solid {CY};padding:16px;'>
                    <div class='kl' style='color:{CY};font-size:.62rem;margin-bottom:10px;'>% ACUERDOS COBERTURA</div>
                    <div style='font-family:JetBrains Mono;font-size:2rem;font-weight:800;color:{CY};
                        text-shadow:0 0 18px rgba(0,212,255,0.5);margin-bottom:12px;'>
                        {_pct_cob:.1f}%
                    </div>
                    <div style='background:rgba(255,255,255,0.04);border-radius:6px;height:14px;
                        overflow:hidden;position:relative;'>
                        <div style='width:{_pct_display}%;height:100%;
                            background:linear-gradient(90deg,{CY},rgba(0,212,255,0.6));
                            border-radius:6px;
                            box-shadow:0 0 12px rgba(0,212,255,0.5),0 0 24px rgba(0,212,255,0.25);
                            transition:width 0.8s ease;'></div>
                    </div>
                    <div style='display:flex;justify-content:space-between;margin-top:6px;'>
                        <span style='font-size:.55rem;color:{TD};'>0%</span>
                        <span style='font-size:.55rem;color:{TD};'>100%</span>
                    </div>
                </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class='dc' style='text-align:center;padding:30px;color:{TD};'>
            Pendiente de conexión con nueva fuente de datos.
        </div>""", unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════
    # REPORT GENERATION — Assemble data and plug into sidebar download btn
    # ═══════════════════════════════════════════════════════════════════════
    filter_parts = []
    if sel_n != "📍 Todos los Nodos":
        filter_parts.append(sel_n)
    if sel_m != "Todos los Municipios":
        filter_parts.append(sel_m)
    filter_ctx = " · ".join(filter_parts) if filter_parts else "Todos los Nodos"

    # Build the data dict for the report
    report_kpis = [
        {"label": "SELECCIONADOS",     "value": f"{post_total:,}", "sub": f"/ {META} AF - {pct_post}%", "pct": pct_post},
        {"label": "CONTRATADOS",       "value": f"{contr:,}",      "sub": f"/ {META} AF - {pct_contr}%", "pct": pct_contr},
        {"label": "VACANTES CRITICAS", "value": f"{vac_criticas:,}", "sub": f"/ {actual_total_ee} EE - {pct_vc}%", "pct": pct_vc},
        {"label": "EE IMPACTADOS",     "value": f"{ee_impacted:,}", "sub": f"/ {actual_total_ee} - {pct_ee}%", "pct": pct_ee},
    ]
    report_extra = [
        {"label": "BENEFICIARIOS", "value": f"{benef:,}", "sub": "Total Nacional", "color": (136, 111, 255)},
        {"label": "EE MAYOR IMPACTO", "value": str(top_ee)[:30], "sub": f"{top_num:,} Benef.", "color": (0, 255, 128)},
        {"label": "SESIONES", "value": f"{sesiones:,}", "sub": "Registros en BD", "color": (255, 159, 28)},
    ]

    # Build chart figures for PDF (re-create them for static export)
    report_nodo_fig = nodo_coverage_chart(mf, h=300)
    report_radar_fig = radar_chart(mf, h=320)

    # Tablero charts (only if data available)
    report_tablero_radar = None
    report_tablero_area = None
    if met_summary:
        def _safe_int_r(v, default=0):
            try:
                f = float(v)
                return int(f) if pd.notna(f) else default
            except: return default

        _s_num = _safe_int_r(met_summary.get("sedes_estimadas"))
        _a_num = _safe_int_r(met_summary.get("acuerdos_cobertura"))
        _c_num = _safe_int_r(met_summary.get("centros_proyectados"))
        _f_num = _safe_int_r(met_summary.get("formadores_activos"))
        _bv_num = _safe_int_r(met_summary.get("benef_validados"))
        _ap_num = _safe_int_r(met_summary.get("acuerdos_plataforma"))
        _bp_num = _safe_int_r(met_summary.get("benef_plataforma"))

        r_axes = ["Sedes", "Acuerdos", "Centros", "Formadores", "Beneficiarios"]
        r_raw  = [_s_num, _a_num, _c_num, _f_num, _bv_num]
        _mx = max(r_raw) if max(r_raw) > 0 else 1
        r_norm = [round(v / _mx * 100, 1) for v in r_raw]
        r_axes_c = r_axes + [r_axes[0]]
        r_norm_c = r_norm + [r_norm[0]]
        r_raw_c  = r_raw  + [r_raw[0]]

        report_tablero_radar = go.Figure()
        report_tablero_radar.add_trace(go.Scatterpolar(
            r=r_norm_c, theta=r_axes_c, fill='toself',
            fillcolor="rgba(255,159,28,0.12)",
            line=dict(color=OR, width=2), marker=dict(size=6, color=OR),
            name="Cobertura", customdata=r_raw_c,
            hovertemplate="%{theta}: %{customdata:,}<extra></extra>"
        ))
        p_raw = [0, _ap_num, 0, 0, _bp_num]
        p_norm = [round(v / _mx * 100, 1) for v in p_raw]
        p_raw_c = p_raw + [p_raw[0]]
        p_norm_c = p_norm + [p_norm[0]]
        report_tablero_radar.add_trace(go.Scatterpolar(
            r=p_norm_c, theta=r_axes_c, fill='toself',
            fillcolor="rgba(0,212,255,0.08)",
            line=dict(color=CY, width=1.5, dash='dot'), marker=dict(size=4, color=CY),
            name="Plataforma", customdata=p_raw_c,
            hovertemplate="%{theta}: %{customdata:,}<extra></extra>"
        ))
        report_tablero_radar.add_trace(go.Scatterpolar(
            r=[100]*6, theta=r_axes_c,
            fill='none', line=dict(color=GN, width=1, dash='dash'),
            marker=dict(size=0), name="Meta", opacity=0.35, hoverinfo='skip'
        ))
        report_tablero_radar.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=40, r=40, t=25, b=10), height=310,
            font=dict(family="Inter", color=TD, size=11), showlegend=True,
            legend=dict(font=dict(size=9, color=TD), orientation="h",
                        x=0.5, xanchor="center", y=-0.05, bgcolor="rgba(0,0,0,0)"),
            polar=dict(bgcolor="rgba(0,0,0,0)",
                       radialaxis=dict(visible=True, showline=False,
                                       gridcolor="rgba(255,255,255,0.06)",
                                       tickfont=dict(size=8, color=TD), range=[0, 110]),
                       angularaxis=dict(gridcolor="rgba(255,255,255,0.08)",
                                        tickfont=dict(size=10, color=TW)))
        )

        area_cats_r = ["Benef. Valid.", "Acuerdos Plat.", "Benef. Plat."]
        area_vals_r = [_bv_num, _ap_num, _bp_num]
        area_clrs_r = [GN, MG, "#CC0066"]
        report_tablero_area = go.Figure()
        for cat_r, val_r, clr_r in zip(area_cats_r, area_vals_r, area_clrs_r):
            report_tablero_area.add_trace(go.Scatter(
                x=[0, 1, 2], y=[0, val_r, val_r * 0.85],
                mode='lines', fill='tozeroy',
                fillcolor=f"rgba({int(clr_r[1:3],16)},{int(clr_r[3:5],16)},{int(clr_r[5:7],16)},0.12)",
                line=dict(color=clr_r, width=2), name=cat_r
            ))
        report_tablero_area.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=5, r=5, t=10, b=5), height=180,
            font=dict(family="Inter", color=TD, size=10), showlegend=True,
            legend=dict(font=dict(size=8, color=TD), orientation="h",
                        x=0.5, xanchor="center", y=-0.15, bgcolor="rgba(0,0,0,0)"),
            xaxis=dict(visible=False),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)",
                       zeroline=False, tickfont=dict(size=8, color=TD))
        )

    # Assemble the full data dict
    report_data = {
        "filter_context": filter_ctx,
        "kpis": report_kpis,
        "extra_cards": report_extra,
        "nodo_chart_fig": report_nodo_fig,
        "radar_chart_fig": report_radar_fig,
        "met_summary": met_summary,
        "tablero_radar_fig": report_tablero_radar,
        "tablero_area_fig": report_tablero_area,
    }

    # ── PDF Report: generate and save directly to Downloads folder ──
    from datetime import datetime as _dt
    from pathlib import Path
    _today = _dt.now().strftime("%Y-%m-%d")
    _report_name = f"Reporte_Dashboard_Artes_Paz_{_today}.pdf"

    # Generate the PDF and cache in session_state
    _cache_key = f"_pdf_cache_{filter_ctx}"
    if _cache_key not in st.session_state:
        for k in list(st.session_state.keys()):
            if k.startswith("_pdf_cache_"):
                del st.session_state[k]
        try:
            st.session_state[_cache_key] = generate_pdf_report(report_data)
        except Exception as e:
            st.session_state[_cache_key] = None
            st.session_state["_pdf_error"] = str(e)

    pdf_bytes = st.session_state.get(_cache_key)

    with report_placeholder:
        if pdf_bytes:
            if st.button("📄 Generar Reporte PDF", use_container_width=True, type="secondary"):
                # Save directly to Downloads folder
                downloads = Path.home() / "Downloads"
                downloads.mkdir(exist_ok=True)
                out_path = downloads / _report_name
                # If file already exists, add a counter
                counter = 1
                while out_path.exists():
                    out_path = downloads / f"Reporte_Dashboard_Artes_Paz_{_today}_{counter}.pdf"
                    counter += 1
                out_path.write_bytes(pdf_bytes)
                st.success(f"✅ Reporte guardado en:\n**{out_path}**")
        else:
            _err = st.session_state.get("_pdf_error", "Error desconocido")
            st.warning(f"Error PDF: {_err}")

if __name__ == "__main__":
    main()
