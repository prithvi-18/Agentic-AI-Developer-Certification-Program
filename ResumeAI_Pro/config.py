"""
ResumeAI Pro - Configuration
Central configuration for all modules
"""

import os
from typing import Dict, List

# ==========================================
# API & MODEL CONFIGURATION
# ==========================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_TEMPERATURE = 0.7
GROQ_TIMEOUT = 30

# ==========================================
# DATABASE CONFIGURATION
# ==========================================

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///resumeai.db")

# ==========================================
# JOB SCRAPING CONFIGURATION
# ==========================================

JOB_SCRAPE_SOURCES = ["indeed", "linkedin"]  # Add "glassdoor" later
MAX_JOBS_TO_SCRAPE = 15
JOB_SEARCH_RADIUS_KM = 50

# ==========================================
# ATS SCORING CONFIGURATION
# ==========================================

# Keywords with importance weights
ATS_KEYWORD_WEIGHTS = {
    "technical_skills": 0.35,      # Python, Java, AWS, etc.
    "certifications": 0.15,         # AWS Certified, etc.
    "metrics": 0.25,                # "increased by 40%", "led team of 5"
    "education": 0.10,              # Bachelor's, Master's
    "experience": 0.15              # Years of experience
}

# Keywords that trigger higher ATS scores
HIGH_VALUE_KEYWORDS = [
    "led", "improved", "increased", "reduced", "optimized",
    "automated", "developed", "architected", "managed", "mentored",
    "delivered", "implemented", "designed", "deployed", "scaled"
]

# ==========================================
# RESUME PROCESSING
# ==========================================

SUPPORTED_FILE_TYPES = [".pdf", ".docx", ".txt"]
MAX_RESUME_SIZE_MB = 5

# ==========================================
# AGENT CONFIGURATION
# ==========================================

AGENT_NAMES = [
    "resume_parser",
    "job_market_analyzer",
    "ats_keyword_matcher",
    "resume_rewriter",
    "feedback_synthesizer"
]

# ==========================================
# UI CONFIGURATION
# ==========================================

STREAMLIT_PAGE_TITLE = "ResumeAI Pro"
STREAMLIT_PAGE_ICON = "📄"
STREAMLIT_LAYOUT = "wide"

# ==========================================
# PERFORMANCE TARGETS
# ==========================================

EXPECTED_ATS_IMPROVEMENT_MIN = 15  # Minimum 15% improvement expected
EXPECTED_EXECUTION_TIME_SECONDS = 45  # Target execution time

# ==========================================
# ERROR MESSAGES
# ==========================================

ERROR_MESSAGES = {
    "no_api_key": "GROQ_API_KEY not found. Add it to .env file",
    "invalid_file": "File must be PDF, DOCX, or TXT",
    "file_too_large": "File exceeds 5MB limit",
    "empty_resume": "Resume appears to be empty",
    "invalid_job_title": "Please enter a valid job title (min 3 characters)",
    "agent_failed": "Agent processing failed. Please try again.",
    "scraping_failed": "Could not fetch job postings. Try another search term."
}
