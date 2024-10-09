# -*- coding: utf-8 -*-
import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from anthropic import APIStatusError
from langchain_anthropic import ChatAnthropic
from ai_helpers import MarkdownOutputParser
import random
from time import sleep

from models import Model


MAX_RETRIES = 5
BASE_DELAY = 1 

def calculate_delay(attempt):
    return BASE_DELAY * (2 ** attempt) + random.uniform(0, 1)

def call_anthropics(model: Model, prompt: str, input: str, temperature: float) -> str:
    model_name = model.name

    llm = ChatAnthropic(model=model_name, temperature=temperature)

    prompt = ChatPromptTemplate.from_messages([
        ("system", prompt),
        ("human", "{input}")
    ])

    parser = MarkdownOutputParser()

    chain = prompt | llm | parser
 
    for attempt in range(MAX_RETRIES):
        try:
            response = chain.invoke({
                "input": input
            })
            return response
        except APIStatusError as e:
            if e.status_code == 429:
                delay = BASE_DELAY * (2 ** attempt)
                st.warning(f"Rate limited. Retrying in {delay} seconds...")
                sleep(delay)
            elif e.status_code == 529:
                delay = calculate_delay(attempt)
                st.warning(f"API overloaded. Retrying in {delay:.2f} seconds... (Attempt {attempt + 1}/{MAX_RETRIES})")
                sleep(delay)
            else:
                raise e
    st.error("Max retries reached. Unable to get a response from the API.")
    return "Error: Unable to process the request due to high demand. Please try again later."



def translate_prompt(title: str, description: str, text: str) -> str:
    model_name = "claude-3-5-sonnet-20240620"

    llm = ChatAnthropic(model=model_name)

    instructions = """
    Translate the following text from English to German:
    
    Keep the markdown formatting.

    Only respond with the translated text.
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", instructions),
        ("human", "{input}")
    ])

    parser = StrOutputParser()

    chain = prompt | llm | parser

    title_de = chain.invoke({
        "input": title
    })

    description_de = chain.invoke({
        "input": description
    })

    text_de = chain.invoke({
        "input": text
    })

    return title_de, description_de, text_de