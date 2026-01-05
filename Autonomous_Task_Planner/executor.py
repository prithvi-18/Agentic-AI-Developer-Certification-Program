def execute_task(task: str) -> tuple[str, bool]:
    """
    Executor Agent:
    - Executes a single task
    - Chooses an execution strategy
    - Returns (result, success)
    """

    if not task or not isinstance(task, str):
        return "", False

    task_lower = task.lower()

    # ---- Execution Strategy Selection ----
    if "identify" in task_lower:
        result = (
            "Key requirements identified:\n"
            "- Clear understanding of the goal\n"
            "- Logical task breakdown\n"
            "- Structured final output\n"
            "- Iterative refinement"
        )

    elif "break" in task_lower or "sequence" in task_lower:
        result = (
            "The goal can be broken into sequential steps:\n"
            "1. Analyze the goal requirements\n"
            "2. Plan actionable tasks\n"
            "3. Execute tasks one by one\n"
            "4. Evaluate results and refine\n"
            "5. Deliver final output"
        )

    elif "generate" in task_lower or "content" in task_lower:
        result = (
            "Detailed content has been generated for the defined steps, "
            "ensuring clarity, logical progression, and alignment with the goal."
        )

    elif "review" in task_lower or "check" in task_lower:
        result = (
            "The generated content was reviewed for completeness, relevance, "
            "and coherence with the original goal."
        )

    elif "final" in task_lower or "consolidated" in task_lower:
        result = (
            "Final output prepared by consolidating all validated steps "
            "into a coherent and structured result."
        )

    else:
        # Fallback execution
        result = f"Executed task: {task} with reasonable output."

    success = True
    return result, success
