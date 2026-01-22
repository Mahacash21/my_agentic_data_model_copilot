from agent_tools import architecture_rag_tool
from dbt_analyzer import analyze_dbt_model
from langchain_community.llms import Ollama

llm = Ollama(model="phi3")

SYSTEM_PROMPT = """
You are a Principal Data Architect Copilot specializing in healthcare.

When reviewing dbt models:
- Validate grain
- Enforce dbt layering standards
- Flag anti-patterns
- Suggest architectural improvements
"""

def planner(question: str, dbt_model_sql: str | None = None):
    print("📐 Architect Copilot thinking...")

    rag_result = architecture_rag_tool(question)

    dbt_analysis = None
    if dbt_model_sql:
        print("🔍 Analyzing dbt model...")
        dbt_analysis = analyze_dbt_model(dbt_model_sql)

    prompt = f"""
{SYSTEM_PROMPT}

Architecture Context:
{rag_result['context']}

dbt Analysis:
{dbt_analysis}

Question:
{question}

Provide:
- Findings
- Risks
- Recommendations
"""

    response = llm.invoke(prompt)

    return {
        "answer": response.strip(),
        "sources": rag_result["sources"],
        "dbt_analysis": dbt_analysis
    }
