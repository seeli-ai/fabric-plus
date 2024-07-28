import streamlit as st
from repository import get_all_models, get_all_prompts
from helpers import Language, find_index_of_model_by_short_name, find_index_of_prompt_by_title
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from models import Prompt, Model

from dotenv import load_dotenv
load_dotenv()



st.session_state.models =  get_all_models()
st.session_state.prompts = get_all_prompts()
#st.session_state.prompt = st.session_state.prompts[0]


if "language" not in st.session_state:
    st.session_state.language = Language.EN

if "model" not in st.session_state:
    st.session_state.model = st.session_state.models[0]

if "prompt" not in st.session_state:
   st.session_state.prompt = st.session_state.prompts[0]

if "input" not in st.session_state:
    st.session_state.input = ""

if "output" not in st.session_state:
    st.session_state.output = ""

st.write(st.session_state.prompt)
if st.session_state.input != "":
    st.write("There is input")
language_list = list(Language)

with st.sidebar:

    st.write("### Language")
    selected_language_name = st.selectbox("Select a language", options=[language.name for language in language_list], index=language_list.index(st.session_state.language))
    if selected_language_name != st.session_state.language.name:
        st.session_state.language = Language[selected_language_name]

    st.write("### Model")
    selected_model_short_name = st.selectbox(
        "Select a model", options=[model.short_name for model in st.session_state.models], index=find_index_of_model_by_short_name(st.session_state.models, st.session_state.model.short_name))
    
    if selected_model_short_name != st.session_state.model.short_name:
        st.session_state.model = st.session_state.models[find_index_of_model_by_short_name(st.session_state.models, selected_model_short_name)]




tab1, tab2, tab3, tab4 = st.tabs(["Select Pattern", "Output" , "Input", "Edit Input"])

with tab1:
    selected_prompt_title = st.selectbox(
        "Select a prompt", options=[prompt.title for prompt in st.session_state.prompts], index=find_index_of_prompt_by_title(st.session_state.prompts, st.session_state.prompt.title))
    if selected_prompt_title != st.session_state.prompt.title:
        st.session_state.prompt = st.session_state.prompts[find_index_of_prompt_by_title(st.session_state.prompts, selected_prompt_title)]
    
    if st.session_state.prompt is not None:
        st.write(st.session_state.prompt.description)

        if st.button("Generate"):
            model = ChatOpenAI()
            prompt = ChatPromptTemplate.from_messages([
            ("system", st.session_state.prompt.system_prompt),
            ("human", "{input}")
            ])

            parser = StrOutputParser()

            chain = prompt | model | parser

            res = chain.invoke({
                "input": st.session_state.input
            })

            st.session_state.output = res

with tab2:
    st.write("## Output")
    st.write(st.session_state.output)

with tab3:
    st.write("## Input")
    st.write(st.session_state.input)

with tab4:
    edited_input = st.text_area("Enter text here", st.session_state.input, height=600, label_visibility="collapsed")
    if st.button("Clear"):
        st.session_state.input = ""

    if st.button("Submit"):
        st.session_state.input = edited_input





