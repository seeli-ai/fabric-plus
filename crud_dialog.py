import streamlit as st
import helper_dlgs as dlgs

def show(repo_class):

    dlgs.manage_state()

    st.title(repo_class.dlg_title)
    
    item = dlgs.select_item_to_edit(repo_class)

    repo_class(item).show_form()
