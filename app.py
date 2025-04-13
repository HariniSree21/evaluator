           
import streamlit as st
import google.generativeai as genai
import json
import re

# ✅ Configure Gemini API with your key
api_key = st.secrets["api"]["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
# ✅ Load the correct model
model = genai.GenerativeModel("models/gemini-1.5-pro")

# 🎨 App UI
st.set_page_config(page_title="LLM Grader", page_icon="📚", layout="centered")
st.title("📚 LLM Grader")
st.markdown("Evaluate any student's answer with AI.\nJust input the concept and the student's explanation.")

# 📥 Input fields
with st.form(key="grader_form"):
    user_question = st.text_input("🔍 Enter the concept or question:")
    student_answer = st.text_area("🧠 Enter the student's explanation or definition:")
    submit = st.form_submit_button("🚀 Evaluate")

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

            # ✅ Clean the output if it has backticks
            cleaned_output = re.sub(r"^```(?:json)?|```$", "", raw_output.strip(), flags=re.MULTILINE).strip()

            try:
                result = json.loads(cleaned_output)
                st.success("✅ Evaluation complete!")
                st.markdown("### 📝 Grading Result")
                st.json(result)
            except Exception as e:
                st.error("❌ The model did not return valid JSON. Here's the raw output:")
                st.code(raw_output)
