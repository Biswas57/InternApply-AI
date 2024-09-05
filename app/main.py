import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
import PyPDF2

from chains import Chain
from portfolio import Portfolio
from utils import clean_text

def get_resume():
    with open('app/resources/resume.pdf', 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        resume_content = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            resume_content += page.extract_text()
    return resume_content

def get_email_temp():
    with open('app/resources/email_template.txt', 'r') as file:
        email_temp = file.read()
    return email_temp

def generate_email_page(llm, portfolio, clean_text):
    st.title("Generate Emails for Job Applications")
    
    url_input = st.text_input("Enter a Job Posting URL:", value="https://example.com/job/posting-number")
    submit_button = st.button("Generate Email")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            resume = get_resume()
            email = get_email_temp()
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = llm.write_email(job, links, resume, email)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")

import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
import PyPDF2

from chains import Chain
from portfolio import Portfolio
from utils import clean_text

def get_resume():
    with open('app/resources/resume.pdf', 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        resume_content = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            resume_content += page.extract_text()
    return resume_content

def get_email_temp():
    with open('app/resources/email_template.txt', 'r') as file:
        email_temp = file.read()
    return email_temp

def generate_email_page(llm, portfolio, clean_text):
    st.title("Generate Emails for Job Applications")
    url_input = st.text_input("Enter a Job Posting URL:", value="https://example.com/job/posting-number")
    submit_button = st.button("Generate Email")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            jobs = llm.extract_jobs(data)
            resume = get_resume()
            email = get_email_temp()
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = llm.write_email(job, links, resume, email)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")

def answer_questions_page(llm, portfolio, clean_text):
    st.subheader("Ask Application Questions")
    url_input = st.text_input("Enter a Job Posting URL:", value="https://example.com/job/posting-number")
    question = st.text_input("Enter your question:")
    submit_button = st.button("Answer Question")
    
    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            jobs = llm.extract_jobs(data)
            resume = get_resume()
            for job in jobs:
                answer = llm.write_answer(job, resume, question)
                st.code(answer, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")


st.set_page_config(layout="wide", page_title="Intern Apply AI", page_icon="👨🏽‍🎓")
page = st.sidebar.radio("Select a Page", ("Generate Emails", "Answer Questions"))
llm = Chain()
portfolio = Portfolio()
portfolio.load_portfolio()
if page == "Generate Emails":
    generate_email_page(llm, portfolio, clean_text)
elif page == "Answer Questions":
    answer_questions_page(llm, portfolio, clean_text)
