from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import PromptTemplate
import pdfplumber
import io
from llm_config import llm

class ResumeBuilder:

    def __init__(self):
        pass

    def extract_text_from_url(self, job_url: str) -> str:
        loader = WebBaseLoader(job_url)
        page_data = loader.load().pop().page_content
        return page_data

    def fetch_job_data(self, job_url: str) -> str:

        page_data = self.extract_text_from_url(job_url)

        prompt = PromptTemplate.from_template(
            """ You are a professional in extracting the job description and skill from the give page data. 
            You need to analyse the data and extract the job title, job description, requirement and skill from {page_data}.
            (NO PREAMBLE) """
        )
        chain_prompt = prompt | llm
        job_data = chain_prompt.invoke(input={'page_data': page_data})
        return job_data.content

    def fetch_resume_data(self, uploaded_resume) -> str:
        resume_text = ""
        try:
            # Ensure uploaded_resume is read correctly as bytes
            resume_bytes = uploaded_resume.read()  # Use .read() instead of .getvalue()
            with pdfplumber.open(io.BytesIO(resume_bytes)) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        resume_text += text
        except Exception as e:
            raise Exception(f"Exception Occurred: {str(e)}") from e

        formatted_resume = self.format_resume(resume_text)
        
        return formatted_resume

    def modify_resume(self, job_data: str, resume_data: str) -> str:
        prompt = PromptTemplate.from_template(
            """
            Modify the resume to align perfectly with the given job description. Take all the skills from the job description (Do
            NOT MISS ANY SKILLS) and get it added into the resume in a more natural sounding manner.

            The number of experience should remain the same the original resume
            Do not add certifications unless they are already present in the original resume.
            Keep the resume highly professional and tailored specifically to the job description.
            Resume:
            {resume_text}
            
            Job Description:
            {job_data}
            """
        )
        chain_prompt = prompt | llm
        update_resume = chain_prompt.invoke(input={'resume_text': resume_data, 'job_data': job_data})
        return update_resume.content

    def format_resume(self, resume_text: str) -> str:

        prompt = PromptTemplate.from_template(
            """
            You are a professional resume formatter. Given the extracted resume text below:

            {resume_text}

            Reformat it into a structured, professional resume with clear sections:

            Ensure the formatting is **clear, well-structured, and professional**.
            Use **bullet points** and **consistent spacing**.
            Separate different skills with **commas**.
            All the heading should be bold, add a new line after each heading and where ever needed
            Proper grouping & section headers for clarity.

            Output the resume in **plain text format** (NO MARKDOWN, NO HTML).

            (NO PREAMBLE, ONLY THE FORMATTED RESUME)
            """
        )

        chain_prompt = prompt | self.llm
        formatted_resume = chain_prompt.invoke(input={'resume_text': resume_text})

        return formatted_resume.content
