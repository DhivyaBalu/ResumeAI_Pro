from langchain_core.prompts import PromptTemplate
from llm_config import llm

class JobPreparation:

    def __init__(self):
        pass

    def getJobprep(self, job_data: str) -> str:
        prompt = PromptTemplate.from_template(
            """
            Here are the details on the job data {job_data}
        
            Identify any key skills or knowledge areas that are crucial for the job, especially those that are not part of my current skill set or experience.
            Organize the study plan by breaking down each topic into manageable learning steps.
            Suggest online resources links, tutorials, and courses that can help me learn each skill.
            Create a weekly plan (or timeline) based on the time I have before the interview to ensure I can comfortably learn the topics.
            If there are any foundational concepts I need to brush up on, make sure to include them as well.
        
            (NO PREAMBLE) """
        )
        chain_prompt = prompt | llm
        job_preparation = chain_prompt.invoke(input={'job_data': job_data})
        return job_preparation.content