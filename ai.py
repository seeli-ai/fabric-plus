# -*- coding: utf-8 -*-
import streamlit as st
from typing import Dict
from ai_anthropic import call_anthropics
from ai_openai import call_open_ai
from models import Prompt, Model
  

def format_memory(memory: Dict[str, str]) -> str:
    return "\n\n".join([f"{key}:\n{value}" for key, value in memory.items()])

def call_ai(model: Model, prompt: Prompt, input: str, temperature: float) -> str:
    
    system_prompt = prompt.system_prompt

    prompt_parts = system_prompt.split("<step>")
    if len(prompt_parts) == 1:
        current_prompt = system_prompt.strip()
        if current_prompt[-6:] != "INPUT:":
           current_prompt + "\n\n" + "# INPUT\n\nINPUT:"
        return call_ai_with_prompt(model, current_prompt, input, temperature)
    else:
        combined_respone = ""
        memory = {}
        total_steps = len(prompt_parts) - 1
        progress_bar = st.progress(0)
        status_text = st.empty()

        for i, part in enumerate(prompt_parts[1:], start=1):
            status_text.text(f"Processing step {i} of {total_steps}")
            temp = part.split("<include>")
            include = False
            if len(temp) > 1:
                part = temp[1]
                include = True
            current_prompt = (
                prompt_parts[0] + "\n\n" + 
                part + "\n\n" + 
                "# PREVIOUS OUTPUTS\n\n" + 
                format_memory(memory) + 
                "\n\n# INPUT\n\nINPUT:"
            )

            response = call_ai_with_prompt(model, current_prompt, input, temperature)
            combined_respone += response + "\n\n"
            if include:
                memory[f"STEP_{i}"] = response
            progress_bar.progress(i / total_steps)

        status_text.text("Processing complete!")    
        return combined_respone
        

def call_ai_with_prompt(model: Model, prompt: str, input: str, temperature: float) -> str:
    
    if model.provider.name == "OpenAI":
        return call_open_ai(model, prompt, input, temperature)
    
    if model.provider.name == "Anthropics":
        return call_anthropics(model, prompt, input, temperature)
    
    return "Provider not supported"

