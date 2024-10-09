import streamlit as st
from repository import get_all_models, get_user_by_id, get_last_input_by_user_id, get_all_prompts_of_a_language, create_input
from helpers import find_index_of_model_by_short_name, find_index_of_prompt_by_title
from ai import call_ai
from st_copy_to_clipboard import st_copy_to_clipboard
from repository import get_db_session


from helpers import ensure_logged_in, get_title_and_text

ensure_logged_in()

st.session_state.models = get_all_models()
st.session_state.prompts = get_all_prompts_of_a_language()
st.session_state.languages = ["EN", "DE"]
st.session_state.user = get_user_by_id(1)
st.session_state.last_input = get_last_input_by_user_id(
    st.session_state.user.id)


if st.session_state.last_input is not None and "input" not in st.session_state:
    st.session_state.input = st.session_state.last_input.text
    st.session_state.input_title = st.session_state.last_input.title
    st.session_state.input_created_at = st.session_state.last_input.created_at

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

if "input_title_save" not in st.session_state:
    st.session_state.input_title_save = ""


if "output" not in st.session_state:
    st.session_state.output = ""

if "temperature" not in st.session_state:
    st.session_state.temperature = 0.05

with st.sidebar:

    st.write("### User")
    st.write(st.session_state.user.name)

    st.write("### Language")

    selected_language_name = st.selectbox("Select a language", options=st.session_state.languages,
                                          index=st.session_state.languages.index(st.session_state.language))
    if selected_language_name != st.session_state.language:
        st.session_state.language = selected_language_name

    st.write("### Model")
    selected_model_short_name = st.selectbox(
        "Select a model", options=[model.short_name for model in st.session_state.models], index=find_index_of_model_by_short_name(st.session_state.models, st.session_state.model.short_name))

    if selected_model_short_name != st.session_state.model.short_name:
        st.session_state.model = st.session_state.models[find_index_of_model_by_short_name(
            st.session_state.models, selected_model_short_name)]

    st.write("### Temperature")
    st.session_state.temperature = st.slider(
        "Select a temperature", min_value=0.0, max_value=1.0, value=st.session_state.temperature, step=0.01)

st.session_state.prompts = get_all_prompts_of_a_language(
    st.session_state.language)
selected_prompt_title = st.selectbox(
    "Select a prompt", options=[prompt.title for prompt in st.session_state.prompts], index=find_index_of_prompt_by_title(st.session_state.prompts, st.session_state.prompt.title))
if selected_prompt_title != st.session_state.prompt.title:
    st.session_state.prompt = st.session_state.prompts[find_index_of_prompt_by_title(
        st.session_state.prompts, selected_prompt_title)]

if st.session_state.prompt is not None:
    st.write(st.session_state.prompt.description)

tab1, tab2 = st.tabs(["Generate from Input", "Generate from Chat"])

with tab1:
   st.session_state.input_title = st.session_state.input_title_save

   input = f"# {st.session_state.input_title}\n\n{st.session_state.input}"
   title = st.session_state.input_title

with tab2:
    title = st.text_input("Title of your Input:")
    input = st.text_area("Your text Input:", height=120)

col1, dummy, col2, col3 = st.columns([2, 3, 3, 1])

if col1.button("Generate"):
    
    st.session_state.output = None
    ai_response = call_ai(
        st.session_state.model, st.session_state.prompt, input, st.session_state.temperature)
    st.session_state.output = f"# {title}\n\n{ai_response}"

if st.session_state.output is not None and len(st.session_state.output) > 5:
    if col2.button("Create Input form Output"):

        title1, text1 = get_title_and_text(st.session_state.output)

        session = next(get_db_session())

        new_input = create_input(
            user_id=st.session_state.user.id, title=title1, text=text1, session=session)

        st.session_state.input = new_input.text
        st.session_state.input_title = new_input.title
        st.session_state.input_id = new_input.id
        st.session_state.input_created_at = new_input.created_at

    with col3:
        st_copy_to_clipboard(st.session_state.output)

if st.session_state.output != "":
    st.write(st.session_state.output)
