# ============================================================
# Smart Home Energy Monitoring Dashboard
#
# Real-time Energy Monitoring Platform
#
# Features
# - Live Monitoring
# - Alert Management
# - Device Health Tracking
# - Energy Analytics
# - Report Downloads
# - Executive Summary
#
# ============================================================

# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd

# pyrefly: ignore [missing-import]
from streamlit_autorefresh import st_autorefresh

from api_client import (
    get_all_readings,
    get_latest,
    get_stats,
    get_device_health,
    get_system_health,
)

from charts import (
    power_chart, 
    energy_chart, 
    appliance_chart, 
    alert_chart,
    power_distribution_chart,
    power_comparison_chart,
    cost_distribution_chart
)

from analytics import calculate_metrics

# Uncomment once report generator is implemented
# from reports.pdf_generator import generate_pdf_report


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Smart Home Energy Monitoring", page_icon="⚡", layout="wide"
)

# Auto refresh dashboard every 5 seconds
st_autorefresh(interval=5000, key="energy_dashboard_refresh")

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("⚡ Navigation")

page = st.sidebar.radio(
    "Select View", ["Overview", "Analytics", "Alerts", "Reports", "Devices"]
)

st.sidebar.markdown("---")

st.sidebar.info("Smart Home Energy Monitoring System v2.5")

# ============================================================
# LOAD DATA
# ============================================================

try:

    df = get_all_readings()
    # st.write("Columns:", df.columns.tolist())

    # st.write("Shape:", df.shape)

    # st.dataframe(df.head())

    if df.empty:
        st.warning("No energy readings available.")
        st.stop()

except Exception as e:

    st.error(f"Backend connection failed.\n\n{e}")

    st.stop()

latest = get_latest()

stats = get_stats()

metrics = calculate_metrics(df)

# ============================================================
# DATA PREPARATION
# ============================================================

if "timestamp" in df.columns:

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    df["date"] = df["timestamp"].dt.date

# ============================================================
# HEADER
# ============================================================

st.title("🏠 Smart Home Energy Monitoring System")

st.caption("Real-Time Energy Analytics Platform")

# ============================================================
# LIVE ALERT BANNER
# ============================================================

latest_alert = latest["alert"]

if latest_alert == "OVERLOAD":

    st.error("🚨 CRITICAL OVERLOAD DETECTED")

elif latest_alert == "HIGH":

    st.warning("⚠ HIGH ENERGY CONSUMPTION DETECTED")

elif latest_alert == "WARNING":

    st.info("⚡ Elevated Energy Usage")

else:

    st.success("✅ System Operating Normally")

st.divider()

# ============================================================
# OVERVIEW PAGE
# ============================================================

