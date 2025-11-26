# 🚀 CareerPath AI

### **Multi-Agent Career Development System (ReadyTensor — Module 2 Project)**

CareerPath AI is a **production-grade multi-agent system** designed to create **personalized career growth plans** using:

* LangGraph orchestration
* Multi-agent coordination
* Real course databases (Coursera, Udemy, edX)
* Tool integration
* Groq LLMs (Llama-3.3-70B Versatile)

This project completes **Module 2** of the **ReadyTensor Agentic AI Developer Certification Program**.

---

# ⭐ Project Highlights

### ✔️ 4 Specialized Agents Working Together

1. **Role Analyzer** – Skill gap analysis, timelines, recommendations
2. **Interview Preparer** – Technical, behavioral & situational questions
3. **Learning Path Creator** – 12-week structured roadmap with real courses
4. **Feedback Analyzer** – Evaluation frameworks, common mistakes, practice tips

### ✔️ Tool Integration

* Real online course database
* Skill taxonomy
* Preparation checklists
* Practice tips
* Learning estimators

### ✔️ LangGraph Orchestration

* StateGraph
* Conditional routing
* Retry logic
* Error handling
* Sequential execution with shared state

### ✔️ Production-Ready

* Fully structured code
* Logging + error handling
* External configuration
* Clean file structure
* Repeatable workflow

---

# 📁 Project Structure

```
career-growth-assistant/
├── full_system_v2.py              # 4-agent system with tools
├── full_system.py                 # Basic 4-agent system
├── simple_demo.py                 # 3-agent starter demo
├── langgraph_orchestrator.py      # LangGraph coordinator
├── tools_enhanced.py              # Real course & skill DB
├── example_scenarios.py           # 3 ready-to-run examples
├── config.py                      # Model + agent config
├── requirements.txt               # Dependencies
├── .env.example                   # Example env file
├── README.md                      # You are here
└── screenshots/
     ├── screenshot1_full_system.png
     ├── screenshot2_langgraph.png
     ├── screenshot3_examples.png
     └── screenshot4_tools.png
```

---

# 🧠 System Architecture

```
User Input (Current Role, Target Role, Skills)
                ↓
[Agent 1: Role Analyzer]
    - Skill gaps
    - Timeline estimation
    - Recommendations
                ↓
[Agent 2: Interview Preparer]
    - 5 technical questions
    - 3 behavioral questions
    - 2 situational questions
                ↓
[Agent 3: Learning Path Creator]
    - 12-week structured plan
    - Course recommendations
                ↓
[Agent 4: Feedback Analyzer]
    - Interview evaluation framework
    - Common mistakes
    - Practice tips
                ↓
Final Career Growth Plan (Complete Report)
```

---

# 🛠️ Setup Instructions

### 1. Clone the Project

```bash
git clone <your-repo-url>
cd career-growth-assistant
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate:

**Windows**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add Environment Variables

Create `.env` file:

```
GROQ_API_KEY=your_groq_api_key_here
```

---

# ▶️ How to Run the System

### ✅ 1. Run the Simple 3-Agent Demo

```bash
python simple_demo.py
```

Shows basic multi-agent pipeline.

---

### ✅ 2. Run the Full 4-Agent System (No Tools)

```bash
python full_system.py
```

---

### ✅ 3. Run the Full 4-Agent System WITH Tools

```bash
python full_system_v2.py
```

Includes:

* Real courses
* Skill taxonomy
* Timeline estimator
* Prep checklist
* Practice tips

---

### ✅ 4. Run LangGraph Orchestrated Version

```bash
python langgraph_orchestrator.py
```

Demonstrates:

* StateGraph
* Conditional edges
* Error handling
* Sequential agent coordination

---

### ✅ 5. Run Example Scenarios

```bash
python example_scenarios.py
```

Includes:

* Designer → Senior UX
* Graphic Designer → Frontend Dev
* Developer → Data Scientist

---

# 🖼️ Screenshots

### 📸 1 — Full System with Tools

`screenshots/screenshot1_full_system.png`

### 📸 2 — LangGraph Orchestrator

`screenshots/screenshot2_langgraph.png`

### 📸 3 — Example Scenarios

`screenshots/screenshot3_examples.png`

### 📸 4 — Tools Module Output

`screenshots/screenshot4_tools.png`

---

# 📚 Tools Included (tools_enhanced.py)

* **COURSE_DATABASE** – 50+ real courses
* **SKILL_CATEGORIES** – UX, Frontend, Data Science
* **INTERVIEW_PREP_TIPS** – Technical, behavioral, portfolio
* **PRACTICE_RESOURCES** – LeetCode, UXChallenge, Pramp
* **EVALUATION_CRITERIA** – Weighted evaluation framework

Tool functions:

* `get_recommended_courses()`
* `get_skills_for_role()`
* `get_practice_tips()`
* `estimate_timeline()`
* `get_interview_prep_checklist()`

---

# 🧪 Testing

Recommended sequence:

1. `python simple_demo.py`
2. `python full_system.py`
3. `python full_system_v2.py`
4. `python langgraph_orchestrator.py`
5. `python example_scenarios.py`

All systems tested and fully operational.

---

# 📦 Requirements

All versions pinned in `requirements.txt`.

```
langchain==0.1.0
langchain-core==0.1.0
langchain-groq==0.0.1
langgraph==0.0.20
python-dotenv==1.0.1
requests
pydantic
numpy
pandas
```

---

# 📄 License

MIT License
Free to modify and extend.

---

# 🎉 Final Notes

This project demonstrates:

* Multi-agent orchestration
* Tool-powered reasoning
* State management with LangGraph
* Real-world architecture patterns
* Production-level design

Suitable for real-world agentic AI applications, portfolio use, and certification requirements.

---