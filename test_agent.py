from planner import planner

question = "What is the canonical grain for Member?"

result = planner(question)

print("Answer:\n", result["answer"])
print("\nSources:\n", result["sources"])
