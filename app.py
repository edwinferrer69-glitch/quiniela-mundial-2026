import streamlit as st
import numpy as np
from scipy.stats import poisson
import plotly.graph_objects as go
import math

# ─────────────────────────────────────────────
#  CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="WorldCup Quant | Bet Analytics",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
#  CSS DARK MODE – ESTILO TRADING DASHBOARD
# ─────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

  :root {
    --bg-base:     #080C18;
    --bg-panel:    #0F1528;
    --bg-card:     #151C35;
    --bg-highlight:#1A2240;
    --accent-cyan: #00D4AA;
    --accent-orange:#FF6B35;
    --accent-blue: #4A90E2;
    --text-primary:#E8EDF5;
    --text-secondary:#7A8BAA;
    --text-muted:  #4A5568;
    --border:      #1E2A45;
    --green:       #00C896;
    --red:         #FF4757;
  }

  html, body, [class*="css"], .stApp {
    background-color: var(--bg-base) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    color: var(--text-primary) !important;
  }

  /* Header top bar */
  .top-bar {
    background: linear-gradient(90deg, #080C18 0%, #0F1528 50%, #080C18 100%);
    border-bottom: 1px solid var(--border);
    padding: 14px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 28px;
  }
  .top-bar-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 3px;
    color: var(--accent-cyan);
    text-transform: uppercase;
  }
  .top-bar-badge {
    background: rgba(0, 212, 170, 0.1);
    border: 1px solid rgba(0, 212, 170, 0.3);
    color: var(--accent-cyan);
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    letter-spacing: 1px;
    padding: 3px 10px;
    border-radius: 2px;
  }

  /* Selectbox y widgets */
  .stSelectbox > div > div {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
    color: var(--text-primary) !important;
  }
  .stSelectbox > div > div:hover {
    border-color: var(--accent-cyan) !important;
  }
  label[data-testid="stWidgetLabel"] p {
    color: var(--text-secondary) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
  }

  /* Paneles */
  .panel {
    background: var(--bg-panel);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 20px 22px;
    margin-bottom: 16px;
  }
  .panel-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    letter-spacing: 2px;
    color: var(--text-muted);
    text-transform: uppercase;
    margin-bottom: 6px;
  }
  .panel-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 28px;
    font-weight: 600;
    color: var(--text-primary);
  }
  .panel-value.cyan  { color: var(--accent-cyan); }
  .panel-value.orange{ color: var(--accent-orange); }

  /* Tarjeta de equipo */
  .team-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 18px 20px;
    text-align: center;
  }
  .team-flag { font-size: 48px; line-height: 1; }
  .team-name {
    font-size: 16px;
    font-weight: 600;
    color: var(--text-primary);
    margin: 8px 0 4px;
  }
  .team-elo {
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    color: var(--accent-cyan);
  }

  /* Sección de proyección */
  .projection-card {
    background: linear-gradient(135deg, #0F1528 0%, #1A2240 100%);
    border: 1px solid var(--accent-cyan);
    border-radius: 8px;
    padding: 24px 26px;
    position: relative;
    overflow: hidden;
  }
  .projection-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent-cyan), var(--accent-orange));
  }
  .projection-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    letter-spacing: 2.5px;
    color: var(--accent-cyan);
    text-transform: uppercase;
    margin-bottom: 18px;
  }

  /* Marcadores */
  .score-badge {
    background: var(--bg-highlight);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 12px 16px;
    text-align: center;
    margin-bottom: 8px;
  }
  .score-badge.top1 {
    border-color: var(--accent-cyan);
    background: rgba(0, 212, 170, 0.07);
  }
  .score-badge.top2 {
    border-color: rgba(74, 144, 226, 0.5);
  }
  .score-badge.top3 {
    border-color: rgba(255, 107, 53, 0.4);
  }
  .score-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 24px;
    font-weight: 600;
    color: var(--text-primary);
  }
  .score-pct {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: var(--text-secondary);
    margin-top: 2px;
  }
  .rank-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 4px;
  }

  /* xG bars */
  .xg-bar-wrap {
    background: var(--bg-highlight);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 14px 18px;
  }
  .xg-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    letter-spacing: 1.5px;
    color: var(--text-muted);
    text-transform: uppercase;
  }
  .xg-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 22px;
    font-weight: 600;
  }

  /* Value bet alert */
  .value-alert {
    background: rgba(255, 107, 53, 0.08);
    border: 1px solid rgba(255, 107, 53, 0.4);
    border-radius: 4px;
    padding: 10px 14px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: var(--accent-orange);
    letter-spacing: 0.5px;
  }
  .value-alert-good {
    background: rgba(0, 200, 150, 0.08);
    border: 1px solid rgba(0, 200, 150, 0.4);
    border-radius: 4px;
    padding: 10px 14px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: var(--green);
    letter-spacing: 0.5px;
  }

  /* Divider */
  .divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 20px 0;
  }

  /* Section titles */
  .section-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    letter-spacing: 2.5px;
    color: var(--text-muted);
    text-transform: uppercase;
    margin-bottom: 14px;
  }

  /* Quitar elementos default de Streamlit */
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding-top: 0 !important; max-width: 1200px; }

  /* Button */
  .stButton > button {
    background: linear-gradient(135deg, var(--accent-cyan), #009980) !important;
    color: #080C18 !important;
    border: none !important;
    border-radius: 4px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    padding: 10px 24px !important;
    width: 100% !important;
    margin-top: 8px !important;
  }
  .stButton > button:hover {
    background: linear-gradient(135deg, #00E8BB, var(--accent-cyan)) !important;
    transform: translateY(-1px);
  }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  BASE DE DATOS ELO – MUNDIAL 2026 (48 EQUIPOS CON BANDERAS)
# ─────────────────────────────────────────────
ELO_RATINGS = {
    # CONMEBOL
    "🇦🇷 Argentina": 2140, "🇧🇷 Brasil": 2050, "🇺🇾 Uruguay": 1950, "🇨🇴 Colombia": 1930, 
    "🇪🇨 Ecuador": 1820, "🇻🇪 Venezuela": 1780, "🇵🇾 Paraguay": 1710,
    
    # UEFA (Europa)
    "🇫🇷 Francia": 2120, "🇪🇸 España": 2040, "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra": 2030, "🇵🇹 Portugal": 2010, 
    "🇳🇱 Países Bajos": 1980, "🇧🇪 Bélgica": 1970, "🇮🇹 Italia": 1960, "🇩🇪 Alemania": 1950, 
    "🇭🇷 Croacia": 1940, "🇨🇭 Suiza": 1890, "🇩🇰 Dinamarca": 1880, "🇦🇹 Austria": 1860, 
    "🇷🇸 Serbia": 1850, "🇭🇺 Hungría": 1820, "🇺🇦 Ucrania": 1810, "🇵🇱 Polonia": 1800,
    
    # CONCACAF
    "🇺🇸 Estados Unidos": 1830, "🇲🇽 México": 1810, "🇨🇦 Canadá": 1760, "🇵🇦 Panamá": 1720, 
    "🇨🇷 Costa Rica": 1680, "🇯🇲 Jamaica": 1640, "🇭🇳 Honduras": 1590,
    
    # CAF (África)
    "🇲🇦 Marruecos": 1880, "🇸🇳 Senegal": 1840, "🇪🇬 Egipto": 1790, "🇩🇿 Argelia": 1760, 
    "🇨🇮 Costa de Marfil": 1750, "🇳🇬 Nigeria": 1740, "🇨🇲 Camerún": 1710, "🇲🇱 Malí": 1690, 
    "🇨🇻 Cabo Verde": 1620,
    
    # AFC (Asia)
    "🇯🇵 Japón": 1850, "🇮🇷 Irán": 1820, "🇰🇷 Corea del Sur": 1790, "🇦🇺 Australia": 1780, 
    "🇸🇦 Arabia Saudita": 1690, "🇶🇦 Qatar": 1670, "🇮🇶 Irak": 1640, "🇦🇪 Emiratos Árabes Unidos": 1610,
    
    # OFC (Oceanía)
    "🇳🇿 Nueva Zelanda": 1580
}
# ─────────────────────────────────────────────
#  MOTOR MATEMÁTICO
# ─────────────────────────────────────────────
def calcular_prob_elo(elo_a: float, elo_b: float, ajuste_empate: bool) -> dict:
    """
    Calcula P(A gana), P(Empate), P(B gana) usando el sistema Elo extendido.
    """
    diff = elo_a - elo_b

    # Probabilidad base Elo (victoria o empate)
    prob_a_raw = 1 / (1 + 10 ** (-diff / 400))

    # Modelo de tres resultados usando transformación logística calibrada
    # Basado en el modelo de Davidson (1970) extendido para fútbol
    k = 0.00552  # Constante calibrada para fútbol internacional

    prob_a_win = prob_a_raw * (1 - math.exp(-abs(diff) * k))
    prob_b_win = (1 - prob_a_raw) * (1 - math.exp(-abs(diff) * k))
    prob_draw = 1 - prob_a_win - prob_b_win

    # Ajuste si la diferencia es menor a 60 puntos → alta probabilidad de empate
    if ajuste_empate and abs(diff) < 60:
        target_draw = 0.37  # 37% empate calibrado para partidos muy igualados
        exceso = target_draw - prob_draw
        if exceso > 0:
            prob_a_win -= exceso * (prob_a_raw)
            prob_b_win -= exceso * (1 - prob_a_raw)
            prob_draw = target_draw

    # Normalizar
    total = prob_a_win + prob_b_win + prob_draw
    return {
        "A": max(0, prob_a_win / total),
        "X": max(0, prob_draw / total),
        "B": max(0, prob_b_win / total),
    }


def calcular_xg(elo_a: float, elo_b: float, equipo_a: str, equipo_b: str) -> tuple:
    """
    Convierte diferencia Elo en goles esperados (xG) para cada equipo.
    En el Mundial 2026 se juega en campo neutral, por lo que la base de xG
    comienza igual para ambos equipos. Si uno de los equipos es anfitrión
    (Estados Unidos, México, Canadá), recibe un pequeño ajuste positivo.
    """
    BASE_XG_POR_EQUIPO = 1.25
    diff = elo_a - elo_b

    # Ajuste por entorno neutral + diferencia Elo
    xg_a = BASE_XG_POR_EQUIPO + diff * 0.0008
    xg_b = BASE_XG_POR_EQUIPO - diff * 0.0008

    anfitriones = {"🇺🇸 Estados Unidos", "🇲🇽 México", "🇨🇦 Canadá"}
    ventaja_anfitrion = 0.08

    if equipo_a in anfitriones and equipo_b not in anfitriones:
        xg_a += ventaja_anfitrion
        xg_b -= ventaja_anfitrion
    elif equipo_b in anfitriones and equipo_a not in anfitriones:
        xg_b += ventaja_anfitrion
        xg_a -= ventaja_anfitrion

    # Clamping razonable [0.3, 3.5]
    xg_a = max(0.3, min(3.5, xg_a))
    xg_b = max(0.3, min(3.5, xg_b))
    return round(xg_a, 2), round(xg_b, 2)


def matriz_poisson(xg_a: float, xg_b: float, max_goles: int = 6) -> list:
    """
    Calcula la probabilidad de cada marcador exacto usando distribución de Poisson.
    Retorna lista ordenada por probabilidad descendente.
    """
    resultados = []
    for g_a in range(max_goles + 1):
        for g_b in range(max_goles + 1):
            p = poisson.pmf(g_a, xg_a) * poisson.pmf(g_b, xg_b)
            resultados.append({
                "score": f"{g_a}-{g_b}",
                "goles_a": g_a,
                "goles_b": g_b,
                "prob": p,
            })
    resultados.sort(key=lambda x: x["prob"], reverse=True)
    return resultados


def cuota_implicita(prob: float) -> float:
    """Convierte probabilidad en cuota decimal."""
    return round(1 / prob, 2) if prob > 0 else 99.99


# ─────────────────────────────────────────────
#  TOP BAR
# ─────────────────────────────────────────────
st.markdown("""
<div class="top-bar">
  <div class="top-bar-title">⚽ WorldCup Quant · Bet Analytics</div>
  <div class="top-bar-badge">SISTEMA ELO + POISSON v2.0</div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SELECCIÓN DE EQUIPOS
# ─────────────────────────────────────────────
equipos = sorted(ELO_RATINGS.keys())
col_a, col_vs, col_b, col_btn = st.columns([5, 1, 5, 2])

with col_a:
    equipo_a = st.selectbox("Equipo Local (A)", equipos, index=equipos.index("🇦🇷 Argentina"))

with col_vs:
    st.markdown("<div style='text-align:center; padding-top:32px; font-family:JetBrains Mono; color:#4A5568; font-size:13px; letter-spacing:2px;'>VS</div>", unsafe_allow_html=True)

with col_b:
    equipo_b = st.selectbox("Equipo Visitante (B)", equipos, index=equipos.index("🇫🇷 Francia"))

with col_btn:
    analizar = st.button("▶ ANALIZAR")

# Verificar equipos iguales
if equipo_a == equipo_b:
    st.warning("⚠ Selecciona dos equipos distintos.")
    st.stop()


# ─────────────────────────────────────────────
#  CÁLCULO
# ─────────────────────────────────────────────
elo_a = ELO_RATINGS[equipo_a]
elo_b = ELO_RATINGS[equipo_b]
diff_elo = elo_a - elo_b
ajuste = abs(diff_elo) < 60

probs = calcular_prob_elo(elo_a, elo_b, ajuste)
xg_a, xg_b = calcular_xg(elo_a, elo_b, equipo_a, equipo_b)
marcadores = matriz_poisson(xg_a, xg_b)
top3 = marcadores[:3]


# ─────────────────────────────────────────────
#  FILA: TARJETAS DE EQUIPO + DIFERENCIA ELO
# ─────────────────────────────────────────────
st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
c1, c2, c3 = st.columns([4, 4, 4])

with c1:
    flag_a = equipo_a.split(" ")[0]
    nombre_a = " ".join(equipo_a.split(" ")[1:])
    st.markdown(f"""
    <div class="team-card">
      <div class="team-flag">{flag_a}</div>
      <div class="team-name">{nombre_a}</div>
      <div class="team-elo">ELO: {elo_a:,}</div>
    </div>""", unsafe_allow_html=True)

with c2:
    color_diff = "#00C896" if diff_elo > 0 else ("#FF4757" if diff_elo < 0 else "#7A8BAA")
    signo = "+" if diff_elo > 0 else ""
    alerta_txt = "⚡ AJUSTE EMPATE ACTIVO" if ajuste else "DIFERENCIA ELO"
    alerta_col = "#FF6B35" if ajuste else "#4A5568"
    st.markdown(f"""
    <div class="panel" style="text-align:center; margin-top:0;">
      <div class="panel-label" style="color:{alerta_col};">{alerta_txt}</div>
      <div class="panel-value" style="color:{color_diff}; font-size:36px;">{signo}{diff_elo}</div>
      <div style="font-family:'JetBrains Mono',monospace; font-size:10px; color:#4A5568; margin-top:8px; letter-spacing:1px;">
        {"Alta prob. empate (±60 pts)" if ajuste else "Favorito: " + ("Local" if diff_elo > 0 else "Visitante")}
      </div>
    </div>""", unsafe_allow_html=True)

with c3:
    flag_b = equipo_b.split(" ")[0]
    nombre_b = " ".join(equipo_b.split(" ")[1:])
    st.markdown(f"""
    <div class="team-card">
      <div class="team-flag">{flag_b}</div>
      <div class="team-name">{nombre_b}</div>
      <div class="team-elo">ELO: {elo_b:,}</div>
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  GRÁFICO 1X2 – DONA
# ─────────────────────────────────────────────
st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
st.markdown('<div class="section-title">Probabilidades 1X2 · Sistema Elo</div>', unsafe_allow_html=True)

col_dona, col_bars = st.columns([5, 7])

with col_dona:
    labels = [f"Victoria {nombre_a}", "Empate", f"Victoria {nombre_b}"]
    values = [probs["A"], probs["X"], probs["B"]]
    colors = ["#00D4AA", "#4A90E2", "#FF6B35"]

    fig_dona = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.62,
        marker=dict(colors=colors, line=dict(color="#080C18", width=2)),
        textinfo="none",
        hovertemplate="<b>%{label}</b><br>%{percent}<extra></extra>",
    ))
    fig_dona.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0),
        height=230,
        annotations=[dict(
            text=f"<b>{probs['A']*100:.1f}%</b><br><span style='font-size:10px'>LOCAL</span>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(color="#E8EDF5", size=16, family="JetBrains Mono"),
        )],
    )
    st.plotly_chart(fig_dona, width="stretch", config={"displayModeBar": False})

