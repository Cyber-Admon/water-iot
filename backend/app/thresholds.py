# WHO-referenced drinking water quality thresholds.
# These are guideline values used for a final year project context,
# not a substitute for certified lab standards.

THRESHOLDS = {
    "turbidity_ntu": {"safe_max": 5.0, "warning_max": 10.0},
    "ph": {"safe_min": 6.5, "safe_max": 8.5, "warning_min": 5.5, "warning_max": 9.5},
    "tds_ppm": {"safe_max": 500.0, "warning_max": 1000.0},
}


def evaluate_turbidity(value: float) -> str:
    if value is None:
        return None
    t = THRESHOLDS["turbidity_ntu"]
    if value <= t["safe_max"]:
        return "safe"
    elif value <= t["warning_max"]:
        return "warning"
    return "danger"


def evaluate_ph(value: float) -> str:
    if value is None:
        return None
    t = THRESHOLDS["ph"]
    if t["safe_min"] <= value <= t["safe_max"]:
        return "safe"
    elif t["warning_min"] <= value <= t["warning_max"]:
        return "warning"
    return "danger"


def evaluate_tds(value: float) -> str:
    if value is None:
        return None
    t = THRESHOLDS["tds_ppm"]
    if value <= t["safe_max"]:
        return "safe"
    elif value <= t["warning_max"]:
        return "warning"
    return "danger"


def build_alerts(node_id: str, turbidity_status, ph_status, tds_status,
                  turbidity_ntu, ph, tds_ppm):
    """Return a list of alert dicts for any parameter not in 'safe' status."""
    alerts = []

    if turbidity_status in ("warning", "danger"):
        alerts.append({
            "node_id": node_id,
            "parameter": "turbidity",
            "value": turbidity_ntu,
            "severity": turbidity_status,
            "message": f"Turbidity reading of {turbidity_ntu} NTU is at {turbidity_status} level."
        })

    if ph_status in ("warning", "danger"):
        alerts.append({
            "node_id": node_id,
            "parameter": "ph",
            "value": ph,
            "severity": ph_status,
            "message": f"pH reading of {ph} is at {ph_status} level."
        })

    if tds_status in ("warning", "danger"):
        alerts.append({
            "node_id": node_id,
            "parameter": "tds",
            "value": tds_ppm,
            "severity": tds_status,
            "message": f"TDS reading of {tds_ppm} ppm is at {tds_status} level."
        })

    return alerts
