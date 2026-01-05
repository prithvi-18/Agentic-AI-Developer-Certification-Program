from state import initialize_state
from planner import plan_tasks
from executor import execute_task
from evaluator import evaluate_task
from config import MAX_REPLANS, MAX_RETRIES_PER_TASK, MAX_TOTAL_TASKS, MAX_EXECUTED_TASKS


def run(goal: str):
    state = initialize_state(goal)

    while state["status"] == "running":
        if state["replan_count"] > 0 and state["completed_tasks"]:
            state["status"] = "completed"
            break

        # Planning phase
        if not state["plan"]:
            state["plan"] = plan_tasks(state)

            if not state["plan"]:
                state["status"] = "completed"
                break

            if len(state["plan"]) > MAX_TOTAL_TASKS:
                state["status"] = "failed"
                break


        # Select next task
        task = state["plan"].pop(0)
        state["current_task"] = task
        
        retry_count = 0
        replanned = False

        while retry_count <= MAX_RETRIES_PER_TASK:
            result, success = execute_task(task)


            if not success:
                retry_count += 1
                continue

            decision = evaluate_task(task, result)

            if decision == "accept":
                # ---- Global execution safety cap ----
                if len(state["completed_tasks"]) >= MAX_EXECUTED_TASKS:
                    state["status"] = "failed"
                    return state

                state["completed_tasks"].append(task)
                state["results"][task] = result
                break

            elif decision == "retry":
                retry_count += 1
                continue

            elif decision == "replan":
                state["failed_tasks"].append(task)
                state["replan_count"] += 1
                replanned = True

                if state["replan_count"] > MAX_REPLANS:
                    state["status"] = "failed"
                    return state

                state["plan"] = []
                break

        # ----- Handle retry exhaustion -----
        if retry_count > MAX_RETRIES_PER_TASK and not replanned:
            state["failed_tasks"].append(task)
            state["replan_count"] += 1

            if state["replan_count"] > MAX_REPLANS:
                state["status"] = "failed"
                return state

            # Force replanning
            state["plan"] = []

            continue



        if not state["plan"] and state["status"] != "failed":
            continue

    return state


if __name__ == "__main__":
    goal = "Prepare a 2-week Python interview plan"
    final_state = run(goal)

    print("Final Status:", final_state["status"])
    print("Completed Tasks:", final_state["completed_tasks"])
