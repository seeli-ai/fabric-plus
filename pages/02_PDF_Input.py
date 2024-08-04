# -*- coding: utf-8 -*-
import streamlit as st
from pdf import convert_pdf_to_markdown
from repository import create_input


if "input" not in st.session_state:
    st.session_state.input = ""


file = st.file_uploader("Please choose a pdf-file", type="pdf") 

if file is not None:
    name = file.name
    bytes_data = file.getvalue() 

    markdown = convert_pdf_to_markdown(bytes_data)
    split_markdown = markdown.split("\n")
    title = split_markdown[0]
    length_of_title = len(title)
    markdown = markdown[length_of_title + 1:]
    title = title.replace("#", "").strip()
    st.write(f"# {title}")
    st.write(markdown)

    new_input = create_input(user_id=st.session_state.user.id, title=title, text=markdown)

    st.session_state.input = new_input.text
    st.session_state.input_title = new_input.title
    st.session_state.input_id = new_input.id   
    st.session_state.input_created_at = new_input.created_at

