from planner import planner

dbt_sql = """
select
    member_id,
    case when status = 'A' then 'Active' else 'Inactive' end as member_status
from members
join enrollments using (member_id)
"""

question = "Review this dbt model for architectural issues."

result = planner(question, dbt_model_sql=dbt_sql)

print("\nANSWER:\n", result["answer"])
print("\nDBT ANALYSIS:\n", result["dbt_analysis"])
print("\nSOURCES:\n", result["sources"])
