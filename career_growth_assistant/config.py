"""
CAREER GROWTH ASSISTANT - Config Module
All settings in one place
"""

# LLM Configuration
LLM_MODEL = "llama-3.3-70b-versatile"
LLM_TEMPERATURE = 0.7
LLM_MAX_TOKENS = 2048

# Agent Configuration
AGENTS = {
    "role_analyzer": {
        "name": "Role Analyzer",
        "description": "Analyzes current vs target role, identifies gaps",
        "max_retries": 3
    },
    "interview_preparer": {
        "name": "Interview Preparer",
        "description": "Generates interview questions, creates prep strategy",
        "max_retries": 2
    },
    "learning_creator": {
        "name": "Learning Creator",
        "description": "Creates learning path, recommends resources",
        "max_retries": 2
    },
    "feedback_analyzer": {
        "name": "Feedback Analyzer",
        "description": "Simulates interviews, provides feedback",
        "max_retries": 2
    }
}

# System Prompts for Each Agent
SYSTEM_PROMPTS = {
    "role_analyzer": """You are a career analyst. Your job is to:
1. Analyze the gap between current and target roles
2. Identify required skills
3. Estimate timeline for transition
4. Provide actionable insights

Be specific and data-driven.""",

    "interview_preparer": """You are an interview coach. Your job is to:
1. Generate relevant interview questions
2. Adjust difficulty levels
3. Cover all important topics
4. Prepare the candidate

Format questions clearly with difficulty levels (Easy/Medium/Hard).""",

    "learning_creator": """You are a learning path designer. Your job is to:
1. Create week-by-week learning schedule
2. Recommend specific resources
3. Define milestones and checkpoints
4. Track progress

Be realistic about timeline and effort.""",

    "feedback_analyzer": """You are an interview evaluator. Your job is to:
1. Ask technical/behavioral questions
2. Evaluate responses
3. Provide constructive feedback
4. Suggest improvements

Be fair but honest in your assessment."""
}

# Tools Configuration
TOOLS_CONFIG = {
    "skill_tools": {
        "enabled": True,
        "methods": ["analyze_skills", "compare_roles", "identify_gaps"]
    },
    "question_tools": {
        "enabled": True,
        "methods": ["generate_questions", "rank_difficulty"]
    },
    "course_tools": {
        "enabled": True,
        "methods": ["find_courses", "recommend_resources"]
    },
    "feedback_tools": {
        "enabled": True,
        "methods": ["simulate_interview", "score_response"]
    }
}

# Paths
DATA_DIR = "./data"
LOGS_DIR = "./logs"
AGENTS_DIR = "./src/agents"
TOOLS_DIR = "./src/tools"

# Agent Flow
AGENT_FLOW = [
    "role_analyzer",
    "interview_preparer", 
    "learning_creator",
    "feedback_analyzer"
]

# Timeouts
AGENT_TIMEOUT = 30  # seconds
TOOL_TIMEOUT = 15   # seconds

print("✓ Config loaded successfully")
