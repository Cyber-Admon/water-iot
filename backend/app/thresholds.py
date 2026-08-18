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


def classify_usability(turbidity_status: str, ph_status: str, tds_status: str) -> dict:
    """
    Combines the three per-parameter WHO-threshold statuses into an
    overall usability classification. Rule-based, using the exact
    same thresholds already validating each parameter individually,
    so there's one consistent source of truth across the system.
    """
    statuses = [s for s in [turbidity_status, ph_status, tds_status] if s is not None]

    if not statuses:
        return {
            "usability_class": "Unknown",
            "guidance": "Insufficient sensor data to determine usability."
        }

    danger_count = statuses.count("danger")
    warning_count = statuses.count("warning")

    # pH danger specifically makes water unsafe even for irrigation,
    # since extreme pH harms soil and crops, not just human consumption
    ph_is_danger = ph_status == "danger"

    if danger_count == 0 and warning_count == 0:
        return {
            "usability_class": "Potable",
            "guidance": "Water quality meets WHO-referenced safe thresholds across all measured parameters. Suitable for drinking and domestic use."
        }

    if danger_count == 0 and warning_count > 0:
        return {
            "usability_class": "Treatment Recommended",
            "guidance": "One or more parameters are outside ideal safe range but not at dangerous levels. Basic treatment (filtration/boiling) recommended before drinking."
        }

    if danger_count >= 1 and not ph_is_danger:
        return {
            "usability_class": "Irrigation Only",
            "guidance": "Water is unsafe for drinking due to elevated contamination levels, but may be usable for irrigation or non-potable purposes. Not recommended for human consumption."
        }

    return {
        "usability_class": "Unsafe for All Use",
        "guidance": "Water quality is significantly outside safe thresholds, including pH extremes. Not recommended for drinking, irrigation, or general use without treatment."
    }