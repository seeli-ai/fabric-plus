from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from ai_helpers import MarkdownOutputParser

from models import Model

def call_open_ai(model: Model, prompt: str, input: str, temperature: float) -> str:
    model_name = model.name

    llm = ChatOpenAI(model=model_name, temperature=temperature)

    prompt = ChatPromptTemplate.from_messages([
        ("system", prompt),
        ("human", "{input}")
    ])

    parser = MarkdownOutputParser()

    chain = prompt | llm | parser

    response = chain.invoke({
        "input": input
    })

    return response

