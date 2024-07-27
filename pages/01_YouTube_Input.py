import streamlit as st
from youtube import get_transcript

if "input" not in st.session_state:
    st.session_state.input = ""


url = st.text_input("Enter the video url here:")

if st.button("Get transcript"):
    transcript = get_transcript(url)

    if transcript:
        st.write(transcript)
        st.session_state.input = transcript

if st.button("Clear"):
    st.session_state.input = ""
