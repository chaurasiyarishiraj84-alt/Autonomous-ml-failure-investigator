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
    page_title="Autonomous ML Failure Investigator",
    layout="wide"
)

# ----------------------------------
# SESSION STATE (SINGLE SOURCE OF TRUTH)
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
    "last_recommendations": [],
    "approval_logs": [],
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# AUTO REFRESH 

if st.session_state.running:
    st_autorefresh(interval=REFRESH_INTERVAL_MS, key="auto_refresh")


# HEADER

st.title("🧠 Autonomous ML Failure Investigator")
st.caption(
    "Live ML monitoring with baseline learning, drift detection, alerts & smooth graphs"
)


# MODEL INPUT

st.subheader("🔗 Model Connection")

prediction_url = st.text_input(
    "Model Prediction API URL",
    "http://127.0.0.1:9000/predict"
)

b1, b2, b3 = st.columns(3)

with b1:
    if st.button("▶ Start Monitoring"):
        st.session_state.running = True

with b2:
    if st.button("⏹ Stop Monitoring"):
        st.session_state.running = False

with b3:
    if st.button("📤 Export CSV") and st.session_state.timestamps:
        df = pd.DataFrame({
            "timestamp": st.session_state.timestamps,
            "avg_confidence": st.session_state.confidence,
            "confidence_std": st.session_state.confidence_std,
            "error_rate": st.session_state.error,
            "latency_ms": st.session_state.latency,
        })
        st.download_button(
            "Download CSV",
            df.to_csv(index=False),
            "model_monitoring.csv",
            "text/csv"
        )

if not prediction_url.strip():
    st.stop()


# SINGLE API CALL PER REFRESH

if st.session_state.running:
    try:
        start = time.time()
        r = requests.post(
            API_URL,
            json={"prediction_url": prediction_url},
            timeout=10 #30
        )
        st.session_state.latency_ms = round((time.time() - start) * 1000, 2)

        if r.status_code == 200:
            data = r.json()
            metrics = data.get("metrics", {})

            st.session_state.last_drift = data.get("drift", {})
            st.session_state.last_rca = data.get("rca", {}) 
            st.session_state.last_recommendations = data.get("recommendations", [])
            st.session_state.avg_conf = metrics.get("avg_confidence", 0.0)
            st.session_state.err_rate = metrics.get("error_rate", 0.0)
            conf_dist = metrics.get("confidence_distribution", [])

            # append history
            st.session_state.timestamps.append(time.strftime("%H:%M:%S"))
            st.session_state.confidence.append(st.session_state.avg_conf)
            st.session_state.error.append(st.session_state.err_rate)
            st.session_state.latency.append(st.session_state.latency_ms)

            std = float(pd.Series(conf_dist).std()) if conf_dist else 0.0
            st.session_state.confidence_std.append(std)
            st.session_state.samples_collected += data.get("samples_collected", 1)     #len(conf_dist)

            # sliding window
            for k in [
                "timestamps",
                "confidence",
                "error",
                "latency",
                "confidence_std",
            ]:
                st.session_state[k] = st.session_state[k][-MAX_POINTS:]

            # baseline learning
            if (
                st.session_state.baseline_conf is None
                and len(st.session_state.confidence) >= BASELINE_WINDOW
            ):
                st.session_state.baseline_conf = (
                    sum(st.session_state.confidence[:BASELINE_WINDOW])
                    / BASELINE_WINDOW
                )

    except Exception as e:
        st.error(f"Backend error: {e}")


# KPI METRICS

st.subheader("📊 Model Health Metrics")

m1, m2, m3, m4, m5 = st.columns(5)

m1.metric("Avg Confidence", round(st.session_state.avg_conf, 4))
m2.metric(
    "Confidence STD",
    round(st.session_state.confidence_std[-1], 4)
    if st.session_state.confidence_std else 0.0
)
m3.metric("Error Rate", round(st.session_state.err_rate, 4))
m4.metric("Latency (ms)", st.session_state.latency_ms)
m5.metric("Samples Collected", st.session_state.samples_collected)


# PLOTLY CHARTS 

st.subheader("📈 Behavioral Trends")

def plot_series(x, y, title, color):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode="lines+markers",
        line=dict(width=2, color=color)
    ))
    fig.update_layout(
        height=320,
        template="plotly_dark",
        title=title,
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis_title="Time"
    )
    return fig

c1, c2 = st.columns(2)

with c1:
    st.plotly_chart(
        plot_series(
            st.session_state.timestamps,
            st.session_state.confidence,
            "Avg Confidence",
            "#00CC96"
        ),
        use_container_width=True
    )

with c2:
    st.plotly_chart(
        plot_series(
            st.session_state.timestamps,
            st.session_state.error,
            "Error Rate",
            "#EF553B"
        ),
        use_container_width=True
    )

st.plotly_chart(
    plot_series(
        st.session_state.timestamps,
        st.session_state.latency,
        "Latency (ms)",
        "#636EFA"
    ),
    use_container_width=True
)


# BASELINE & DRIFT

st.subheader("📌 Baseline & Drift Detection")

anomaly = False
if st.session_state.baseline_conf is not None:
    if (st.session_state.baseline_conf - st.session_state.avg_conf) > 0.15:
        anomaly = True

if anomaly:
    st.error("🚨 Confidence drift detected — retraining recommended")
else:
    st.success("✅ Model behavior within baseline")

# ✅ Show actual drift details from backend
drift = st.session_state.get("last_drift", {})

