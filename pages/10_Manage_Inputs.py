# -*- coding: utf-8 -*-
import streamlit as st
import repository as repo
import helper_dlgs as dlgs
from models import Prompt
from helpers import Language
from ai import translate_prompt
import crud_dialog

from helpers import Language, ensure_logged_in

ensure_logged_in()

class CrudDialog:

    dlg_title = "Your Inputs"

    # repo functions
    add_func = repo.create_empty_input
    read_all_func = repo.get_inputs_by_user_id
    transfer_to_one = repo.get_input_by_id
    read_one_func = repo.get_input_by_id
    delete_func = repo.delete_input
    save_func = repo.update_input
    

    def __init__(self, item: Prompt):
        self.item = item
        self.id = item.id
        self.title = item.title
        self.text = item.text
        self.created_at = item.created_at
        self.extra_left = []
        self.extra_right = ["Set as Current"]
        self.func_left = []
        self.func_right = [self.set_as_current]

    def set_as_current(self):
        st.session_state.input = self.text
        st.session_state.input_title = self.title
        st.session_state.input_id = self.id   
        st.session_state.input_created_at = self.created_at
        st.info(f"{self.title} set as current input")
        


    def show_form(self):
    
        with st.form(key="form"):
            self.title = st.text_input("Title", value=self.title)
            st.write(f"Created at: {self.created_at.strftime('%d.%m.%Y %H:%M:%S')}")
            self.text = st.text_area("Input Text", value=self.text, height=300)
            buttons =  dlgs.add_buttons(extra_left=self.extra_left, extra_right=self.extra_right)
    
        dlgs.handle_buttons(buttons, self, self.func_left, self.func_right)
    
    def save(self):
        return CrudDialog.save_func(self.id, title=self.title, text=self.text)

crud_dialog.show(CrudDialog)
