import streamlit as st
import pyttsx3

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Live Interview", layout="centered")

# ---------------- SESSION STATE ----------------
if "questions" not in st.session_state:
    st.session_state.questions = [
        "What keyword is used to define a function in Python?",
        "What is the difference between a list and a tuple?",
        "Explain what a dictionary is in Python.",
        "What does the return keyword do?",
        "What is a lambda function?"
    ]

if "current_q_index" not in st.session_state:
    st.session_state.current_q_index = 0

if "answers" not in st.session_state:
    st.session_state.answers = []

if "last_spoken_index" not in st.session_state:
    st.session_state.last_spoken_index = -1

# ---------------- INIT TTS ENGINE (ONLY ONCE) ----------------
if "tts_engine" not in st.session_state:
    engine = pyttsx3.init()
    engine.setProperty("rate", 160)
    st.session_state.tts_engine = engine

def speak(text):
    engine = st.session_state.tts_engine
    engine.say(text)
    engine.runAndWait()

# ---------------- UI ----------------
st.title("🎤 Live Interview Session")

total = len(st.session_state.questions)
idx = st.session_state.current_q_index

st.caption(f"Question {idx + 1} of {total}")
st.divider()

question = st.session_state.questions[idx]
st.subheader(question)

# 🔊 SPEAK QUESTION ONLY ON CHANGE
if st.session_state.last_spoken_index != idx:
    speak(question)
    st.session_state.last_spoken_index = idx

# ---------------- ANSWER INPUT ----------------
answer = st.text_area("Your Answer", height=120, key=f"answer_{idx}")

# ---------------- CONTROLS ----------------
col1, col2 = st.columns(2)

with col1:
    if st.button("⏭ Next Question"):
        st.session_state.answers.append(answer)

        if idx + 1 >= total:
            st.success("✅ Interview Completed!")
            st.stop()

        st.session_state.current_q_index += 1
        st.rerun()

with col2:
    if st.button("⏹ End Interview"):
        st.warning("Interview ended early.")
        st.stop()
