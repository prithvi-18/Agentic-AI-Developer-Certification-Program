"""
FULL SYSTEM: Career Growth Assistant with 4 Agents
Integrates all agents into one complete system

Usage:
    python full_system.py
"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.7,
    api_key=os.getenv("GROQ_API_KEY")
)

print("\n" + "="*70)
print("🎯 CAREER GROWTH ASSISTANT - FULL 4-AGENT SYSTEM")
print("="*70)

# ==========================================
# AGENT 1: ROLE ANALYZER
# ==========================================
def agent_1_role_analyzer(current_role: str, target_role: str, current_skills: list):
    """Analyzes career gap"""
    print("\n[AGENT 1] 📊 Role Analyzer - Analyzing gap...")
    
    system_prompt = """You are a career analyst. Analyze gap between roles.
    
Provide:
1. Current role summary
2. Target role summary  
3. Top 5 skill gaps
4. Timeline estimate (weeks)
5. Key recommendations"""
    
    user_prompt = f"""Analyze this transition:
    
Current: {current_role}
Skills: {', '.join(current_skills)}
Target: {target_role}

Be specific and actionable."""
    
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ])
    
    return response.content


# ==========================================
# AGENT 2: INTERVIEW PREPARER
# ==========================================
def agent_2_interview_preparer(target_role: str, gap_analysis: str):
    """Generates interview questions"""
    print("[AGENT 2] ❓ Interview Preparer - Generating questions...")
    
    system_prompt = """You are an interview coach. Generate questions.
    
Provide:
1. 5 technical questions
2. 3 behavioral questions
3. 2 situational questions
4. Difficulty level for each
5. Why each matters"""
    
    user_prompt = f"""Based on this gap analysis:
    
{gap_analysis}

Generate interview questions for: {target_role}
Focus on identified skill gaps."""
    
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ])
    
    return response.content


# ==========================================
# AGENT 3: LEARNING CREATOR
# ==========================================
def agent_3_learning_creator(gap_analysis: str, interview_questions: str):
    """Creates learning path"""
    print("[AGENT 3] 📚 Learning Creator - Creating learning path...")
    
    system_prompt = """You are a learning designer. Create 12-week plan.
    
Provide:
1. Week-by-week topics
2. Recommended resources
3. Milestones at weeks 4, 8, 12
4. Estimated hours/week
5. Success criteria"""
    
    user_prompt = f"""Create learning path based on:
    
Gap Analysis:
{gap_analysis}

Interview Focus:
{interview_questions}

Create realistic 12-week plan."""
    
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ])
    
    return response.content


# ==========================================
# AGENT 4: FEEDBACK ANALYZER (NEW!)
# ==========================================
def agent_4_feedback_analyzer(interview_questions: str, target_role: str):
    """Provides interview feedback"""
    print("[AGENT 4] 🎤 Feedback Analyzer - Generating insights...")
    
    system_prompt = """You are an interview coach. Provide feedback strategy.
    
For the given interview questions:
1. Identify key evaluation criteria
2. Common mistakes to avoid
3. Strong answer framework
4. Practice tips
5. Expected difficulty level"""
    
    user_prompt = f"""For {target_role} position, analyze these questions:
    
{interview_questions[:500]}...

Provide comprehensive feedback strategy for preparation."""
    
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ])
    
    return response.content


# ==========================================
# ORCHESTRATOR: Runs all agents
# ==========================================
def run_full_system(current_role: str, target_role: str, current_skills: list):
    """
    Orchestrator: Runs all 4 agents in sequence
    Passes output of one agent to the next
    """
    
    print("\n\n" + "🎯 "*20)
    print("STARTING 4-AGENT SYSTEM")
    print("🎯 "*20)
    
    print(f"\n📋 Input:")
    print(f"  Current Role: {current_role}")
    print(f"  Target Role: {target_role}")
    print(f"  Current Skills: {', '.join(current_skills)}")
    
    # RUN AGENT 1
    print("\n[STEP 1/4] Running Agent 1...")
    gap_analysis = agent_1_role_analyzer(current_role, target_role, current_skills)
    
    # RUN AGENT 2 (uses Agent 1 output)
    print("\n[STEP 2/4] Running Agent 2...")
    interview_questions = agent_2_interview_preparer(target_role, gap_analysis)
    
    # RUN AGENT 3 (uses Agent 1 and 2 outputs)
    print("\n[STEP 3/4] Running Agent 3...")
    learning_path = agent_3_learning_creator(gap_analysis, interview_questions)
    
    # RUN AGENT 4 (NEW!)
    print("\n[STEP 4/4] Running Agent 4...")
    feedback = agent_4_feedback_analyzer(interview_questions, target_role)
    
    # FINAL SUMMARY
    print("\n" + "="*70)
    print("✅ 4-AGENT SYSTEM COMPLETE!")
    print("="*70)
    
    final_report = f"""
╔══════════════════════════════════════════════════════════════════════════╗
║                    CAREER GROWTH PLAN - FINAL REPORT                     ║
╚══════════════════════════════════════════════════════════════════════════╝

CAREER TRANSITION: {current_role} → {target_role}

┌─────────────────────────────────────────────────────────────────────────┐
│ 1. GAP ANALYSIS (from Agent 1)                                          │
└─────────────────────────────────────────────────────────────────────────┘
{gap_analysis[:500]}...

┌─────────────────────────────────────────────────────────────────────────┐
│ 2. INTERVIEW PREPARATION (from Agent 2)                                 │
└─────────────────────────────────────────────────────────────────────────┘
{interview_questions[:500]}...

┌─────────────────────────────────────────────────────────────────────────┐
│ 3. LEARNING PATH (from Agent 3)                                         │
└─────────────────────────────────────────────────────────────────────────┘
{learning_path[:500]}...

┌─────────────────────────────────────────────────────────────────────────┐
│ 4. INTERVIEW FEEDBACK STRATEGY (from Agent 4)                           │
└─────────────────────────────────────────────────────────────────────────┘
{feedback[:500]}...

╔══════════════════════════════════════════════════════════════════════════╗
║                        SYSTEM SUMMARY                                    ║
║                                                                          ║
║ ✅ 4 agents working together                                             ║
║ ✅ Gap analysis complete                                                 ║
║ ✅ Interview questions generated                                         ║
║ ✅ Learning path created                                                 ║
║ ✅ Feedback strategy provided                                            ║
║                                                                          ║
║ Your personalized career growth plan is ready!                           ║
╚══════════════════════════════════════════════════════════════════════════╝
"""
    
    return {
        "gap_analysis": gap_analysis,
        "interview_prep": interview_questions,
        "learning_path": learning_path,
        "feedback": feedback,
        "report": final_report
    }


# ==========================================
# MAIN
# ==========================================
if __name__ == "__main__":
    # Example: Graphic Designer → UX Designer
    current_role = "Junior Graphic Designer (1 years)"
    target_role = "Senior UX Designer"
    current_skills = ["Photoshop", "Illustrator", "Wireframing", "UI Design"]
    
    # Run the system
    result = run_full_system(current_role, target_role, current_skills)
    
    # Print final report
    print(result["report"])
    
    print("\n" + "="*70)
    print("🎉 4-Agent System Demo Complete!")
    print("="*70)
    print("\nNext steps:")
    print("1. Modify inputs and run again")
    print("2. Add tools to agents")
    print("3. Integrate with LangGraph for advanced orchestration")
    print("4. Create interactive mode for users")
    print("="*70 + "\n")
