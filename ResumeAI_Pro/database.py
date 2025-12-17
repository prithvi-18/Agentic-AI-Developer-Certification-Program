"""
ResumeAI Pro - Database Layer
SQLAlchemy models and database management
"""

import os
import logging
from datetime import datetime
from typing import Optional, Dict, List
from sqlalchemy import create_engine, Column, String, DateTime, Text, Float, Integer, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from config import DATABASE_URL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database setup
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# ==========================================
# DATABASE MODELS
# ==========================================

class User(Base):
    """User account"""
    __tablename__ = "users"
    
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Resume(Base):
    """Uploaded resume"""
    __tablename__ = "resumes"
    
    id = Column(String, primary_key=True)
    user_id = Column(String)
    original_text = Column(Text)                    # Raw resume text
    file_name = Column(String)
    parsed_data = Column(JSON)                      # Structured extraction
    created_at = Column(DateTime, default=datetime.utcnow)


class JobPosting(Base):
    """Job postings from scraping"""
    __tablename__ = "job_postings"
    
    id = Column(String, primary_key=True)
    job_title = Column(String)
    company = Column(String)
    description = Column(Text)
    requirements = Column(JSON)                     # Extracted requirements
    keywords = Column(JSON)                         # Extracted keywords
    source = Column(String)                         # indeed, linkedin, etc.
    url = Column(String)
    scraped_at = Column(DateTime, default=datetime.utcnow)


class ResumeOptimization(Base):
    """Optimization results"""
    __tablename__ = "resume_optimizations"
    
    id = Column(String, primary_key=True)
    user_id = Column(String)
    resume_id = Column(String)
    target_job = Column(String)
    
    # Scores
    ats_score_before = Column(Float)
    ats_score_after = Column(Float)
    improvement_percentage = Column(Float)
    
    # Content
    original_resume = Column(Text)
    optimized_resume = Column(Text)
    keyword_gaps = Column(JSON)                     # Keywords that were missing
    changes_made = Column(JSON)                     # Summary of changes
    feedback = Column(Text)                         # Agent 5 feedback
    
    # Metadata
    job_requirements = Column(JSON)
    market_analysis = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AgentExecution(Base):
    """Track agent executions"""
    __tablename__ = "agent_executions"
    
    id = Column(String, primary_key=True)
    optimization_id = Column(String)
    agent_name = Column(String)
    status = Column(String)                         # pending, running, success, failed
    input_data = Column(JSON)
    output_data = Column(JSON)
    error_message = Column(Text, nullable=True)
    execution_time_seconds = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)


# ==========================================
# DATABASE MANAGER
# ==========================================

