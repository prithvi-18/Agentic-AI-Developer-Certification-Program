"""
FULL SYSTEM v2: Career Growth Assistant with Tools Integration
Integrates all 4 agents + tools for powerful output

Usage:
    python full_system_v2.py
"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from tools_enhanced import (
    get_role_requirements, 
    find_courses, 
    estimate_timeline,
    get_practice_tips,
    get_interview_prep_checklist
)

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.7,
    api_key=os.getenv("GROQ_API_KEY")
)

print("\n" + "="*70)
print("🎯 CAREER GROWTH ASSISTANT v2 - WITH TOOLS")
print("="*70)

# ==========================================
# ENHANCED AGENT 1: ROLE ANALYZER + TOOLS
# ==========================================
def agent_1_role_analyzer_v2(current_role: str, target_role: str, current_skills: list):
    """Analyzes career gap using tools"""
    print("\n[AGENT 1] 📊 Role Analyzer - Using tools...")
    
    # USE TOOLS
    target_requirements = get_role_requirements(target_role)
    timeline = estimate_timeline(current_skills, target_requirements["technical_skills"], 10)
    
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

Target Role Requirements:
{target_requirements}

Timeline Data:
{timeline}

Be specific and data-driven."""
    
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ])
    
    return response.content, target_requirements


# ==========================================
# ENHANCED AGENT 2: INTERVIEW PREPARER + TOOLS
# ==========================================
def agent_2_interview_preparer_v2(target_role: str, gap_analysis: str):
    """Generates interview questions + prep checklist"""
    print("[AGENT 2] ❓ Interview Preparer - Using tools...")
    
    # USE TOOLS
    prep_checklist = get_interview_prep_checklist()
    
    system_prompt = """You are an interview coach. Generate questions + prep tips.
    
Provide:
1. 5 technical questions
2. 3 behavioral questions
3. 2 situational questions
4. Difficulty level for each
5. Why each matters"""
    
    user_prompt = f"""Based on this gap analysis:
    
{gap_analysis}

Generate interview questions for: {target_role}

Also reference this prep checklist:
{prep_checklist}

Focus on identified skill gaps."""
    
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ])
    
    return response.content, prep_checklist


# ==========================================
# ENHANCED AGENT 3: LEARNING CREATOR + TOOLS
# ==========================================
def agent_3_learning_creator_v2(gap_analysis: str, target_role: str, target_requirements: dict):
    """Creates learning path with actual courses"""
    print("[AGENT 3] 📚 Learning Creator - Using tools...")
    
    # USE TOOLS
    courses_user_research = find_courses("User Research", 2)
    courses_interaction_design = find_courses("Interaction Design", 2)
    
    system_prompt = """You are a learning designer. Create 12-week plan with real resources.
    
Provide:
1. Week-by-week topics
2. Recommended resources
3. Milestones at weeks 4, 8, 12
4. Estimated hours/week
5. Success criteria"""
    
    user_prompt = f"""Create learning path based on:
    
Gap Analysis: {gap_analysis}

Target Role: {target_role}
Requirements: {target_requirements['technical_skills']}

Recommended Courses:
- User Research: {courses_user_research}
- Interaction Design: {courses_interaction_design}

Create realistic 12-week plan using these resources."""
    
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ])
    
    return response.content


# ==========================================
# ENHANCED AGENT 4: FEEDBACK ANALYZER + TOOLS
# ==========================================
def agent_4_feedback_analyzer_v2(target_role: str, gap_analysis: str):
    """Provides interview feedback + practice tips"""
    print("[AGENT 4] 🎤 Feedback Analyzer - Using tools...")
    
    # USE TOOLS (could add more specific ones based on role)
    practice_tips = get_practice_tips("User Research")
    
    system_prompt = """You are an interview coach. Provide feedback strategy + practice tips.
    
For the given role:
1. Identify key evaluation criteria
2. Common mistakes to avoid
3. Strong answer framework
4. Practice tips
5. Expected difficulty level"""
    
    user_prompt = f"""For {target_role} position, provide feedback strategy.

Gap Analysis: {gap_analysis}

Practice Tips for Success:
{practice_tips}

Provide comprehensive feedback strategy for preparation."""
    
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ])
    
    return response.content


