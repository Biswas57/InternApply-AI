import os
import PyPDF2
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()
os.getenv("GROQ_API_KEY")

class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key='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',
            model_name="llama-3.1-70b-versatile"
        )
    
    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={'page_data': cleaned_text})
        
        try:
            json_parser = JsonOutputParser()
            json_res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return json_res if isinstance(json_res, list) else [json_res]

    def write_email(self, job, links):
        
        with open('app/resources/resume.pdf', 'rb') as file:
            reader = PyPDF2.PdfReader(file)

            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                resume_content = page.extract_text()
        
        with open('app/resources/email_template.txt', 'r') as file:
            email_temp = file.read()
        
        prompt_email = PromptTemplate.from_template(
            """
        ### JOB DESCRIPTION:
        {job_description}
        
        ### RESUME CONTENT:
        {resume_content}
        
        ### INSTRUCTION:
        You are the person whose resume is attached above. Your skills, experiences and education match theirs exactly
        Your job is to write a cold email to a job recruiter regarding the job mentioned above in the position of the person the resume is about, showcasing your expertise in the skills required by the job description, your ability to build scalable and efficient solutions, and your experience with relevant technologies that meet their needs.
        Write this cold email in the format of the email template below
        Also, ONLY add the most relevant project from the following links to highlight your portfolio: {link_list}
        
        ### EMAIL TEMPLATE:
        {email_temp}
        
        Do not provide a preamble.
        ### EMAIL (NO PREAMBLE):
        """
        )

        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job),"resume_content": resume_content, "link_list": links, "email_temp": email_temp})
        return res.content

