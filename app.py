import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from collections import Counter
import warnings
warnings.filterwarnings("ignore")

# ─── Page config ────────────────────────────────────────────
st.set_page_config(
    page_title="SPK Seleksi Beasiswa",
    page_icon="assets/favicon.png" if False else None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS global ─────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  .main { background: #0d1117; }
  section[data-testid="stSidebar"] { background: #161b22 !important; border-right: 1px solid #30363d; }
  section[data-testid="stSidebar"] * { color: #e6edf3 !important; }

  /* Metric cards */
  [data-testid="metric-container"] {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 14px 18px !important;
  }
  [data-testid="metric-container"] label { color: #8b949e !important; font-size: 12px !important; }
  [data-testid="metric-container"] [data-testid="metric-value"] { color: #e6edf3 !important; font-weight: 700 !important; }

  /* Tabs */
  button[data-baseweb="tab"] { background: transparent !important; color: #8b949e !important; border-bottom: 2px solid transparent !important; font-weight: 500; }
  button[data-baseweb="tab"][aria-selected="true"] { color: #58a6ff !important; border-bottom: 2px solid #58a6ff !important; }

  /* Buttons */
  .stButton > button {
    background: #1f6feb; color: white; border: none;
    border-radius: 8px; font-weight: 600; padding: 10px 24px;
    transition: all .2s; width: 100%;
  }
  .stButton > button:hover { background: #388bfd; transform: translateY(-1px); box-shadow: 0 4px 12px #1f6feb44; }

  /* Inputs */
  .stNumberInput input, .stTextInput input {
    background: #161b22 !important; border: 1px solid #30363d !important;
    color: #e6edf3 !important; border-radius: 6px !important;
  }
  .stSelectbox > div > div { background: #161b22 !important; border: 1px solid #30363d !important; color: #e6edf3 !important; }

  /* Divider */
  hr { border-color: #30363d !important; }

  /* Scrollbar */
  ::-webkit-scrollbar { width: 6px; height: 6px; }
  ::-webkit-scrollbar-track { background: #161b22; }
  ::-webkit-scrollbar-thumb { background: #30363d; border-radius: 3px; }

  /* Tables */
  .spk-table { width: 100%; border-collapse: collapse; font-size: 13px; font-family: 'Inter', sans-serif; }
  .spk-table thead th {
    background: #1f6feb; color: #fff; padding: 10px 14px;
    text-align: center; border: 1px solid #30363d; font-weight: 600; font-size: 13px;
  }
  .spk-table tbody tr:nth-child(odd)  { background: #161b22; }
  .spk-table tbody tr:nth-child(even) { background: #1c2128; }
  .spk-table tbody td { padding: 9px 14px; text-align: center; border: 1px solid #21262d; color: #e6edf3; }
  .spk-table tbody tr:hover { background: #21262d; }

  .badge-benefit { background: #0d419d44; color: #79c0ff; font-weight: 600; padding: 2px 8px; border-radius: 4px; }
  .badge-cost    { background: #da363344; color: #f78166; font-weight: 600; padding: 2px 8px; border-radius: 4px; }

  .result-box {
    background: linear-gradient(135deg, #161b22, #1c2128);
    border: 2px solid #ffd700; border-radius: 12px;
    padding: 24px; text-align: center; margin: 16px 0;
  }
  .winner-name { font-size: 26px; font-weight: 700; color: #ffd700; margin: 6px 0; }
  .winner-sub  { font-size: 13px; color: #8b949e; }

  .info-card {
    background: #161b22; border: 1px solid #30363d;
    border-radius: 10px; padding: 16px; margin: 8px 0;
  }
  .section-header {
    background: linear-gradient(90deg, #1f6feb28, transparent);
    border-left: 4px solid #1f6feb; border-radius: 0 8px 8px 0;
    padding: 10px 16px; margin: 20px 0 12px;
    font-size: 15px; font-weight: 600; color: #e6edf3;
  }
</style>
""", unsafe_allow_html=True)

# ─── Matplotlib dark theme ───────────────────────────────────
plt.rcParams.update({
    "figure.facecolor": "#0d1117", "axes.facecolor": "#161b22",
    "axes.edgecolor": "#30363d",   "axes.labelcolor": "#e6edf3",
    "xtick.color": "#e6edf3",      "ytick.color": "#e6edf3",
    "text.color": "#e6edf3",       "grid.color": "#21262d",
    "font.family": "DejaVu Sans",  "font.size": 11,
    "axes.titlesize": 13,          "axes.titleweight": "bold",
    "legend.facecolor": "#21262d", "legend.edgecolor": "#30363d",
})
COLORS = ["#58a6ff","#3fb950","#f78166","#d2a8ff","#ffa657","#79c0ff","#56d364","#ff7b72","#e3b341","#a5d6ff"]
MC     = {"SAW":"#58a6ff","SMART":"#3fb950","MOORA":"#f78166","WP":"#d2a8ff"}

# ─── Kriteria tetap ──────────────────────────────────────────
KRITERIA = [
    {"kode":"C1","nama":"IPK",               "satuan":"Skala 0–4",   "jenis":"Benefit","bobot":0.30},
    {"kode":"C2","nama":"Penghasilan Ortu",  "satuan":"Rp / bulan",  "jenis":"Cost",   "bobot":0.25},
    {"kode":"C3","nama":"Nilai Tes Akademik","satuan":"Skor 0–100",  "jenis":"Benefit","bobot":0.20},
    {"kode":"C4","nama":"Prestasi",          "satuan":"Skor 1–10",   "jenis":"Benefit","bobot":0.15},
    {"kode":"C5","nama":"Semester",          "satuan":"Semester",    "jenis":"Cost",   "bobot":0.10},
]
K_NAMA  = [k["nama"]  for k in KRITERIA]
K_KODE  = [k["kode"]  for k in KRITERIA]
K_JENIS = [k["jenis"] for k in KRITERIA]
K_BOBOT = np.array([k["bobot"] for k in KRITERIA])

INPUT_CFG = {
    "IPK":               (0.0, 4.0,  0.01, 3.50),
    "Penghasilan Ortu":  (0,   1e10, 500000, 3000000),
    "Nilai Tes Akademik":(0.0, 100.0, 0.5,  75.0),
    "Prestasi":          (1.0, 10.0, 0.5,   7.0),
    "Semester":          (1,   14,   1,     4),
}

# ─── Helper: tabel HTML ─────────────────────────────────────
def spk_table(df, hi_col=None, rank_col=None, fmt=None):
    rows = ""
    for i, (_, row) in enumerate(df.iterrows()):
        cells = ""
        for c in df.columns:
            v   = row[c]
            sty = ""
            if fmt and c in fmt:
                try:    txt = fmt[c].format(v)
                except: txt = str(v)
            elif isinstance(v, float):
                txt = f"{v:.4f}"
            else:
                txt = str(v)
            if hi_col and c == hi_col:
                try:
                    mn = df[c].min(); mx = df[c].max()
                    t  = (float(v)-mn)/(mx-mn) if mx!=mn else 1.0
                    g  = int(100 + 85*t)
                    sty = f"background:rgba(30,{g},60,0.5);font-weight:600;"
                except: pass
            if rank_col and c == rank_col:
                try:
                    rv = int(v)
                    if rv == 1:   sty = "background:#2ea04340;color:#3fb950;font-weight:700;"; txt = f"1"
                    elif rv == 2: sty = "background:#9e6a0330;color:#ffa657;font-weight:600;"; txt = f"2"
                    elif rv == 3: sty = "background:#6e40c920;color:#d2a8ff;font-weight:500;"; txt = f"3"
                except: pass
            cells += f'<td style="padding:9px 14px;text-align:center;border:1px solid #21262d;color:#e6edf3;{sty}">{txt}</td>'
        rows += f"<tr>{cells}</tr>"
    hdrs = "".join(f'<th style="background:#1f6feb;color:#fff;padding:10px 14px;text-align:center;border:1px solid #30363d;font-weight:600">{c}</th>' for c in df.columns)
    return f'<div style="overflow-x:auto"><table class="spk-table"><thead><tr>{hdrs}</tr></thead><tbody>{rows}</tbody></table></div>'

def show_table(df, caption="", hi_col=None, rank_col=None, fmt=None):
    if caption:
        st.markdown(f'<p style="color:#8b949e;font-size:12px;margin:0 0 4px">{caption}</p>', unsafe_allow_html=True)
    st.markdown(spk_table(df, hi_col, rank_col, fmt), unsafe_allow_html=True)
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ─── SPK Functions ───────────────────────────────────────────
def calc_saw(df, bobot, jenis):
    R = df.copy().astype(float)
    for j, kri in enumerate(df.columns):
        col = df[kri]
        R[kri] = col / col.max() if jenis[j]=="Benefit" else col.min() / col
    scores = R.multiply(bobot, axis="columns").sum(axis=1)
    return R, scores

def calc_smart(df, bobot, jenis):
    U = df.copy().astype(float)
    for j, kri in enumerate(df.columns):
        col = df[kri]; cmx = col.max(); cmn = col.min(); dn = cmx - cmn
        if abs(dn) < 1e-9: U[kri] = 1.0
        elif jenis[j]=="Benefit": U[kri] = (col - cmn) / dn
        else:                     U[kri] = (cmx - col) / dn
    scores = U.multiply(bobot, axis="columns").sum(axis=1)
    return U, scores

def calc_moora(df, bobot, jenis):
    X = df.copy().astype(float)
    for kri in df.columns:
        col = df[kri]; dn = np.sqrt((col**2).sum())
        X[kri] = col / dn if dn > 0 else 0
    Xw = X.multiply(bobot, axis="columns")
    bcols = [df.columns[j] for j in range(len(jenis)) if jenis[j]=="Benefit"]
    ccols = [df.columns[j] for j in range(len(jenis)) if jenis[j]=="Cost"]
    b = Xw[bcols].sum(axis=1) if bcols else pd.Series(0, index=df.index)
    c = Xw[ccols].sum(axis=1) if ccols else pd.Series(0, index=df.index)
    return X, Xw, b, c, b - c

def calc_wp(df, bobot, jenis):
    bwp = np.array([b if jenis[j]=="Benefit" else -b for j,b in enumerate(bobot)])
    dfc = df.clip(lower=1e-9)
    S   = np.array([np.prod(dfc.loc[alt].values ** bwp) for alt in df.index])
    V   = S / S.sum()
    return bwp, S, V

def get_ranking(scores):
    return scores.rank(ascending=False, method="min").astype(int)

def minmax_norm(s):
    mn, mx = s.min(), s.max()
    return (s - mn)/(mx - mn) if mx != mn else s*0 + 0.5

# ─── Plot helpers ────────────────────────────────────────────
def bar_chart(labels, values, title, ylabel, best_label="", color_list=None):
    fig, ax = plt.subplots(figsize=(max(8, len(labels)*1.6), 5))
    cl = color_list or [COLORS[i % len(COLORS)] for i in range(len(labels))]
    order = np.argsort(values)[::-1]
    xl = [labels[i] for i in order]
    yv = [values[i] for i in order]
    cl_ord = [cl[i] for i in order]
    bars = ax.bar(xl, yv, color=cl_ord, edgecolor="#30363d", linewidth=1.2, zorder=3)
    bars[0].set_edgecolor("#ffd700"); bars[0].set_linewidth(2.5)
    for b in bars:
        v = b.get_height()
        ax.text(b.get_x()+b.get_width()/2, v + abs(v)*0.02 + 1e-6,
                f"{v:.4f}", ha="center", va="bottom", fontsize=9.5,
                color="#e6edf3", fontweight="bold")
    ax.set_title(title, pad=12)
    ax.set_xlabel("Pendaftar"); ax.set_ylabel(ylabel)
    ylim = max(abs(v) for v in yv) * 1.22
    ax.set_ylim((min(0, min(yv) - ylim*0.08)), ylim if ylim > 0 else 1)
    ax.axhline(0, color="#8b949e", linewidth=0.8, linestyle="--", alpha=0.6)
    ax.yaxis.grid(True, linestyle="--", alpha=0.4, zorder=0); ax.set_axisbelow(True)
    if best_label:
        ax.text(0.98, 0.97, f"Terbaik: {best_label}", transform=ax.transAxes,
                ha="right", va="top", fontsize=10.5, color="#ffd700", fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.4", fc="#21262d", ec="#ffd700", alpha=0.9))
    rot = 25 if max((len(l) for l in labels), default=0) > 7 else 0
    plt.xticks(rotation=rot, ha="right" if rot else "center")
    plt.tight_layout()
    return fig

# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:20px 0 16px">
      <div style="font-size:32px">&#9733;</div>
      <div style="font-size:17px;font-weight:700;color:#e6edf3;margin-top:6px">SPK Beasiswa</div>
      <div style="font-size:12px;color:#8b949e;margin-top:4px">Sistem Pendukung Keputusan</div>
    </div>
    <hr style="border-color:#30363d;margin:0 0 16px">
    """, unsafe_allow_html=True)

    st.markdown('<div style="font-size:12px;color:#8b949e;font-weight:600;letter-spacing:.5px;margin-bottom:8px">METODE AKTIF</div>', unsafe_allow_html=True)
    use_saw   = st.checkbox("SAW",   value=True)
    use_smart = st.checkbox("SMART", value=True)
    use_moora = st.checkbox("MOORA", value=True)
    use_wp    = st.checkbox("WP",    value=True)

    st.markdown("<hr style='border-color:#30363d;margin:16px 0'>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:12px;color:#8b949e;font-weight:600;letter-spacing:.5px;margin-bottom:8px">KRITERIA PENILAIAN</div>', unsafe_allow_html=True)
    for k in KRITERIA:
        color = "#79c0ff" if k["jenis"]=="Benefit" else "#f78166"
        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;align-items:center;
                    padding:6px 0;border-bottom:1px solid #21262d">
          <span style="color:#e6edf3;font-size:13px">{k['kode']} — {k['nama']}</span>
          <span style="color:{color};font-size:12px;font-weight:600">{k['bobot']:.2f}</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#30363d;margin:16px 0'>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:11px;color:#8b949e;text-align:center">v1.0 &nbsp;|&nbsp; SAW · SMART · MOORA · WP</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(135deg,#0d1117 0%,#161b22 100%);
            border:1px solid #30363d;border-radius:14px;
            padding:28px 32px;margin-bottom:24px">
  <div style="display:flex;align-items:center;gap:16px">
    <div style="font-size:42px;line-height:1">&#9733;</div>
    <div>
      <h1 style="margin:0;font-size:22px;font-weight:700;color:#e6edf3">
        Sistem Pendukung Keputusan</h1>
      <p style="margin:4px 0 0;font-size:14px;color:#8b949e">
        Seleksi Penerima Beasiswa &nbsp;·&nbsp; SAW &nbsp;·&nbsp; SMART &nbsp;·&nbsp; MOORA &nbsp;·&nbsp; Weighted Product</p>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# TAB LAYOUT
# ─────────────────────────────────────────────────────────────
tab_input, tab_saw, tab_smart, tab_moora, tab_wp, tab_compare, tab_result = st.tabs([
    "Input Data", "SAW", "SMART", "MOORA", "WP", "Perbandingan", "Kesimpulan"
])

# ══════════════════════════════════════════════════
# TAB 1 — INPUT DATA
# ══════════════════════════════════════════════════
with tab_input:
    st.markdown('<div class="section-header">Kriteria & Bobot Penilaian</div>', unsafe_allow_html=True)

    # Tabel kriteria
    rows_k = ""
    for i, k in enumerate(KRITERIA):
        bg   = "#161b22" if i%2==0 else "#1c2128"
        jbdg = "benefit" if k["jenis"]=="Benefit" else "cost"
        rows_k += (f'<tr style="background:{bg}">'
                   f'<td style="padding:9px 14px;text-align:center;border:1px solid #21262d;color:#8b949e;font-weight:600">{k["kode"]}</td>'
                   f'<td style="padding:9px 14px;border:1px solid #21262d;color:#e6edf3;font-weight:500">{k["nama"]}</td>'
                   f'<td style="padding:9px 14px;text-align:center;border:1px solid #21262d;color:#8b949e">{k["satuan"]}</td>'
                   f'<td style="padding:9px 14px;text-align:center;border:1px solid #21262d"><span class="badge-{jbdg}">{k["jenis"]}</span></td>'
                   f'<td style="padding:9px 14px;text-align:center;border:1px solid #21262d;color:#e6edf3;font-weight:600">{k["bobot"]:.2f}</td>'
                   f'</tr>')
    rows_k += (f'<tr style="background:#21262d">'
               f'<td colspan="4" style="padding:9px 14px;text-align:right;border:1px solid #21262d;color:#8b949e;font-weight:600">Total Bobot</td>'
               f'<td style="padding:9px 14px;text-align:center;border:1px solid #21262d;color:#3fb950;font-weight:700">{K_BOBOT.sum():.2f}</td>'
               f'</tr>')
    hdrs_k = "".join(f'<th style="background:#1f6feb;color:#fff;padding:10px 14px;text-align:center;border:1px solid #30363d;font-weight:600">{c}</th>'
                     for c in ["Kode","Kriteria","Satuan","Jenis","Bobot"])
    st.markdown(f'<div style="overflow-x:auto"><table class="spk-table"><thead><tr>{hdrs_k}</tr></thead><tbody>{rows_k}</tbody></table></div>',
                unsafe_allow_html=True)
    st.caption("Benefit = nilai lebih tinggi lebih baik  ·  Cost = nilai lebih rendah lebih baik")

    st.markdown("---")
    st.markdown('<div class="section-header">Data Pendaftar Beasiswa</div>', unsafe_allow_html=True)

    col_l, col_r = st.columns([1, 3])
    with col_l:
        n_alt = st.number_input("Jumlah pendaftar", min_value=2, max_value=20, value=3, step=1)

    st.markdown(f'<div class="info-card" style="margin-bottom:16px"><span style="color:#8b949e;font-size:13px">Masukkan data untuk <b style="color:#58a6ff">{int(n_alt)}</b> pendaftar berikut.</span></div>',
                unsafe_allow_html=True)

    # Inisiasi / reset session state saat jumlah pendaftar berubah
    n_alt_int = int(n_alt)
    default_row = [3.5, 2000000.0, 80.0, 8.0, 2.0]

    if "names" not in st.session_state or len(st.session_state.names) != n_alt_int:
        st.session_state.names  = [f"Pendaftar {i+1}" for i in range(n_alt_int)]
        st.session_state.data_values = [default_row.copy() for _ in range(n_alt_int)]

    # Pastikan panjang values selalu sama dengan n_alt (jaga-jaga)
    while len(st.session_state.data_values) < n_alt_int:
        st.session_state.data_values.append(default_row.copy())
    while len(st.session_state.names) < n_alt_int:
        st.session_state.names.append(f"Pendaftar {len(st.session_state.names)+1}")

    # Form input
    with st.form("input_form"):
        names_input  = []
        values_input = []

        cols_head = st.columns([2] + [1]*5)
        cols_head[0].markdown('<div style="font-size:12px;color:#8b949e;font-weight:600;padding:4px 0">NAMA PENDAFTAR</div>', unsafe_allow_html=True)
        for ci, k in enumerate(KRITERIA):
            cols_head[ci+1].markdown(f'<div style="font-size:11px;color:#8b949e;font-weight:600;padding:4px 0;text-align:center">{k["kode"]}<br><span style="color:#58a6ff">{k["bobot"]:.2f}</span></div>', unsafe_allow_html=True)

        for i in range(n_alt_int):
            cols = st.columns([2] + [1]*5)
            name = cols[0].text_input(f"Nama {i+1}", value=st.session_state.names[i],
                                      label_visibility="collapsed", key=f"name_{i}")
            names_input.append(name.strip() or f"Pendaftar {i+1}")
            row_vals = []
            for j, k in enumerate(KRITERIA):
                lo, hi, step, def_v = INPUT_CFG[k["nama"]]
                saved_val = st.session_state.data_values[i][j] if j < len(st.session_state.data_values[i]) else def_v
                v = cols[j+1].number_input(
                    k["nama"], min_value=float(lo), max_value=float(hi),
                    value=float(saved_val),
                    step=float(step), label_visibility="collapsed", key=f"val_{i}_{j}"
                )
                row_vals.append(v)
            values_input.append(row_vals)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Jalankan Analisis SPK", use_container_width=True)

    if submitted:
        st.session_state.names  = names_input
        st.session_state.data_values = values_input
        st.session_state.ready  = True
        st.success("Data berhasil disimpan. Buka tab metode atau Kesimpulan untuk melihat hasil.")

    # Preview matriks
    if st.session_state.get("ready"):
        st.markdown('<div class="section-header" style="border-color:#3fb950">Matriks Keputusan</div>', unsafe_allow_html=True)
        df_mx = pd.DataFrame(st.session_state.data_values,
                             index=st.session_state.names, columns=K_NAMA)
        df_show = df_mx.reset_index().rename(columns={"index":"Pendaftar"})
        show_table(df_show, "Tabel 1. Matriks Keputusan Awal (X)",
                   fmt={"Penghasilan Ortu":"Rp {:,.0f}"})

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Pendaftar", int(n_alt))
        c2.metric("Kriteria", 5)
        c3.metric("Total Bobot", f"{K_BOBOT.sum():.2f}")
        c4.metric("Metode Aktif", sum([use_saw, use_smart, use_moora, use_wp]))

# ── Pastikan data tersedia ────────────────────────────────────
if not st.session_state.get("ready", False):
    for tab in [tab_saw, tab_smart, tab_moora, tab_wp, tab_compare, tab_result]:
        with tab:
            st.info("Isi dan kirim form di tab **Input Data** terlebih dahulu.")
    st.stop()

# ── Siapkan data ─────────────────────────────────────────────
alternatif = st.session_state.names
df_matrix  = pd.DataFrame(st.session_state.data_values, index=alternatif, columns=K_NAMA)

# Hitung semua metode
R_saw,   saw_sc   = calc_saw(df_matrix,   K_BOBOT, K_JENIS)
U_smart, smart_sc = calc_smart(df_matrix, K_BOBOT, K_JENIS)
X_nm, X_wm, b_sum, c_sum, moora_sc = calc_moora(df_matrix, K_BOBOT, K_JENIS)
bwp, S_wp, V_wp   = calc_wp(df_matrix, K_BOBOT, K_JENIS)
wp_sc = pd.Series(V_wp, index=alternatif)

rk_saw   = get_ranking(saw_sc)
rk_smart = get_ranking(smart_sc)
rk_moora = get_ranking(moora_sc)
rk_wp    = get_ranking(wp_sc)

def best_of(scores): return scores.idxmin() if scores.name=="rank" else scores.idxmax()
best_saw   = saw_sc.idxmax();   best_saw_v   = saw_sc.max()
best_smart = smart_sc.idxmax(); best_smart_v = smart_sc.max()
best_moora = moora_sc.idxmax(); best_moora_v = moora_sc.max()
best_wp    = wp_sc.idxmax();    best_wp_v    = wp_sc.max()

n_alt_i = len(alternatif)

# ══════════════════════════════════════════════════
# TAB 2 — SAW
# ══════════════════════════════════════════════════
with tab_saw:
    if not use_saw:
        st.info("Metode SAW tidak diaktifkan. Centang SAW di sidebar.")
    else:
        st.markdown('<div class="section-header">Simple Additive Weighting (SAW)</div>', unsafe_allow_html=True)
        with st.expander("Konsep & Rumus", expanded=False):
            st.markdown(r"""
**SAW** mencari penjumlahan terbobot dari rating kinerja yang telah dinormalisasi.

Normalisasi:
$$r_{ij} = \begin{cases} \dfrac{x_{ij}}{\max_i(x_{ij})} & \text{Benefit} \\[6pt] \dfrac{\min_i(x_{ij})}{x_{ij}} & \text{Cost} \end{cases}$$

Skor akhir: $V_i = \sum_{j=1}^{n} w_j \cdot r_{ij}$
""")
        t1, t2, t3 = st.tabs(["Normalisasi", "Terbobot", "Hasil"])
        with t1:
            show_table(R_saw.reset_index().rename(columns={"index":"Pendaftar"}),
                       "Matriks Normalisasi (R)")
        with t2:
            df_saw_w = R_saw.multiply(K_BOBOT, axis="columns")
            show_table(df_saw_w.reset_index().rename(columns={"index":"Pendaftar"}),
                       "Matriks Terbobot (R x W)")
        with t3:
            df_sr = pd.DataFrame({
                "Pendaftar": alternatif,
                "Skor Vi"  : saw_sc.values,
                "Ranking"  : rk_saw.values,
            }).sort_values("Ranking").reset_index(drop=True)
            show_table(df_sr, "Skor Akhir dan Ranking SAW", hi_col="Skor Vi", rank_col="Ranking")
            st.markdown(f'<div style="background:#2ea04320;border:1px solid #3fb950;border-radius:8px;padding:12px 16px;margin-top:8px">Terbaik SAW: <b style="color:#3fb950">{best_saw}</b> &nbsp;—&nbsp; Vi = {best_saw_v:.4f}</div>', unsafe_allow_html=True)

        st.markdown("---")
        fig = bar_chart(alternatif, saw_sc.values, "Skor SAW per Pendaftar", "Skor Vi", best_saw)
        st.pyplot(fig); plt.close()

# ══════════════════════════════════════════════════
# TAB 3 — SMART
# ══════════════════════════════════════════════════
with tab_smart:
    if not use_smart:
        st.info("Metode SMART tidak diaktifkan.")
    else:
        st.markdown('<div class="section-header" style="border-color:#3fb950">Simple Multi-Attribute Rating Technique (SMART)</div>', unsafe_allow_html=True)
        with st.expander("Konsep & Rumus", expanded=False):
            st.markdown(r"""
**SMART** menghitung nilai utilitas yang memetakan nilai aktual ke [0,1].

$$U_{ij} = \begin{cases} \dfrac{x_{ij}-\min}{\max-\min} & \text{Benefit} \\[6pt] \dfrac{\max-x_{ij}}{\max-\min} & \text{Cost} \end{cases}$$

Skor akhir: $S_i = \sum_{j=1}^{n} w_j \cdot U_{ij}$
""")
        t1, t2, t3 = st.tabs(["Utilitas", "Terbobot", "Hasil"])
        with t1:
            show_table(U_smart.reset_index().rename(columns={"index":"Pendaftar"}),
                       "Matriks Nilai Utilitas U(xij)")
        with t2:
            U_w = U_smart.multiply(K_BOBOT, axis="columns")
            show_table(U_w.reset_index().rename(columns={"index":"Pendaftar"}),
                       "Utilitas Terbobot (U x W)")
        with t3:
            df_smr = pd.DataFrame({
                "Pendaftar": alternatif,
                "Skor Si"  : smart_sc.values,
                "Ranking"  : rk_smart.values,
            }).sort_values("Ranking").reset_index(drop=True)
            show_table(df_smr, "Skor Akhir dan Ranking SMART", hi_col="Skor Si", rank_col="Ranking")
            st.markdown(f'<div style="background:#2ea04320;border:1px solid #3fb950;border-radius:8px;padding:12px 16px;margin-top:8px">Terbaik SMART: <b style="color:#3fb950">{best_smart}</b> &nbsp;—&nbsp; Si = {best_smart_v:.4f}</div>', unsafe_allow_html=True)

        st.markdown("---")
        fig = bar_chart(alternatif, smart_sc.values, "Skor SMART per Pendaftar", "Skor Utilitas Si", best_smart,
                        color_list=[MC["SMART"]]*n_alt_i)
        st.pyplot(fig); plt.close()

# ══════════════════════════════════════════════════
# TAB 4 — MOORA
# ══════════════════════════════════════════════════
with tab_moora:
    if not use_moora:
        st.info("Metode MOORA tidak diaktifkan.")
    else:
        st.markdown('<div class="section-header" style="border-color:#f78166">Multi-Objective Optimization on the Basis of Ratio Analysis (MOORA)</div>', unsafe_allow_html=True)
        with st.expander("Konsep & Rumus", expanded=False):
            st.markdown(r"""
**MOORA** menggunakan normalisasi berbasis rasio akar kuadrat.

$$x^*_{ij} = \frac{x_{ij}}{\sqrt{\sum_{i=1}^{m} x_{ij}^2}}$$

Skor akhir: $Y_i = \sum_{j \in \text{Benefit}} w_j x^*_{ij} - \sum_{j \in \text{Cost}} w_j x^*_{ij}$
""")
        t1, t2, t3 = st.tabs(["Normalisasi", "Terbobot", "Hasil"])
        with t1:
            show_table(X_nm.reset_index().rename(columns={"index":"Pendaftar"}),
                       "Matriks Normalisasi Rasio (x*)")
        with t2:
            show_table(X_wm.reset_index().rename(columns={"index":"Pendaftar"}),
                       "Matriks Normalisasi Terbobot (w x x*)")
        with t3:
            df_mor = pd.DataFrame({
                "Pendaftar"   : alternatif,
                "Sigma Benefit": b_sum.values,
                "Sigma Cost"  : c_sum.values,
                "Skor Yi"     : moora_sc.values,
                "Ranking"     : rk_moora.values,
            }).sort_values("Ranking").reset_index(drop=True)
            show_table(df_mor, "Skor Akhir dan Ranking MOORA", hi_col="Skor Yi", rank_col="Ranking")
            st.markdown(f'<div style="background:#f7816620;border:1px solid #f78166;border-radius:8px;padding:12px 16px;margin-top:8px">Terbaik MOORA: <b style="color:#f78166">{best_moora}</b> &nbsp;—&nbsp; Yi = {best_moora_v:.4f}</div>', unsafe_allow_html=True)

        st.markdown("---")
        fig = bar_chart(alternatif, moora_sc.values, "Skor MOORA per Pendaftar", "Skor Yi", best_moora,
                        color_list=["#3fb950" if v>=0 else "#f78166" for v in moora_sc.values])
        st.pyplot(fig); plt.close()

# ══════════════════════════════════════════════════
# TAB 5 — WP
# ══════════════════════════════════════════════════
with tab_wp:
    if not use_wp:
        st.info("Metode WP tidak diaktifkan.")
    else:
        st.markdown('<div class="section-header" style="border-color:#d2a8ff">Weighted Product (WP)</div>', unsafe_allow_html=True)
        with st.expander("Konsep & Rumus", expanded=False):
            st.markdown(r"""
**WP** menggunakan perkalian nilai berpangkat bobot. Benefit = pangkat positif, Cost = pangkat negatif.

$$S_i = \prod_{j=1}^{n} x_{ij}^{w_j} \qquad V_i = \frac{S_i}{\sum_{k=1}^{m} S_k}$$
""")
        t1, t2 = st.tabs(["Vektor S", "Vektor V & Ranking"])
        with t1:
            df_sv = pd.DataFrame({"Pendaftar": alternatif, "Vektor S": S_wp})
            show_table(df_sv, "Vektor S (Si)", fmt={"Vektor S": "{:.6f}"})
        with t2:
            df_vv = pd.DataFrame({
                "Pendaftar": alternatif,
                "Vektor S" : S_wp,
                "Vektor V" : V_wp,
                "Ranking"  : rk_wp.values,
            }).sort_values("Ranking").reset_index(drop=True)
            show_table(df_vv, "Vektor V dan Ranking WP",
                       hi_col="Vektor V", rank_col="Ranking",
                       fmt={"Vektor S":"{:.6f}","Vektor V":"{:.4f}"})
            st.markdown(f'<div style="background:#d2a8ff20;border:1px solid #d2a8ff;border-radius:8px;padding:12px 16px;margin-top:8px">Terbaik WP: <b style="color:#d2a8ff">{best_wp}</b> &nbsp;—&nbsp; Vi = {best_wp_v:.4f}</div>', unsafe_allow_html=True)

        st.markdown("---")
        fig = bar_chart(alternatif, wp_sc.values, "Skor WP per Pendaftar", "Vektor Vi", best_wp,
                        color_list=[MC["WP"]]*n_alt_i)
        st.pyplot(fig); plt.close()

# ══════════════════════════════════════════════════
# TAB 6 — PERBANDINGAN
# ══════════════════════════════════════════════════
with tab_compare:
    st.markdown('<div class="section-header">Perbandingan Seluruh Metode</div>', unsafe_allow_html=True)

    # Skor
    df_cmp = pd.DataFrame({
        "Pendaftar": alternatif,
        "SAW"       : saw_sc.values,
        "SMART"     : smart_sc.values,
        "MOORA"     : moora_sc.values,
        "WP"        : wp_sc.values,
    })
    show_table(df_cmp, "Perbandingan Skor Semua Metode")

    st.markdown("<br>", unsafe_allow_html=True)

    # Ranking
    df_rk = pd.DataFrame({
        "Pendaftar" : alternatif,
        "Rank SAW"  : rk_saw.values,
        "Rank SMART": rk_smart.values,
        "Rank MOORA": rk_moora.values,
        "Rank WP"   : rk_wp.values,
    })
    show_table(df_rk, "Perbandingan Ranking Semua Metode",
               rank_col="Rank SAW")

    st.markdown("---")

    # Grafik grouped bar
    ns = {m: minmax_norm(s).values for m, s in
          [("SAW",saw_sc),("SMART",smart_sc),("MOORA",moora_sc),("WP",wp_sc)]}

    fig, ax = plt.subplots(figsize=(max(11, n_alt_i*2.2), 5.5))
    x = np.arange(n_alt_i); w = 0.18
    for mth, off in zip(["SAW","SMART","MOORA","WP"], [-1.5,-0.5,0.5,1.5]):
        ax.bar(x+off*w, ns[mth], w, label=mth, color=MC[mth],
               edgecolor="#30363d", linewidth=0.8, alpha=0.9, zorder=3)
    ax.set_xticks(x)
    rot = 25 if max((len(a) for a in alternatif), default=0) > 7 else 0
    ax.set_xticklabels(alternatif, rotation=rot, ha="right" if rot else "center")
    ax.set_title("Perbandingan Skor Antar Metode (Ternormalisasi 0–1)", pad=14)
    ax.set_xlabel("Pendaftar"); ax.set_ylabel("Skor Ternormalisasi")
    ax.legend(loc="upper right", framealpha=0.3, fontsize=11)
    ax.set_ylim(0, 1.25)
    ax.yaxis.grid(True, linestyle="--", alpha=0.4, zorder=0); ax.set_axisbelow(True)
    plt.tight_layout()
    st.pyplot(fig); plt.close()

    # Heatmap
    rmt = np.array([rk_saw.values, rk_smart.values, rk_moora.values, rk_wp.values])
    fig2, ax2 = plt.subplots(figsize=(max(8, n_alt_i*1.5), 4))
    sns.heatmap(rmt, annot=True, fmt="d", cmap="YlOrRd_r",
                xticklabels=alternatif,
                yticklabels=["SAW","SMART","MOORA","WP"],
                ax=ax2, linewidths=0.5, linecolor="#30363d",
                cbar_kws={"label":"Ranking"})
    ax2.set_title("Heatmap Ranking — Semua Metode", pad=14)
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=rot, ha="right" if rot else "center")
    plt.tight_layout()
    st.pyplot(fig2); plt.close()

# ══════════════════════════════════════════════════
# TAB 7 — KESIMPULAN
# ══════════════════════════════════════════════════
with tab_result:
    st.markdown('<div class="section-header" style="border-color:#3fb950">Kesimpulan & Rekomendasi Penerima Beasiswa</div>', unsafe_allow_html=True)

    best_per = {"SAW":best_saw,"SMART":best_smart,"MOORA":best_moora,"WP":best_wp}
    r1cnt    = Counter(best_per.values())

    avg_r = {}
    for alt in alternatif:
        avg_r[alt] = np.mean([rk_saw[alt], rk_smart[alt], rk_moora[alt], rk_wp[alt]])

    final    = sorted(avg_r.items(), key=lambda x: x[1])
    best_all = final[0][0]
    best_avg = final[0][1]
    best_n   = r1cnt[best_all]
    all_same = len(set(best_per.values())) == 1

    # Kartu pemenang
    st.markdown(f"""
    <div class="result-box">
      <div class="winner-sub">Rekomendasi Penerima Beasiswa</div>
      <div class="winner-name">&#9733; {best_all}</div>
      <div class="winner-sub">Didukung {best_n}/4 metode &nbsp;·&nbsp; Rata-rata Ranking {best_avg:.2f}</div>
    </div>
    """, unsafe_allow_html=True)

    # Ringkasan metode (kartu 4 kolom)
    c1, c2, c3, c4 = st.columns(4)
    for col, (mth, bst, sc, clr) in zip(
        [c1,c2,c3,c4],
        [("SAW",best_saw,best_saw_v,"#58a6ff"),
         ("SMART",best_smart,best_smart_v,"#3fb950"),
         ("MOORA",best_moora,best_moora_v,"#f78166"),
         ("WP",best_wp,best_wp_v,"#d2a8ff")]
    ):
        col.markdown(f"""
        <div style="background:#161b22;border:1px solid #30363d;border-top:3px solid {clr};
                    border-radius:8px;padding:14px;text-align:center">
          <div style="font-size:11px;color:#8b949e;font-weight:600;letter-spacing:.5px">{mth}</div>
          <div style="font-size:14px;font-weight:700;color:#e6edf3;margin:6px 0">{bst}</div>
          <div style="font-size:12px;color:{clr}">{sc:.4f}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Ranking akhir
    df_fin = pd.DataFrame([{
        "Rank Akhir"     : i+1,
        "Pendaftar"      : alt,
        "Avg Rank"       : round(avg, 2),
        "Dipilih Metode" : f"{r1cnt.get(alt,0)}/4",
    } for i, (alt, avg) in enumerate(final)])
    show_table(df_fin, "Ranking Akhir Keseluruhan (berdasarkan rata-rata ranking)", rank_col="Rank Akhir")

    # Statistik
    st.markdown("<br>", unsafe_allow_html=True)
    df_st = pd.DataFrame({
        "Statistik": ["Min","Max","Rata-rata","Std Deviasi"],
        "SAW"  : [f"{saw_sc.min():.4f}",f"{saw_sc.max():.4f}",f"{saw_sc.mean():.4f}",f"{saw_sc.std():.4f}"],
        "SMART": [f"{smart_sc.min():.4f}",f"{smart_sc.max():.4f}",f"{smart_sc.mean():.4f}",f"{smart_sc.std():.4f}"],
        "MOORA": [f"{moora_sc.min():.4f}",f"{moora_sc.max():.4f}",f"{moora_sc.mean():.4f}",f"{moora_sc.std():.4f}"],
        "WP"   : [f"{wp_sc.min():.4f}",f"{wp_sc.max():.4f}",f"{wp_sc.mean():.4f}",f"{wp_sc.std():.4f}"],
    })
    show_table(df_st, "Statistik Skor per Metode")

    # Grafik ringkasan
    st.markdown("---")
    fig, axes = plt.subplots(1, 2, figsize=(max(14, n_alt_i*2.4), 5.5))
    ax1, ax2  = axes

    freq = [r1cnt.get(a,0) for a in alternatif]
    bars1 = ax1.bar(alternatif, freq,
                    color=[COLORS[i%len(COLORS)] for i in range(n_alt_i)],
                    edgecolor="#30363d", linewidth=1.2, zorder=3)
    for b,v in zip(bars1, freq):
        ax1.text(b.get_x()+b.get_width()/2, b.get_height()+0.06,
                 f"{v}", ha="center", va="bottom",
                 fontsize=11, color="#e6edf3", fontweight="bold")
    ax1.set_title("Frekuensi Peringkat 1", pad=12)
    ax1.set_xlabel("Pendaftar"); ax1.set_ylabel("Jumlah Metode")
    ax1.set_ylim(0, 4.9); ax1.set_yticks(range(5))
    ax1.yaxis.grid(True, linestyle="--", alpha=0.4, zorder=0); ax1.set_axisbelow(True)
    rot = 25 if max((len(a) for a in alternatif), default=0) > 7 else 0
    plt.setp(ax1.get_xticklabels(), rotation=rot, ha="right" if rot else "center")

    sp   = sorted(zip(alternatif, [avg_r[a] for a in alternatif]), key=lambda x:x[1])
    sa, sv = zip(*sp)
    barcols2 = [COLORS[i%len(COLORS)] for i in range(n_alt_i)]
    bars2 = ax2.barh(list(sa)[::-1], list(sv)[::-1],
                     color=barcols2[::-1], edgecolor="#30363d", linewidth=1.2, zorder=3)
    bars2[-1].set_edgecolor("#ffd700"); bars2[-1].set_linewidth(2.5)
    for b, v in zip(bars2, list(sv)[::-1]):
        ax2.text(b.get_width()+0.04, b.get_y()+b.get_height()/2,
                 f"{v:.2f}", ha="left", va="center",
                 fontsize=10, color="#e6edf3", fontweight="bold")
    ax2.set_title("Rata-rata Ranking (lebih kecil = lebih baik)", pad=12)
    ax2.set_xlabel("Avg Rank"); ax2.set_ylabel("Pendaftar")
    ax2.xaxis.grid(True, linestyle="--", alpha=0.4, zorder=0); ax2.set_axisbelow(True)
    ax2.set_xlim(0, n_alt_i + 0.8)

    plt.suptitle("Ringkasan Akhir SPK — Seleksi Beasiswa", fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    st.pyplot(fig); plt.close()

    # Narasi
    st.markdown("---")
    st.markdown('<div class="section-header" style="border-color:#8b949e">Analisis Hasil</div>', unsafe_allow_html=True)
    consist_txt = ("Keempat metode menghasilkan pilihan yang seragam, menunjukkan konsistensi yang tinggi dalam proses seleksi ini."
                   if all_same else
                   f"Terdapat variasi hasil antar metode. Keputusan akhir diambil berdasarkan rata-rata ranking keempat metode.")
    st.markdown(f"""
    <div class="info-card">
      <p style="color:#e6edf3;font-size:14px;line-height:1.75;margin:0">
        Proses seleksi mengevaluasi <b>{n_alt_i} pendaftar</b> menggunakan 5 kriteria melalui
        4 metode SPK: SAW, SMART, MOORA, dan Weighted Product.<br><br>
        {consist_txt}<br><br>
        Pendaftar <b style="color:#ffd700">{best_all}</b> menempati posisi teratas dengan
        rata-rata ranking <b>{best_avg:.2f}</b> dan dipilih oleh <b>{best_n} dari 4 metode</b>,
        sehingga menjadi kandidat paling layak untuk menerima beasiswa berdasarkan kriteria
        yang telah ditetapkan.
      </p>
    </div>
    """, unsafe_allow_html=True)