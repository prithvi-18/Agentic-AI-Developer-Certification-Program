"""
EXAMPLE SCENARIOS - Career Growth Assistant
Three realistic career transition examples

Scenario 1: Junior Designer → Senior UX Designer
Scenario 2: Graphic Designer → Frontend Developer  
Scenario 3: Software Developer → Data Scientist
"""

from langgraph_orchestrator import run_langgraph_system

def scenario_1_designer_to_senior_ux():
    """Junior Designer → Senior UX Designer"""
    print("\n" + "="*70)
    print("SCENARIO 1: Junior Graphic Designer → Senior UX Designer")
    print("="*70)
    
    result = run_langgraph_system(
        current_role="Junior Graphic Designer (1 year experience)",
        target_role="Senior UX Designer",
        current_skills=["Photoshop", "Illustrator", "Wireframing", "UI Design", "Typography"]
    )
    
    print("\n✅ Scenario 1 Complete!")
    print(f"Steps Completed: {result['step']}/4")
    return result


def scenario_2_designer_to_frontend():
    """Graphic Designer → Frontend Developer"""
    print("\n" + "="*70)
    print("SCENARIO 2: Graphic Designer → Frontend Developer")
    print("="*70)
    
    result = run_langgraph_system(
        current_role="Graphic Designer (2 years experience)",
        target_role="Frontend Developer",
        current_skills=["HTML", "CSS", "Basic JavaScript", "Adobe Suite", "Responsive Design"]
    )
    
    print("\n✅ Scenario 2 Complete!")
    print(f"Steps Completed: {result['step']}/4")
    return result


def scenario_3_dev_to_data_scientist():
    """Software Developer → Data Scientist"""
    print("\n" + "="*70)
    print("SCENARIO 3: Software Developer → Data Scientist")
    print("="*70)
    
    result = run_langgraph_system(
        current_role="Software Developer (3 years experience)",
        target_role="Data Scientist",
        current_skills=["Python", "Java", "SQL", "Git", "APIs", "Problem Solving"]
    )
    
    print("\n✅ Scenario 3 Complete!")
    print(f"Steps Completed: {result['step']}/4")
    return result


if __name__ == "__main__":
    print("\n🎯 CAREER GROWTH ASSISTANT - EXAMPLE SCENARIOS")
    print("Demonstrating 3 different career transitions\n")
    
    # Run all scenarios
    scenario_1_designer_to_senior_ux()
    scenario_2_designer_to_frontend()
    scenario_3_dev_to_data_scientist()
    
    print("\n" + "="*70)
    print("✅ ALL 3 SCENARIOS COMPLETED SUCCESSFULLY!")
    print("="*70)
    print("\nThese examples demonstrate:")
    print("  ✅ Different career paths (design, development, data)")
    print("  ✅ Varying experience levels (1-3 years)")
    print("  ✅ Different skill gaps and requirements")
    print("  ✅ Personalized recommendations for each path")
    print("  ✅ Production-quality error handling")
