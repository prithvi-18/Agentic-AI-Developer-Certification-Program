"""
ResumeAI Pro - 5-Agent LangGraph System
Multi-agent orchestration for resume optimization
"""

import logging
import re
from typing import TypedDict, List, Dict
from uuid import uuid4
from datetime import datetime
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, END

from config import GROQ_API_KEY, GROQ_MODEL, GROQ_TEMPERATURE, ATS_KEYWORD_WEIGHTS, HIGH_VALUE_KEYWORDS
from database import DB
from job_scraper import JobScraper

load_dotenv()
logger = logging.getLogger(__name__)

# LLM Configuration
llm = ChatGroq(
    model=GROQ_MODEL,
    temperature=GROQ_TEMPERATURE,
    api_key=GROQ_API_KEY,
    timeout=30
)

# ==========================================
# STATE DEFINITION (TypedDict)
# ==========================================

class ResumeState(TypedDict):
    """State for resume optimization workflow"""
    # Input
    user_id: str
    resume_id: str
    original_resume: str
    target_job: str
    location: str
    
    # Agent 1 output
    parsed_resume: Dict
    
    # Agent 2 output
    job_postings: List[Dict]
    job_requirements: List[str]
    market_analysis: str
    
    # Agent 3 output
    keyword_gaps: List[str]
    ats_score_before: float
    resume_keywords: List[str]
    
    # Agent 4 output
    rewritten_resume: str
    ats_score_after: float
    changes_made: Dict
    
    # Agent 5 output
    feedback: str
    improvement_percentage: float
    next_steps: List[str]
    
    # Tracking
    error_count: int
    error_message: str

# ==========================================
# AGENT 1: RESUME PARSER
# ==========================================

def agent_resume_parser(state: ResumeState) -> ResumeState:
    """Extract structured data from raw resume"""
    try:
        logger.info("[AGENT 1] Parsing resume...")
        
        prompt = """Analyze this resume and extract structured data. Return as JSON with these fields:
        {
            "current_role": "...",
            "experience_years": 0,
            "technical_skills": ["skill1", "skill2"],
            "soft_skills": ["skill1", "skill2"],
            "certifications": ["cert1"],
            "education": "...",
            "achievements_with_metrics": ["achievement1", "achievement2"],
            "summary": "..."
        }
        
        Resume to analyze:
        """ + state["original_resume"]
        
        response = llm.invoke([
            SystemMessage(content="You are a resume analyzer. Extract and structure resume data."),
            HumanMessage(content=prompt)
        ])
        
        # Parse JSON response
        response_text = response.content
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        
        if json_match:
            import json
            state["parsed_resume"] = json.loads(json_match.group())
        else:
            state["parsed_resume"] = {"error": "Could not parse resume"}
        
        logger.info("[AGENT 1] ✓ Resume parsed successfully")
        return state
        
    except Exception as e:
        logger.error(f"[AGENT 1] Error: {e}")
        state["error_count"] += 1
        state["error_message"] = str(e)
        return state

# ==========================================
# AGENT 2: JOB MARKET ANALYZER
# ==========================================

def agent_job_market_analyzer(state: ResumeState) -> ResumeState:
    """Analyze job market and extract common requirements"""
    if state["error_count"] > 0:
        return state
    
    try:
        logger.info("[AGENT 2] Analyzing job market...")
        
        # Scrape job postings
        jobs = JobScraper.scrape_jobs(state["target_job"], state["location"])
        state["job_postings"] = jobs
        
        # Extract all requirements and keywords from jobs
        all_requirements = []
        all_keywords = []
        
        for job in jobs:
            all_requirements.extend(job.get("requirements", []))
            all_keywords.extend(job.get("keywords", []))
        
        # Find most common requirements
        from collections import Counter
        requirement_counts = Counter(all_requirements)
        state["job_requirements"] = [req for req, _ in requirement_counts.most_common(15)]
        
        # Generate market analysis
        prompt = f"""Based on these job postings for '{state['target_job']}', provide market analysis:
        
        Common requirements: {state['job_requirements']}
        Job count analyzed: {len(jobs)}
        
        Provide a 2-3 sentence market insight about what companies are looking for."""
        
        response = llm.invoke([
            SystemMessage(content="You are a job market analyst."),
            HumanMessage(content=prompt)
        ])
        
        state["market_analysis"] = response.content
        logger.info(f"[AGENT 2] ✓ Analyzed {len(jobs)} job postings")
        return state
        
    except Exception as e:
        logger.error(f"[AGENT 2] Error: {e}")
        state["error_count"] += 1
        return state

# ==========================================
# AGENT 3: ATS KEYWORD MATCHER
# ==========================================

def agent_ats_keyword_matcher(state: ResumeState) -> ResumeState:
    """Calculate ATS scores and identify keyword gaps"""
    if state["error_count"] > 0:
        return state
    
    try:
        logger.info("[AGENT 3] Matching ATS keywords...")
        
        # Extract keywords from resume
        resume_lower = state["original_resume"].lower()
        state["resume_keywords"] = [
            keyword for keyword in state["job_requirements"]
            if keyword.lower() in resume_lower
        ]
        
        # Calculate ATS score before
        matched = len(state["resume_keywords"])
        total_required = len(state["job_requirements"])
        state["ats_score_before"] = (matched / total_required * 100) if total_required > 0 else 0
        
        # Identify gaps
        state["keyword_gaps"] = [
            req for req in state["job_requirements"]
            if req not in state["resume_keywords"]
        ]
        
        logger.info(f"[AGENT 3] ✓ ATS Score Before: {state['ats_score_before']:.1f}%")
        logger.info(f"[AGENT 3] ✓ Identified {len(state['keyword_gaps'])} keyword gaps")
        return state
        
    except Exception as e:
        logger.error(f"[AGENT 3] Error: {e}")
        state["error_count"] += 1
        return state

