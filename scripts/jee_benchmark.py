import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

# The rest of your imports
import json
from backend.app.core.math_agent import math_agent, AgentState

# Placeholder JEE-like dataset. In a real scenario, you would
# use a larger, dedicated dataset.
JEE_BENCHMARK_DATA = [
    {
        "question": "If the sum of an infinite geometric progression is 15 and the sum of the squares of its terms is 45, find the first term and the common ratio.",
        "answer": "First term is 5, common ratio is 2/3."
    },
    {
        "question": "What is the value of the definite integral of sin(x) from 0 to pi?",
        "answer": "2"
    },
    {
        "question": "Solve the quadratic equation x^2 - 4x + 4 = 0.",
        "answer": "x = 2"
    }
]

def run_jee_benchmark():
    """
    Runs the agent against a set of JEE-level problems and reports the results.
    """
    print("Starting JEE Benchmark...")
    total_questions = len(JEE_BENCHMARK_DATA)
    correct_answers = 0

    for i, problem in enumerate(JEE_BENCHMARK_DATA):
        question = problem["question"]
        correct_answer = problem["answer"]

        print(f"\n--- Problem {i + 1}/{total_questions}: {question}")

        try:
            # Invoke the agent with the problem question
            final_state = math_agent.invoke(AgentState(question=question, retrieved_content="", solution="", source="error"))
            agent_solution = final_state.get("solution", "").strip()
            agent_source = final_state.get("source", "error")

            print(f"Agent's solution (Source: {agent_source}):\n{agent_solution}")
            print(f"Correct answer: {correct_answer}")

            # Simple check for correctness
            # This is a basic check. For real-world, this would need a more
            # robust evaluation method, e.g., a dedicated evaluation LLM.
            if correct_answer.lower() in agent_solution.lower():
                correct_answers += 1
                print("Result: Correct ✅")
            else:
                print("Result: Incorrect ❌")

        except Exception as e:
            print(f"An error occurred while processing the question: {e}")
            print("Result: Skipped ❌")

    # Final report
    accuracy = (correct_answers / total_questions) * 100
    print("\n--- Benchmark Complete ---")
    print(f"Total Questions: {total_questions}")
    print(f"Correctly Solved: {correct_answers}")
    print(f"Accuracy: {accuracy:.2f}%")

if __name__ == "__main__":
    run_jee_benchmark()