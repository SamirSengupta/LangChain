import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain.prompts import PromptTemplate
from langchain.chains import SimpleSequentialChain, LLMChain

def generate_company_info(comp_name):
    hist = []
    os.environ['GOOGLE_API_KEY'] = 'AIzaSyArLPSqQsvFK3_sXbLHMxx6U3hfomsZ8J4'
    llm = ChatGoogleGenerativeAI(model='gemini-pro')

    # Generate a company name suggestion
    comp = PromptTemplate.from_template(f"Suggest me a name of a {comp_name} company, suggest only 1 name ")
    comp_chain = LLMChain(llm=llm, prompt=comp)
    resp = comp_chain.run(topic=comp_name)

    # Generate a prompt for suggesting services related to the company
    service = PromptTemplate.from_template(f"Suggest me the services which {resp} provides, give me 5 services in list format ")
    service_chain = LLMChain(llm=llm, prompt=service)
    service_resp = service_chain.run(topic=resp)

    # Split services into a list
    services = [s.strip() for s in service_resp.split('\n') if s.strip()]

    hist.append((comp, resp))   
    hist.append((service, services))

    return resp, services

# Streamlit UI
st.title("LangChain Based Company Name and Services Generator")

comp_name = st.text_input("Enter the type of company you want to generate a name for (e.g., EduTech)")

if st.button("Generate"):
    if comp_name:
        comp_name = comp_name.strip()
        company_name, services = generate_company_info(comp_name)
        st.write(f"Company Name: {company_name}")
        st.write("Services Provided:")
        for i, service in enumerate(services, start=1):
            st.write(f"{service}")

