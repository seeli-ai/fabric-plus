import streamlit as st
from repository import get_all_models, get_all_prompts, get_user_by_id, get_inputs_by_user_id, delete_input
from helpers import Language, find_index_of_model_by_short_name, find_index_of_prompt_by_title
from ai import call_ai
from models import Prompt, Model

if "user" not in st.session_state:
    st.stop()

if "input_id" not in st.session_state:  
    st.session_state.input_id = None

user_inputs = get_inputs_by_user_id(st.session_state.user.id)

input_ids = [input.id for input in user_inputs]
input_titles = [input.title + " ---- " + input.created_at.strftime("%d.%m.%Y")  for input in user_inputs]

selected_input = st.selectbox("Select an input", input_titles, index=None)

if selected_input is not None:
    
    input_id = input_ids[input_titles.index(selected_input)]
    input_text = user_inputs[input_ids.index(input_id)].text
    input_title = user_inputs[input_ids.index(input_id)].title
    col1, col2 = st.columns(2)
    if col1.button("Set as current input"):
        st.session_state.input = input_text
        st.session_state.input_title = input_title
        st.session_state.input_id = input_id

    if col2.button("Delete input") and input_id is not None:
       delete_input(input_id)
       selected_input = None
       input_text = None
       st.rerun()
        
    if selected_input is not None:
       st.write(f"### {selected_input}")
       st.write(input_text)

