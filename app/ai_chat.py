import json
import subprocess
from functools import lru_cache

DATA_FILE = "output.jsonl"
BEST_FILE = "best_hospital.jsonl"

# -----------------------------
# Load latest streaming data
# -----------------------------
def load_latest_data():
    rows = []
    try:
        with open(DATA_FILE) as f:
            for line in f:
                rows.append(json.loads(line))
    except:
        pass
    return rows[-30:]  # keep it small for speed


# -----------------------------
# Rule-based FAST answers (no AI)
# -----------------------------
def fast_answer(question, data):
    q = question.lower()

    if "icu" in q and ("available" in q or "empty" in q):
        available = [
            f"{r['hospital_name']} (ICU: {r['icu_beds']})"
            for r in data if r.get("icu_beds", 0) > 0
        ]
        return "ICU available at: " + ", ".join(available) if available else "No ICU beds available."

    if "oxygen" in q:
        available = [
            f"{r['hospital_name']} (Oxygen: {r['oxygen_beds']})"
            for r in data if r.get("oxygen_beds", 0) > 0
        ]
        return "Oxygen beds available at: " + ", ".join(available) if available else "No oxygen beds available."

    if "recommend" in q or "best hospital" in q or "where should" in q:
        return get_best_hospital()

    return None


# -----------------------------
# Best hospital (precomputed)
# -----------------------------
def get_best_hospital():
    try:
        with open(BEST_FILE) as f:
            lines = f.readlines()
            if not lines:
                return "No hospital currently has ICU beds available."
            d = json.loads(lines[-1])
            return f"Recommended hospital: {d['hospital']} (ICU: {d['icu']}, Oxygen: {d['oxygen']})"
    except:
        return "Recommendation service unavailable."


# -----------------------------
# Cached AI call (FAST)
# -----------------------------
@lru_cache(maxsize=50)
def ask_ai_cached(prompt: str) -> str:
    try:
        result = subprocess.run(
            ["ollama", "run", "phi"],
            input=prompt,
            text=True,
            capture_output=True,
            timeout=8
        )
        return result.stdout.strip()
    except:
        return "AI service not available right now."


# -----------------------------
# Main chat loop
# -----------------------------
def main():
    print("\n--- Hospital AI Assistant ---")
    print("Type a question (or 'exit')\n")

    while True:
        question = input("You: ")
        if question.lower() in ("exit", "quit"):
            break

        data = load_latest_data()

        quick = fast_answer(question, data)
        if quick:
            print("AI:", quick)
            print("-" * 50)
            continue

        print("AI: thinking...")
        context = f"Hospital data:\n{json.dumps(data, indent=2)}\n\nQuestion: {question}"
        answer = ask_ai_cached(context)
        print("AI:", answer)
        print("-" * 50)


if __name__ == "__main__":
    main()

