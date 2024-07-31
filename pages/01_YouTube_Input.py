# -*- coding: utf-8 -*-
import streamlit as st
from youtube import get_transcript
from repository import create_input
from helpers import Language

st.session_state.languages = list(Language)

if "input" not in st.session_state:
    st.session_state.input = ""

if "input_title" not in st.session_state:
    st.session_state.input_title = ""


if "language" not in st.session_state:
    st.session_state.language = Language.EN

with st.sidebar:

    st.write("### User")
    st.write(st.session_state.user.name)

    st.write("### Language")
    if st.session_state.language is None:
        st.session_state.language = Language.EN
    selected_language_name = st.selectbox("Select a language", options=[language.name for language in st.session_state.languages], index=st.session_state.languages.index(st.session_state.language))
    if selected_language_name != st.session_state.language.name:
        st.session_state.language = Language[selected_language_name]


url = st.text_input("Enter the video url here:")

if st.button("Get transcript"):
    titel, transcript = get_transcript(url, st.session_state.language.name.lower())

    if transcript:
        st.write(f"## {titel}")
        st.write(transcript)
        st.session_state.input = transcript

        create_input(st.session_state.user.id, titel, transcript)

if st.button("Clear"):
    st.session_state.input = ""
