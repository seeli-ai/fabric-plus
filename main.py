import streamlit as st
from repository import get_all_models, get_all_prompts, get_user_by_id, get_last_input_by_user_id
from helpers import Language, find_index_of_model_by_short_name, find_index_of_prompt_by_title
from ai import call_ai
from models import Prompt, Model

from dotenv import load_dotenv
load_dotenv()

st.session_state.models =  get_all_models()
st.session_state.prompts = get_all_prompts()
st.session_state.languages = list(Language)
st.session_state.user = get_user_by_id(1)
st.session_state.last_input = get_last_input_by_user_id(st.session_state.user.id)


if st.session_state.last_input is not None and "input" not in st.session_state:
    st.session_state.input = st.session_state.last_input.text
    st.session_state.input_title = st.session_state.last_input.title

if "language" not in st.session_state:
    st.session_state.language = Language.EN

if "model" not in st.session_state:
    st.session_state.model = st.session_state.models[0]

if "prompt" not in st.session_state:
   st.session_state.prompt = st.session_state.prompts[0]

if "input" not in st.session_state:
    st.session_state.input = ""

if "input_title" not in st.session_state:
    st.session_state.input_title = ""


if "output" not in st.session_state:
    st.session_state.output = ""

if "temperature" not in st.session_state:
    st.session_state.temperature = 0.2

with st.sidebar:

    st.write("### User")
    st.write(st.session_state.user.name)

    st.write("### Language")
    if st.session_state.language is None:
        st.session_state.language = Language.EN
    selected_language_name = st.selectbox("Select a language", options=[language.name for language in st.session_state.languages], index=st.session_state.languages.index(st.session_state.language))
    if selected_language_name != st.session_state.language.name:
        st.session_state.language = Language[selected_language_name]

    st.write("### Model")
    selected_model_short_name = st.selectbox(
        "Select a model", options=[model.short_name for model in st.session_state.models], index=find_index_of_model_by_short_name(st.session_state.models, st.session_state.model.short_name))
    
    if selected_model_short_name != st.session_state.model.short_name:
        st.session_state.model = st.session_state.models[find_index_of_model_by_short_name(st.session_state.models, selected_model_short_name)]

    st.write("### Temperature")
    st.session_state.temperature = st.slider("Select a temperature", min_value=0.0, max_value=1.0, value=st.session_state.temperature, step=0.01)



tab1, tab3, tab4 = st.tabs(["Generate", "Input", "Edit Input"])

with tab1:
    st.session_state.prompts = get_all_prompts(st.session_state.language.value)
    selected_prompt_title = st.selectbox(
        "Select a prompt", options=[prompt.title for prompt in st.session_state.prompts]) # , index=find_index_of_prompt_by_title(st.session_state.prompts, st.session_state.prompt.title))
    if selected_prompt_title != st.session_state.prompt.title:
        st.session_state.prompt = st.session_state.prompts[find_index_of_prompt_by_title(st.session_state.prompts, selected_prompt_title)]
    
    if st.session_state.prompt is not None:
        st.write(st.session_state.prompt.description)

        if st.button("Generate"):
            input = f"# {st.session_state.input_title}\n\n{st.session_state.input}"
            st.session_state.output = call_ai(st.session_state.model, st.session_state.prompt, input, st.session_state.temperature)

    if st.session_state.output != "":
        st.write("#### Output")
        st.write(st.session_state.output)




with tab3:
    # st.write("#### Input")
    st.write (f"#### {st.session_state.input_title}\n")
    st.write(st.session_state.input)

with tab4:
    edited_input = st.text_area("Enter text here", st.session_state.input, height=600, label_visibility="collapsed")
    if st.button("Clear"):
        st.session_state.input = ""

    if st.button("Submit"):
        st.session_state.input = edited_input





