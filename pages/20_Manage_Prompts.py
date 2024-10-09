# -*- coding: utf-8 -*-
import streamlit as st
import repository as repo
import helper_dlgs as dlgs
from models import Prompt
from helpers import Language
from ai_anthropic import translate_prompt
from repository import create_prompt
import crud_dialog

from helpers import Language, ensure_logged_in

ensure_logged_in()

class CrudDialog:

    dlg_title = "Prompt"

    # repo functions
    add_func = repo.create_empty_prompt
    read_all_func = repo.get_all_prompts
    transfer_to_one = repo.get_prompt_by_id
    read_one_func = repo.get_prompt_by_id
    delete_func = repo.delete_prompt
    save_func = repo.update_prompt
    

    def __init__(self, item: Prompt):
        self.item = item
        self.id = item.id
        self.title = item.title
        self.system_prompt = item.system_prompt
        self.description = item.description
        self.language_cd = item.language_cd
        self.extra_left = []
        self.extra_right = ["Translate"]
        self.func_left = []
        self.func_right = [self.translate]

    def translate(self):
        print("Attempting translation")
        self.save()
        if self.language_cd == 2:
            st.warning("This is already a prompt in German and can not be translated again")
            st.stop()
        
        tit, desc, txt = translate_prompt(self.title, self.description, self.system_prompt)
        print(tit)
        create_prompt(title=tit, system_prompt=txt, language_cd=2, description=desc)
        st.info(f"German Prompt created with Title: {tit}")
        


    def show_form(self):
    
        with st.form(key="form"):
            col1, col2 = st.columns([4, 1])
            self.title = col1.text_input("Title", value=self.title)
            self.language_cd = col2.number_input("Language (1 or 2)", value=self.language_cd)
            self.description = st.text_input("Description", value=self.description)
            self.system_prompt = st.text_area("Prompt", value=self.system_prompt, height=300)
            buttons =  dlgs.add_buttons(extra_left=self.extra_left, extra_right=self.extra_right)
    
        dlgs.handle_buttons(buttons, self, self.func_left, self.func_right)
    
    def save(self):
        return CrudDialog.save_func(self.id, title=self.title, system_prompt=self.system_prompt, description=self.description, language_cd=self.language_cd)

crud_dialog.show(CrudDialog)
