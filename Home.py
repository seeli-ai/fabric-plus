import streamlit as st
from repository import get_all_models, get_user_by_id, get_last_input_by_user_id, get_all_prompts_of_a_language, get_user_by_userid
from helpers import Language, find_index_of_model_by_short_name, find_index_of_prompt_by_title
from ai import call_ai
from models import Prompt, Model, User
from dotenv import load_dotenv
import hashlib


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user: User = get_user_by_userid(username)
        if user is None or user.is_active == False:
            st.error("Incorrect username or password")
            st.session_state.logged_in = False
            st.session_state.user = None
            st.stop()

        if user.password == hash_password(password):
            st.session_state.logged_in = True
            st.session_state.user = user
            st.success("Logged in successfully!")
            st.switch_page("Home.py")
        else:
            st.error("Incorrect username or password")
            st.session_state.logged_in = False
            st.session_state.user = None
            st.stop()


def main_app():

    # load_dotenv()

    st.session_state.models = get_all_models()
    st.session_state.prompts = get_all_prompts_of_a_language()
    st.session_state.languages = ["EN", "DE"]
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

    if "output" not in st.session_state:
        st.session_state.output = ""

    if "temperature" not in st.session_state:
        st.session_state.temperature = 0.05

    with st.sidebar:

        st.write("### User")
        st.write(st.session_state.user.name)

    st.write("# Your current Input:")
    st.write(f"### {st.session_state.input_title}")
    if "input_created_at" in st.session_state:
        st.write(
            f"Created at: {st.session_state.input_created_at.strftime('%d.%m.%Y %H:%M:%S')}")
    st.write(st.session_state.input)


if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
else:
    main_app()
