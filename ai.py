# -*- coding: utf-8 -*-
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
import os

from models import Prompt, Model

from dotenv import load_dotenv
load_dotenv()

def call_ai(model: Model, prompt: Prompt, input: str, temperature: float) -> str:
    
    if model.provider.name == "OpenAI":
        return call_open_ai(model, prompt, input, temperature)
    
    if model.provider.name == "Anthropics":
        return call_anthropics(model, prompt, input, temperature)
    
    return "Provider not supported"



def call_open_ai(model: Model, prompt: Prompt, input: str, temperature: float) -> str:
    model_name = model.name

    llm = ChatOpenAI(model=model_name, temperature=temperature)

    prompt = ChatPromptTemplate.from_messages([
        ("system", prompt.system_prompt),
        ("human", "{input}")
    ])

    parser = StrOutputParser()

    chain = prompt | llm | parser

    response = chain.invoke({
        "input": input
    })

    return response

def call_anthropics(model: Model, prompt: Prompt, input: str, temperature: float) -> str:
    model_name = model.name

    llm = ChatAnthropic(model=model_name, temperature=temperature)

    prompt = ChatPromptTemplate.from_messages([
        ("system", prompt.system_prompt),
        ("human", "{input}")
    ])

    parser = StrOutputParser()

    chain = prompt | llm | parser

    response = chain.invoke({
        "input": input
    })

    return response


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