# -*- coding: utf-8 -*-
import streamlit as st
from pdf import convert_pdf_to_markdown
from repository import create_input
from helpers import Language, ensure_logged_in, get_title_and_text
from repository import get_db_session


ensure_logged_in()

if "input" not in st.session_state:
    st.session_state.input = ""


file = st.file_uploader("Please choose a pdf-file", type="pdf")

if file is not None:
    name = file.name
    bytes_data = file.getvalue()

    markdown = convert_pdf_to_markdown(name, bytes_data)
    title, markdown = get_title_and_text(markdown)
    st.write(f"# {title}")
    st.write(markdown)

    session = next(get_db_session())

    new_input = create_input(
        user_id=st.session_state.user.id, title=title, text=markdown, session=session)

    st.session_state.input = markdown
    st.session_state.input_title = title
    st.session_state.input_id = new_input.id
    st.session_state.input_created_at = new_input.created_at
