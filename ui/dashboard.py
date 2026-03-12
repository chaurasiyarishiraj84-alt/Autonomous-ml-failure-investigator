import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import time
from streamlit_autorefresh import st_autorefresh

# ----------------------------------
# CONFIG
# ----------------------------------
API_URL = "http://localhost:8000/monitoring/analyze"
REFRESH_INTERVAL_MS = 2000
MAX_POINTS = 50
CONFIDENCE_ALERT_THRESHOLD = 0.6
ERROR_ALERT_THRESHOLD = 0.2
BASELINE_WINDOW = 10

st.set_page_config(
    page_title="ML Failure Investigator",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ----------------------------------
# PROFESSIONAL CSS
# ----------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');

/* ── Root Variables ── */
:root {
    --bg-primary: #050810;
    --bg-card: #0c1120;
    --bg-card2: #0f1628;
    --border: #1e2d4a;
    --border-bright: #2a3f6a;
    --accent-blue: #3b82f6;
    --accent-cyan: #06b6d4;
    --accent-green: #10b981;
    --accent-red: #ef4444;
    --accent-orange: #f59e0b;
    --accent-purple: #8b5cf6;
    --text-primary: #f0f4ff;
    --text-secondary: #8b9cc4;
    --text-muted: #4a5578;
    --glow-blue: 0 0 20px rgba(59,130,246,0.3);
    --glow-green: 0 0 20px rgba(16,185,129,0.3);
    --glow-red: 0 0 20px rgba(239,68,68,0.3);
}

/* ── Global Reset ── */
html, body, [class*="css"] {
    font-family: 'Syne', sans-serif !important;
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
}

.main { background-color: var(--bg-primary) !important; }
.block-container { padding: 1.5rem 2rem 3rem !important; max-width: 1400px !important; }

/* ── Hide Streamlit Branding ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Header Banner ── */
.hero-banner {
    background: linear-gradient(135deg, #050810 0%, #0c1a35 50%, #050810 100%);
    border: 1px solid var(--border-bright);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -20%;
    width: 60%;
    height: 200%;
    background: radial-gradient(ellipse, rgba(59,130,246,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.hero-banner::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent-blue), var(--accent-cyan), transparent);
}
.hero-title {
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    background: linear-gradient(135deg, #f0f4ff 0%, #3b82f6 50%, #06b6d4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.3rem 0;
    line-height: 1.2;
}
.hero-sub {
    color: var(--text-secondary);
    font-size: 0.9rem;
    font-family: 'Space Mono', monospace;
    letter-spacing: 0.5px;
}
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(16,185,129,0.1);
    border: 1px solid rgba(16,185,129,0.3);
    border-radius: 999px;
    padding: 4px 12px;
    font-size: 0.75rem;
    font-family: 'Space Mono', monospace;
    color: var(--accent-green);
    margin-top: 0.8rem;
}
.status-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: var(--accent-green);
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(0.8); }
}

