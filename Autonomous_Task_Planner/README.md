# Autonomous Task Planner – Module 3

## Overview

This project implements an autonomous task planning system that follows a
Plan → Execute → Evaluate → Retry/Replan loop.

The system can break a high-level goal into tasks, execute them step-by-step,
evaluate results, retry failed tasks, and replan when necessary until the goal
is completed or limits are reached.

## Architecture

The system consists of the following components:

- Planner: Converts a goal into an ordered list of tasks
- Executor: Executes one task at a time
- Evaluator: Decides whether to accept, retry, or replan based on execution result
- State Manager: Maintains shared state across the entire execution
- Config: Safety limits to prevent infinite loops

## Execution Flow

1. Initialize state with user goal
2. Planner generates task list
3. Executor runs the next task
4. Evaluator evaluates result
5. System retries or replans if needed
6. Loop continues until goal completion or failure

## Files Description

- state.py: Maintains global execution state
- planner.py: Task decomposition logic
- executor.py: Task execution logic
- evaluator.py: Decision-making logic
- config.py: Retry and safety limits
- run.py: Main autonomous execution loop

## How to Run

```bash
pip install -r requirements.txt
python main.py

## Note
The Streamlit UI (ui.py) is optional and provided only for demonstration.
The core autonomous system is executed via main.py.
