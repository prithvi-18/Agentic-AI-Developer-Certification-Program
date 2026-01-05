import streamlit as st
from main import run

st.set_page_config(page_title="Autonomous Task Planner", layout="centered")

st.title("🧠 Autonomous Task Planner (Module 3)")
st.write(
    "This UI demonstrates an autonomous agent system that plans, executes, "
    "evaluates, adapts, and terminates safely based on a user-defined goal."
)

# ---- User Input ----
goal = st.text_input(
    "Enter a high-level goal:",
    placeholder="e.g. Prepare a 2-week Python interview plan"
)

run_button = st.button("Run Agent System")

# ---- Run System ----
if run_button:
    if not goal.strip():
        st.warning("Please enter a goal before running the system.")
    else:
        with st.spinner("Running autonomous agent system..."):
            final_state = run(goal)

        st.subheader("📊 Execution Result")

        st.write(f"**Final Status:** `{final_state['status']}`")
        st.write(f"**Replan Count:** {final_state['replan_count']}")

        st.subheader("✅ Completed Tasks")
        for task in final_state["completed_tasks"]:
            st.markdown(f"- {task}")

        st.subheader("📝 Generated Output")

        for task, output in final_state["results"].items():
            st.markdown(f"**{task}**")
            st.write(output)


        if final_state["failed_tasks"]:
            st.subheader("❌ Failed Tasks")
            for task in final_state["failed_tasks"]:
                st.markdown(f"- {task}")
