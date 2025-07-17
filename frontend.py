import streamlit as st
import requests
import pdfplumber

API_URL = "http://127.0.0.1:8000"  # Update if your FastAPI service runs elsewhere

st.set_page_config(page_title="AI Resume Matcher", layout="centered")
st.title(" Resume vs Job Description Matcher")

# ------------------------------------------------------------------
# Resume Upload
# ------------------------------------------------------------------
st.subheader(" Upload Your Resume (.pdf only)")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

# ------------------------------------------------------------------
# Job Description Input
# ------------------------------------------------------------------
st.subheader(" Paste Job Description")
job_description = st.text_area("Paste the job description here...", height=200)


def extract_pdf_text(upload) -> str:
    """Extract plaintext from an uploaded PDF file-like object."""
    try:
        with pdfplumber.open(upload) as pdf:
            parts = []
            for page in pdf.pages:
                parts.append(page.extract_text() or "")
        return "\n".join(parts)
    except Exception as e:  # broad but user friendly
        st.error(f"Failed to read PDF: {e}")
        return ""


# ------------------------------------------------------------------
# Main Action
# ------------------------------------------------------------------
if st.button("🔍 Match Resume"):
    if not uploaded_file or not job_description.strip():
        st.warning("Please upload a resume and paste the job description.")
        st.stop()

    resume_text = extract_pdf_text(uploaded_file)

    # Basic sanity check
    if len(resume_text.strip()) < 50:
        st.error("Resume content is too short to analyze.")
        st.stop()

    with st.spinner("Analyzing and matching..."):
        analyze_resp = requests.post(
            f"{API_URL}/analyze_resume",
            json={"text": resume_text},
            timeout=60,
        )

        if analyze_resp.status_code != 200:
            st.error("❌ Backend error while analyzing resume.")
            with st.expander("See error response"):
                st.write(analyze_resp.status_code, analyze_resp.text)
            st.stop()

        analyze_data = analyze_resp.json()
        summary = analyze_data.get("summary", "")
        skills = analyze_data.get("skills", [])
        experience_section = analyze_data.get("experience", "")

        # --- Match resume to job description (skill %, experience %, overall %) ---
        match_resp = requests.post(
            f"{API_URL}/match-resume",
            json={
                "resume_text": resume_text,
                "job_description": job_description,
            },
            timeout=60,
        )

        if match_resp.status_code != 200:
            st.error("❌ Backend error while matching resume.")
            with st.expander("See error response"):
                st.write(match_resp.status_code, match_resp.text)
            st.stop()

        match_data = match_resp.json()
        experience_pct = match_data.get("experience_pct", 0.0)
        skill_pct = match_data.get("skill_pct", 0.0)
        overall_pct = match_data.get("overall_pct", 0.0)

    # ------------------------------------------------------------------
    # Display results
    # ------------------------------------------------------------------
    st.success("✅ Analysis complete!")

    st.subheader("📊 Match Results")

    # Progress bars
    st.write(f"**Overall Match:** {overall_pct}%")
    st.progress(min(int(overall_pct), 100))

    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Skill Match:** {skill_pct}%")
        st.progress(min(int(skill_pct), 100))
    with col2:
        st.write(f"**Experience Match:** {experience_pct}%")
        st.progress(min(int(experience_pct), 100))

    # ------------------------------------------------------------------
    # Resume Analysis Details
    # ------------------------------------------------------------------
    st.markdown("---")
    st.subheader(" Resume Insights")

    st.markdown("**Summary**")
    st.write(summary if summary else "_No summary extracted._")

   
