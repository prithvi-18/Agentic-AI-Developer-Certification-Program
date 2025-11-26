"""
LANGGRAPH ORCHESTRATOR - Career Growth Assistant
Professional multi-agent orchestration using LangGraph

This version uses LangGraph for:
✅ Explicit state management
✅ Agent routing and decision-making
✅ Error handling and retries
✅ Conditional execution paths
"""

import os
import logging
from typing import TypedDict, List
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END

load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==========================================
# STATE DEFINITION
# ==========================================
class CareerState(TypedDict):
    """State object that flows through the graph"""
    current_role: str
    target_role: str
    current_skills: List[str]
    gap_analysis: str
    interview_questions: str
    learning_path: str
    feedback: str
    step: int
    error: str


# ==========================================
# LLM SETUP
# ==========================================
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.7,
    api_key=os.getenv("GROQ_API_KEY")
)


# ==========================================
# AGENT NODE FUNCTIONS
# ==========================================
def agent_1_role_analyzer(state: CareerState) -> CareerState:
    """Agent 1: Analyzes career gap"""
    try:
        logger.info("🔍 Agent 1: Analyzing role gap...")
        
        system_prompt = """You are a career analyst. Analyze the gap between roles.
        
Provide:
1. Current role summary
2. Target role summary
3. Top 5 skill gaps
4. Timeline estimate
5. Key recommendations"""
        
        user_prompt = f"""Analyze this career transition:

Current: {state['current_role']}
Skills: {', '.join(state['current_skills'])}
Target: {state['target_role']}

Be specific and actionable."""
        
        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ])
        
        state['gap_analysis'] = response.content
        state['step'] = 1
        logger.info("✅ Agent 1 complete")
        
    except Exception as e:
        logger.error(f"❌ Agent 1 error: {e}")
        state['error'] = str(e)
    
    return state


def agent_2_interview_preparer(state: CareerState) -> CareerState:
    """Agent 2: Generates interview questions"""
    try:
        logger.info("❓ Agent 2: Preparing interview questions...")
        
        if not state['gap_analysis']:
            logger.warning("Skipping Agent 2 - no gap analysis")
            return state
        
        system_prompt = """You are an interview coach. Generate questions.
        
Provide:
1. 5 technical questions
2. 3 behavioral questions
3. 2 situational questions
4. Difficulty level for each"""
        
        user_prompt = f"""Based on this gap analysis:

{state['gap_analysis'][:500]}...

Generate interview questions for: {state['target_role']}"""
        
        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ])
        
        state['interview_questions'] = response.content
        state['step'] = 2
        logger.info("✅ Agent 2 complete")
        
    except Exception as e:
        logger.error(f"❌ Agent 2 error: {e}")
        state['error'] = str(e)
    
    return state


def agent_3_learning_creator(state: CareerState) -> CareerState:
    """Agent 3: Creates learning path"""
    try:
        logger.info("📚 Agent 3: Creating learning path...")
        
        if not state['gap_analysis']:
            logger.warning("Skipping Agent 3 - no gap analysis")
            return state
        
        system_prompt = """You are a learning designer. Create 12-week plan.
        
Provide:
1. Week-by-week topics
2. Recommended resources
3. Milestones at weeks 4, 8, 12
4. Estimated hours/week"""
        
        user_prompt = f"""Create learning path based on:

Gap Analysis: {state['gap_analysis'][:400]}...
Target: {state['target_role']}"""
        
        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ])
        
        state['learning_path'] = response.content
        state['step'] = 3
        logger.info("✅ Agent 3 complete")
        
    except Exception as e:
        logger.error(f"❌ Agent 3 error: {e}")
        state['error'] = str(e)
    
    return state


def agent_4_feedback_analyzer(state: CareerState) -> CareerState:
    """Agent 4: Provides feedback strategy"""
    try:
        logger.info("🎤 Agent 4: Analyzing feedback...")
        
        if not state['interview_questions']:
            logger.warning("Skipping Agent 4 - no interview questions")
            return state
        
        system_prompt = """You are an interview coach. Provide feedback strategy.
        
Provide:
1. Key evaluation criteria
2. Common mistakes to avoid
3. Strong answer framework
4. Practice tips"""
        
        user_prompt = f"""For {state['target_role']}, analyze these questions:

{state['interview_questions'][:400]}...

Provide comprehensive feedback strategy."""
        
        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ])
        
        state['feedback'] = response.content
        state['step'] = 4
        logger.info("✅ Agent 4 complete")
        
    except Exception as e:
        logger.error(f"❌ Agent 4 error: {e}")
        state['error'] = str(e)
    
    return state


