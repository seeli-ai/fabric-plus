import streamlit as st
from pdf import convert_pdf_to_text

if "input" not in st.session_state:
    st.session_state.input = ""


name = st.text_input("Enter pdf file name:")

if st.button("Get transcript"):
    transcript = convert_pdf_to_text(name)

    if transcript:
        st.write(transcript)
        st.session_state.input = transcript

if st.button("Clear"):
    st.session_state.input = ""