/* ── Section Headers ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 1.8rem 0 1rem 0;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid var(--border);
}
.section-title {
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--text-secondary);
}
.section-accent {
    width: 24px; height: 2px;
    background: linear-gradient(90deg, var(--accent-blue), var(--accent-cyan));
    border-radius: 2px;
}

/* ── KPI Cards ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 12px;
    margin-bottom: 1.5rem;
}
.kpi-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem 1rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s;
}
.kpi-card:hover { border-color: var(--border-bright); }
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    border-radius: 12px 12px 0 0;
}
.kpi-card.blue::before { background: linear-gradient(90deg, var(--accent-blue), var(--accent-cyan)); }
.kpi-card.green::before { background: linear-gradient(90deg, var(--accent-green), #34d399); }
.kpi-card.red::before { background: linear-gradient(90deg, var(--accent-red), #f87171); }
.kpi-card.orange::before { background: linear-gradient(90deg, var(--accent-orange), #fbbf24); }
.kpi-card.purple::before { background: linear-gradient(90deg, var(--accent-purple), #a78bfa); }
.kpi-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 0.5rem;
    font-family: 'Space Mono', monospace;
}
.kpi-value {
    font-size: 1.8rem;
    font-weight: 800;
    line-height: 1;
    letter-spacing: -1px;
}
.kpi-value.blue { color: var(--accent-blue); }
.kpi-value.green { color: var(--accent-green); }
.kpi-value.red { color: var(--accent-red); }
.kpi-value.orange { color: var(--accent-orange); }
.kpi-value.purple { color: var(--accent-purple); }
.kpi-trend {
    font-size: 0.7rem;
    color: var(--text-muted);
    margin-top: 0.4rem;
    font-family: 'Space Mono', monospace;
}

/* ── URL Input ── */
.stTextInput > div > div > input {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-bright) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.85rem !important;
    padding: 0.6rem 1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent-blue) !important;
    box-shadow: 0 0 0 2px rgba(59,130,246,0.2) !important;
}
.stTextInput label {
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    color: var(--text-secondary) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-bright) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 0.5rem 1.2rem !important;
    transition: all 0.2s !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: rgba(59,130,246,0.1) !important;
    border-color: var(--accent-blue) !important;
    color: var(--accent-blue) !important;
}

/* ── Alert Cards ── */
.alert-card {
    border-radius: 10px;
    padding: 0.9rem 1.2rem;
    margin: 0.5rem 0;
    display: flex;
    align-items: flex-start;
    gap: 12px;
    font-size: 0.88rem;
}
.alert-critical {
    background: rgba(239,68,68,0.08);
    border: 1px solid rgba(239,68,68,0.3);
    color: #fca5a5;
}
.alert-warning {
    background: rgba(245,158,11,0.08);
    border: 1px solid rgba(245,158,11,0.3);
    color: #fcd34d;
}
.alert-success {
    background: rgba(16,185,129,0.08);
    border: 1px solid rgba(16,185,129,0.3);
    color: #6ee7b7;
}
.alert-info {
    background: rgba(59,130,246,0.08);
    border: 1px solid rgba(59,130,246,0.3);
    color: #93c5fd;
}
.alert-icon { font-size: 1rem; margin-top: 1px; }

