def evaluate_task(task: str, result: str) -> str:
    """
    Evaluator Agent:
    Decides whether to accept, retry, or replan a task result.
    """

    if not result or len(result.strip()) < 40:
        # Output too short or empty → retry
        return "retry"

    # Simple relevance check
    task_keywords = task.lower().split()[:3]
    relevance_hits = sum(1 for kw in task_keywords if kw in result.lower())

    if relevance_hits == 0:
        # Output exists but does not address the task → replan
        return "replan"

    # Output looks acceptable
    return "accept"
