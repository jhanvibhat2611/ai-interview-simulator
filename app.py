import streamlit as st
import tempfile

# Import your resume parser functions
from resume_parser import extract_text_from_resume, extract_skills, extract_experience

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Interview Simulator", layout="centered")

# ---------------- CUSTOM CSS (FONT + CLEAN LOOK) ----------------
st.markdown("""
<style>
body {
    font-size: 18px;
}
h1 {
    font-size: 36px !important;
}
h2 {
    font-size: 26px !important;
}
h3 {
    font-size: 22px !important;
}
label, div, span, p {
    font-size: 18px !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- APP HEADER (MAIN PROJECT NAME) ----------------
st.markdown("<h2 style='margin-bottom: 5px;'>AI Interview Simulator</h2>", unsafe_allow_html=True)
st.markdown("<p style='color: gray; margin-top: 0px;'>Resume Analysis Module</p>", unsafe_allow_html=True)

st.divider()

# ---------------- PAGE TITLE ----------------
st.markdown("<h1>Resume Analysis</h1>", unsafe_allow_html=True)
st.write("Upload your resume to extract skills and estimate experience level.")

st.divider()

# ---------------- SESSION STATE INIT ----------------
if "analyzed" not in st.session_state:
    st.session_state.analyzed = False

if "final_skills" not in st.session_state:
    st.session_state.final_skills = []

if "experience" not in st.session_state:
    st.session_state.experience = ""

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader("Upload Resume (PDF format only)", type=["pdf"])

if uploaded_file is not None:
    st.info("Resume uploaded successfully.")

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        temp_path = tmp.name

    # ---------------- ANALYZE BUTTON ----------------
    if st.button("Analyze Resume"):
        with st.spinner("Analyzing resume, please wait..."):
            text = extract_text_from_resume(temp_path)
            skills = extract_skills(text)
            experience = extract_experience(text)

        # Store results in session state
        st.session_state.final_skills = skills.copy()
        st.session_state.experience = experience
        st.session_state.analyzed = True

# ---------------- SHOW RESULTS ONLY AFTER ANALYSIS ----------------
if st.session_state.analyzed:

    st.divider()
    st.subheader("Analysis Result")

    # ---------------- SKILLS SECTION ----------------
    st.write("Detected Skills (editable)")

    selected_skills = st.multiselect(
        "Select the skills you actually have (remove incorrect ones if needed):",
        options=st.session_state.final_skills,
        default=st.session_state.final_skills
    )

    st.session_state.final_skills = selected_skills

    # ---------------- ADD NEW SKILL (FORM - FIXED) ----------------
    st.write("Add a missing skill manually")

    with st.form("add_skill_form", clear_on_submit=True):
        col1, col2 = st.columns([3, 1])

        with col1:
            new_skill = st.text_input("Enter skill name")

        with col2:
            submitted = st.form_submit_button("Add Skill")

        if submitted and new_skill:
            new_skill = new_skill.strip().lower()

            if new_skill not in st.session_state.final_skills:
                st.session_state.final_skills.append(new_skill)
                st.success(f"Skill added: {new_skill}")
            else:
                st.warning("This skill is already in the list.")

    # ---------------- FINAL SKILLS DISPLAY ----------------
    st.write("Final Confirmed Skills")

    if st.session_state.final_skills:
        st.write(", ".join(st.session_state.final_skills))
    else:
        st.warning("No skills selected.")

    # ---------------- EXPERIENCE SECTION ----------------
    st.divider()
    st.write("Estimated Experience Level")
    st.success(st.session_state.experience.capitalize())