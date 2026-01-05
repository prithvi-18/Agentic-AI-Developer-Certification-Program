def plan_tasks(state: dict) -> list[str]:
    """
    Planner Agent:
    - Decomposes a high-level goal into ordered tasks
    - Adapts plan during replanning
    """
    # ----- Stop planning if goal already satisfied -----
    if state.get("completed_tasks") and not state.get("failed_tasks"):
        return []


    goal = state["goal"]
    completed = state.get("completed_tasks", [])
    failed = state.get("failed_tasks", [])
    replan_count = state.get("replan_count", 0)

    # ----- Initial Planning -----
    if replan_count == 0:
        tasks = [
            f"Create a detailed 4-week Python interview preparation plan. "
            f"Include weekly goals, daily topics, practice tasks, and revision strategy."
        ]
        return tasks


    # ----- Replanning Logic -----
    # If something failed, refine remaining tasks
    tasks = []

    if failed:
        tasks.append(
            "Re-evaluate previous outputs and identify what is missing or incorrect"
        )

    tasks.extend([
        "Refine the remaining steps to better satisfy the goal",
        "Generate improved content based on feedback",
        "Re-check final output for completeness and alignment with the goal"
    ])

    return tasks