with col_bars:
    resultados_bar = ["1 · " + nombre_a, "X · Empate", "2 · " + nombre_b]
    probs_bar = [probs["A"], probs["X"], probs["B"]]
    cuotas_bar = [cuota_implicita(p) for p in probs_bar]
    colores_bar = ["#00D4AA", "#4A90E2", "#FF6B35"]

    fig_bar = go.Figure()
    for i, (r, p, c, col) in enumerate(zip(resultados_bar, probs_bar, cuotas_bar, colores_bar)):
        fig_bar.add_trace(go.Bar(
            name=r,
            x=[r],
            y=[p * 100],
            marker=dict(
                color=col,
                opacity=0.85,
                line=dict(color=col, width=1),
            ),
            text=f"<b>{p*100:.1f}%</b><br><span style='font-size:10px'>@ {c}</span>",
            textposition="outside",
            textfont=dict(color="#E8EDF5", size=12, family="JetBrains Mono"),
            hovertemplate=f"<b>{r}</b><br>Prob: {p*100:.2f}%<br>Cuota justa: {c}<extra></extra>",
        ))

    fig_bar.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        margin=dict(l=0, r=0, t=30, b=0),
        height=230,
        yaxis=dict(
            range=[0, max(probs_bar) * 140],
            showgrid=True,
            gridcolor="#1E2A45",
            gridwidth=1,
            zeroline=False,
            tickfont=dict(color="#4A5568", size=9, family="JetBrains Mono"),
            ticksuffix="%",
        ),
        xaxis=dict(
            showgrid=False,
            tickfont=dict(color="#7A8BAA", size=10, family="JetBrains Mono"),
        ),
        bargap=0.4,
    )
    st.plotly_chart(fig_bar, width="stretch", config={"displayModeBar": False})


