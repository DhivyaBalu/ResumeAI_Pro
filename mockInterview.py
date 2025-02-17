from langchain_core.prompts import PromptTemplate
from llm_config import llm

class MockInterview:
    def __init__(self):
        pass

    def getMockInterviewQues(self, job_data: str) -> str:
        prompt = PromptTemplate.from_template(
            """
            I am preparing for a job interview with the following job data. I would like you to generate a set of mock interview questions 
            based on the job details and skills, including technical questions, behavioral questions, and situational questions. These questions should help me practice 
            for the interview and assess my understanding of the required skills.

            {job_data}

            Generate technical questions based on the skills mentioned in the job description (e.g., programming languages, frameworks, tools, methodologies).
            Include behavioral questions that assess how I work in teams, handle challenges, and demonstrate leadership.
            Create situational questions that test how I would approach real-world challenges specific to the role.
            For technical questions, include questions that gauge both conceptual understanding and hands-on experience with the technologies and tools mentioned.
            Prioritize the questions based on the importance of each skill in the job description, starting with the most crucial areas.

            (NO PREAMBLE) 
            """
        )
        chain_prompt = prompt | llm
        mock_interview_ques = chain_prompt.invoke(input={'job_data': job_data})
        return mock_interview_ques.content