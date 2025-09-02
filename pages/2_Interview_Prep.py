import streamlit as st

st.set_page_config(page_title="Interview Prep", page_icon="🧠", layout="wide")
st.title("🧠 Interview Prep")

st.markdown("""
### General Tips
- Review your **resume** stories (STAR): Situation, Task, Action, Result.
- Practice **behavioral** answers: teamwork, conflict, leadership, impact.
- Brush up on **fundamentals** (DSA for SWE, stats/SQL for data roles, case-style for consulting).
- Prepare **questions** to ask recruiters about teams, projects, timelines.

### Sample Questions
- *Tell me about yourself.*
- *Walk me through a challenging project—what was your role?*
- *How do you handle ambiguous requirements?*
- *Describe a time you influenced a decision with data.*
- *What do you want to work on here and why?*

### Company‑Specific Research
Upload career fair PDFs and use the **Ask the Assistant** page to query for employer specifics (roles, locations, sponsorship).
""")
