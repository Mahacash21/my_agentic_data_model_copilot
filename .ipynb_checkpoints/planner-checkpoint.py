from agent_tools import architecture_rag_tool
from langchain_community.llms import Ollama

# Initialize LLM
llm = Ollama(model="phi3")  # or your preferred Ollama model

SYSTEM_PROMPT = """
You are a Principal Data Architect Copilot specializing in healthcare.

Your job:
- Reason about data architecture questions
- Use architecture knowledge (standards, canonical models, checklists)
- Suggest actions, identify risks, and explain tradeoffs
- Cite sources when possible
"""

def planner(question: str):
    """
    Returns a reasoned response using RAG context.
    """
    # Step 1: retrieve relevant architecture knowledge
    rag_result = architecture_rag_tool(question)

    # Step 2: feed into LLM
    prompt = f"""
{SYSTEM_PROMPT}

Context:
{rag_result['context']}

Question:
{question}

Please answer clearly, and cite sources where possible.
"""

    response = llm.invoke(prompt)
    answer = response.strip()

    return {
        "answer": answer,
        "sources": rag_result['sources']
    }
