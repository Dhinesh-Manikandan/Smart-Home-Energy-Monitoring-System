# ============================================================
# charts.py
#
# Centralized Plotly chart styling for the
# Smart Home Energy Monitoring System
#
# ============================================================

import plotly.express as px


# ============================================================
# COMMON THEME
# ============================================================


def apply_theme(fig):

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0f172a",
        plot_bgcolor="#0f172a",
        font=dict(family="Arial", size=14),
        title_font=dict(size=22),
        margin=dict(l=20, r=20, t=60, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=450,
    )

    fig.update_xaxes(showgrid=False)

    fig.update_yaxes(gridcolor="rgba(255,255,255,0.08)")

    return fig


# ============================================================
# POWER TREND
# ============================================================


def power_chart(df):

    fig = px.line(
        df, x="timestamp", y="power", title="⚡ Power Consumption Trend", markers=True
    )

    fig.update_traces(line_width=3)

    return apply_theme(fig)


# ============================================================
# ENERGY TREND
# ============================================================


def energy_chart(df):

    fig = px.area(df, x="timestamp", y="energy", title="🔋 Energy Consumption Trend")

    return apply_theme(fig)


# ============================================================
# APPLIANCE DISTRIBUTION
# ============================================================


def appliance_chart(df):

    appliance_counts = df["appliance"].value_counts().reset_index()

    appliance_counts.columns = ["appliance", "count"]

    fig = px.pie(
        appliance_counts,
        names="appliance",
        values="count",
        title="🏠 Appliance Distribution",
        hole=0.55,
    )

    return apply_theme(fig)


# ============================================================
# ALERT DISTRIBUTION
# ============================================================


def alert_chart(df):

    fig = px.histogram(df, x="alert", title="🚨 Alert Distribution")

    return apply_theme(fig)


# ============================================================
# APPLIANCE POWER DISTRIBUTION (DONUT)
# ============================================================

def power_distribution_chart(df):
    fig = px.pie(
        df,
        names="appliance",
        values="power",
        title="⚡ Power Distribution by Appliance",
        hole=0.55,
    )
    return apply_theme(fig)


# ============================================================
# APPLIANCE POWER COMPARISON (BAR)
# ============================================================

def power_comparison_chart(df):
    fig = px.bar(
        df,
        x="appliance",
        y="power",
        title="📈 Appliance Power Consumption",
        color="appliance"
    )
    return apply_theme(fig)


# ============================================================
# APPLIANCE COST DISTRIBUTION (BAR)
# ============================================================

def cost_distribution_chart(df):
    fig = px.bar(
        df,
        x="appliance",
        y="cost",
        title="💰 Estimated Cost by Appliance",
        color="appliance"
    )
    return apply_theme(fig)


# ============================================================
# TEMPERATURE TREND
# ============================================================

def temperature_chart(df):
    df_clean = df.dropna(subset=['temperature'])
    fig = px.line(
        df_clean, x="timestamp", y="temperature", title="🌡️ Temperature Trend", markers=True
    )
    fig.update_traces(line_color="#ef4444")
    return apply_theme(fig)


# ============================================================
# HUMIDITY TREND
# ============================================================

def humidity_chart(df):
    df_clean = df.dropna(subset=['humidity'])
    fig = px.line(
        df_clean, x="timestamp", y="humidity", title="💧 Humidity Trend", markers=True
    )
    fig.update_traces(line_color="#3b82f6")
    return apply_theme(fig)

