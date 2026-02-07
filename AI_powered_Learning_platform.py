# AI-powered Learning platform
import streamlit as st
from groq import Groq


client = Groq(api_key=st.secrets["GROQ_API_KEY"])
st.header("AI Learning Assistant 📝")

if "material" not in st.session_state:
    st.session_state.material = ""
if "task" not in st.session_state:
    st.session_state.task = ""
if "language" not in st.session_state:
    st.session_state.language = "English"
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "score" not in st.session_state:
    st.session_state.score = ""

with st.sidebar: 
    st.subheader("*Learning Input*")
    topic = st.text_input("Enter your chapter or topic")
    generate = st.button("Generate")

tab1, tab2 = st.tabs(["Learning Material", "Tasks"])

with tab1:   # STUDY MATERIAL
    col1, col2 = st.columns([2, 2])
    with col1:
        st.subheader("Learning Material")
    with col2:
        language = st.selectbox("Select language",["Tamil", "English", "Spanish"],
            index=["Tamil", "English", "Spanish"].index(st.session_state.language))
    if language != st.session_state.language and st.session_state.material:
        st.session_state.language = language
        switch_prompt = f"""
        Explain the topic in detail '{topic}' clearly for beginners with diagram.
        Language: {st.session_state.language}.
        Give simple explanation with examples."""
        switch_res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": switch_prompt}])
        st.session_state.material = switch_res.choices[0].message.content
        st.rerun()
    if generate and topic:
        st.session_state.language = language
        material_prompt = f"""
        Explain the topic in detail '{topic}' clearly for beginners with diagram.
        Language: {st.session_state.language}.
        Give simple explanation with examples."""
        material_res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": material_prompt}])
        st.session_state.material = material_res.choices[0].message.content
        st.rerun()
    if st.session_state.material:
        st.write(st.session_state.material)
        if st.button("Completed"):
            st.session_state.submitted = True
            st.success("Learning completed successfully! Try to complete the task.")

with tab2:
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Task Questions")

    with col2:
        answer_file = st.file_uploader("Upload your answers (.txt)", type=["txt"])

    if st.session_state.submitted and not st.session_state.task:
        task_prompt = f"""
Ask exactly 5 questions based on the study material below.
Do NOT include answers.

STUDY MATERIAL:
{st.session_state.material}
"""
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": task_prompt}]
)
        st.session_state.task = res.choices[0].message.content

    # Show questions
    if st.session_state.task:
        st.write(st.session_state.task)

    # Evaluation
    if answer_file:
        user_answers = answer_file.read().decode("utf-8")

        if st.button("🧮 Evaluate Answers"):
            score_prompt = f"""You are a STRICT examiner.

QUESTIONS:
{st.session_state.task}

STUDENT ANSWERS:
{user_answers}

EVALUATION RULES (FOLLOW STRICTLY):
- There are exactly 5 questions.
- Each question carries 1 mark.
- Award ✅ 1 mark ONLY if the answer is:
  • Fully correct
  • Directly relevant
- Award ❌ 0 marks if the answer is:
  • Incorrect
  • Incomplete
  • Irrelevant
  • Missing
- Do NOT assume intent.
- Do NOT add missing information.
- Do NOT give partial marks.

OUTPUT FORMAT (VERY IMPORTANT):

🎯 **Total Score:** X / 5

📋 **Question-wise Evaluation:**

Q1: ✅ Correct / ❌ Wrong  
Feedback: (one short, strict sentence)

Q2: ✅ Correct / ❌ Wrong  
Feedback: (one short, strict sentence)

Q3: ✅ Correct / ❌ Wrong  
Feedback: (one short, strict sentence)

Q4: ✅ Correct / ❌ Wrong  
Feedback: (one short, strict sentence)

Q5: ✅ Correct / ❌ Wrong  
Feedback: (one short, strict sentence)

Keep the tone objective and strict.
Do NOT include answers or suggestions.
"""
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": score_prompt}])
            st.session_state.score = res.choices[0].message.content
    if st.session_state.score:
        st.success("✅ Your answers are evaluated")
        st.subheader("📊 Score Card")

        st.write(st.session_state.score)



