def analyze_dbt_model(model_sql: str) -> dict:
    """
    Lightweight dbt model analysis.
    This is NOT parsing SQL perfectly — it's architectural pattern detection.
    """

    findings = {
        "grain": None,
        "issues": [],
        "recommendations": []
    }

    sql_lower = model_sql.lower()

    # 1. Detect potential grain
    if "group by" in sql_lower:
        findings["grain"] = "Aggregated (GROUP BY detected)"
    else:
        findings["grain"] = "Row-level (no GROUP BY detected)"

    # 2. Detect anti-patterns
    if "case when" in sql_lower:
        findings["issues"].append(
            "CASE logic detected — business logic may be leaking into mart layer"
        )

    if "join" in sql_lower and "stg_" not in sql_lower:
        findings["issues"].append(
            "Join detected without clear staging reference — verify layering"
        )

    if "select *" in sql_lower:
        findings["issues"].append(
            "SELECT * used — violates modeling standards"
        )

    # 3. Recommendations
    if findings["issues"]:
        findings["recommendations"].append(
            "Refactor model to align with dbt layering and grain standards"
        )

    return findings
