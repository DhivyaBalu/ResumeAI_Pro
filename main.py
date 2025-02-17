import streamlit as st
from resumeBuilder import ResumeBuilder
from jobPreparation import JobPreparation
from mockInterview import MockInterview

# Page Configuration
st.set_page_config(page_title="Resume Analyzer", layout="wide")

# Sidebar for Job Details
with st.sidebar:
    st.title("Job Details")
    job_url = st.text_input("Enter the job posting URL")
    uploaded_resume = st.file_uploader("Upload the current resume", type=["pdf"])
    submit_button = st.button("Generate Resume")
    job_preparation = st.button("Job Preparation")
    mock_interview = st.button("Mock Interview")

# Main Content - Resume Output
st.title("AI Resume Optimizer")
resume_container = st.empty()
builder = ResumeBuilder()

if submit_button:
    if job_url and uploaded_resume:
        job_data = builder.fetch_job_data(job_url)
        resume_data = builder.fetch_resume_data(uploaded_resume)
        updated_resume = builder.modify_resume(job_data, resume_data)

        resume_container = st.container()
        resume_container.markdown("## **Updated Resume**")
        resume_container.write(updated_resume)

if job_preparation:
    if job_url:
        jobPrep = JobPreparation()
        resume_container = st.container()
        job_data = builder.fetch_job_data(job_url)
        preparationData = jobPrep.getJobprep(job_data)

        resume_container.markdown("## **Job Preparation - Study Plan**")
        resume_container.write(preparationData)

if mock_interview:
    if job_url:
        resume_container = st.container()
        mock_interview = MockInterview()
        job_data = builder.fetch_job_data(job_url)
        mock_interview_ques = mock_interview.getMockInterviewQues(job_data)

        resume_container.markdown("## ** Mock Interview Questions**")
        resume_container.write(mock_interview_ques)


