import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are an autonomous task execution agent.
Execute ONLY the given task.
Do not plan, do not evaluate, do not ask questions.
Produce clear, structured, actionable output.
"""

def execute_task(task: str) -> tuple[str, bool]:
    if not task or not isinstance(task, str):
        return "", False

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": task}
            ],
            temperature=0.3,
            max_tokens=500,
        )

        result = response.choices[0].message.content.strip()
        return result, True

    except Exception as e:
        return f"Execution error: {str(e)}", False
