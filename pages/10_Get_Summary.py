from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import streamlit as st

from dotenv import load_dotenv
load_dotenv()


if "input" not in st.session_state:
    st.session_state.input = ""

if st.session_state.input == "":
    st.write("No text to summarize.")
    st.stop()

pattern = """
# IDENTITY and PURPOSE

You are an expert content summarizer. You take content in and output a Markdown formatted summary using the format below.

Take a deep breath and think step by step about how to best accomplish this goal using the following steps.

# OUTPUT SECTIONS

- Combine all of your understanding of the content into a single, 20-word sentence in a section called ONE SENTENCE SUMMARY:.

- Output the 3 most important points of the content as a list with no more than 12 words per point into a section called MAIN POINTS:.

- Output a list of the 3 best takeaways from the content in 12 words or less each in a section called TAKEAWAYS:.

# OUTPUT INSTRUCTIONS

- Output bullets not numbers.
- You only output human readable Markdown.
- Keep each bullet to 12 words or less.
- Do not output warnings or notes—just the requested sections.
- Do not repeat items in the output sections.
- Do not start items with the same opening words.

# INPUT:

INPUT:
"""
if st.button("Get summary"):
    model = ChatOpenAI()
    prompt = ChatPromptTemplate.from_messages([
        ("system", pattern),
        ("human", "{input}")
    ])

    parser = StrOutputParser()

    chain = prompt | model | parser

    res = chain.invoke({
        "input": st.session_state.input
    })

    st.write(res)