if drift and drift.get("status") != "no_drift_detected":
    st.markdown("**Drift Analysis Details:**")

    # KS-Test result
    conf_dist = drift.get("confidence_distribution", {})
    if conf_dist:
        ks_stat = conf_dist.get("statistic", "N/A")
        p_val = conf_dist.get("p_value", "N/A")
        detected = conf_dist.get("drift_detected", False)
        st.write(f"📊 **KS-Test (Confidence Distribution):** statistic=`{ks_stat}` | p-value=`{p_val}` | drift={'🔴 YES' if detected else '🟢 NO'}")

    # Confidence variance drift
    conf_var = drift.get("confidence_variance", {})
    if conf_var:
        st.write(f"📉 **Confidence Variance Drift:** baseline_std=`{conf_var.get('baseline_std')}` | current_std=`{conf_var.get('current_std')}` | 🔴 DRIFT DETECTED")

    # Feature mean shift
    feature_shifts = drift.get("feature_mean_shift", [])
    if feature_shifts:
        st.markdown("**Feature Mean Shifts:**")
        for f in feature_shifts:
            st.write(f"• Feature `{f['feature']}`: baseline=`{f['baseline_mean']}` → current=`{f['current_mean']}` | drift_score=`{f['drift_score']}`")
else:
    st.info("ℹ️ No drift signals detected in this cycle")




# ROOT CAUSE ANALYSIS

st.subheader("🧠 Root Cause Analysis")

rca = st.session_state.get("last_rca", {})

if rca:
    severity = rca.get("severity", "none")
    severity_color = {
        "critical": "🔴",
        "high": "🟠",
        "medium": "🟡",
        "low": "🟢",
        "none": "🟢"
    }.get(severity, "🟢")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Root Cause", rca.get("root_cause", "none"))
        st.metric("Severity", f"{severity_color} {severity.upper()}")

    with col2:
        st.metric("RCA Confidence", rca.get("confidence", "low"))
        st.metric("Affected Segment", rca.get("affected_segment", "unknown"))

    st.markdown(f"**Failure Reason:** {rca.get('failure_reason', 'N/A')}")

    affected = rca.get("affected_features", [])
    if affected:
        st.markdown(f"**Affected Features:** {', '.join(affected)}")
else:
    st.success("✅ No root cause identified — model healthy")


# ALERTS

st.subheader("🚨 Alerts")

if st.session_state.avg_conf < CONFIDENCE_ALERT_THRESHOLD:
    st.error("⚠️ Confidence below safe threshold")

if st.session_state.err_rate > ERROR_ALERT_THRESHOLD:
    st.error("⚠️ Error rate above safe threshold")

if (
    st.session_state.avg_conf >= CONFIDENCE_ALERT_THRESHOLD
    and st.session_state.err_rate <= ERROR_ALERT_THRESHOLD
):
    st.success("✅ Model operating normally")


# HUMAN APPROVAL / GOVERNANCE

st.subheader("🛡️ Human Approval & Governance")

recommendations = st.session_state.get("last_recommendations", [])

actionable = [
    r for r in recommendations
    if r.get("priority") in ("CRITICAL", "HIGH", "MEDIUM")
]

if actionable:
    st.warning("⚠️ The following actions require your approval:")

    for i, rec in enumerate(actionable):
        priority = rec.get("priority", "")
        action = rec.get("action", "")
        detail = rec.get("detail", "")

        with st.expander(f"[{priority}] {action}"):
            st.write(f"**Detail:** {detail}")
            st.write(f"**Type:** {rec.get('type', 'N/A')}")

            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"✅ Approve", key=f"approve_{i}"):
                    log = {
                        "action": action,
                        "decision": "approved",
                        "timestamp": __import__('time').strftime("%H:%M:%S"),
                    }
                    st.session_state.approval_logs.append(log)
                    st.success(f"✅ Approved: {action}")

            with col2:
                if st.button(f"❌ Reject", key=f"reject_{i}"):
                    log = {
                        "action": action,
                        "decision": "rejected",
                        "timestamp": __import__('time').strftime("%H:%M:%S"),
                    }
                    st.session_state.approval_logs.append(log)
                    st.error(f"❌ Rejected: {action}")

else:
    st.success("✅ No actions require approval — model is healthy")

# Show audit log
if st.session_state.approval_logs:
    st.markdown("**📋 Audit Log:**")
    for log in st.session_state.approval_logs[-5:]:  # show last 5
        icon = "✅" if log["decision"] == "approved" else "❌"
        st.write(f"{icon} [{log['timestamp']}] {log['action']} → {log['decision'].upper()}")


# RECOMMENDATION ENGINE

st.subheader("💊 Recommendations")

recommendations = st.session_state.get("last_recommendations", [])

priority_colors = {
    "CRITICAL": "🔴",
    "HIGH": "🟠",
    "MEDIUM": "🟡",
    "LOW": "🟢",
    "NONE": "🟢",
}

if recommendations:
    for rec in recommendations:
        priority = rec.get("priority", "NONE")
        icon = priority_colors.get(priority, "🟢")
        action = rec.get("action", "")
        detail = rec.get("detail", "")

        if priority == "NONE":
            st.success(f"✅ {action} — {detail}")
        elif priority == "CRITICAL":
            st.error(f"{icon} [{priority}] {action}: {detail}")
        elif priority == "HIGH":
            st.warning(f"{icon} [{priority}] {action}: {detail}")
        else:
            st.info(f"{icon} [{priority}] {action}: {detail}")
else:
    st.success("✅ Model performance is healthy")

st.caption("⏱ Dashboard auto-refreshes every 2 seconds while monitoring is active")