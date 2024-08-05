# -*- coding: utf-8 -*-
import streamlit as st
from youtube import get_transcript
from repository import create_input
from helpers import Language, ensure_logged_in

ensure_logged_in()

st.session_state.languages = ["EN", "DE"]

if "input" not in st.session_state:
    st.session_state.input = ""

if "input_title" not in st.session_state:
    st.session_state.input_title = ""


if "language" not in st.session_state:
    st.session_state.language = st.session_state.languages[0]

with st.sidebar:

    st.write("### User")
    st.write(st.session_state.user.name)

    st.write("### Language")
    selected_language_name = st.selectbox("Select a language", options=st.session_state.languages, index=st.session_state.languages.index(st.session_state.language))
    if selected_language_name != st.session_state.language:
        st.session_state.language = selected_language_name


url = st.text_input("Enter the video url here:")

if st.button("Get transcript"):
    titel, transcript = get_transcript(url, st.session_state.language.lower())

    if transcript:
        st.write(f"# {titel}")
        st.write(transcript)
        st.session_state.input = transcript

        new_input = create_input(st.session_state.user.id, titel, transcript)

        st.session_state.input = new_input.text
        st.session_state.input_title = new_input.title
        st.session_state.input_id = new_input.id   
        st.session_state.input_created_at = new_input.created_at


