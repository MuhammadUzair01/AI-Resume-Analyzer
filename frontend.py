import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"  # FastAPI backend URL

st.set_page_config(page_title="AI Resume Analyzer", layout="centered")
st.title("📄 AI Resume Analyzer")
st.markdown("Upload your resume in PDF format to extract key insights.")

uploaded_file = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])

if uploaded_file:
    # Step 1: Upload resume to FastAPI backend
    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
    with st.spinner("Uploading and extracting..."):
        upload_response = requests.post(f"{API_URL}/upload_resume", files=files)

    if upload_response.status_code == 200:
        resume_text = upload_response.json()["text"]

        # Step 2: Analyze resume
        with st.spinner("Analyzing resume..."):
            analysis_response = requests.post(
                f"{API_URL}/analyze_resume",
                json={"text": resume_text}
            )

        if analysis_response.status_code == 200:
            analysis = analysis_response.json()

            st.subheader("🔍 Summary")
            st.write(analysis["summary"])

            st.subheader("💡 Skills")
            if analysis["skills"]:
                st.write(", ".join(analysis["skills"]))
            else:
                st.warning("No skills detected.")

            st.subheader("🧑‍💼 Experience")
            if analysis["experience"] != "Not matched":
                st.write(analysis["experience"])
            else:
                st.warning("No experience section matched.")
        else:
            st.error("❌ Error analyzing resume.")
    else:
        st.error("❌ Failed to extract text. Make sure it's a valid PDF.")