# ==========================================
# ORCHESTRATOR v2: Runs all agents with tools
# ==========================================
def run_full_system_v2(current_role: str, target_role: str, current_skills: list):
    """
    Orchestrator v2: Runs all 4 agents with tool integration
    """
    
    print("\n\n" + "🎯 "*20)
    print("STARTING 4-AGENT SYSTEM WITH TOOLS")
    print("🎯 "*20)
    
    print(f"\n📋 Input:")
    print(f"  Current Role: {current_role}")
    print(f"  Target Role: {target_role}")
    print(f"  Current Skills: {', '.join(current_skills)}")
    
    # RUN AGENT 1 (with tools)
    print("\n[STEP 1/4] Running Agent 1 with tools...")
    gap_analysis, target_requirements = agent_1_role_analyzer_v2(current_role, target_role, current_skills)
    
    # RUN AGENT 2 (with tools)
    print("\n[STEP 2/4] Running Agent 2 with tools...")
    interview_prep, prep_checklist = agent_2_interview_preparer_v2(target_role, gap_analysis)
    
    # RUN AGENT 3 (with tools)
    print("\n[STEP 3/4] Running Agent 3 with tools...")
    learning_path = agent_3_learning_creator_v2(gap_analysis, target_role, target_requirements)
    
    # RUN AGENT 4 (with tools)
    print("\n[STEP 4/4] Running Agent 4 with tools...")
    feedback = agent_4_feedback_analyzer_v2(target_role, gap_analysis)
    
    # FINAL SUMMARY
    print("\n" + "="*70)
    print("✅ 4-AGENT SYSTEM WITH TOOLS COMPLETE!")
    print("="*70)
    
    final_report = f"""
╔══════════════════════════════════════════════════════════════════════════╗
║              CAREER GROWTH PLAN v2 - WITH TOOLS INTEGRATION              ║
╚══════════════════════════════════════════════════════════════════════════╝

CAREER TRANSITION: {current_role} → {target_role}

┌─────────────────────────────────────────────────────────────────────────┐
│ 1. GAP ANALYSIS (Agent 1 + Tools)                                       │
└─────────────────────────────────────────────────────────────────────────┘
{gap_analysis[:600]}...

┌─────────────────────────────────────────────────────────────────────────┐
│ 2. INTERVIEW PREPARATION (Agent 2 + Prep Checklist)                     │
└─────────────────────────────────────────────────────────────────────────┘
{interview_prep[:600]}...

Interview Prep Checklist:
{chr(10).join(prep_checklist[:5])}...

┌─────────────────────────────────────────────────────────────────────────┐
│ 3. LEARNING PATH (Agent 3 + Recommended Courses)                        │
└─────────────────────────────────────────────────────────────────────────┘
{learning_path[:600]}...

┌─────────────────────────────────────────────────────────────────────────┐
│ 4. INTERVIEW FEEDBACK STRATEGY (Agent 4 + Practice Tips)                │
└─────────────────────────────────────────────────────────────────────────┘
{feedback[:600]}...

╔══════════════════════════════════════════════════════════════════════════╗
║                    SYSTEM ACHIEVEMENTS                                   ║
║                                                                          ║
║ ✅ 4 agents working together                                             ║
║ ✅ Tools integrated into agents                                          ║
║ ✅ Real courses and resources recommended                                ║
║ ✅ Interview prep checklist generated                                    ║
║ ✅ Practice tips provided                                                ║
║ ✅ Complete career growth plan ready                                     ║
║                                                                          ║
║ Your personalized career growth plan is complete!                        ║
╚══════════════════════════════════════════════════════════════════════════╝
"""
    
    return {
        "gap_analysis": gap_analysis,
        "interview_prep": interview_prep,
        "learning_path": learning_path,
        "feedback": feedback,
        "report": final_report
    }


# ==========================================
# MAIN
# ==========================================
if __name__ == "__main__":
    current_role = "Junior Graphic Designer (1 years)"
    target_role = "Senior UX Designer"
    current_skills = ["Photoshop", "Illustrator", "Wireframing", "UI Design"]
    
    # Run the enhanced system
    result = run_full_system_v2(current_role, target_role, current_skills)
    
    # Print final report
    print(result["report"])
    
    print("\n" + "="*70)
    print("🎉 4-Agent System with Tools Complete!")
    print("="*70)
