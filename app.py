import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(page_title="SPK Seleksi Beasiswa", page_icon="",
                   layout="wide", initial_sidebar_state="expanded")

# ── CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif!important}
section[data-testid="stSidebar"]{background:#0d1117!important;border-right:1px solid #21262d}
section[data-testid="stSidebar"] *{color:#e6edf3!important}
[data-testid="metric-container"]{background:#161b22!important;border:1px solid #30363d!important;border-radius:12px!important;padding:16px 20px!important}
[data-testid="metric-container"] label{color:#8b949e!important;font-size:11px!important;text-transform:uppercase;letter-spacing:.6px}
[data-testid="metric-container"] [data-testid="metric-value"]{color:#e6edf3!important;font-size:26px!important;font-weight:700!important}
button[data-baseweb="tab"]{background:transparent!important;color:#8b949e!important;border-bottom:2px solid transparent!important;font-weight:500!important;font-size:14px!important;padding:10px 18px!important}
button[data-baseweb="tab"][aria-selected="true"]{color:#58a6ff!important;border-bottom:2px solid #58a6ff!important;font-weight:600!important}
.stButton>button{background:linear-gradient(135deg,#1f6feb,#388bfd)!important;color:white!important;border:none!important;border-radius:10px!important;font-weight:600!important;padding:12px 28px!important;transition:all .2s!important}
.stButton>button:hover{transform:translateY(-2px)!important;box-shadow:0 6px 20px #1f6feb55!important}
.stNumberInput input,.stTextInput input{background:#161b22!important;border:1px solid #30363d!important;color:#e6edf3!important;border-radius:8px!important;font-size:13px!important}
details{background:#161b22!important;border:1px solid #30363d!important;border-radius:10px!important}
details summary{padding:12px 16px!important;font-weight:600!important;color:#e6edf3!important}
::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-track{background:#0d1117}
::-webkit-scrollbar-thumb{background:#30363d;border-radius:3px}
hr{border-color:#21262d!important;margin:20px 0!important}
.badge-b{background:#0d419d33;color:#79c0ff;font-weight:600;padding:3px 10px;border-radius:6px;font-size:12px}
.badge-c{background:#da363333;color:#f78166;font-weight:600;padding:3px 10px;border-radius:6px;font-size:12px}
.spk-table{width:100%;border-collapse:collapse;font-size:13px;font-family:'Inter',sans-serif}
.spk-table thead th{background:#1f6feb;color:#fff;padding:11px 14px;text-align:center;border:1px solid #30363d;font-weight:600}
.spk-table tbody tr:nth-child(odd){background:#161b22}
.spk-table tbody tr:nth-child(even){background:#1c2128}
.spk-table tbody td{padding:9px 14px;text-align:center;border:1px solid #21262d;color:#e6edf3}
.spk-table tbody tr:hover{background:#21262d;transition:.15s}
.sec-hdr{background:linear-gradient(90deg,#1f6feb22,transparent);border-left:4px solid #1f6feb;border-radius:0 10px 10px 0;padding:11px 18px;margin:22px 0 14px;font-size:15px;font-weight:700;color:#e6edf3}
.formula-box{background:#161b22;border:1px solid #30363d;border-left:4px solid #58a6ff;border-radius:0 10px 10px 0;padding:16px 20px;margin:12px 0}
.formula-title{font-size:13px;font-weight:700;color:#58a6ff;margin-bottom:8px;text-transform:uppercase;letter-spacing:.5px}
.formula-desc{font-size:13px;color:#8b949e;line-height:1.7;margin-top:8px}
.step-box{background:#161b22;border:1px solid #21262d;border-radius:10px;padding:14px 18px;margin:10px 0}
.step-num{display:inline-block;background:#1f6feb;color:white;font-weight:700;width:24px;height:24px;border-radius:50%;text-align:center;line-height:24px;font-size:12px;margin-right:10px}
.result-card{background:linear-gradient(135deg,#0d1117,#161b22);border:2px solid #ffd700;border-radius:14px;padding:28px;text-align:center;margin:18px 0;box-shadow:0 0 30px #ffd70022}
.method-card{background:#161b22;border:1px solid #30363d;border-radius:12px;padding:18px;text-align:center}
.tooltip-box{background:#1c2128;border:1px solid #30363d;border-radius:8px;padding:12px 16px;margin:8px 0;font-size:13px;color:#8b949e;line-height:1.7}
.tie-box{background:linear-gradient(135deg,#1c2128,#21262d);border:2px solid #ffa657;border-radius:12px;padding:20px 24px;margin:14px 0;box-shadow:0 0 20px #ffa65722}
</style>
""", unsafe_allow_html=True)

plt.rcParams.update({
    "figure.facecolor":"#0d1117","axes.facecolor":"#161b22","axes.edgecolor":"#30363d",
    "axes.labelcolor":"#e6edf3","xtick.color":"#e6edf3","ytick.color":"#e6edf3",
    "text.color":"#e6edf3","grid.color":"#21262d","font.family":"DejaVu Sans",
    "font.size":11,"axes.titlesize":13,"axes.titleweight":"bold",
    "legend.facecolor":"#21262d","legend.edgecolor":"#30363d",
})
COLORS=["#58a6ff","#3fb950","#f78166","#d2a8ff","#ffa657","#79c0ff","#56d364","#ff7b72","#e3b341","#a5d6ff"]
MC={"SAW":"#58a6ff","SMART":"#3fb950","MOORA":"#f78166","WP":"#d2a8ff"}

# ── Kriteria tetap ────────────────────────────────────────────
KRITERIA=[
    {"kode":"C1","nama":"IPK",               "satuan":"Skala 0–4",  "jenis":"Benefit","bobot":0.30,
     "desc":"Indeks Prestasi Kumulatif. Semakin tinggi IPK, semakin besar peluang mendapat beasiswa."},
    {"kode":"C2","nama":"Penghasilan Ortu",  "satuan":"Rp / bulan", "jenis":"Cost",   "bobot":0.25,
     "desc":"Penghasilan bulanan orang tua. Semakin rendah, semakin diprioritaskan (berbasis kebutuhan)."},
    {"kode":"C3","nama":"Nilai Tes Akademik","satuan":"Skor 0–100", "jenis":"Benefit","bobot":0.20,
     "desc":"Skor ujian/tes akademik yang diselenggarakan panitia. Semakin tinggi skor semakin baik."},
    {"kode":"C4","nama":"Prestasi",          "satuan":"Skor 1–10",  "jenis":"Benefit","bobot":0.15,
     "desc":"Penilaian prestasi non-akademik (lomba, organisasi, dll) dalam skala 1–10."},
    {"kode":"C5","nama":"Semester",          "satuan":"Semester",   "jenis":"Cost",   "bobot":0.10,
     "desc":"Semester aktif. Diprioritaskan mahasiswa semester awal (lebih banyak sisa waktu studi)."},
]
K_NAMA=[k["nama"] for k in KRITERIA]
K_KODE=[k["kode"] for k in KRITERIA]
K_JENIS=[k["jenis"] for k in KRITERIA]
K_BOBOT=np.array([k["bobot"] for k in KRITERIA])
INPUT_CFG={
    "IPK"               :(0.0,4.0,  0.01,3.50),
    "Penghasilan Ortu"  :(0,  1e10, 500000,3000000),
    "Nilai Tes Akademik":(0.0,100.0,0.5,  75.0),
    "Prestasi"          :(1.0,10.0, 0.5,  7.0),
    "Semester"          :(1,  14,   1,    4),
}

# ════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ════════════════════════════════════════════════════════════
def spk_table(df, hi_col=None, rank_col=None, fmt=None):
    rows=""
    for i,(_,row) in enumerate(df.iterrows()):
        cells=""
        for c in df.columns:
            v=row[c]; sty=""
            if fmt and c in fmt:
                try: txt=fmt[c].format(v)
                except: txt=str(v)
            elif isinstance(v,float): txt=f"{v:.4f}"
            else: txt=str(v)
            if hi_col and c==hi_col:
                try:
                    mn=df[c].min(); mx=df[c].max()
                    t=(float(v)-mn)/(mx-mn) if mx!=mn else 1.0
                    g=int(100+85*t)
                    sty=f"background:rgba(30,{g},60,0.45);font-weight:600;"
                except: pass
            if rank_col and c==rank_col:
                try:
                    rv=int(v)
                    if rv==1:   sty="background:#2ea04340;color:#3fb950;font-weight:700;"; txt="1"
                    elif rv==2: sty="background:#9e6a0330;color:#ffa657;font-weight:600;"; txt="2"
                    elif rv==3: sty="background:#6e40c920;color:#d2a8ff;font-weight:600;"; txt="3"
                except: pass
            cells+=f'<td style="padding:9px 14px;text-align:center;border:1px solid #21262d;color:#e6edf3;{sty}">{txt}</td>'
        rows+=f"<tr>{cells}</tr>"
    hdrs="".join(f'<th style="background:#1f6feb;color:#fff;padding:11px 14px;text-align:center;border:1px solid #30363d;font-weight:600">{c}</th>' for c in df.columns)
    return f'<div style="overflow-x:auto;margin:8px 0"><table class="spk-table"><thead><tr>{hdrs}</tr></thead><tbody>{rows}</tbody></table></div>'

def show_table(df, caption="", note="", hi_col=None, rank_col=None, fmt=None):
    if caption:
        st.markdown(f'<p style="color:#8b949e;font-size:12px;font-weight:600;margin:12px 0 4px;text-transform:uppercase;letter-spacing:.5px">{caption}</p>', unsafe_allow_html=True)
    st.markdown(spk_table(df,hi_col,rank_col,fmt), unsafe_allow_html=True)
    if note:
        st.markdown(f'<div class="tooltip-box">{note}</div>', unsafe_allow_html=True)

def sec(title, color="#1f6feb"):
    st.markdown(f'<div class="sec-hdr" style="border-color:{color}">{title}</div>', unsafe_allow_html=True)

def step_header(n, title, desc=""):
    txt=f'<div class="step-box"><span class="step-num">{n}</span><b style="color:#e6edf3">{title}</b>'
    if desc: txt+=f'<div style="color:#8b949e;font-size:12px;margin-top:6px;margin-left:34px">{desc}</div>'
    st.markdown(txt+"</div>", unsafe_allow_html=True)

# ── Fungsi deteksi pemenang (SUPPORT TIE) ───────────────────
def get_winners(scores, tol=1e-9):
    """Kembalikan LIST semua alternatif dengan skor tertinggi (handle tie)."""
    mx = scores.max()
    return [alt for alt in scores.index if abs(scores[alt] - mx) <= tol]

def winner_box(winners, scores, score_label, color, method_name):
    """Tampilkan box pemenang — support 1 atau lebih kandidat (tie)."""
    is_tie = len(winners) > 1
    if is_tie:
        names_html = " &nbsp;&amp;&nbsp; ".join(
            f'<b style="color:#ffa657;font-size:15px">{w}</b>' for w in winners)
        st.markdown(f"""
        <div class="tie-box">
          <div style="font-size:12px;color:#8b949e;text-transform:uppercase;letter-spacing:.5px;margin-bottom:8px">
            Hasil Seri — {method_name}</div>
          <div style="margin:4px 0">{names_html}</div>
          <div style="color:#8b949e;font-size:13px;margin-top:8px">
            Kedua pendaftar memiliki {score_label} yang sama:
            <b style="color:#ffa657">{scores[winners[0]]:.4f}</b>
          </div>
          <div style="background:#ffa65722;border-radius:6px;padding:8px 12px;margin-top:10px;font-size:12px;color:#ffa657">
            Terdapat nilai seri. Diperlukan pertimbangan kriteria tambahan atau keputusan panitia
            untuk memilih satu di antara kandidat dengan skor yang sama.
          </div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background:{color}18;border:1px solid {color};border-radius:10px;
                    padding:14px 18px;margin-top:10px;display:flex;align-items:center;gap:12px">
          <span style="font-size:20px">🏆</span>
          <div><b style="color:{color};font-size:14px">{winners[0]}</b>
          <span style="color:#8b949e;margin-left:10px">{score_label} = {scores[winners[0]]:.4f}</span></div>
        </div>""", unsafe_allow_html=True)

def bar_chart_multi_winner(labels, values, title, ylabel, winners, clr=None):
    """Bar chart dengan highlight SEMUA pemenang (support tie)."""
    fig,ax=plt.subplots(figsize=(max(9,len(labels)*1.7),5))
    cl=clr or [COLORS[i%len(COLORS)] for i in range(len(labels))]
    order=np.argsort(values)[::-1]
    xl=[labels[i] for i in order]; yv=[values[i] for i in order]; cc=[cl[i] for i in order]
    bars=ax.bar(xl,yv,color=cc,edgecolor="#30363d",linewidth=1.2,zorder=3,width=0.6)
    # Highlight semua pemenang
    for bi,xli in enumerate(xl):
        if xli in winners:
            bars[bi].set_edgecolor("#ffd700"); bars[bi].set_linewidth(2.8)
    for b in bars:
        v=b.get_height()
        ax.text(b.get_x()+b.get_width()/2, v+abs(v)*0.025+1e-6,
                f"{v:.4f}",ha="center",va="bottom",fontsize=9.5,color="#e6edf3",fontweight="bold")
    ax.set_title(title,pad=14)
    ax.set_xlabel("Pendaftar",labelpad=8); ax.set_ylabel(ylabel,labelpad=8)
    ylim=max(abs(v) for v in yv)*1.25
    ax.set_ylim(min(0,min(yv)-ylim*0.1), ylim if ylim>0 else 1)
    ax.axhline(0,color="#8b949e",linewidth=0.8,linestyle="--",alpha=0.5)
    ax.yaxis.grid(True,linestyle="--",alpha=0.35,zorder=0); ax.set_axisbelow(True)
    # Label terbaik di pojok
    if len(winners)==1:
        lbl=f"Terbaik: {winners[0]}"
        ec="#ffd700"
    else:
        lbl=f"Seri: {' & '.join(winners)}"
        ec="#ffa657"
    ax.text(0.98,0.97,lbl,transform=ax.transAxes,
            ha="right",va="top",fontsize=10,color=ec,fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.4",fc="#21262d",ec=ec,alpha=0.9))
    rot=25 if max((len(l) for l in labels),default=0)>7 else 0
    plt.xticks(rotation=rot,ha="right" if rot else "center")
    plt.tight_layout(); return fig

# ── SPK Functions ─────────────────────────────────────────────
def calc_saw(df,bobot,jenis):
    R=df.copy().astype(float)
    for j,kri in enumerate(df.columns):
        col=df[kri]
        R[kri]=col/col.max() if jenis[j]=="Benefit" else col.min()/col
    return R, R.multiply(bobot,axis="columns").sum(axis=1)

def calc_smart(df,bobot,jenis):
    U=df.copy().astype(float)
    for j,kri in enumerate(df.columns):
        col=df[kri]; cmx=col.max(); cmn=col.min(); dn=cmx-cmn
        if abs(dn)<1e-9: U[kri]=1.0
        elif jenis[j]=="Benefit": U[kri]=(col-cmn)/dn
        else: U[kri]=(cmx-col)/dn
    return U, U.multiply(bobot,axis="columns").sum(axis=1)

def calc_moora(df,bobot,jenis):
    X=df.copy().astype(float)
    for kri in df.columns:
        col=df[kri]; dn=np.sqrt((col**2).sum())
        X[kri]=col/dn if dn>0 else 0
    Xw=X.multiply(bobot,axis="columns")
    bc=[df.columns[j] for j in range(len(jenis)) if jenis[j]=="Benefit"]
    cc=[df.columns[j] for j in range(len(jenis)) if jenis[j]=="Cost"]
    b=Xw[bc].sum(axis=1) if bc else pd.Series(0,index=df.index)
    c=Xw[cc].sum(axis=1) if cc else pd.Series(0,index=df.index)
    return X,Xw,b,c,b-c

def calc_wp(df,bobot,jenis):
    bwp=np.array([b if jenis[j]=="Benefit" else -b for j,b in enumerate(bobot)])
    dfc=df.clip(lower=1e-9)
    S=np.array([np.prod(dfc.loc[alt].values**bwp) for alt in df.index])
    V=S/S.sum()
    return bwp,S,V

def get_rank(scores): return scores.rank(ascending=False,method="min").astype(int)
def mmn(s):
    mn,mx=s.min(),s.max()
    return (s-mn)/(mx-mn) if mx!=mn else s*0+0.5

# ════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:24px 0 18px">
      <div style="font-size:38px"></div>
      <div style="font-size:18px;font-weight:800;color:#e6edf3;margin-top:8px">SPK Beasiswa</div>
      <div style="font-size:12px;color:#8b949e;margin-top:4px">Sistem Penunjang Keputusan</div>
    </div><hr>""", unsafe_allow_html=True)

    st.markdown('<div style="font-size:11px;color:#8b949e;font-weight:700;letter-spacing:.8px;margin-bottom:10px">METODE AKTIF</div>', unsafe_allow_html=True)
    use_saw  =st.checkbox("SAW   — Simple Additive Weighting",        value=True)
    use_smart=st.checkbox("SMART — Multi Attribute Rating Technique",  value=True)
    use_moora=st.checkbox("MOORA — Optimization Ratio Analysis",       value=True)
    use_wp   =st.checkbox("WP    — Weighted Product",                  value=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:11px;color:#8b949e;font-weight:700;letter-spacing:.8px;margin-bottom:10px">KRITERIA PENILAIAN</div>', unsafe_allow_html=True)
    for k in KRITERIA:
        color="#79c0ff" if k["jenis"]=="Benefit" else "#f78166"
        st.markdown(f"""
        <div style="padding:8px 0;border-bottom:1px solid #21262d">
          <div style="display:flex;justify-content:space-between">
            <span style="color:#e6edf3;font-size:13px;font-weight:500">{k['kode']} — {k['nama']}</span>
            <span style="color:{color};font-size:12px;font-weight:700">{k['bobot']:.2f}</span>
          </div>
          <div style="display:flex;justify-content:space-between;margin-top:2px">
            <span style="color:#8b949e;font-size:11px">{k['satuan']}</span>
            <span style="color:{color};font-size:11px;opacity:.8">{k['jenis']}</span>
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:11px;color:#8b949e;text-align:center;line-height:1.8">v2.1 · SAW · SMART · MOORA · WP<br>Sistem Penunjang Keputusan<br>Seleksi Penerima Beasiswa</div>', unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(135deg,#161b22,#1c2128);border:1px solid #30363d;
            border-radius:16px;padding:32px 36px;margin-bottom:24px;box-shadow:0 4px 24px #00000055">
  <div style="display:flex;align-items:center;gap:20px;flex-wrap:wrap">
    <div style="font-size:52px;line-height:1"></div>
    <div style="flex:1">
      <h1 style="margin:0;font-size:24px;font-weight:800;color:#e6edf3;letter-spacing:-.3px">
        Sistem Penunjang Keputusan (SPK)</h1>
      <p style="margin:6px 0 0;font-size:15px;color:#8b949e">
        Seleksi Penerima Beasiswa ·
        <span style="color:#58a6ff;font-weight:600">SAW</span> ·
        <span style="color:#3fb950;font-weight:600">SMART</span> ·
        <span style="color:#f78166;font-weight:600">MOORA</span> ·
        <span style="color:#d2a8ff;font-weight:600">Weighted Product</span></p>
    </div>
    <div style="background:#1f6feb22;border:1px solid #1f6feb55;border-radius:10px;padding:12px 20px;text-align:center">
      <div style="font-size:22px;font-weight:800;color:#58a6ff">4</div>
      <div style="font-size:11px;color:#8b949e;margin-top:2px">Metode SPK</div></div>
    <div style="background:#3fb95022;border:1px solid #3fb95055;border-radius:10px;padding:12px 20px;text-align:center">
      <div style="font-size:22px;font-weight:800;color:#3fb950">5</div>
      <div style="font-size:11px;color:#8b949e;margin-top:2px">Kriteria</div></div>
  </div>
</div>""", unsafe_allow_html=True)

# ── Tabs ─────────────────────────────────────────────────────
tab_input,tab_saw,tab_smart,tab_moora,tab_wp,tab_cmp,tab_result=st.tabs([
    "  Input Data  ","  SAW  ","  SMART  ","  MOORA  ","  WP  ","  Perbandingan  ","  Kesimpulan  "
])

# ════════════════════════════════════════════════════════════
# TAB INPUT
# ════════════════════════════════════════════════════════════
with tab_input:
    sec("Kriteria & Bobot Penilaian")
    st.markdown("""<div class="tooltip-box">
      Kriteria dan bobot sudah ditetapkan panitia dan <b>tidak dapat diubah</b>.<br>
      <b style="color:#79c0ff">Benefit</b> = nilai lebih tinggi lebih baik &nbsp;|&nbsp;
      <b style="color:#f78166">Cost</b> = nilai lebih rendah lebih baik (diprioritaskan)
    </div>""", unsafe_allow_html=True)

    TH="background:#1f6feb;color:#fff;padding:11px 14px;text-align:center;border:1px solid #30363d;font-weight:600;"
    TD="padding:10px 14px;border:1px solid #21262d;color:#e6edf3;"
    hk=f'<div style="overflow-x:auto;margin:10px 0"><table class="spk-table"><thead><tr>'
    for col in ["Kode","Nama Kriteria","Keterangan","Satuan","Jenis","Bobot"]:
        hk+=f'<th style="{TH}">{col}</th>'
    hk+="</tr></thead><tbody>"
    for i,k in enumerate(KRITERIA):
        bg="#161b22" if i%2==0 else "#1c2128"
        jb="b" if k["jenis"]=="Benefit" else "c"
        hk+=(f'<tr style="background:{bg}">'
             f'<td style="{TD}text-align:center;color:#58a6ff;font-weight:700">{k["kode"]}</td>'
             f'<td style="{TD}font-weight:600">{k["nama"]}</td>'
             f'<td style="{TD}color:#8b949e;font-size:12px">{k["desc"]}</td>'
             f'<td style="{TD}text-align:center;color:#8b949e">{k["satuan"]}</td>'
             f'<td style="{TD}text-align:center"><span class="badge-{jb}">{k["jenis"]}</span></td>'
             f'<td style="{TD}text-align:center;font-weight:700">{k["bobot"]:.2f}</td></tr>')
    hk+=(f'<tr style="background:#21262d">'
         f'<td colspan="5" style="{TD}text-align:right;font-weight:700">Total Bobot</td>'
         f'<td style="{TD}text-align:center;font-weight:800;color:#3fb950;font-size:15px">{K_BOBOT.sum():.2f}</td>'
         f'</tr></tbody></table></div>')
    st.markdown(hk, unsafe_allow_html=True)

    st.markdown("---")
    sec("Input Data Pendaftar", color="#3fb950")
    col_l,_=st.columns([1,3])
    with col_l:
        n_alt=st.number_input("Jumlah pendaftar",min_value=2,max_value=20,value=3,step=1)
    n_int=int(n_alt)
    st.markdown(f'<div class="tooltip-box">Masukkan data untuk <b style="color:#58a6ff">{n_int} pendaftar</b>. Isi semua kolom lalu klik <b style="color:#3fb950">Jalankan Analisis SPK</b>.</div>', unsafe_allow_html=True)

    drow=[3.5,2000000.0,80.0,7.0,2.0]
    if "ss_names" not in st.session_state or len(st.session_state.ss_names)!=n_int:
        st.session_state.ss_names=[f"Pendaftar {i+1}" for i in range(n_int)]
        st.session_state.ss_data =[drow.copy() for _ in range(n_int)]
    while len(st.session_state.ss_data) <n_int: st.session_state.ss_data.append(drow.copy())
    while len(st.session_state.ss_names)<n_int: st.session_state.ss_names.append(f"Pendaftar {len(st.session_state.ss_names)+1}")

    with st.form("form_spk"):
        ch=st.columns([2]+[1]*5)
        ch[0].markdown('<div style="font-size:11px;color:#8b949e;font-weight:700;letter-spacing:.5px;padding:4px 0">NAMA PENDAFTAR</div>', unsafe_allow_html=True)
        for ci,k in enumerate(KRITERIA):
            col="#79c0ff" if k["jenis"]=="Benefit" else "#f78166"
            ch[ci+1].markdown(f'<div style="font-size:11px;text-align:center;padding:4px 0"><span style="color:{col};font-weight:700">{k["kode"]}</span><br><span style="color:#8b949e;font-size:10px">{k["nama"]}</span><br><span style="color:#58a6ff;font-weight:600">{k["bobot"]:.2f}</span></div>', unsafe_allow_html=True)
        st.markdown('<hr style="margin:8px 0">', unsafe_allow_html=True)
        ni=[]; vi=[]
        for i in range(n_int):
            cc=st.columns([2]+[1]*5)
            nm=cc[0].text_input(f"n{i}",value=st.session_state.ss_names[i],label_visibility="collapsed",key=f"nm_{i}")
            ni.append(nm.strip() or f"Pendaftar {i+1}")
            rv=[]
            for j,k in enumerate(KRITERIA):
                lo,hi,step,dv=INPUT_CFG[k["nama"]]
                sv=st.session_state.ss_data[i][j] if j<len(st.session_state.ss_data[i]) else dv
                v=cc[j+1].number_input(k["nama"],min_value=float(lo),max_value=float(hi),
                                       value=float(sv),step=float(step),
                                       label_visibility="collapsed",key=f"v_{i}_{j}")
                rv.append(v)
            vi.append(rv)
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        submitted=st.form_submit_button("Jalankan Analisis SPK",use_container_width=True)

    if submitted:
        st.session_state.ss_names=ni; st.session_state.ss_data=vi; st.session_state.ready=True
        st.success("Data berhasil disimpan. Buka tab SAW, SMART, MOORA, WP, atau Kesimpulan.")

    if st.session_state.get("ready"):
        sec("Matriks Keputusan Awal", color="#ffa657")
        st.markdown('<div class="tooltip-box"><b>Matriks Keputusan</b> memuat nilai mentah setiap pendaftar pada setiap kriteria. Tabel ini menjadi dasar perhitungan semua metode SPK. Baris = pendaftar, Kolom = kriteria.</div>', unsafe_allow_html=True)
        df_mx=pd.DataFrame(st.session_state.ss_data,index=st.session_state.ss_names,columns=K_NAMA)
        show_table(df_mx.reset_index().rename(columns={"index":"Pendaftar"}),
                   caption="Tabel 1. Matriks Keputusan X",fmt={"Penghasilan Ortu":"Rp {:,.0f}"})
        c1,c2,c3,c4=st.columns(4)
        c1.metric("Jumlah Pendaftar",n_int)
        c2.metric("Jumlah Kriteria",5)
        c3.metric("Total Bobot",f"{K_BOBOT.sum():.2f}")
        c4.metric("Metode Aktif",sum([use_saw,use_smart,use_moora,use_wp]))

# ── Guard ─────────────────────────────────────────────────────
if not st.session_state.get("ready",False):
    for t in [tab_saw,tab_smart,tab_moora,tab_wp,tab_cmp,tab_result]:
        with t:
            st.markdown("""<div style="text-align:center;padding:60px 20px">
              <div style="font-size:48px;margin-bottom:16px">📋</div>
              <div style="font-size:18px;font-weight:600;color:#e6edf3;margin-bottom:8px">Data Belum Diinput</div>
              <div style="font-size:14px;color:#8b949e">Isi form di tab <b>Input Data</b> lalu klik <b>Jalankan Analisis SPK</b>.</div>
            </div>""", unsafe_allow_html=True)
    st.stop()

# ── Prepare data & hitung semua metode ───────────────────────
alternatif=st.session_state.ss_names
df_matrix =pd.DataFrame(st.session_state.ss_data,index=alternatif,columns=K_NAMA)
n_alt_i   =len(alternatif)

R_saw,   saw_sc  =calc_saw(df_matrix,K_BOBOT,K_JENIS)
U_smart, smart_sc=calc_smart(df_matrix,K_BOBOT,K_JENIS)
X_nm,X_wm,b_sum,c_sum,moora_sc=calc_moora(df_matrix,K_BOBOT,K_JENIS)
bwp,S_wp,V_wp=calc_wp(df_matrix,K_BOBOT,K_JENIS)
wp_sc=pd.Series(V_wp,index=alternatif)

rk_saw  =get_rank(saw_sc);   rk_smart=get_rank(smart_sc)
rk_moora=get_rank(moora_sc); rk_wp   =get_rank(wp_sc)

# Deteksi semua pemenang (handle tie)
winners_saw  =get_winners(saw_sc)
winners_smart=get_winners(smart_sc)
winners_moora=get_winners(moora_sc)
winners_wp   =get_winners(wp_sc)

# ════════════════════════════════════════════════════════════
# TAB SAW
# ════════════════════════════════════════════════════════════
with tab_saw:
    if not use_saw:
        st.info("Aktifkan metode SAW di sidebar kiri.")
    else:
        st.markdown("""<div style="background:linear-gradient(135deg,#161b22,#1c2128);border:1px solid #58a6ff44;border-radius:12px;padding:20px 24px;margin-bottom:16px">
          <div style="font-size:18px;font-weight:800;color:#58a6ff;margin-bottom:6px">SAW — Simple Additive Weighting</div>
          <div style="font-size:13px;color:#8b949e;line-height:1.7">Metode SAW adalah yang paling sederhana dan populer. Nilai setiap pendaftar dinormalisasi agar sebanding, lalu dikalikan bobot kriteria, kemudian dijumlahkan. Alternatif dengan total skor <b style="color:#e6edf3">Vi tertinggi</b> menjadi rekomendasi terbaik.</div>
        </div>""", unsafe_allow_html=True)

        with st.expander("Rumus & Penjelasan SAW", expanded=True):
            ca,cb=st.columns(2)
            with ca:
                st.markdown('<div class="formula-box"><div class="formula-title">Rumus Normalisasi</div>', unsafe_allow_html=True)
                st.markdown(r"""$$r_{ij}=\begin{cases}\dfrac{x_{ij}}{\max_i(x_{ij})}&\text{Benefit}\\[8pt]\dfrac{\min_i(x_{ij})}{x_{ij}}&\text{Cost}\end{cases}$$""")
                st.markdown('<div class="formula-desc"><b>r<sub>ij</sub></b> = nilai ternormalisasi (0–1)<br><b>x<sub>ij</sub></b> = nilai asli pendaftar i kriteria j<br><b>Benefit</b>: dibagi nilai terbesar → 1.0 = terbaik<br><b>Cost</b>: nilai terkecil dibagi nilai aktual → nilai rendah jadi unggul</div></div>', unsafe_allow_html=True)
            with cb:
                st.markdown('<div class="formula-box"><div class="formula-title">Rumus Skor Akhir</div>', unsafe_allow_html=True)
                st.markdown(r"""$$V_i=\sum_{j=1}^{n}w_j\cdot r_{ij}$$""")
                st.markdown('<div class="formula-desc"><b>V<sub>i</sub></b> = skor akhir pendaftar ke-i (0–1)<br><b>w<sub>j</sub></b> = bobot kriteria ke-j<br><b>r<sub>ij</sub></b> = nilai ternormalisasi<br><br>Alternatif dengan <b>V<sub>i</sub> terbesar</b> = rekomendasi terbaik</div></div>', unsafe_allow_html=True)

        t1,t2,t3=st.tabs(["Langkah 1 — Normalisasi","Langkah 2 — Terbobot","Langkah 3 — Hasil"])
        with t1:
            step_header(1,"Normalisasi Matriks (R)","Nilai setiap kriteria diubah ke skala [0,1] agar dapat dibandingkan secara adil.")
            show_table(R_saw.reset_index().rename(columns={"index":"Pendaftar"}),"Tabel SAW-1. Matriks Normalisasi R",
                       note="Nilai 1.0 = terbaik di antara semua pendaftar pada kriteria tersebut. Nilai mendekati 0 = terlemah.")
        with t2:
            step_header(2,"Matriks Terbobot (R × W)","Nilai normalisasi dikalikan bobot kriteria.")
            df_saw_w=R_saw.multiply(K_BOBOT,axis="columns")
            show_table(df_saw_w.reset_index().rename(columns={"index":"Pendaftar"}),"Tabel SAW-2. Matriks Terbobot",
                       note="C1 (IPK, bobot 0.30) memberi kontribusi terbesar. C5 (Semester, bobot 0.10) terkecil.")
        with t3:
            step_header(3,"Skor Akhir V dan Ranking","Jumlahkan setiap baris → skor Vi. Tertinggi = terbaik.")
            df_sr=pd.DataFrame({"Pendaftar":alternatif,"Skor Vi":saw_sc.values,"Ranking":rk_saw.values}).sort_values("Ranking").reset_index(drop=True)
            show_table(df_sr,"Tabel SAW-3. Skor Akhir dan Ranking SAW",hi_col="Skor Vi",rank_col="Ranking",
                       note="Skor Vi di rentang [0,1]. Semakin tinggi = semakin layak menerima beasiswa.")
            winner_box(winners_saw, saw_sc, "Skor Vi", "#58a6ff", "SAW")

        st.markdown("---")
        fig=bar_chart_multi_winner(alternatif,saw_sc.values,"Distribusi Skor SAW per Pendaftar","Skor Vi",winners_saw)
        st.pyplot(fig); plt.close()

# ════════════════════════════════════════════════════════════
# TAB SMART
# ════════════════════════════════════════════════════════════
with tab_smart:
    if not use_smart:
        st.info("Aktifkan metode SMART di sidebar kiri.")
    else:
        st.markdown("""<div style="background:linear-gradient(135deg,#161b22,#1c2128);border:1px solid #3fb95044;border-radius:12px;padding:20px 24px;margin-bottom:16px">
          <div style="font-size:18px;font-weight:800;color:#3fb950;margin-bottom:6px">SMART — Simple Multi-Attribute Rating Technique</div>
          <div style="font-size:13px;color:#8b949e;line-height:1.7">SMART menggunakan <b style="color:#e6edf3">fungsi utilitas</b> — seberapa "berguna" nilai pendaftar dibanding sesama. Berbeda dari SAW yang mengacu pada nilai terbaik saja, SMART menggunakan rentang nilai terendah–tertinggi, sehingga lebih sensitif terhadap sebaran data.</div>
        </div>""", unsafe_allow_html=True)

        with st.expander("Rumus & Penjelasan SMART", expanded=True):
            ca,cb=st.columns(2)
            with ca:
                st.markdown('<div class="formula-box"><div class="formula-title">Rumus Nilai Utilitas U(x<sub>ij</sub>)</div>', unsafe_allow_html=True)
                st.markdown(r"""$$U(x_{ij})=\begin{cases}\dfrac{x_{ij}-\min}{\max-\min}&\text{Benefit}\\[8pt]\dfrac{\max-x_{ij}}{\max-\min}&\text{Cost}\end{cases}$$""")
                st.markdown('<div class="formula-desc"><b>Nilai Utilitas U(x<sub>ij</sub>)</b> = seberapa "berguna" nilai pendaftar i pada kriteria j, dalam skala 0–1.<br><br>U = 1.0 → terbaik di antara semua pendaftar<br>U = 0.0 → terburuk di antara semua pendaftar<br>U = 0.5 → tepat di tengah-tengah<br><br><b>Benefit</b>: (nilai − min) / (max − min)<br><b>Cost</b>: (max − nilai) / (max − min)</div></div>', unsafe_allow_html=True)
            with cb:
                st.markdown('<div class="formula-box"><div class="formula-title">Rumus Skor Akhir S<sub>i</sub></div>', unsafe_allow_html=True)
                st.markdown(r"""$$S_i=\sum_{j=1}^{n}w_j\cdot U(x_{ij})$$""")
                st.markdown('<div class="formula-desc"><b>S<sub>i</sub></b> = skor utilitas total pendaftar ke-i (0–1)<br><b>w<sub>j</sub></b> = bobot kriteria ke-j<br><b>U(x<sub>ij</sub>)</b> = nilai utilitas<br><br>S<sub>i</sub> adalah rata-rata tertimbang utilitas semua kriteria. Semakin tinggi = semakin layak.</div></div>', unsafe_allow_html=True)

        t1,t2,t3=st.tabs(["Langkah 1 — Nilai Utilitas","Langkah 2 — Terbobot","Langkah 3 — Hasil"])
        with t1:
            step_header(1,"Matriks Nilai Utilitas U(xij)","Nilai mentah diubah menjadi utilitas [0,1] berdasarkan rentang data.")
            show_table(U_smart.reset_index().rename(columns={"index":"Pendaftar"}),"Tabel SMART-1. Matriks Nilai Utilitas",
                       note="Nilai Utilitas (U) mengukur posisi relatif pendaftar. U=1.0 berarti terbaik, U=0.0 terburuk di antara peserta. Ini berbeda dari nilai asli karena sudah dipetakan ke skala 0–1.")
        with t2:
            step_header(2,"Utilitas Terbobot (U × W)","Nilai utilitas dikalikan bobot untuk memberi pengaruh proporsional.")
            Uw=U_smart.multiply(K_BOBOT,axis="columns")
            show_table(Uw.reset_index().rename(columns={"index":"Pendaftar"}),"Tabel SMART-2. Utilitas Terbobot",
                       note="C1 (IPK, bobot 0.30) memberi kontribusi terbesar. C5 (Semester, bobot 0.10) terkecil.")
        with t3:
            step_header(3,"Skor Akhir S dan Ranking","Jumlahkan semua utilitas terbobot per baris.")
            df_smr=pd.DataFrame({"Pendaftar":alternatif,"Skor Si":smart_sc.values,"Ranking":rk_smart.values}).sort_values("Ranking").reset_index(drop=True)
            show_table(df_smr,"Tabel SMART-3. Skor Akhir dan Ranking SMART",hi_col="Skor Si",rank_col="Ranking",
                       note="Skor Si berkisar 0–1. Semakin tinggi = semakin layak mendapat beasiswa.")
            winner_box(winners_smart, smart_sc, "Skor Si", "#3fb950", "SMART")

        st.markdown("---")
        fig=bar_chart_multi_winner(alternatif,smart_sc.values,"Distribusi Skor SMART per Pendaftar","Skor Utilitas Si",winners_smart,[MC["SMART"]]*n_alt_i)
        st.pyplot(fig); plt.close()

# ════════════════════════════════════════════════════════════
# TAB MOORA
# ════════════════════════════════════════════════════════════
with tab_moora:
    if not use_moora:
        st.info("Aktifkan metode MOORA di sidebar kiri.")
    else:
        st.markdown("""<div style="background:linear-gradient(135deg,#161b22,#1c2128);border:1px solid #f7816644;border-radius:12px;padding:20px 24px;margin-bottom:16px">
          <div style="font-size:18px;font-weight:800;color:#f78166;margin-bottom:6px">MOORA — Multi-Objective Optimization on the Basis of Ratio Analysis</div>
          <div style="font-size:13px;color:#8b949e;line-height:1.7">Dikembangkan Brauers & Zavadskas (2006). MOORA menggunakan <b style="color:#e6edf3">normalisasi akar kuadrat</b> (lebih stabil secara matematis), lalu memisahkan kontribusi kriteria Benefit dan Cost secara eksplisit. Skor bisa bernilai negatif jika pengaruh Cost mendominasi.</div>
        </div>""", unsafe_allow_html=True)

        with st.expander("Rumus & Penjelasan MOORA", expanded=True):
            ca,cb=st.columns(2)
            with ca:
                st.markdown('<div class="formula-box"><div class="formula-title">Rumus Normalisasi Rasio</div>', unsafe_allow_html=True)
                st.markdown(r"""$$x^*_{ij}=\dfrac{x_{ij}}{\sqrt{\displaystyle\sum_{i=1}^{m}x_{ij}^2}}$$""")
                st.markdown('<div class="formula-desc"><b>x*<sub>ij</sub></b> = nilai ternormalisasi dengan panjang vektor<br><b>√Σx²</b> = akar kuadrat jumlah kuadrat kolom j<br><br>Normalisasi ini mempertahankan proporsi antar nilai lebih baik dibanding min-max, terutama saat ada nilai ekstrem.</div></div>', unsafe_allow_html=True)
            with cb:
                st.markdown('<div class="formula-box"><div class="formula-title">Rumus Skor Optimasi Y<sub>i</sub></div>', unsafe_allow_html=True)
                st.markdown(r"""$$Y_i=\sum_{j\in\text{Benefit}}w_jx^*_{ij}-\sum_{j\in\text{Cost}}w_jx^*_{ij}$$""")
                st.markdown('<div class="formula-desc"><b>Y<sub>i</sub></b> = skor optimasi akhir pendaftar ke-i<br>Bagian <b>+</b> = kontribusi kriteria Benefit (IPK, Tes, Prestasi)<br>Bagian <b>−</b> = penalti kriteria Cost (Penghasilan, Semester)<br><br>Y<sub>i</sub> positif → manfaat lebih besar dari cost<br>Y<sub>i</sub> negatif → cost mendominasi<br>Ranking dari Y<sub>i</sub> terbesar ke terkecil.</div></div>', unsafe_allow_html=True)

        t1,t2,t3=st.tabs(["Langkah 1 — Normalisasi Rasio","Langkah 2 — Terbobot","Langkah 3 — Hasil"])
        with t1:
            step_header(1,"Matriks Normalisasi Rasio (x*)","Nilai dibagi akar kuadrat jumlah kuadrat seluruh nilai pada kolom yang sama.")
            show_table(X_nm.reset_index().rename(columns={"index":"Pendaftar"}),"Tabel MOORA-1. Matriks Normalisasi Rasio",
                       note="Nilai x* kecil (0.0x–0.9x) karena dibagi panjang vektor kolom. Berbeda dari SAW/SMART yang skalanya lebih intuitif.")
        with t2:
            step_header(2,"Matriks Terbobot (w × x*)","Nilai normalisasi dikalikan bobot kriteria.")
            show_table(X_wm.reset_index().rename(columns={"index":"Pendaftar"}),"Tabel MOORA-2. Matriks Terbobot",
                       note="Kolom Benefit (C1,C3,C4) akan dijumlahkan (+). Kolom Cost (C2,C5) akan dikurangkan (−) dari skor akhir.")
        with t3:
            step_header(3,"Skor Optimasi Y dan Ranking","Yi = Jumlah benefit terbobot dikurangi jumlah cost terbobot.")
            df_mor=pd.DataFrame({
                "Pendaftar":alternatif,
                "Sigma Benefit (+)":b_sum.values,
                "Sigma Cost (−)":c_sum.values,
                "Skor Yi (Benefit − Cost)":moora_sc.values,
                "Ranking":rk_moora.values
            }).sort_values("Ranking").reset_index(drop=True)
            show_table(df_mor,"Tabel MOORA-3. Skor Akhir dan Ranking MOORA",hi_col="Skor Yi (Benefit − Cost)",rank_col="Ranking",
                       note="'Sigma Benefit (+)' = total terbobot C1+C3+C4. 'Sigma Cost (−)' = total terbobot C2+C5. Yi = selisihnya. Semakin besar Yi = semakin baik.")
            winner_box(winners_moora, moora_sc, "Skor Yi", "#f78166", "MOORA")

        st.markdown("---")
        fig=bar_chart_multi_winner(alternatif,moora_sc.values,"Distribusi Skor MOORA per Pendaftar","Skor Optimasi Yi",winners_moora,
                                   ["#3fb950" if v>=0 else "#f78166" for v in moora_sc.values])
        st.pyplot(fig); plt.close()

# ════════════════════════════════════════════════════════════
# TAB WP
# ════════════════════════════════════════════════════════════
with tab_wp:
    if not use_wp:
        st.info("Aktifkan metode WP di sidebar kiri.")
    else:
        st.markdown("""<div style="background:linear-gradient(135deg,#161b22,#1c2128);border:1px solid #d2a8ff44;border-radius:12px;padding:20px 24px;margin-bottom:16px">
          <div style="font-size:18px;font-weight:800;color:#d2a8ff;margin-bottom:6px">WP — Weighted Product</div>
          <div style="font-size:13px;color:#8b949e;line-height:1.7">WP menggunakan <b style="color:#e6edf3">perkalian</b> (bukan penjumlahan) untuk menggabungkan kriteria. Nilai dipangkatkan dengan bobotnya. Benefit = pangkat positif, Cost = pangkat negatif. Metode ini lebih sensitif terhadap nilai ekstrem.</div>
        </div>""", unsafe_allow_html=True)

        with st.expander("Rumus & Penjelasan WP", expanded=True):
            ca,cb=st.columns(2)
            with ca:
                st.markdown('<div class="formula-box"><div class="formula-title">Rumus Vektor S (Nilai Perkalian Terbobot)</div>', unsafe_allow_html=True)
                st.markdown(r"""$$S_i=\prod_{j=1}^{n}x_{ij}^{w_j}$$""")
                st.markdown('<div class="formula-desc"><b>S<sub>i</sub></b> = hasil perkalian nilai berpangkat bobot<br><b>x<sub>ij</sub></b> = nilai asli pendaftar i kriteria j<br><b>w<sub>j</sub></b> = pangkat bobot:<br>&nbsp;&nbsp;• Benefit → pangkat <b>positif (+w)</b><br>&nbsp;&nbsp;• Cost → pangkat <b>negatif (−w)</b><br><br>Pangkat negatif pada Cost otomatis "menghukum" nilai tinggi pada kriteria tersebut.</div></div>', unsafe_allow_html=True)
            with cb:
                st.markdown('<div class="formula-box"><div class="formula-title">Rumus Vektor V (Skor Akhir Proporsi)</div>', unsafe_allow_html=True)
                st.markdown(r"""$$V_i=\dfrac{S_i}{\displaystyle\sum_{k=1}^{m}S_k}$$""")
                st.markdown('<div class="formula-desc"><b>V<sub>i</sub></b> = proporsi skor pendaftar ke-i terhadap total (0–1)<br><b>ΣS<sub>k</sub></b> = jumlah semua nilai S<br><br>Jumlah semua V<sub>i</sub> = 1.00 (100%). V<sub>i</sub> menunjukkan <b>porsi keunggulan</b> pendaftar dibanding seluruh peserta.</div></div>', unsafe_allow_html=True)

        t1,t2=st.tabs(["Langkah 1 — Vektor S","Langkah 2 — Vektor V & Ranking"])
        with t1:
            step_header(1,"Pangkat Bobot & Hitung Vektor S","Sesuaikan tanda pangkat (+/−) lalu kalikan semua nilai berpangkat.")
            df_bwp=pd.DataFrame({"Kode":K_KODE,"Kriteria":K_NAMA,"Jenis":K_JENIS,
                                  "Bobot Asli":[f"{b:.2f}" for b in K_BOBOT],
                                  "Pangkat WP":[f"{b:+.2f}" for b in bwp]})
            show_table(df_bwp,"Tabel WP-1. Penyesuaian Pangkat Bobot",
                       note="Kriteria Cost mendapat pangkat NEGATIF sehingga pendaftar dengan penghasilan ortu tinggi atau semester lanjut otomatis mendapat nilai S lebih kecil.")
            df_sv=pd.DataFrame({"Pendaftar":alternatif,"Vektor S (Si)":S_wp})
            show_table(df_sv,"Tabel WP-2. Vektor S",fmt={"Vektor S (Si)":"{:.6f}"},
                       note="Nilai Si bisa sangat kecil/besar tergantung skala data. Perlu dinormalisasi menjadi Vektor V agar bisa dibandingkan.")
        with t2:
            step_header(2,"Hitung Vektor V dan Ranking","Bagi setiap Si dengan total ΣSi untuk mendapat proporsi akhir.")
            df_vv=pd.DataFrame({"Pendaftar":alternatif,"Vektor S (Si)":S_wp,
                                 "Vektor V (Vi — Skor Akhir)":V_wp,"Ranking":rk_wp.values}).sort_values("Ranking").reset_index(drop=True)
            show_table(df_vv,"Tabel WP-3. Vektor V dan Ranking WP",hi_col="Vektor V (Vi — Skor Akhir)",rank_col="Ranking",
                       fmt={"Vektor S (Si)":"{:.6f}","Vektor V (Vi — Skor Akhir)":"{:.4f}"},
                       note="Jumlah semua Vi = 1.00 (100%). Semakin besar Vi = semakin besar proporsi keunggulan pendaftar tersebut.")
            winner_box(winners_wp, wp_sc, "Vektor Vi", "#d2a8ff", "WP")

        st.markdown("---")
        fig=bar_chart_multi_winner(alternatif,wp_sc.values,"Distribusi Skor WP per Pendaftar","Vektor Vi",winners_wp,[MC["WP"]]*n_alt_i)
        st.pyplot(fig); plt.close()

# ════════════════════════════════════════════════════════════
# TAB PERBANDINGAN
# ════════════════════════════════════════════════════════════
with tab_cmp:
    sec("Perbandingan Hasil Semua Metode")
    st.markdown('<div class="tooltip-box">Tab ini membandingkan hasil keempat metode secara berdampingan. Jika semua metode menunjuk pendaftar yang sama = hasil <b style="color:#3fb950">konsisten dan kuat</b>. Jika berbeda = diperlukan pertimbangan lebih lanjut.</div>', unsafe_allow_html=True)

    df_cmp_tbl=pd.DataFrame({"Pendaftar":alternatif,"Skor SAW":saw_sc.values,
                              "Skor SMART":smart_sc.values,"Skor MOORA":moora_sc.values,"Skor WP":wp_sc.values})
    show_table(df_cmp_tbl,"Tabel 8.1. Perbandingan Skor Semua Metode",
               note="Skala skor antar metode berbeda-beda — tidak bisa dibandingkan langsung. Gunakan tabel ranking di bawah untuk perbandingan yang adil.")

    st.markdown("<br>", unsafe_allow_html=True)
    TH2="background:#1f6feb;color:#fff;padding:11px 14px;text-align:center;border:1px solid #30363d;font-weight:600;"
    TD2="padding:9px 14px;border:1px solid #21262d;color:#e6edf3;"
    hr2=f'<div style="overflow-x:auto;margin:8px 0"><table class="spk-table"><thead><tr>'
    for c in ["Pendaftar","Rank SAW","Rank SMART","Rank MOORA","Rank WP","Konsistensi"]:
        hr2+=f'<th style="{TH2}">{c}</th>'
    hr2+="</tr></thead><tbody>"
    all_rk=list(zip(rk_saw.values,rk_smart.values,rk_moora.values,rk_wp.values))
    for i,(alt,rv) in enumerate(zip(alternatif,all_rk)):
        bg="#161b22" if i%2==0 else "#1c2128"
        hr2+=f'<tr style="background:{bg}"><td style="{TD2}font-weight:600">{alt}</td>'
        for r in rv:
            if r==1:   tds=f"{TD2}background:#2ea04340;color:#3fb950;font-weight:700"; lbl="1"
            elif r==2: tds=f"{TD2}background:#9e6a0330;color:#ffa657;font-weight:600"; lbl="2"
            elif r==3: tds=f"{TD2}background:#6e40c920;color:#d2a8ff";                lbl="3"
            else:      tds=TD2; lbl=str(r)
            hr2+=f'<td style="{tds}">{lbl}</td>'
        uniq=len(set(rv)); kc="#3fb950" if uniq==1 else "#ffa657"
        ks="Semua metode sepakat" if uniq==1 else f"Bervariasi ({uniq} nilai berbeda)"
        hr2+=f'<td style="{TD2}color:{kc};font-weight:600">{ks}</td></tr>'
    hr2+="</tbody></table></div>"
    st.markdown('<p style="color:#8b949e;font-size:12px;font-weight:600;margin:12px 0 4px;text-transform:uppercase;letter-spacing:.5px">Tabel 8.2. Perbandingan Ranking Semua Metode</p>', unsafe_allow_html=True)
    st.markdown(hr2, unsafe_allow_html=True)
    st.markdown('<div class="tooltip-box">Kolom <b>Konsistensi</b> = apakah keempat metode memberikan ranking yang sama. "Semua metode sepakat" = hasil sangat dapat diandalkan.</div>', unsafe_allow_html=True)

    st.markdown("---")
    ns={m:mmn(s).values for m,s in [("SAW",saw_sc),("SMART",smart_sc),("MOORA",moora_sc),("WP",wp_sc)]}
    fig,ax=plt.subplots(figsize=(max(11,n_alt_i*2.2),5.5))
    x=np.arange(n_alt_i); w=0.18
    for mth,off in zip(["SAW","SMART","MOORA","WP"],[-1.5,-0.5,0.5,1.5]):
        ax.bar(x+off*w,ns[mth],w,label=mth,color=MC[mth],edgecolor="#30363d",linewidth=0.8,alpha=0.9,zorder=3)
    ax.set_xticks(x)
    rot=25 if max((len(a) for a in alternatif),default=0)>7 else 0
    ax.set_xticklabels(alternatif,rotation=rot,ha="right" if rot else "center")
    ax.set_title("Perbandingan Skor Ternormalisasi [0–1] Antar Metode",pad=14)
    ax.set_xlabel("Pendaftar"); ax.set_ylabel("Skor (ternormalisasi 0–1)")
    ax.legend(loc="upper right",framealpha=0.3,fontsize=11)
    ax.set_ylim(0,1.28); ax.yaxis.grid(True,linestyle="--",alpha=0.4,zorder=0); ax.set_axisbelow(True)
    plt.tight_layout(); st.pyplot(fig); plt.close()

    rmt=np.array([rk_saw.values,rk_smart.values,rk_moora.values,rk_wp.values])
    fig2,ax2=plt.subplots(figsize=(max(8,n_alt_i*1.5),4))
    sns.heatmap(rmt,annot=True,fmt="d",cmap="YlOrRd_r",xticklabels=alternatif,
                yticklabels=["SAW","SMART","MOORA","WP"],ax=ax2,
                linewidths=0.5,linecolor="#30363d",cbar_kws={"label":"Ranking"})
    ax2.set_title("Heatmap Ranking per Metode dan Pendaftar — Warna Hijau = Ranking Terbaik",pad=14)
    ax2.set_xticklabels(ax2.get_xticklabels(),rotation=rot,ha="right" if rot else "center")
    plt.tight_layout(); st.pyplot(fig2); plt.close()

# ════════════════════════════════════════════════════════════
# TAB KESIMPULAN
# ════════════════════════════════════════════════════════════
with tab_result:
    sec("Kesimpulan & Rekomendasi Penerima Beasiswa", color="#3fb950")

    # Kumpulkan semua pemenang tiap metode (support tie)
    all_winners={
        "SAW":winners_saw,"SMART":winners_smart,
        "MOORA":winners_moora,"WP":winners_wp
    }
    all_scores={
        "SAW":saw_sc,"SMART":smart_sc,"MOORA":moora_sc,"WP":wp_sc
    }
    best_score_per={
        "SAW":saw_sc.max(),"SMART":smart_sc.max(),"MOORA":moora_sc.max(),"WP":wp_sc.max()
    }

    # Hitung skor vote setiap pendaftar (1 pemenang = 1 vote; tie = semua dapat 1 vote)
    vote_count=Counter()
    for mth,wlist in all_winners.items():
        for w in wlist: vote_count[w]+=1

    # Rata-rata ranking
    avg_r={alt:np.mean([rk_saw[alt],rk_smart[alt],rk_moora[alt],rk_wp[alt]]) for alt in alternatif}
    final=sorted(avg_r.items(),key=lambda x:x[1])

    # Tentukan pemenang akhir (bisa lebih dari satu jika avg_rank sama)
    min_avg=final[0][1]
    overall_winners=[alt for alt,avg in final if abs(avg-min_avg)<1e-9]
    all_same=len(set([w for wl in all_winners.values() for w in wl]))==1 and len(overall_winners)==1

    # ── Box pemenang ─────────────────────────────────────────
    if len(overall_winners)==1:
        bst=overall_winners[0]; bn=vote_count[bst]; bavg=avg_r[bst]
        st.markdown(f"""
        <div class="result-card">
          <div style="font-size:13px;color:#8b949e;letter-spacing:.5px;text-transform:uppercase;margin-bottom:8px">Rekomendasi Penerima Beasiswa</div>
          <div style="font-size:30px;font-weight:800;color:#ffd700;margin:8px 0;letter-spacing:-.5px">🏆 {bst}</div>
          <div style="display:flex;justify-content:center;gap:24px;margin-top:12px;flex-wrap:wrap">
            <div style="background:#ffffff11;border-radius:8px;padding:8px 16px">
              <span style="color:#8b949e;font-size:12px">Didukung metode</span>
              <span style="color:#ffd700;font-weight:700;font-size:14px;margin-left:8px">{bn}/4</span>
            </div>
            <div style="background:#ffffff11;border-radius:8px;padding:8px 16px">
              <span style="color:#8b949e;font-size:12px">Rata-rata ranking</span>
              <span style="color:#ffd700;font-weight:700;font-size:14px;margin-left:8px">{bavg:.2f}</span>
            </div>
            <div style="background:#ffffff11;border-radius:8px;padding:8px 16px">
              <span style="color:#8b949e;font-size:12px">Status</span>
              <span style="color:#3fb950;font-weight:700;font-size:14px;margin-left:8px">{"Semua metode sepakat" if all_same else "Mayoritas sepakat"}</span>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)
    else:
        # Multiple overall winners (tie)
        names_str=" &nbsp;&amp;&nbsp; ".join(f'<b style="color:#ffa657;font-size:18px">{w}</b>' for w in overall_winners)
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0d1117,#161b22);border:2px solid #ffa657;border-radius:14px;padding:28px;text-align:center;margin:18px 0;box-shadow:0 0 30px #ffa65722">
          <div style="font-size:13px;color:#8b949e;letter-spacing:.5px;text-transform:uppercase;margin-bottom:8px">Hasil Seri — Rekomendasi Penerima Beasiswa</div>
          <div style="font-size:24px;margin:10px 0">{names_str}</div>
          <div style="color:#8b949e;font-size:13px;margin-top:12px">Rata-rata ranking sama: <b style="color:#ffa657">{min_avg:.2f}</b></div>
          <div style="background:#ffa65722;border-radius:8px;padding:10px 16px;margin-top:14px;font-size:13px;color:#ffa657">
            Terdapat nilai seri pada ranking akhir. Diperlukan pertimbangan kriteria tambahan atau keputusan panitia.
          </div>
        </div>""", unsafe_allow_html=True)

    # ── Kartu per metode ──────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    c1,c2,c3,c4=st.columns(4)
    for col,(mth,clr) in zip([c1,c2,c3,c4],[("SAW","#58a6ff"),("SMART","#3fb950"),("MOORA","#f78166"),("WP","#d2a8ff")]):
        wlist=all_winners[mth]
        names_card=" & ".join(wlist) if len(wlist)>1 else wlist[0]
        tag="SERI" if len(wlist)>1 else "TERBAIK"
        tag_c="#ffa657" if len(wlist)>1 else clr
        col.markdown(f"""
        <div class="method-card" style="border-top:3px solid {clr}">
          <div style="font-size:11px;color:#8b949e;font-weight:700;letter-spacing:.5px">{mth}</div>
          <div style="font-size:11px;color:{tag_c};font-weight:700;margin-top:4px">{tag}</div>
          <div style="font-size:13px;font-weight:700;color:#e6edf3;margin:6px 0;word-break:break-word">{names_card}</div>
          <div style="font-size:12px;color:{clr};font-weight:600">{best_score_per[mth]:.4f}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Ranking akhir ─────────────────────────────────────────
    sec("Ranking Akhir Keseluruhan", color="#ffa657")
    st.markdown('<div class="tooltip-box"><b>Ranking akhir</b> dihitung dari rata-rata ranking keempat metode. Semakin kecil rata-ratanya, semakin konsisten pendaftar dipilih sebagai terbaik. Kolom "Vote" = berapa metode yang memilihnya sebagai peringkat 1.</div>', unsafe_allow_html=True)

    df_fin=pd.DataFrame([{
        "Rank Akhir":i+1,
        "Pendaftar":alt,
        "Rank SAW":rk_saw[alt],"Rank SMART":rk_smart[alt],
        "Rank MOORA":rk_moora[alt],"Rank WP":rk_wp[alt],
        "Rata-rata Rank":round(avg,2),
        "Vote (jadi Rank 1)":f"{vote_count.get(alt,0)}/4",
        "Keterangan":"SERI" if alt in overall_winners and len(overall_winners)>1 else ("Terbaik" if alt==overall_winners[0] and len(overall_winners)==1 else ""),
    } for i,(alt,avg) in enumerate(final)])
    show_table(df_fin,"Tabel 9.1. Ranking Akhir Keseluruhan",rank_col="Rank Akhir")

    # ── Statistik ─────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    sec("Statistik Skor per Metode", color="#8b949e")
    st.markdown('<div class="tooltip-box"><b>Std Deviasi</b> = seberapa menyebar skor antar pendaftar. Tinggi = ada perbedaan besar antar peserta. Rendah = skor berdekatan, seleksi lebih ketat.</div>', unsafe_allow_html=True)
    df_st=pd.DataFrame({
        "Statistik":["Nilai Minimum","Nilai Maksimum","Rata-rata","Std Deviasi"],
        "SAW"  :[f"{saw_sc.min():.4f}",f"{saw_sc.max():.4f}",f"{saw_sc.mean():.4f}",f"{saw_sc.std():.4f}"],
        "SMART":[f"{smart_sc.min():.4f}",f"{smart_sc.max():.4f}",f"{smart_sc.mean():.4f}",f"{smart_sc.std():.4f}"],
        "MOORA":[f"{moora_sc.min():.4f}",f"{moora_sc.max():.4f}",f"{moora_sc.mean():.4f}",f"{moora_sc.std():.4f}"],
        "WP"   :[f"{wp_sc.min():.4f}",f"{wp_sc.max():.4f}",f"{wp_sc.mean():.4f}",f"{wp_sc.std():.4f}"],
    })
    show_table(df_st,"Tabel 9.2. Statistik Skor")

    # ── Grafik ringkasan ──────────────────────────────────────
    st.markdown("---")
    fig,axes=plt.subplots(1,2,figsize=(max(14,n_alt_i*2.4),5.5))
    ax1,ax2=axes
    freq=[vote_count.get(a,0) for a in alternatif]
    bars1=ax1.bar(alternatif,freq,color=[COLORS[i%len(COLORS)] for i in range(n_alt_i)],
                  edgecolor="#30363d",linewidth=1.2,zorder=3,width=0.6)
    for bi,(b,v) in enumerate(zip(bars1,freq)):
        if alternatif[bi] in overall_winners: b.set_edgecolor("#ffd700"); b.set_linewidth(2.5)
        ax1.text(b.get_x()+b.get_width()/2,b.get_height()+0.06,f"{v}",
                 ha="center",va="bottom",fontsize=12,color="#e6edf3",fontweight="bold")
    ax1.set_title("Jumlah Metode yang Memilih sebagai Peringkat 1\n(border emas = pemenang akhir)",pad=12)
    ax1.set_xlabel("Pendaftar"); ax1.set_ylabel("Vote (Jumlah Metode)")
    ax1.set_ylim(0,5); ax1.set_yticks(range(5))
    ax1.yaxis.grid(True,linestyle="--",alpha=0.4,zorder=0); ax1.set_axisbelow(True)
    rot=25 if max((len(a) for a in alternatif),default=0)>7 else 0
    plt.setp(ax1.get_xticklabels(),rotation=rot,ha="right" if rot else "center")

    sp=sorted(zip(alternatif,[avg_r[a] for a in alternatif]),key=lambda x:x[1])
    sa,sv=zip(*sp)
    bars2=ax2.barh(list(sa)[::-1],list(sv)[::-1],
                   color=[COLORS[i%len(COLORS)] for i in range(n_alt_i)][::-1],
                   edgecolor="#30363d",linewidth=1.2,zorder=3)
    for bi,(b,sai) in enumerate(zip(bars2,list(sa)[::-1])):
        if sai in overall_winners: b.set_edgecolor("#ffd700"); b.set_linewidth(2.5)
    for b,v in zip(bars2,list(sv)[::-1]):
        ax2.text(b.get_width()+0.04,b.get_y()+b.get_height()/2,f"{v:.2f}",
                 ha="left",va="center",fontsize=10,color="#e6edf3",fontweight="bold")
    ax2.set_title("Rata-rata Ranking (lebih kecil = lebih baik)\n(border emas = pemenang akhir)",pad=12)
    ax2.set_xlabel("Rata-rata Ranking"); ax2.set_ylabel("Pendaftar")
    ax2.xaxis.grid(True,linestyle="--",alpha=0.4,zorder=0); ax2.set_axisbelow(True)
    ax2.set_xlim(0,n_alt_i+0.8)
    plt.suptitle("Ringkasan Akhir SPK — Seleksi Penerima Beasiswa",fontsize=14,fontweight="bold",y=1.02)
    plt.tight_layout(); st.pyplot(fig); plt.close()

    # ── Narasi otomatis ───────────────────────────────────────
    st.markdown("---")
    sec("Analisis Hasil", color="#8b949e")
    tie_methods=[mth for mth,wl in all_winners.items() if len(wl)>1]
    tie_note=f" Metode yang menghasilkan nilai seri: <b style='color:#ffa657'>{', '.join(tie_methods)}</b>." if tie_methods else ""
    if len(overall_winners)==1:
        bst=overall_winners[0]; bn=vote_count[bst]; bavg=avg_r[bst]
        consist_txt=(f"Keempat metode menghasilkan pilihan yang <b style='color:#3fb950'>seragam dan konsisten</b>."
                     if all_same else
                     f"Terdapat variasi antar metode. Keputusan diambil dari rata-rata ranking keempat metode.")
        narasi=(f"Proses seleksi mengevaluasi <b style='color:#58a6ff'>{n_alt_i} pendaftar</b> "
                f"menggunakan 5 kriteria melalui 4 metode SPK.{tie_note}<br><br>"
                f"{consist_txt}<br><br>"
                f"Pendaftar <b style='color:#ffd700'>{bst}</b> menempati posisi teratas dengan "
                f"rata-rata ranking <b>{bavg:.2f}</b> dan didukung oleh <b>{bn}/4 metode</b>, "
                f"sehingga menjadi kandidat paling layak menerima beasiswa.")
    else:
        names_str=" dan ".join(f"<b style='color:#ffa657'>{w}</b>" for w in overall_winners)
        narasi=(f"Proses seleksi mengevaluasi <b style='color:#58a6ff'>{n_alt_i} pendaftar</b> "
                f"menggunakan 5 kriteria melalui 4 metode SPK.{tie_note}<br><br>"
                f"Terdapat <b style='color:#ffa657'>nilai seri pada ranking akhir</b> antara {names_str} "
                f"dengan rata-rata ranking yang sama ({min_avg:.2f}). "
                f"Diperlukan pertimbangan kriteria tambahan atau keputusan panitia untuk menentukan penerima beasiswa.")

    st.markdown(f'<div style="background:#1c2128;border:1px solid #30363d;border-left:4px solid #3fb950;border-radius:0 10px 10px 0;padding:18px 22px;font-size:14px;color:#e6edf3;line-height:1.85">{narasi}</div>', unsafe_allow_html=True)