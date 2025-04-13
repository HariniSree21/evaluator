import streamlit as st
import google.generativeai as genai
import json
import re

# ✅ Securely load API key from Streamlit secrets
api_key = st.secrets["api"]["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# ✅ Load Gemini model
model = genai.GenerativeModel("models/gemini-1.5-pro")

# 🎨 Page setup
st.set_page_config(page_title="Smart Answer Scorer", page_icon="🧠", layout="centered")

# 🧠 App title and description
st.markdown("""
# 📚 Smart Answer Scorer  
*AI-Powered Feedback for Student Responses*

Enter a question and a student’s answer. This tool will analyze the explanation and provide a score, feedback, and a verdict — instantly!
""")

# 📥 Input form
with st.form(key="grader_form"):
    user_question = st.text_input("🔍 Enter the concept or question:")
    student_answer = st.text_area("🧠 Enter the student's explanation or definition:")
    submit = st.form_submit_button("🚀 Evaluate Answer", use_container_width=True)

st.markdown("---")

# 🧠 Evaluation logic
if submit:
    if not user_question or not student_answer:
        st.warning("⚠️ Please fill in both the question and the student's answer.")
    else:
        prompt = f"""
You are an intelligent grader.

A student has written the following answer for the question:
Question: {user_question}
Student's Answer: {student_answer}

Evaluate how correct, complete, and well-explained this answer is in simple English.
Return your evaluation in **valid JSON format** with the following keys:
- score_out_of_10: number
- feedback: short sentence or two
- verdict: One of ["Excellent", "Good", "Average", "Poor"]
"""

        with st.spinner("Evaluating with Gemini..."):
            response = model.generate_content(prompt)
            raw_output = response.text

            # ✅ Clean Gemini's output
            cleaned_output = re.sub(r"^```(?:json)?|```$", "", raw_output.strip(), flags=re.MULTILINE).strip()

            try:
                # Parse cleaned output into JSON
                result = json.loads(cleaned_output)

                # ✅ Display JSON format output
                st.success("✅ Evaluation complete!")
                st.markdown("### 📝 Grading Result")
                st.json(result)  # Show as JSON

            except Exception as e:
                st.error("❌ The model did not return valid JSON. Here's the raw output:")
                st.code(raw_output)
