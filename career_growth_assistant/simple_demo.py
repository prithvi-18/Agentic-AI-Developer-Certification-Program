"""
SIMPLE 3-AGENT DEMO - Career Growth Assistant
Run this to understand multi-agent concepts immediately!

Usage:
    python simple_demo.py
"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

# Load environment
load_dotenv()

# Initialize LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.7,
    api_key=os.getenv("GROQ_API_KEY")
)

print("\n" + "="*70)
print("🚀 CAREER GROWTH ASSISTANT - SIMPLE DEMO")
print("="*70)

# ==========================================
# AGENT 1: ROLE ANALYZER
# ==========================================
def agent_1_role_analyzer(current_role: str, target_role: str, current_skills: list):
    """
    Agent 1: Analyzes the gap between current and target role
    """
    print("\n" + "="*70)
    print("📊 AGENT 1: ROLE ANALYZER")
    print("="*70)
    
    system_prompt = """You are a career analyst. Analyze the gap between two roles.
    
    Provide:
    1. Current role overview
    2. Target role overview
    3. Top 5 skill gaps
    4. Timeline estimate for transition (weeks)
    5. Key recommendations
    
    Be specific and actionable."""
    
    user_prompt = f"""Analyze this career transition:
    
    Current Role: {current_role}
    Current Skills: {', '.join(current_skills)}
    Target Role: {target_role}
    
    What are the key gaps and how long would transition take?"""
    
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ])
    
    print(f"\n{response.content}")
    return response.content


# ==========================================
# AGENT 2: INTERVIEW PREPARER
# ==========================================
def agent_2_interview_preparer(target_role: str, gap_analysis: str):
    """
    Agent 2: Generates interview questions for target role
    """
    print("\n" + "="*70)
    print("❓ AGENT 2: INTERVIEW PREPARER")
    print("="*70)
    
    system_prompt = """You are an interview coach. Generate interview questions.
    
    Provide:
    1. 5 technical questions (for target role)
    2. 3 behavioral questions
    3. 2 situational questions
    4. Difficulty level for each (Easy/Medium/Hard)
    5. Why each question is important
    
    Format clearly."""
    
    user_prompt = f"""Based on this gap analysis:
    
    {gap_analysis}
    
    Generate interview questions for someone transitioning to: {target_role}
    Focus on the skill gaps identified above."""
    
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ])
    
    print(f"\n{response.content}")
    return response.content


# ==========================================
# AGENT 3: LEARNING CREATOR
# ==========================================
def agent_3_learning_creator(gap_analysis: str, interview_questions: str):
    """
    Agent 3: Creates learning path based on gap analysis and interview prep
    """
    print("\n" + "="*70)
    print("📚 AGENT 3: LEARNING CREATOR")
    print("="*70)
    
    system_prompt = """You are a learning path designer. Create a week-by-week plan.
    
    Provide:
    1. 12-week learning roadmap
    2. Week-by-week topics
    3. Recommended resources (free and paid)
    4. Milestones at weeks 4, 8, 12
    5. Estimated hours per week
    
    Be realistic."""
    
    user_prompt = f"""Create a learning path based on:
    
    Gap Analysis:
    {gap_analysis}
    
    Interview Focus:
    {interview_questions}
    
    Create a 12-week plan to close skill gaps and prepare for interviews."""
    
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ])
    
    print(f"\n{response.content}")
    return response.content


# ==========================================
# ORCHESTRATOR: Runs all agents
# ==========================================
def run_career_assistant(current_role: str, target_role: str, current_skills: list):
    """
    Orchestrator: Runs all 3 agents in sequence
    Passes output of one agent to the next
    """
    print("\n\n" + "🎯 "*15)
    print("STARTING MULTI-AGENT SYSTEM")
    print("🎯 "*15)
    
    print(f"\nUser Input:")
    print(f"  Current Role: {current_role}")
    print(f"  Target Role: {target_role}")
    print(f"  Current Skills: {', '.join(current_skills)}")
    
    # RUN AGENT 1
    gap_analysis = agent_1_role_analyzer(current_role, target_role, current_skills)
    
    # RUN AGENT 2 (uses Agent 1 output)
    interview_questions = agent_2_interview_preparer(target_role, gap_analysis)
    
    # RUN AGENT 3 (uses Agent 1 and 2 outputs)
    learning_path = agent_3_learning_creator(gap_analysis, interview_questions)
    
    # FINAL SUMMARY
    print("\n" + "="*70)
    print("✅ CAREER GROWTH PLAN COMPLETE!")
    print("="*70)
    print("\nYour personalized plan includes:")
    print("  1. Gap Analysis (from Agent 1)")
    print("  2. Interview Questions (from Agent 2)")
    print("  3. Learning Path (from Agent 3)")
    print("\nAll agents worked together to create your complete plan!")
    
    return {
        "gap_analysis": gap_analysis,
        "interview_prep": interview_questions,
        "learning_path": learning_path
    }


# ==========================================
# MAIN: Run the demo
# ==========================================
if __name__ == "__main__":
    # Example input
    current_role = "Junior Graphic Designer (1 years)"
    target_role = "Senior UX Designer"
    current_skills = ["Photoshop", "Illustrator", "Wireframing",  "UI Design"]
    
    # Run the system
    result = run_career_assistant(current_role, target_role, current_skills)
    
    print("\n" + "="*70)
    print("Demo complete! You now understand multi-agent systems!")
    print("="*70)
    print("\nNext steps:")
    print("1. Modify the input and run again")
    print("2. Add more agents")
    print("3. Add tools to make it more powerful")
    print("4. Build the full 4-agent system")
    print("="*70 + "\n")
