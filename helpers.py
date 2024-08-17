from enum import Enum
import streamlit as st


class Language(Enum):
    EN = 1
    DE = 2


def find_index_of_model_by_short_name(models, short_name):
    for i, model in enumerate(models):
        if model.short_name == short_name:
            return i
    return 0


def find_index_of_prompt_by_title(prompts, title):
    for i, model in enumerate(prompts):
        if model.title == title:
            return i
    return 0


def ensure_logged_in():
    if 'logged_in' not in st.session_state:
        st.switch_page("Home.py")
        st.stop()
    if not st.session_state.logged_in:
        st.switch_page("Home.py")
        st.stop()


def get_title_and_text(markdown: str):
    split_markdown = markdown.split("\n")
    title = split_markdown[0]
    length_of_title = len(title)
    markdown = markdown[length_of_title + 1:]
    title = title.replace("#", "").strip()
    return title, markdown
