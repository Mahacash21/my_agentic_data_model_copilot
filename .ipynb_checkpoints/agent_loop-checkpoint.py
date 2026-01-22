from agent_state import AgentState
from decision_prompt import DECISION_PROMPT
from agent_tools import architecture_rag_tool
from dbt_analyzer import analyze_dbt_model
from langchain_ollama import OllamaLLM

# --- LLM (stable + deterministic) ---
llm = OllamaLLM(
    model="phi3",
    temperature=0
)


def _parse_decision(raw) -> str:
    """
    Extract ONLY the first valid decision token
    """
    if raw is None:
        return ""

    # OllamaLLM may return str OR BaseMessage
    if hasattr(raw, "content"):
        raw = raw.content

    if not isinstance(raw, str):
        return ""

    token = raw.strip().split()[0].upper()
    allowed = {"RAG_LOOKUP", "ANALYZE_DBT", "FINAL_ANSWER"}
    return token if token in allowed else ""


def _clean_context(text: str) -> str:
    """
    Prevent prompt / agent personality contamination
    """
    forbidden_phrases = [
        "You are",
        "Available actions",
        "Rules:",
        "SYSTEM",
        "Respond with",
        "Begin only after"
    ]

    cleaned = text or ""
    for phrase in forbidden_phrases:
        cleaned = cleaned.replace(phrase, "")

    return cleaned.strip()


def run_agent(question: str, dbt_model_sql: str | None = None):
    state = AgentState(question=question)

    while not state.done:
        state.step += 1
        print(f"\n🧠 Step {state.step}")

        # ---- HARD RULES (NO LLM YET) ----
        if not state.context:
            decision = "RAG_LOOKUP"
        elif dbt_model_sql and not state.dbt_analysis:
            decision = "ANALYZE_DBT"
        else:
            decision = "FINAL_ANSWER"

        print("➡️ Decision:", decision)

        # ---- EXECUTION ----
        if decision == "RAG_LOOKUP":
            result = architecture_rag_tool(state.question)
            state.context = _clean_context(result.get("context", ""))

        elif decision == "ANALYZE_DBT":
            state.dbt_analysis = analyze_dbt_model(dbt_model_sql)

        elif decision == "FINAL_ANSWER":
            final_prompt = f"""
You are a Principal Data Architect.

Architecture Context:
{state.context}

dbt Analysis:
{state.dbt_analysis}

Question:
{state.question}

Respond with:
- Findings
- Risks
- Recommendations
"""
            state.final_answer = llm.invoke(final_prompt).strip()
            state.done = True

    return state