if page == "Overview":

    latest_appliances = df.sort_values("timestamp").groupby("appliance").tail(1)
    
    total_power = latest_appliances["power"].sum() / 1000.0  # kW
    total_energy = float(latest_appliances["energy"].sum())  # kWh
    total_cost = float(latest_appliances["cost"].sum())
    voltage = float(latest_appliances["voltage"].mean()) if not latest_appliances.empty else 0.0

    try:
        health = get_system_health()
    except Exception:
        health = {"mqtt_connected": False, "messages_received": 0, "seconds_since_last_message": None, "uptime_seconds": 0}

    mqtt_status = "ONLINE" if health.get("mqtt_connected") else "OFFLINE"
    
    st.markdown("### 🏠 HOUSEHOLD ENERGY SUMMARY")
    st.markdown(f"""
    <div style="padding: 20px; background-color: #1e293b; border-radius: 10px; margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between;">
            <div><b>Supply Voltage</b> <span style="font-size: 10px; background: #3b82f6; color: white; padding: 2px 6px; border-radius: 8px; margin-left: 4px;">LIVE</span><br><span style="font-size: 24px;">{voltage:.2f} V</span></div>
            <div><b>Total Power</b> <span style="font-size: 10px; background: #3b82f6; color: white; padding: 2px 6px; border-radius: 8px; margin-left: 4px;">LIVE</span><br><span style="font-size: 24px;">{total_power:.2f} kW</span></div>
            <div><b>Total Energy</b> <span style="font-size: 10px; background: #8b5cf6; color: white; padding: 2px 6px; border-radius: 8px; margin-left: 4px;">CUMULATIVE</span><br><span style="font-size: 24px;">{total_energy:.2f} kWh</span></div>
            <div><b>Estimated Cost</b> <span style="font-size: 10px; background: #8b5cf6; color: white; padding: 2px 6px; border-radius: 8px; margin-left: 4px;">CUMULATIVE</span><br><span style="font-size: 24px;">₹{total_cost:.2f}</span></div>
            <div><b>Active Appliances</b><br><span style="font-size: 24px;">{len(latest_appliances)} / 4</span></div>
            <div><b>MQTT Status</b><br><span style="font-size: 24px; color: {'#4ade80' if mqtt_status == 'ONLINE' else '#ef4444'};">{mqtt_status}</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ⚡ APPLIANCE ENERGY MONITORING")
    
    cols = st.columns(4)
    icons = {"Fan": "🌀", "Tv": "📺", "Refrigerator": "❄️", "Ac": "❄️"}
    
    for idx, (_, row) in enumerate(latest_appliances.iterrows()):
        app_name = row["appliance"]
        icon = icons.get(app_name, "🔌")
        status = row["alert"]
        color = "#4ade80"
        if status == "WARNING": color = "#facc15"
        elif status == "HIGH": color = "#f97316"
        elif status == "OVERLOAD": color = "#ef4444"
        
        with cols[idx % 4]:
            html_content = f"""
<div style="padding: 15px; background-color: #1e293b; border-radius: 10px; border-left: 5px solid {color}; margin-bottom: 15px; position: relative;">
<h3 style="margin-top: 0;">{icon} {app_name.upper()}</h3>
<p style="margin: 5px 0; font-size: 17px; display: flex; justify-content: space-between; align-items: center;">
<span><b>Current:</b> {row['current']:.2f} A</span>
<span style="font-size: 10px; background: #3b82f6; color: white; padding: 2px 6px; border-radius: 8px;">LIVE</span>
</p>
<p style="margin: 5px 0; font-size: 17px; display: flex; justify-content: space-between; align-items: center;">
<span><b>Power:</b> {row['power']:.0f} W</span>
<span style="font-size: 10px; background: #3b82f6; color: white; padding: 2px 6px; border-radius: 8px;">LIVE</span>
</p>
<div style="height: 1px; background: #334155; margin: 10px 0;"></div>
<p style="margin: 5px 0; font-size: 17px; display: flex; justify-content: space-between; align-items: center;">
<span><b>Energy:</b> {row['energy']:.2f} kWh</span>
<span style="font-size: 10px; background: #8b5cf6; color: white; padding: 2px 6px; border-radius: 8px;">TOTAL</span>
</p>
<p style="margin: 5px 0; font-size: 17px; display: flex; justify-content: space-between; align-items: center;">
<span><b>Cost:</b> ₹{row['cost']:.2f}</span>
<span style="font-size: 10px; background: #8b5cf6; color: white; padding: 2px 6px; border-radius: 8px;">TOTAL</span>
</p>
<p style="margin: 15px 0 0 0; font-size: 16px; color: {color};"><b>● {status}</b></p>
</div>
"""
            st.markdown(html_content, unsafe_allow_html=True)

    st.divider()

    st.markdown("### 📊 POWER DISTRIBUTION")
    st.plotly_chart(power_distribution_chart(latest_appliances), use_container_width=True)

    st.markdown("### 📈 APPLIANCE POWER COMPARISON")
    st.plotly_chart(power_comparison_chart(latest_appliances), use_container_width=True)
    
    st.markdown("### 💰 COST DISTRIBUTION")
    st.plotly_chart(cost_distribution_chart(latest_appliances), use_container_width=True)

    st.markdown("### 📈 HISTORICAL POWER TREND")
    st.plotly_chart(power_chart(df), use_container_width=True)

# ============================================================
# ANALYTICS PAGE
# ============================================================

elif page == "Analytics":

    st.subheader("📊 Energy Analytics")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Peak Power", f"{metrics['max_power']:.2f} W")

    c2.metric("Average Power", f"{metrics['avg_power']:.2f} W")

    c3.metric("Total Energy", f"{metrics['total_energy']:.2f} kWh")

    c4.metric("Total Cost", f"₹ {metrics['total_cost']:.2f}")

    st.divider()

    left, right = st.columns(2)

    with left:

        st.plotly_chart(appliance_chart(df), use_container_width=True)

    with right:

        st.plotly_chart(alert_chart(df), use_container_width=True)

# ============================================================
# ALERTS PAGE
# ============================================================

elif page == "Alerts":

    st.subheader("🚦 Alert Monitoring Center")

    selected_alert = st.radio(
        "Filter Alert Level",
        ["ALL", "NORMAL", "WARNING", "HIGH", "OVERLOAD"],
        horizontal=True,
    )

    filtered_df = df.copy()

    if selected_alert != "ALL":

        filtered_df = df[df["alert"] == selected_alert]

    st.dataframe(
        filtered_df.sort_values(by="timestamp", ascending=False),
        use_container_width=True,
    )

# ============================================================
# REPORTS PAGE
# ============================================================

elif page == "Reports":

    st.subheader("📄 Reports & Exports")

    csv_data = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download CSV Report",
        data=csv_data,
        file_name="energy_report.csv",
        mime="text/csv",
    )

    st.markdown("---")

    st.info("PDF export will be enabled after integrating the report generator.")

    # Example Future Implementation
    #
    # if st.button(
    #     "Generate PDF Report"
    # ):
    #
    #     pdf_path = generate_pdf_report(df)
    #
    #     with open(
    #         pdf_path,
    #         "rb"
    #     ) as pdf_file:
    #
    #         st.download_button(
    #             "Download PDF",
    #             pdf_file,
    #             file_name="energy_report.pdf"
    #         )

# ============================================================
# DEVICES PAGE
# ============================================================

elif page == "Devices":

    st.subheader("🏠 Appliance Status Board")

    latest_appliances = df.sort_values("timestamp").groupby("appliance").tail(1)

    status_board = latest_appliances[["appliance", "power", "alert"]].sort_values(
        by="power", ascending=False
    )

    st.dataframe(status_board, use_container_width=True)

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Smart Home Energy Monitoring System | FastAPI + SQLite + Plotly + Streamlit"
)
