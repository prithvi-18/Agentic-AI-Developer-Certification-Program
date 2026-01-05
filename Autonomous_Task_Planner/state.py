def initialize_state(goal: str) -> dict:
    return {
        "goal": goal,
        "plan": [],
        "current_task": None,
        "completed_tasks": [],
        "failed_tasks": [],
        "results": {},
        "status": "running",
        "replan_count": 0
    }
