from dataclasses import dataclass, field

@dataclass
class AgentState:
    question: str
    context: str = ""
    dbt_analysis: dict | None = None
    final_answer: str = ""
    step: int = 0
    done: bool = False