# ==========================================
# AGENT 4: RESUME REWRITER
# ==========================================

def agent_resume_rewriter(state: ResumeState) -> ResumeState:
    """Rewrite resume to improve ATS score"""
    if state["error_count"] > 0:
        return state
    
    try:
        logger.info("[AGENT 4] Rewriting resume...")
        
        prompt = f"""Rewrite this resume to improve ATS compatibility for the '{state['target_job']}' role.
        
        Original Resume:
        {state['original_resume']}
        
        Keywords to add naturally (missing skills): {', '.join(state['keyword_gaps'][:10])}
        
        Market Requirements: {state['market_analysis']}
        
        Guidelines:
        1. Add missing keywords naturally without lying
        2. Enhance achievement descriptions with metrics
        3. Reorganize sections for ATS readability
        4. Use bullet points and clear formatting
        5. Add action verbs from: {', '.join(HIGH_VALUE_KEYWORDS[:10])}
        
        Return ONLY the rewritten resume text."""
        
        response = llm.invoke([
            SystemMessage(content="You are an expert resume writer specializing in ATS optimization."),
            HumanMessage(content=prompt)
        ])
        
        state["rewritten_resume"] = response.content
        
        # Calculate new ATS score
        rewritten_lower = state["rewritten_resume"].lower()
        matched_after = sum(
            1 for keyword in state["job_requirements"]
            if keyword.lower() in rewritten_lower
        )
        
        state["ats_score_after"] = (matched_after / len(state["job_requirements"]) * 100) if state["job_requirements"] else 0
        state["improvement_percentage"] = state["ats_score_after"] - state["ats_score_before"]
        
        logger.info(f"[AGENT 4] ✓ ATS Score After: {state['ats_score_after']:.1f}%")
        logger.info(f"[AGENT 4] ✓ Improvement: +{state['improvement_percentage']:.1f}%")
        return state
        
    except Exception as e:
        logger.error(f"[AGENT 4] Error: {e}")
        state["error_count"] += 1
        return state

# ==========================================
# AGENT 5: FEEDBACK SYNTHESIZER
# ==========================================

def agent_feedback_synthesizer(state: ResumeState) -> ResumeState:
    """Generate insights and next steps"""
    if state["error_count"] > 0:
        return state
    
    try:
        logger.info("[AGENT 5] Generating feedback...")
        
        prompt = f"""Based on this resume optimization:
        - Original ATS Score: {state['ats_score_before']:.1f}%
        - New ATS Score: {state['ats_score_after']:.1f}%
        - Improvement: +{state['improvement_percentage']:.1f}%
        
        Target Role: {state['target_job']}
        Keywords Added: {', '.join(state['keyword_gaps'][:5])}
        
        Provide:
        1. Summary of improvements made
        2. How changes will improve interview callbacks
        3. 3-4 next steps to further strengthen resume
        
        Be specific and actionable."""
        
        response = llm.invoke([
            SystemMessage(content="You are a career coach providing resume feedback."),
            HumanMessage(content=prompt)
        ])
        
        state["feedback"] = response.content
        
        # Extract next steps
        state["next_steps"] = [
            "Review optimized resume carefully",
            "Customize cover letter for target companies",
            "Practice answers to common interview questions",
            "Update LinkedIn profile with new resume content"
        ]
        
        logger.info("[AGENT 5] ✓ Feedback generated")
        return state
        
    except Exception as e:
        logger.error(f"[AGENT 5] Error: {e}")
        state["error_count"] += 1
        return state

# ==========================================
# CONDITIONAL EDGES
# ==========================================

def should_continue_to_agent_2(state: ResumeState) -> str:
    return "end" if state["error_count"] > 0 else "agent_2"

def should_continue_to_agent_3(state: ResumeState) -> str:
    return "end" if state["error_count"] > 0 else "agent_3"

def should_continue_to_agent_4(state: ResumeState) -> str:
    return "end" if state["error_count"] > 0 else "agent_4"

def should_continue_to_agent_5(state: ResumeState) -> str:
    return "end" if state["error_count"] > 0 else "agent_5"

# ==========================================
# BUILD LANGGRAPH
# ==========================================

def build_resume_optimizer_graph():
    """Build and compile the LangGraph"""
    graph = StateGraph(ResumeState)
    
    # Add nodes
    graph.add_node("agent_1", agent_resume_parser)
    graph.add_node("agent_2", agent_job_market_analyzer)
    graph.add_node("agent_3", agent_ats_keyword_matcher)
    graph.add_node("agent_4", agent_resume_rewriter)
    graph.add_node("agent_5", agent_feedback_synthesizer)
    
    # Set entry point
    graph.set_entry_point("agent_1")
    
    # Add edges with conditional routing
    graph.add_conditional_edges(
        "agent_1",
        should_continue_to_agent_2,
        {"agent_2": "agent_2", "end": END}
    )
    graph.add_conditional_edges(
        "agent_2",
        should_continue_to_agent_3,
        {"agent_3": "agent_3", "end": END}
    )
    graph.add_conditional_edges(
        "agent_3",
        should_continue_to_agent_4,
        {"agent_4": "agent_4", "end": END}
    )
    graph.add_conditional_edges(
        "agent_4",
        should_continue_to_agent_5,
        {"agent_5": "agent_5", "end": END}
    )
    graph.add_edge("agent_5", END)
    
    return graph.compile()

# Compile graph
RESUME_OPTIMIZER_GRAPH = build_resume_optimizer_graph()