class DB:
    """Database operations manager"""
    
    @staticmethod
    def init():
        """Initialize database"""
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized")
    
    @staticmethod
    @contextmanager
    def session():
        """Get database session"""
        db = SessionLocal()
        try:
            yield db
            db.commit()
        except Exception as e:
            db.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            db.close()
    
    # ==========================================
    # USER OPERATIONS
    # ==========================================
    
    @staticmethod
    def create_user(user_id: str, email: str = None) -> User:
        """Create new user"""
        with DB.session() as db:
            user = User(id=user_id, email=email)
            db.add(user)
            logger.info(f"Created user: {user_id}")
            return user
    
    @staticmethod
    def get_user(user_id: str) -> Optional[User]:
        """Get user by ID"""
        with DB.session() as db:
            return db.query(User).filter(User.id == user_id).first()
    
    # ==========================================
    # RESUME OPERATIONS
    # ==========================================
    
    @staticmethod
    def save_resume(resume_id: str, user_id: str, original_text: str, 
                   file_name: str, parsed_data: Dict = None) -> Resume:
        """Save uploaded resume"""
        with DB.session() as db:
            resume = Resume(
                id=resume_id,
                user_id=user_id,
                original_text=original_text,
                file_name=file_name,
                parsed_data=parsed_data or {}
            )
            db.add(resume)
            logger.info(f"Saved resume: {resume_id}")
            return resume
    
    @staticmethod
    def get_resume(resume_id: str) -> Optional[Resume]:
        """Get resume by ID"""
        with DB.session() as db:
            return db.query(Resume).filter(Resume.id == resume_id).first()
    
    @staticmethod
    def get_user_resumes(user_id: str) -> List[Resume]:
        """Get all resumes for user"""
        with DB.session() as db:
            return db.query(Resume).filter(Resume.user_id == user_id).all()
    
    # ==========================================
    # JOB POSTING OPERATIONS
    # ==========================================
    
    @staticmethod
    def save_job_posting(job_id: str, job_title: str, company: str,
                        description: str, requirements: List[str],
                        keywords: List[str], source: str, url: str = None) -> JobPosting:
        """Save scraped job posting"""
        with DB.session() as db:
            job = JobPosting(
                id=job_id,
                job_title=job_title,
                company=company,
                description=description,
                requirements=requirements,
                keywords=keywords,
                source=source,
                url=url
            )
            db.add(job)
            logger.info(f"Saved job posting: {job_id}")
            return job
    
    @staticmethod
    def find_jobs_by_title(job_title: str) -> List[JobPosting]:
        """Find jobs by title"""
        with DB.session() as db:
            return db.query(JobPosting).filter(
                JobPosting.job_title.ilike(f"%{job_title}%")
            ).limit(20).all()
    
    # ==========================================
    # OPTIMIZATION OPERATIONS
    # ==========================================
    
    @staticmethod
    def save_optimization(optimization_id: str, user_id: str, resume_id: str,
                         target_job: str, ats_before: float, ats_after: float,
                         original_resume: str, optimized_resume: str,
                         keyword_gaps: List[str], feedback: str,
                         job_requirements: List[str], market_analysis: str) -> ResumeOptimization:
        """Save optimization results"""
        improvement = ((ats_after - ats_before) / ats_before * 100) if ats_before > 0 else 0
        
        with DB.session() as db:
            opt = ResumeOptimization(
                id=optimization_id,
                user_id=user_id,
                resume_id=resume_id,
                target_job=target_job,
                ats_score_before=ats_before,
                ats_score_after=ats_after,
                improvement_percentage=improvement,
                original_resume=original_resume,
                optimized_resume=optimized_resume,
                keyword_gaps=keyword_gaps,
                feedback=feedback,
                job_requirements=job_requirements,
                market_analysis=market_analysis
            )
            db.add(opt)
            logger.info(f"Saved optimization: {optimization_id}")
            return opt
    
    @staticmethod
    def get_optimization(optimization_id: str) -> Optional[ResumeOptimization]:
        """Get optimization by ID"""
        with DB.session() as db:
            return db.query(ResumeOptimization).filter(
                ResumeOptimization.id == optimization_id
            ).first()
    
    @staticmethod
    def get_user_optimizations(user_id: str) -> List[ResumeOptimization]:
        """Get all optimizations for user"""
        with DB.session() as db:
            return db.query(ResumeOptimization).filter(
                ResumeOptimization.user_id == user_id
            ).order_by(ResumeOptimization.created_at.desc()).all()
    
    # ==========================================
    # AGENT EXECUTION LOGGING
    # ==========================================
    
    @staticmethod
    def log_agent_execution(execution_id: str, optimization_id: str,
                           agent_name: str, status: str, input_data: Dict = None,
                           output_data: Dict = None, error_message: str = None,
                           execution_time: float = 0.0):
        """Log agent execution"""
        with DB.session() as db:
            execution = AgentExecution(
                id=execution_id,
                optimization_id=optimization_id,
                agent_name=agent_name,
                status=status,
                input_data=input_data or {},
                output_data=output_data or {},
                error_message=error_message,
                execution_time_seconds=execution_time
            )
            db.add(execution)
            logger.info(f"Logged agent execution: {agent_name} - {status}")
