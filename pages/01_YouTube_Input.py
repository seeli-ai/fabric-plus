import streamlit as st
from youtube import get_transcript
from repository import create_input

if "input" not in st.session_state:
    st.session_state.input = ""

if "input_title" not in st.session_state:
    st.session_state.input_title = ""


url = st.text_input("Enter the video url here:")

if st.button("Get transcript"):
    titel, transcript = get_transcript(url)

    if transcript:
        st.write(f"## {titel}")
        st.write(transcript)
        st.session_state.input = transcript

        create_input(st.session_state.user.id, titel, transcript)

if st.button("Clear"):
    st.session_state.input = ""