# ─────────────────────────────────────────────
#  HEATMAP DE MARCADORES EXACTOS
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">Matriz de Probabilidad · Marcadores Exactos (Poisson)</div>', unsafe_allow_html=True)

MAX_G = 5
z_matrix = np.zeros((MAX_G + 1, MAX_G + 1))
for r in marcadores:
    if r["goles_a"] <= MAX_G and r["goles_b"] <= MAX_G:
        z_matrix[r["goles_b"]][r["goles_a"]] = r["prob"] * 100  # filas=B, cols=A

# Texto en celdas
text_matrix = [[f"{z_matrix[j][i]:.1f}%" for i in range(MAX_G + 1)] for j in range(MAX_G + 1)]

fig_heat = go.Figure(go.Heatmap(
    z=z_matrix,
    x=[str(i) for i in range(MAX_G + 1)],
    y=[str(j) for j in range(MAX_G + 1)],
    text=text_matrix,
    texttemplate="%{text}",
    textfont=dict(size=10, family="JetBrains Mono", color="white"),
    colorscale=[
        [0.0,  "#0F1528"],
        [0.15, "#0D2340"],
        [0.35, "#0A4D6E"],
        [0.6,  "#007A8A"],
        [0.8,  "#00B49A"],
        [1.0,  "#00D4AA"],
    ],
    showscale=True,
    colorbar=dict(
        thickness=10,
        tickfont=dict(color="#7A8BAA", size=9, family="JetBrains Mono"),
        ticksuffix="%",
        outlinewidth=0,
        bgcolor="rgba(0,0,0,0)",
    ),
    hovertemplate=f"<b>{nombre_a} %{{x}} – %{{y}} {nombre_b}</b><br>Prob: %{{text}}<extra></extra>",
))

