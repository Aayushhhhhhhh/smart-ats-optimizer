import streamlit as st
import os
import PyPDF2 as pdf
from langchain_openai import ChatOpenAI
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 1. Configuration & Setup
st.set_page_config(page_title="Smart ATS: Resume Optimizer", layout="wide")
st.title("Smart ATS: Resume Optimizer 🚀")
st.markdown("### Improve Your Resume Ranking with AI & Math")

# 2. Sidebar Inputs
st.sidebar.header("Job Details")
jd = st.sidebar.text_area("Paste the Job Description (JD) here:", height=300)

# 3. API Key Management
try:
    api_key = st.secrets["OPENROUTER_API_KEY"]
except:
    st.error("API Key missing. Please set OPENROUTER_API_KEY in Streamlit Secrets.")
    st.stop()

# --- HELPER FUNCTIONS ---

def input_pdf_text(uploaded_file):
    """Extracts text from the uploaded PDF file."""
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

def calculate_match_score(resume_text, jd_text):
    """
    Calculates the percentage match between the resume and JD 
    using Cosine Similarity (Vector Math).
    """
    # Create a list of text
    text_list = [resume_text, jd_text]
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(text_list)
    
    # Calculate cosine similarity
    matchPercentage = cosine_similarity(count_matrix)[0][1] * 100
    return round(matchPercentage, 2)

def get_llm_response(input_text):
    """Calls the LLM to get a qualitative analysis."""
    llm = ChatOpenAI(
        openai_api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        model_name="meta-llama/llama-3.3-70b-instruct:free",
        temperature=0.0
    )
    response = llm.invoke(input_text)
    return response.content

# --- MAIN APP LOGIC ---

uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type="pdf", help="Please upload the pdf")

submit = st.button("Evaluate Resume")

if submit:
    if uploaded_file is not None and jd:
        # A. Processing
        with st.spinner('Parsing PDF and Calculating Score...'):
            resume_text = input_pdf_text(uploaded_file)
            
            # B. The MATH (Cosine Similarity)
            match_score = calculate_match_score(resume_text, jd)
        
        # Display Score nicely
        st.divider()
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.metric("ATS Match Score", f"{match_score}%")
            if match_score < 50:
                st.error("⚠️ Low Match: Your resume might be filtered out.")
            elif match_score < 75:
                st.warning("⚠️ Moderate Match: Needs improvement.")
            else:
                st.success("✅ High Match: Looking good!")

        # C. The AI (Qualitative Analysis)
        with col2:
            st.subheader("🤖 AI Analysis")
            with st.spinner('Generating detailed feedback...'):
                input_prompt = f"""
                Act as a skilled Application Tracking System (ATS) and Technical Recruiter with deep knowledge of tech field. 
                Your goal is to evaluate the resume against the job description.
                
                Resume Text:
                {resume_text}
                
                Job Description:
                {jd}
                
                PROVIDE THE FOLLOWING IN MARKDOWN FORMAT:
                1. **Missing Keywords:** List the critical technical keywords from the JD that are missing in the resume.
                2. **Profile Summary Rewrite:** Write a crisp, 3-sentence profile summary optimized for this JD.
                3. **Action Plan:** Give 3 specific bullet points on what to change in the "Projects" or "Experience" section to increase the match score.
                """
                
                response = get_llm_response(input_prompt)
                st.markdown(response)

    else:
        st.warning("Please upload a PDF Resume and paste the Job Description.")
