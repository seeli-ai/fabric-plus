# -*- coding: utf-8 -*-
import streamlit as st
from pdf import convert_pdf_to_markdown


if "input" not in st.session_state:
    st.session_state.input = ""


file = st.file_uploader("Please choose a pdf-file", type="pdf") 

if file is not None:
    name = file.name
    bytes_data = file.getvalue() 

    markdown = convert_pdf_to_markdown(bytes_data)
    st.write(markdown)
    st.session_state.input = markdown

if st.button("Clear"):
    st.session_state.input = ""
