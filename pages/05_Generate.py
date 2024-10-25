import streamlit as st
import extra_streamlit_components as stx
from repository import get_all_models, get_user_by_id, get_last_input_by_user_id, get_all_prompts_of_a_language, create_input
from helpers import find_index_of_model_by_short_name, find_index_of_prompt_by_title
from ai import call_ai
from st_copy_to_clipboard import st_copy_to_clipboard
from repository import get_db_session
import extra_streamlit_components as stx


from helpers import ensure_logged_in, get_title_and_text

ensure_logged_in()

def create_input_from_output(output):
    title, text = get_title_and_text(output)

    session = next(get_db_session())

    new_input = create_input(user_id=st.session_state.user.id, 
                             title=title, text=text, session=session)

    st.session_state.input = new_input.text
    st.session_state.input_title = new_input.title
    st.session_state.input_id = new_input.id
    st.session_state.input_created_at = new_input.created_at

st.session_state.models = get_all_models()
st.session_state.prompts = get_all_prompts_of_a_language()
st.session_state.languages = ["EN", "DE"]
#st.session_state.user = get_user_by_id(1)
st.session_state.last_input = get_last_input_by_user_id(
    st.session_state.user.id)

if "language" not in st.session_state:
    st.session_state.language = st.session_state.languages[0]

if "model" not in st.session_state:
    st.session_state.model = st.session_state.models[0]

if "prompt" not in st.session_state:
    st.session_state.prompt = st.session_state.prompts[0]

if "input" not in st.session_state:
    st.session_state.input = ""

if "input_title" not in st.session_state:
    st.session_state.input_title = ""

if "output1" not in st.session_state:
    st.session_state.output1 = ""

if "output2" not in st.session_state:
    st.session_state.output2 = ""

if "temperature" not in st.session_state:
    st.session_state.temperature = 0.05



with st.sidebar:

    st.write("**User: " + st.session_state.user.name + "**")

    selected_language_name = st.selectbox("**Select a Language**", options=st.session_state.languages,
                                          index=st.session_state.languages.index(st.session_state.language))
    if selected_language_name != st.session_state.language:
        st.session_state.language = selected_language_name

    selected_model_short_name = st.selectbox(
        "**Select a model**", options=[model.short_name for model in st.session_state.models], index=find_index_of_model_by_short_name(st.session_state.models, st.session_state.model.short_name))

    if selected_model_short_name != st.session_state.model.short_name:
        st.session_state.model = st.session_state.models[find_index_of_model_by_short_name(
            st.session_state.models, selected_model_short_name)]

    st.session_state.temperature = st.slider(
        "**Select a Temperature**", min_value=0.0, max_value=1.0, value=st.session_state.temperature, step=0.01)

st.session_state.prompts = get_all_prompts_of_a_language(st.session_state.language)

selected_prompt_title = st.selectbox(
    "**Select a Prompt**", options=[prompt.title for prompt in st.session_state.prompts], index=find_index_of_prompt_by_title(st.session_state.prompts, st.session_state.prompt.title))
if selected_prompt_title != st.session_state.prompt.title:
    st.session_state.prompt = st.session_state.prompts[find_index_of_prompt_by_title(
        st.session_state.prompts, selected_prompt_title)]

if st.session_state.prompt is not None:
    st.write(st.session_state.prompt.description)
st.write("---")

# Use TabBar component
chosen_id = stx.tab_bar(data=[
    stx.TabBarItemData(id="tab1", title="Generate from Input", description=""),
    stx.TabBarItemData(id="tab2", title="Generate from Chat",description=""),
], default="tab1")


# Generate from Input
if chosen_id == "tab1":
   
    col1a, dummya, col2a, col3a = st.columns([2, 3, 3, 1])
    if col1a.button("Generate Output"):
        input1 = f"# {st.session_state.input_title}\n\n{st.session_state.input}"
        title1 = st.session_state.input_title
        print('### from Input ' + title1 + input1[0:300])
        print(st.session_state.model)
        st.session_state.output = None
        ai_response1 = call_ai(st.session_state.model, 
                               st.session_state.prompt, 
                               input1 , 
                               st.session_state.temperature)
        st.session_state.output1 = f"# {title1}\n\n{ai_response1}"

    if st.session_state.output1 is not None and len(st.session_state.output1) > 5:
        if col2a.button("Create Input from Output"):
            create_input_from_output(st.session_state.output1)
        with col3a:
            st_copy_to_clipboard(st.session_state.output1)

        st.write(st.session_state.output1)

# Generate from Chat
elif chosen_id == "tab2":
    title2 = st.text_input("**Title of your Input:**")
    input2 = st.text_area("**Your text Input:**", height=120)
    col1b, dummyb, col2b, col3b = st.columns([2, 3, 3, 1])
    if col1b.button("Generate Output"):
        print('### from Chat ' + title2 + input2[0:300])
        print(st.session_state.model)
        ai_response2 = call_ai(st.session_state.model, st.session_state.prompt, 
                              input2 , st.session_state.temperature)
        st.session_state.output2 = f"# {title2}\n\n{ai_response2}"

    if st.session_state.output2 is not None and len(st.session_state.output2) > 5:
        if col2b.button("Create Input from Output"):
            create_input_from_output(st.session_state.output2)
        with col3b:
            st_copy_to_clipboard(st.session_state.output2)

        st.write(st.session_state.output2)

