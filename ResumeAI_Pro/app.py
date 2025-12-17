"""
ResumeAI Pro - Streamlit Application
Web interface for resume optimization
"""

import streamlit as st
from uuid import uuid4
import logging
import PyPDF2
from docx import Document
from io import BytesIO
import json

from dotenv import load_dotenv
from database import DB
from agents import RESUME_OPTIMIZER_GRAPH, ResumeState
from config import ERROR_MESSAGES, STREAMLIT_PAGE_TITLE, STREAMLIT_LAYOUT

load_dotenv()
logger = logging.getLogger(__name__)

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title=STREAMLIT_PAGE_TITLE,
    page_icon="📄",
    layout=STREAMLIT_LAYOUT,
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main { padding: 2rem; }
    .stTabs { margin-top: 2rem; }
    .metric-card { background: #f0f2f6; padding: 1rem; border-radius: 8px; }
    .improvement { color: #00d084; font-weight: bold; }
    .before { color: #ff6b6b; }
    .after { color: #00d084; }
    .comparison { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================

if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid4())
    DB.init()
    DB.create_user(st.session_state.user_id)

if "step" not in st.session_state:
    st.session_state.step = "upload"

if "result" not in st.session_state:
    st.session_state.result = None

if "optimization_id" not in st.session_state:
    st.session_state.optimization_id = None

# ==========================================
# UTILITY FUNCTIONS
# ==========================================

def extract_text_from_pdf(file) -> str:
    """Extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""

def extract_text_from_docx(file) -> str:
    """Extract text from DOCX file"""
    try:
        doc = Document(file)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except Exception as e:
        st.error(f"Error reading DOCX: {e}")
        return ""

def extract_resume_text(uploaded_file) -> str:
    """Extract text from uploaded resume"""
    if uploaded_file.name.endswith('.pdf'):
        return extract_text_from_pdf(uploaded_file)
    elif uploaded_file.name.endswith('.docx'):
        return extract_text_from_docx(uploaded_file)
    elif uploaded_file.name.endswith('.txt'):
        return uploaded_file.read().decode('utf-8')
    else:
        st.error("Unsupported file format. Use PDF, DOCX, or TXT")
        return ""

def create_comparison_display(original: str, optimized: str):
    """Create side-by-side comparison"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📄 Original Resume")
        with st.expander("Click to expand", expanded=False):
            st.text_area("Original", original, height=400, disabled=True, key="original_display")
    
    with col2:
        st.markdown("### ✨ Optimized Resume")
        with st.expander("Click to expand", expanded=True):
            st.text_area("Optimized", optimized, height=400, disabled=True, key="optimized_display")

# ==========================================
# PAGE 1: UPLOAD RESUME
# ==========================================

def page_upload():
    """Upload resume and job details"""
    st.markdown("# 📄 ResumeAI Pro")
    st.markdown("*AI-Powered Resume Optimization for Better Interview Callbacks*")
    
    st.markdown("---")
    
    with st.form("resume_upload_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Your Resume")
            resume_file = st.file_uploader(
                "Upload your resume (PDF, DOCX, or TXT)",
                type=["pdf", "docx", "txt"],
                help="Max 5MB"
            )
        
        with col2:
            st.markdown("### Target Job")
            job_title = st.text_input(
                "Job title you're applying for",
                placeholder="e.g., Senior Python Developer",
                help="Be specific for better analysis"
            )
            location = st.text_input(
                "Location (optional)",
                value="India",
                placeholder="e.g., Bangalore, India"
            )
        
        submitted = st.form_submit_button("🚀 ANALYZE RESUME", type="primary", use_container_width=True)
        
        if submitted:
            # Validation
            if not resume_file:
                st.error("❌ Please upload a resume file")
                return
            
            if not job_title or len(job_title) < 3:
                st.error("❌ Please enter a valid job title (min 3 characters)")
                return
            
            # Extract resume text
            resume_text = extract_resume_text(resume_file)
            
            if not resume_text or len(resume_text) < 50:
                st.error("❌ Resume appears to be empty or too short")
                return
            
            # Save resume to database
            resume_id = str(uuid4())
            DB.save_resume(
                resume_id=resume_id,
                user_id=st.session_state.user_id,
                original_text=resume_text,
                file_name=resume_file.name
            )
            
            # Store in session
            st.session_state.resume_text = resume_text
            st.session_state.resume_id = resume_id
            st.session_state.job_title = job_title
            st.session_state.location = location
            st.session_state.step = "processing"
            
            st.rerun()

# ==========================================
# PAGE 2: PROCESSING
# ==========================================

def page_processing():
    """Run agents and process resume"""
    st.markdown("# ⚙️ Processing Your Resume")
    st.markdown("*Running 5 agents to optimize your resume...*")
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Initialize state
        state: ResumeState = {
            "user_id": st.session_state.user_id,
            "resume_id": st.session_state.resume_id,
            "original_resume": st.session_state.resume_text,
            "target_job": st.session_state.job_title,
            "location": st.session_state.location,
            "parsed_resume": {},
            "job_postings": [],
            "job_requirements": [],
            "market_analysis": "",
            "keyword_gaps": [],
            "ats_score_before": 0,
            "resume_keywords": [],
            "rewritten_resume": "",
            "ats_score_after": 0,
            "changes_made": {},
            "feedback": "",
            "improvement_percentage": 0,
            "next_steps": [],
            "error_count": 0,
            "error_message": ""
        }
        
        agents = [
            ("Agent 1: Resume Parser", 20),
            ("Agent 2: Job Market Analyzer", 40),
            ("Agent 3: ATS Keyword Matcher", 60),
            ("Agent 4: Resume Rewriter", 80),
            ("Agent 5: Feedback Synthesizer", 100)
        ]
        
        with st.spinner("Running agents..."):
            for agent_name, progress in agents:
                status_text.write(f"🔄 {agent_name}...")
                progress_bar.progress(progress)
        
        # Execute agent graph
        st.write("🧠 Analyzing with AI...")
        result = RESUME_OPTIMIZER_GRAPH.invoke(state)
        
        if result["error_count"] > 0:
            st.error(f"⚠️ Error during processing: {result['error_message']}")
            if st.button("↩️ Try Again"):
                st.session_state.step = "upload"
                st.rerun()
            return
        
        # Save optimization to database
        optimization_id = str(uuid4())
        DB.save_optimization(
            optimization_id=optimization_id,
            user_id=st.session_state.user_id,
            resume_id=st.session_state.resume_id,
            target_job=st.session_state.job_title,
            ats_before=result["ats_score_before"],
            ats_after=result["ats_score_after"],
            original_resume=result["original_resume"],
            optimized_resume=result["rewritten_resume"],
            keyword_gaps=result["keyword_gaps"],
            feedback=result["feedback"],
            job_requirements=result["job_requirements"],
            market_analysis=result["market_analysis"]
        )
        
        # Store result in session
        st.session_state.result = result
        st.session_state.optimization_id = optimization_id
        st.session_state.step = "results"
        
        progress_bar.progress(100)
        status_text.write("✅ Analysis complete!")
        
        st.rerun()
        
    except Exception as e:
        st.error(f"❌ Processing failed: {str(e)}")
        logger.error(f"Processing error: {e}")
        
        if st.button("↩️ Try Again"):
            st.session_state.step = "upload"
            st.rerun()

# ==========================================
# PAGE 3: RESULTS
# ==========================================

def page_results():
    """Display optimization results"""
    if not st.session_state.result:
        st.error("No results found. Please start over.")
        st.session_state.step = "upload"
        st.rerun()
        return
    
    result = st.session_state.result
    
    st.markdown(f"# ✨ Your Optimized Resume")
    st.markdown(f"*Target Role: **{st.session_state.job_title}***")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "ATS Score Before",
            f"{result['ats_score_before']:.1f}%",
            delta=None
        )
    
    with col2:
        st.metric(
            "ATS Score After",
            f"{result['ats_score_after']:.1f}%",
            delta=None
        )
    
    with col3:
        improvement = result['improvement_percentage']
        st.metric(
            "Improvement",
            f"+{improvement:.1f}%",
            delta_color="normal"
        )
    
    with col4:
        keyword_count = len(result['keyword_gaps'])
        st.metric(
            "Keywords Added",
            keyword_count,
            delta=None
        )
    
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Analysis",
        "🔄 Comparison",
        "💡 Feedback",
        "📥 Download"
    ])
    
    # TAB 1: ANALYSIS
    with tab1:
        st.markdown("### Market Insights")
        st.info(result['market_analysis'])
        
        st.markdown("### Keywords Added to Resume")
        if result['keyword_gaps']:
            cols = st.columns(3)
            for idx, keyword in enumerate(result['keyword_gaps'][:9]):
                with cols[idx % 3]:
                    st.success(f"✅ {keyword}")
        else:
            st.write("No keywords needed to be added.")
    
    # TAB 2: COMPARISON
    with tab2:
        create_comparison_display(
            result['original_resume'],
            result['rewritten_resume']
        )
    
    # TAB 3: FEEDBACK
    with tab3:
        st.markdown(result['feedback'])
        
        st.markdown("### Next Steps")
        for i, step in enumerate(result['next_steps'], 1):
            st.write(f"{i}. {step}")
    
    # TAB 4: DOWNLOAD
    with tab4:
        st.markdown("### Download Your Optimized Resume")
        
        # Download as text
        st.download_button(
            label="📥 Download as TXT",
            data=result['rewritten_resume'],
            file_name="resume_optimized.txt",
            mime="text/plain",
            use_container_width=True
        )
        
        st.markdown("---")
        st.info("💡 Tip: Copy the optimized resume and format it in your preferred tool (Word, Google Docs, Canva)")
    
    st.markdown("---")
    
    if st.button("🔄 Optimize Another Resume", use_container_width=True):
        st.session_state.step = "upload"
        st.session_state.result = None
        st.rerun()

# ==========================================
# MAIN APP ROUTING
# ==========================================

def main():
    """Main application"""
    if st.session_state.step == "upload":
        page_upload()
    elif st.session_state.step == "processing":
        page_processing()
    elif st.session_state.step == "results":
        page_results()

if __name__ == "__main__":
    main()
