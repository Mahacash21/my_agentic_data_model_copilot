from agent_loop import run_agent

dbt_sql = """
select
    member_id,
    case when status = 'A' then 'Active' else 'Inactive' end as member_status
from members
join enrollments using (member_id)
"""

question = "Review this dbt model for architectural issues."

state = run_agent(question, dbt_model_sql=dbt_sql)

print("\n✅ FINAL ANSWER:\n")
print(state.final_answer)
