# ============================================================
# analytics.py
#
# Analytics calculations used across dashboard
#
# ============================================================


def calculate_metrics(df):

    latest_appliances = df.sort_values("timestamp").groupby("appliance").tail(1)
    total_energy = float(latest_appliances["energy"].sum()) if not latest_appliances.empty else 0.0
    total_cost = float(latest_appliances["cost"].sum()) if not latest_appliances.empty else 0.0

    return {
        "max_power": float(df["power"].max()),
        "avg_power": float(df["power"].mean()),
        "total_energy": total_energy,
        "total_cost": total_cost,
        "total_records": len(df),
        "total_alerts": len(df[df["alert"] != "NORMAL"]),
    }