fig_heat.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(
        title=dict(text=f"Goles {nombre_a} (Local)", font=dict(color="#7A8BAA", size=10, family="JetBrains Mono")),
        tickfont=dict(color="#E8EDF5", size=11, family="JetBrains Mono"),
        side="bottom",
    ),
    yaxis=dict(
        title=dict(text=f"Goles {nombre_b} (Visitante)", font=dict(color="#7A8BAA", size=10, family="JetBrains Mono")),
        tickfont=dict(color="#E8EDF5", size=11, family="JetBrains Mono"),
        autorange="reversed",
    ),
    margin=dict(l=10, r=0, t=10, b=10),
    height=320,
)
st.plotly_chart(fig_heat, width="stretch", config={"displayModeBar": False})


# ─────────────────────────────────────────────
#  PANEL: PROYECCIÓN DE APUESTA RECOMENDADA
# ─────────────────────────────────────────────
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

rank_styles  = ["top1", "top2", "top3"]
rank_labels  = ["🥇 MÁXIMA PROB.", "🥈 2° PROB.", "🥉 3° PROB."]
rank_colors  = ["#00D4AA", "#4A90E2", "#FF6B35"]

col_proj, col_scores = st.columns([5, 7])

with col_proj:
    st.markdown(f"""
    <div class="projection-card">
      <div class="projection-title">📊 Proyección de Apuesta Recomendada</div>
      
      <div style="display:flex; gap:12px; margin-bottom:18px;">
        <div class="xg-bar-wrap" style="flex:1; text-align:center;">
          <div class="xg-label">{nombre_a} xG</div>
          <div class="xg-val" style="color:#00D4AA;">{xg_a}</div>
        </div>
        <div class="xg-bar-wrap" style="flex:1; text-align:center;">
          <div class="xg-label">{nombre_b} xG</div>
          <div class="xg-val" style="color:#FF6B35;">{xg_b}</div>
        </div>
      </div>
    """, unsafe_allow_html=True)

    # Alerta de value bet
    if ajuste:
        st.markdown(f"""
        <div class="value-alert">
          ⚡ DIFF ELO &lt; 60 · Empate inflado estadísticamente<br>
          Cuota justa empate: <b>{cuota_implicita(probs['X'])}</b> · Busca cuota &gt; {cuota_implicita(probs['X'])+0.2:.2f}
        </div>""", unsafe_allow_html=True)
    else:
        fav = nombre_a if diff_elo > 0 else nombre_b
        prob_fav = probs["A"] if diff_elo > 0 else probs["B"]
        st.markdown(f"""
        <div class="value-alert-good">
          ✅ FAVORITO CLARO: {fav}<br>
          Cuota justa: <b>{cuota_implicita(prob_fav)}</b> · Busca cuota &gt; {cuota_implicita(prob_fav)+0.1:.2f}
        </div>""", unsafe_allow_html=True)

    # Cuotas resumen
    st.markdown(f"""
      <hr class="divider">
      <div style="display:flex; gap:8px;">
        <div style="flex:1; text-align:center;">
          <div class="panel-label">CUOTA 1</div>
          <div style="font-family:'JetBrains Mono',monospace; font-size:18px; color:#00D4AA; font-weight:600;">{cuota_implicita(probs['A'])}</div>
        </div>
        <div style="flex:1; text-align:center;">
          <div class="panel-label">CUOTA X</div>
          <div style="font-family:'JetBrains Mono',monospace; font-size:18px; color:#4A90E2; font-weight:600;">{cuota_implicita(probs['X'])}</div>
        </div>
        <div style="flex:1; text-align:center;">
          <div class="panel-label">CUOTA 2</div>
          <div style="font-family:'JetBrains Mono',monospace; font-size:18px; color:#FF6B35; font-weight:600;">{cuota_implicita(probs['B'])}</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

with col_scores:
    st.markdown('<div class="section-title">Top 3 Marcadores Exactos Sugeridos</div>', unsafe_allow_html=True)

    for i, (m, style, label, color) in enumerate(zip(top3, rank_styles, rank_labels, rank_colors)):
        pct = m["prob"] * 100
        cuota_m = cuota_implicita(m["prob"])
        ga, gb = m["goles_a"], m["goles_b"]

        if ga > gb:
            tipo = f"Victoria {nombre_a}"
            tipo_color = "#00D4AA"
        elif gb > ga:
            tipo = f"Victoria {nombre_b}"
            tipo_color = "#FF6B35"
        else:
            tipo = "Empate"
            tipo_color = "#4A90E2"

        st.markdown(f"""
        <div class="score-badge {style}" style="margin-bottom: 10px;">
          <div style="display:flex; align-items:center; justify-content:space-between;">
            <div>
              <div class="rank-tag" style="color:{color};">{label}</div>
              <div class="score-num">{ga} – {gb}</div>
              <div style="font-family:'JetBrains Mono',monospace; font-size:10px; color:{tipo_color}; margin-top:2px;">{tipo}</div>
            </div>
            <div style="text-align:right;">
              <div style="font-family:'JetBrains Mono',monospace; font-size:22px; font-weight:600; color:{color};">{pct:.2f}%</div>
              <div style="font-family:'JetBrains Mono',monospace; font-size:10px; color:#4A5568;">Cuota justa</div>
              <div style="font-family:'JetBrains Mono',monospace; font-size:16px; color:#7A8BAA; font-weight:600;">@ {cuota_m}</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # Gráfico mini de top 5 marcadores
    top5 = marcadores[:8]
    fig_scores = go.Figure(go.Bar(
        x=[m["score"] for m in top5],
        y=[m["prob"] * 100 for m in top5],
        marker=dict(
            color=[m["prob"] * 100 for m in top5],
            colorscale=[[0, "#1A2240"], [1, "#00D4AA"]],
            showscale=False,
            line=dict(color="#00D4AA", width=0.5),
        ),
        text=[f"{m['prob']*100:.1f}%" for m in top5],
        textposition="outside",
        textfont=dict(color="#7A8BAA", size=9, family="JetBrains Mono"),
        hovertemplate="<b>%{x}</b><br>%{y:.2f}%<extra></extra>",
    ))
    fig_scores.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=28, b=0),
        height=150,
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        xaxis=dict(tickfont=dict(color="#7A8BAA", size=9, family="JetBrains Mono"), showgrid=False),
        title=dict(
            text="Top 8 marcadores por probabilidad",
            font=dict(color="#4A5568", size=10, family="JetBrains Mono"),
            x=0,
        ),
    )
    st.plotly_chart(fig_scores, width="stretch", config={"displayModeBar": False})


# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown(f"""
<div style="border-top: 1px solid #1E2A45; margin-top: 28px; padding: 14px 0; display:flex; justify-content:space-between;">
  <div style="font-family:'JetBrains Mono',monospace; font-size:9px; color:#2D3A50; letter-spacing:1px;">
    WORLDCUP QUANT · ELO + POISSON MODEL · SOLO FINES ESTADÍSTICOS
  </div>
  <div style="font-family:'JetBrains Mono',monospace; font-size:9px; color:#2D3A50; letter-spacing:1px;">
    {nombre_a} {elo_a} vs {nombre_b} {elo_b} · DIFF {diff_elo:+d}
  </div>
</div>
""", unsafe_allow_html=True)