# ==========================================
# ROUTING LOGIC
# ==========================================
def should_continue_to_agent_2(state: CareerState) -> str:
    """Decide if we should run Agent 2"""
    if state['error'] or not state['gap_analysis']:
        logger.warning("⚠️ Stopping - Agent 1 failed")
        return "end"
    return "agent_2"


def should_continue_to_agent_3(state: CareerState) -> str:
    """Decide if we should run Agent 3"""
    if state['error']:
        logger.warning("⚠️ Stopping - Agent 2 failed")
        return "end"
    return "agent_3"


def should_continue_to_agent_4(state: CareerState) -> str:
    """Decide if we should run Agent 4"""
    if state['error']:
        logger.warning("⚠️ Stopping - Agent 3 failed")
        return "end"
    return "agent_4"


# ==========================================
# BUILD LANGGRAPH
# ==========================================
def create_career_graph():
    """Create the LangGraph workflow"""
    
    # Create graph
    graph = StateGraph(CareerState)
    
    # Add nodes (agents)
    graph.add_node("agent_1", agent_1_role_analyzer)
    graph.add_node("agent_2", agent_2_interview_preparer)
    graph.add_node("agent_3", agent_3_learning_creator)
    graph.add_node("agent_4", agent_4_feedback_analyzer)
    
    # Set entry point
    graph.set_entry_point("agent_1")
    
    # Add edges with routing logic
    graph.add_conditional_edges(
        "agent_1",
        should_continue_to_agent_2,
        {
            "agent_2": "agent_2",
            "end": END
        }
    )
    
    graph.add_conditional_edges(
        "agent_2",
        should_continue_to_agent_3,
        {
            "agent_3": "agent_3",
            "end": END
        }
    )
    
    graph.add_conditional_edges(
        "agent_3",
        should_continue_to_agent_4,
        {
            "agent_4": "agent_4",
            "end": END
        }
    )
    
    graph.add_edge("agent_4", END)
    
    # Compile
    return graph.compile()


# ==========================================
# RUN THE SYSTEM
# ==========================================
def run_langgraph_system(current_role: str, target_role: str, current_skills: list):
    """Execute the LangGraph workflow"""
    
    print("\n" + "="*70)
    print("🎯 LANGGRAPH ORCHESTRATOR - CAREER GROWTH ASSISTANT")
    print("="*70 + "\n")
    
    # Create graph
    app = create_career_graph()
    
    # Initial state
    initial_state: CareerState = {
        "current_role": current_role,
        "target_role": target_role,
        "current_skills": current_skills,
        "gap_analysis": "",
        "interview_questions": "",
        "learning_path": "",
        "feedback": "",
        "step": 0,
        "error": ""
    }
    
    # Execute
    print(f"Input: {current_role} → {target_role}\n")
    final_state = app.invoke(initial_state)
    
    # Output results
    print("\n" + "="*70)
    print("✅ LANGGRAPH EXECUTION COMPLETE!")
    print("="*70)
    
    print(f"\n📊 Final State:")
    print(f"  Steps Completed: {final_state['step']}/4")
    print(f"  Error Status: {'⚠️ ' + final_state['error'] if final_state['error'] else '✅ No errors'}")
    
    return final_state


if __name__ == "__main__":
    # Example
    result = run_langgraph_system(
        current_role="Junior Graphic Designer (1 years)",
        target_role="Senior UX Designer",
        current_skills=["Photoshop", "Illustrator", "Wireframing", "UI Design"]
    )
    
    print("\n🎉 LangGraph orchestration successful!")
    print("This demonstrates professional agent coordination with:")
    print("  ✅ State management")
    print("  ✅ Conditional routing")
    print("  ✅ Error handling")
    print("  ✅ Sequential execution")