/* ── RCA Card ── */
.rca-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-bottom: 1rem;
}
.rca-item {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem 1.2rem;
}
.rca-item-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--text-muted);
    font-family: 'Space Mono', monospace;
    margin-bottom: 0.4rem;
}
.rca-item-value {
    font-size: 1rem;
    font-weight: 700;
    color: var(--text-primary);
}
.severity-critical { color: var(--accent-red) !important; }
.severity-high { color: var(--accent-orange) !important; }
.severity-medium { color: #fbbf24 !important; }
.severity-low { color: var(--accent-green) !important; }
.severity-none { color: var(--accent-green) !important; }

/* ── Recommendation Cards ── */
.rec-card {
    background: var(--bg-card);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin: 0.5rem 0;
    border-left: 3px solid;
    display: flex;
    flex-direction: column;
    gap: 4px;
}
.rec-card.critical { border-color: var(--accent-red); background: rgba(239,68,68,0.05); }
.rec-card.high { border-color: var(--accent-orange); background: rgba(245,158,11,0.05); }
.rec-card.medium { border-color: #fbbf24; background: rgba(251,191,36,0.05); }
.rec-card.low { border-color: var(--accent-green); background: rgba(16,185,129,0.05); }
.rec-card.none { border-color: var(--accent-green); background: rgba(16,185,129,0.05); }
.rec-priority {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    font-family: 'Space Mono', monospace;
}
.rec-priority.critical { color: var(--accent-red); }
.rec-priority.high { color: var(--accent-orange); }
.rec-priority.medium { color: #fbbf24; }
.rec-priority.low, .rec-priority.none { color: var(--accent-green); }
.rec-action { font-size: 0.92rem; font-weight: 700; color: var(--text-primary); }
.rec-detail { font-size: 0.8rem; color: var(--text-secondary); line-height: 1.4; }

/* ── Audit Log ── */
.audit-entry {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 0.5rem 0.8rem;
    border-radius: 6px;
    background: var(--bg-card);
    border: 1px solid var(--border);
    margin: 4px 0;
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: var(--text-secondary);
}

/* ── Drift Table ── */
.drift-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.6rem 1rem;
    border-radius: 8px;
    background: var(--bg-card);
    border: 1px solid var(--border);
    margin: 4px 0;
    font-size: 0.82rem;
}
.drift-label { color: var(--text-secondary); font-family: 'Space Mono', monospace; font-size: 0.75rem; }
.drift-value { color: var(--text-primary); font-family: 'Space Mono', monospace; font-size: 0.75rem; }
.badge {
    padding: 2px 10px;
    border-radius: 999px;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 1px;
    font-family: 'Space Mono', monospace;
}
.badge-yes { background: rgba(239,68,68,0.15); color: #fca5a5; border: 1px solid rgba(239,68,68,0.3); }
.badge-no { background: rgba(16,185,129,0.15); color: #6ee7b7; border: 1px solid rgba(16,185,129,0.3); }

/* ── Expander Overrides ── */
.streamlit-expanderHeader {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    font-size: 0.85rem !important;
}
.streamlit-expanderContent {
    background: var(--bg-card2) !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
}

/* ── Metrics Override ── */
[data-testid="metric-container"] {
    display: none;
}

/* ── Divider ── */
hr { border-color: var(--border) !important; margin: 1rem 0 !important; }

/* ── Plotly Chart Containers ── */
[data-testid="stPlotlyChart"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 0.5rem !important;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------
# SESSION STATE
# ----------------------------------
defaults = {
    "running": False,
    "timestamps": [],
    "confidence": [],
    "confidence_std": [],
    "error": [],
    "latency": [],
    "avg_conf": 0.0,
    "err_rate": 0.0,
    "latency_ms": 0.0,
    "samples_collected": 0,
    "baseline_conf": None,
    "last_drift": {},
    "last_rca": {},
    "last_recommendations": [],
    "approval_logs": [],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

if st.session_state.running:
    st_autorefresh(interval=REFRESH_INTERVAL_MS, key="auto_refresh")

# ----------------------------------
# HERO BANNER
# ----------------------------------
status_text = "MONITORING ACTIVE" if st.session_state.running else "MONITORING PAUSED"
status_color = "var(--accent-green)" if st.session_state.running else "var(--accent-orange)"
dot_color = "#10b981" if st.session_state.running else "#f59e0b"

st.markdown(f"""
<div class="hero-banner">
    <div class="hero-title">🧠 Autonomous ML Failure Investigator</div>
    <div class="hero-sub">Tier-1+ MLOps · Real-Time Monitoring · Root Cause Analysis · Governance</div>
    <div class="status-pill" style="background: rgba(16,185,129,0.1); border-color: {dot_color}40; color: {dot_color};">
        <div class="status-dot" style="background: {dot_color};"></div>
        {status_text}
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------------------------
# MODEL CONNECTION
# ----------------------------------
st.markdown('<div class="section-header"><div class="section-accent"></div><div class="section-title">Model Connection</div></div>', unsafe_allow_html=True)

prediction_url = st.text_input(
    "MODEL PREDICTION API URL",
    "http://127.0.0.1:9000/predict",
    label_visibility="visible"
)

b1, b2, b3 = st.columns(3)
with b1:
    if st.button("▶  Start Monitoring"):
        st.session_state.running = True
with b2:
    if st.button("⏹  Stop Monitoring"):
        st.session_state.running = False
with b3:
    if st.button("📤  Export CSV") and st.session_state.timestamps:
        df = pd.DataFrame({
            "timestamp": st.session_state.timestamps,
            "avg_confidence": st.session_state.confidence,
            "confidence_std": st.session_state.confidence_std,
            "error_rate": st.session_state.error,
            "latency_ms": st.session_state.latency,
        })
        st.download_button("Download CSV", df.to_csv(index=False), "monitoring.csv", "text/csv")

if not prediction_url.strip():
    st.stop()

# ----------------------------------
# API CALL
# ----------------------------------
if st.session_state.running:
    try:
        start = time.time()
        r = requests.post(API_URL, json={"prediction_url": prediction_url}, timeout=10)
        st.session_state.latency_ms = round((time.time() - start) * 1000, 2)

        if r.status_code == 200:
            data = r.json()
            metrics = data.get("current_metrics") or data.get("metrics", {})
            st.session_state.last_drift = data.get("drift", {})
            st.session_state.last_rca = data.get("rca", {})
            st.session_state.last_recommendations = data.get("recommendations", [])
            st.session_state.avg_conf = metrics.get("avg_confidence", 0.0)
            st.session_state.err_rate = metrics.get("error_rate", 0.0)
            conf_dist = metrics.get("confidence_distribution", [])

            st.session_state.timestamps.append(time.strftime("%H:%M:%S"))
            st.session_state.confidence.append(st.session_state.avg_conf)
            st.session_state.error.append(st.session_state.err_rate)
            st.session_state.latency.append(st.session_state.latency_ms)
            std = float(pd.Series(conf_dist).std()) if conf_dist else 0.0
            st.session_state.confidence_std.append(std)
            st.session_state.samples_collected += data.get("samples_collected", 1)

            for k in ["timestamps", "confidence", "error", "latency", "confidence_std"]:
                st.session_state[k] = st.session_state[k][-MAX_POINTS:]

            if st.session_state.baseline_conf is None and len(st.session_state.confidence) >= BASELINE_WINDOW:
                st.session_state.baseline_conf = sum(st.session_state.confidence[:BASELINE_WINDOW]) / BASELINE_WINDOW

    except Exception as e:
        st.markdown(f'<div class="alert-card alert-critical"><span class="alert-icon">🔴</span><span>Backend connection error: {e}</span></div>', unsafe_allow_html=True)

# ----------------------------------
# KPI METRICS
# ----------------------------------
st.markdown('<div class="section-header"><div class="section-accent"></div><div class="section-title">Model Health Metrics</div></div>', unsafe_allow_html=True)

conf_std_val = round(st.session_state.confidence_std[-1], 4) if st.session_state.confidence_std else 0.0

st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi-card blue">
        <div class="kpi-label">Avg Confidence</div>
        <div class="kpi-value blue">{round(st.session_state.avg_conf, 4)}</div>
        <div class="kpi-trend">prediction quality</div>
    </div>
    <div class="kpi-card purple">
        <div class="kpi-label">Confidence STD</div>
        <div class="kpi-value purple">{conf_std_val}</div>
        <div class="kpi-trend">variance indicator</div>
    </div>
    <div class="kpi-card red">
        <div class="kpi-label">Error Rate</div>
        <div class="kpi-value red">{round(st.session_state.err_rate, 4)}</div>
        <div class="kpi-trend">failure frequency</div>
    </div>
    <div class="kpi-card orange">
        <div class="kpi-label">Latency (ms)</div>
        <div class="kpi-value orange">{st.session_state.latency_ms}</div>
        <div class="kpi-trend">response time</div>
    </div>
    <div class="kpi-card green">
        <div class="kpi-label">Samples Collected</div>
        <div class="kpi-value green">{st.session_state.samples_collected}</div>
        <div class="kpi-trend">total probes</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------------------------
# CHARTS
# ----------------------------------
st.markdown('<div class="section-header"><div class="section-accent"></div><div class="section-title">Behavioral Trends</div></div>', unsafe_allow_html=True)

def make_chart(x, y, title, color, fill_color):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode="lines+markers",
        line=dict(width=2.5, color=color),
        marker=dict(size=5, color=color, line=dict(width=1, color="rgba(255,255,255,0.3)")),
        fill="tozeroy",
        fillcolor=fill_color,
        hovertemplate=f"<b>{title}</b><br>Time: %{{x}}<br>Value: %{{y:.4f}}<extra></extra>"
    ))
    fig.update_layout(
        height=280,
        template="plotly_dark",
        title=dict(text=title, font=dict(size=13, color="#8b9cc4", family="Space Mono"), x=0.01),
        paper_bgcolor="rgba(12,17,32,0)",
        plot_bgcolor="rgba(12,17,32,0)",
        margin=dict(l=10, r=10, t=40, b=30),
        xaxis=dict(
            title="Time",
            tickfont=dict(size=10, color="#4a5578", family="Space Mono"),
            gridcolor="rgba(30,45,74,0.5)",
            showgrid=True,
            zeroline=False,
        ),
        yaxis=dict(
            tickfont=dict(size=10, color="#4a5578", family="Space Mono"),
            gridcolor="rgba(30,45,74,0.5)",
            showgrid=True,
            zeroline=False,
        ),
        hoverlabel=dict(bgcolor="#0c1120", font=dict(size=12, family="Space Mono")),
    )
    return fig

c1, c2 = st.columns(2)
with c1:
    st.plotly_chart(
        make_chart(st.session_state.timestamps, st.session_state.confidence, "Avg Confidence", "#3b82f6", "rgba(59,130,246,0.08)"),
        use_container_width=True
    )
with c2:
    st.plotly_chart(
        make_chart(st.session_state.timestamps, st.session_state.error, "Error Rate", "#ef4444", "rgba(239,68,68,0.08)"),
        use_container_width=True
    )

st.plotly_chart(
    make_chart(st.session_state.timestamps, st.session_state.latency, "Latency (ms)", "#8b5cf6", "rgba(139,92,246,0.08)"),
    use_container_width=True
)

# ----------------------------------
# BASELINE & DRIFT
# ----------------------------------
st.markdown('<div class="section-header"><div class="section-accent"></div><div class="section-title">Baseline & Drift Detection</div></div>', unsafe_allow_html=True)

anomaly = False
if st.session_state.baseline_conf is not None:
    if (st.session_state.baseline_conf - st.session_state.avg_conf) > 0.15:
        anomaly = True

if anomaly:
    st.markdown('<div class="alert-card alert-critical"><span class="alert-icon">🚨</span><span><strong>Confidence Drift Detected</strong> — Significant deviation from baseline. Retraining recommended.</span></div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="alert-card alert-success"><span class="alert-icon">✅</span><span><strong>Baseline Normal</strong> — Model behavior within expected parameters.</span></div>', unsafe_allow_html=True)

drift = st.session_state.get("last_drift", {})
if drift and drift.get("status") != "no_drift_detected":
    conf_dist = drift.get("confidence_distribution", {})
    if conf_dist:
        detected = conf_dist.get("drift_detected", False)
        st.markdown(f"""
        <div class="drift-row">
            <span class="drift-label">📊 KS-TEST (CONFIDENCE DISTRIBUTION)</span>
            <div style="display:flex;gap:16px;align-items:center;">
                <span class="drift-value">stat={conf_dist.get('statistic','N/A')} | p={conf_dist.get('p_value','N/A')}</span>
                <span class="badge {'badge-yes' if detected else 'badge-no'}">{'DRIFT' if detected else 'NORMAL'}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    conf_var = drift.get("confidence_variance", {})
    if conf_var:
        st.markdown(f"""
        <div class="drift-row">
            <span class="drift-label">📉 VARIANCE DRIFT</span>
            <div style="display:flex;gap:16px;align-items:center;">
                <span class="drift-value">baseline={conf_var.get('baseline_std')} → current={conf_var.get('current_std')}</span>
                <span class="badge badge-yes">DETECTED</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    feature_shifts = drift.get("feature_mean_shift", [])
    for f in feature_shifts:
        st.markdown(f"""
        <div class="drift-row">
            <span class="drift-label">⚡ FEATURE: {f['feature'].upper()}</span>
            <span class="drift-value">baseline={f['baseline_mean']} → current={f['current_mean']} | score={f['drift_score']}</span>
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown('<div class="alert-card alert-info"><span class="alert-icon">ℹ️</span><span>No drift signals detected in this monitoring cycle.</span></div>', unsafe_allow_html=True)

# ----------------------------------
# ROOT CAUSE ANALYSIS
# ----------------------------------
st.markdown('<div class="section-header"><div class="section-accent"></div><div class="section-title">Root Cause Analysis</div></div>', unsafe_allow_html=True)

rca = st.session_state.get("last_rca", {})
if rca:
    severity = rca.get("severity", "none").lower()
    sev_icons = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢", "none": "🟢"}
    icon = sev_icons.get(severity, "🟢")

    st.markdown(f"""
    <div class="rca-grid">
        <div class="rca-item">
            <div class="rca-item-label">Root Cause</div>
            <div class="rca-item-value">{rca.get('root_cause', 'none').replace('_', ' ').title()}</div>
        </div>
        <div class="rca-item">
            <div class="rca-item-label">Severity</div>
            <div class="rca-item-value severity-{severity}">{icon} {severity.upper()}</div>
        </div>
        <div class="rca-item">
            <div class="rca-item-label">RCA Confidence</div>
            <div class="rca-item-value">{rca.get('confidence', 'low').title()}</div>
        </div>
        <div class="rca-item">
            <div class="rca-item-label">Affected Segment</div>
            <div class="rca-item-value">{rca.get('affected_segment', 'unknown').replace('_', ' ').title()}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    failure_reason = rca.get('failure_reason', 'N/A')
    st.markdown(f'<div class="alert-card alert-info"><span class="alert-icon">🔍</span><span><strong>Failure Reason:</strong> {failure_reason}</span></div>', unsafe_allow_html=True)

    affected = rca.get("affected_features", [])
    if affected:
        st.markdown(f'<div class="alert-card alert-warning"><span class="alert-icon">⚡</span><span><strong>Affected Features:</strong> {", ".join(affected)}</span></div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="alert-card alert-success"><span class="alert-icon">✅</span><span><strong>No Root Cause Identified</strong> — Model is operating normally.</span></div>', unsafe_allow_html=True)

# ----------------------------------
# ALERTS
# ----------------------------------
st.markdown('<div class="section-header"><div class="section-accent"></div><div class="section-title">Live Alerts</div></div>', unsafe_allow_html=True)

alerts_fired = False
if st.session_state.avg_conf < CONFIDENCE_ALERT_THRESHOLD and st.session_state.avg_conf > 0:
    st.markdown(f'<div class="alert-card alert-critical"><span class="alert-icon">⚠️</span><span><strong>Low Confidence Alert</strong> — Current: {round(st.session_state.avg_conf,4)} | Threshold: {CONFIDENCE_ALERT_THRESHOLD}</span></div>', unsafe_allow_html=True)
    alerts_fired = True
if st.session_state.err_rate > ERROR_ALERT_THRESHOLD:
    st.markdown(f'<div class="alert-card alert-critical"><span class="alert-icon">⚠️</span><span><strong>High Error Rate Alert</strong> — Current: {round(st.session_state.err_rate,4)} | Threshold: {ERROR_ALERT_THRESHOLD}</span></div>', unsafe_allow_html=True)
    alerts_fired = True
if not alerts_fired:
    st.markdown('<div class="alert-card alert-success"><span class="alert-icon">✅</span><span><strong>All Clear</strong> — Model operating within safe thresholds.</span></div>', unsafe_allow_html=True)

# ----------------------------------
# GOVERNANCE / HUMAN APPROVAL
# ----------------------------------
st.markdown('<div class="section-header"><div class="section-accent"></div><div class="section-title">Human Approval & Governance</div></div>', unsafe_allow_html=True)

recommendations = st.session_state.get("last_recommendations", [])
actionable = [r for r in recommendations if r.get("priority") in ("CRITICAL", "HIGH", "MEDIUM")]

if actionable:
    st.markdown('<div class="alert-card alert-warning"><span class="alert-icon">⚠️</span><span>The following actions require your explicit approval before execution.</span></div>', unsafe_allow_html=True)
    for i, rec in enumerate(actionable):
        priority = rec.get("priority", "")
        action = rec.get("action", "")
        detail = rec.get("detail", "")
        with st.expander(f"[{priority}] {action}"):
            st.markdown(f"**Detail:** {detail}")
            st.markdown(f"**Type:** `{rec.get('type', 'N/A')}`")
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"✅ Approve", key=f"approve_{i}"):
                    st.session_state.approval_logs.append({"action": action, "decision": "approved", "timestamp": time.strftime("%H:%M:%S")})
                    st.success(f"Approved: {action}")
            with col2:
                if st.button(f"❌ Reject", key=f"reject_{i}"):
                    st.session_state.approval_logs.append({"action": action, "decision": "rejected", "timestamp": time.strftime("%H:%M:%S")})
                    st.error(f"Rejected: {action}")
else:
    st.markdown('<div class="alert-card alert-success"><span class="alert-icon">✅</span><span>No pending approvals — model is healthy.</span></div>', unsafe_allow_html=True)

if st.session_state.approval_logs:
    st.markdown("**📋 Audit Log:**")
    for log in st.session_state.approval_logs[-5:]:
        icon = "✅" if log["decision"] == "approved" else "❌"
        st.markdown(f'<div class="audit-entry">{icon} <span style="color:#4a5578">[{log["timestamp"]}]</span> <span>{log["action"]}</span> <span style="margin-left:auto;font-weight:700;color:{"#6ee7b7" if log["decision"]=="approved" else "#fca5a5"}">{log["decision"].upper()}</span></div>', unsafe_allow_html=True)

# ----------------------------------
# RECOMMENDATIONS
# ----------------------------------
st.markdown('<div class="section-header"><div class="section-accent"></div><div class="section-title">Recommendations</div></div>', unsafe_allow_html=True)

if recommendations:
    for rec in recommendations:
        priority = rec.get("priority", "NONE").lower()
        icons = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢", "none": "🟢"}
        icon = icons.get(priority, "🟢")
        st.markdown(f"""
        <div class="rec-card {priority}">
            <div class="rec-priority {priority}">{icon} {priority.upper()}</div>
            <div class="rec-action">{rec.get('action','')}</div>
            <div class="rec-detail">{rec.get('detail','')}</div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown('<div class="alert-card alert-success"><span class="alert-icon">✅</span><span>Model performance is healthy — no recommendations at this time.</span></div>', unsafe_allow_html=True)

# ----------------------------------
# FOOTER
# ----------------------------------
st.markdown("""
<div style="margin-top:3rem;padding-top:1.5rem;border-top:1px solid var(--border);display:flex;justify-content:space-between;align-items:center;">
    <div style="font-family:'Space Mono',monospace;font-size:0.7rem;color:var(--text-muted);">
        AUTONOMOUS ML FAILURE INVESTIGATOR · TIER-1+ MLOPS
    </div>
    <div style="font-family:'Space Mono',monospace;font-size:0.7rem;color:var(--text-muted);">
        ⏱ AUTO-REFRESH · 2s INTERVAL · MAX {MAX_POINTS} POINTS
    </div>
</div>
""", unsafe_allow_html=True)
