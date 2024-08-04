from models import Base, User, Prompt, Parameter, Model, Provider, Input
from sqlalchemy.orm import Session
from typing import List
from connect_db import engine
from datetime import datetime
import streamlit as st

session = Session(bind=engine)

# User

# Read


def get_user_by_id(user_id: int) -> User:
    return session.query(User).filter(User.id == user_id).first()


def get_user_by_userid(userid: str) -> User:
    return session.query(User).filter(User.userid == userid).first()


def get_all_users() -> List[User]:
    return session.query(User).all()

# Create


def create_user(userid: str, name: str, password: str, is_active: bool = True) -> User:
    new_user = User(userid=userid, name=name,
                    password=password, is_active=is_active)
    session.add(new_user)
    session.commit()
    return new_user

# Update


def update_user(user_id: int, **kwargs) -> User:
    user = get_user_by_id(user_id)
    for key, value in kwargs.items():
        setattr(user, key, value)
    session.commit()
    return user

# Delete


def delete_user(user_id: int) -> User:
    user = get_user_by_id(user_id)
    session.delete(user)
    session.commit()
    return user

# Prompts

# Read


def get_prompt_by_id(prompt_id: int) -> Prompt:
    return session.query(Prompt).filter(Prompt.id == prompt_id).first()

def get_all_prompts() -> List[Prompt]:
    return session.query(Prompt).order_by(Prompt.title).all()

def get_all_prompts_of_a_language(language_cd: int = 1) -> List[Prompt]:
    return session.query(Prompt).filter(Prompt.language_cd == language_cd).order_by(Prompt.title).all()


def get_prompt_by_title(title: str) -> Prompt:
    return session.query(Prompt).filter(Prompt.title == title).first()

# Create


def create_prompt(title: str, system_prompt: str, language_cd : int = 1, user_prompt: str = None, description: str = None) -> Prompt:
    print(f"Creating prompt with title: {title} and language_cd: {language_cd}")
    new_prompt = Prompt(title=title, system_prompt=system_prompt, language_cd = language_cd,
                         user_prompt=user_prompt, description=description)
    session.add(new_prompt)
    session.commit()
    return new_prompt

def create_empty_prompt(id = None) -> Prompt:
    title = "New Prompt"
    system_prompt = "New Prompt"
    language_cd = 1
    description = "New Prompt"
    new_prompt = Prompt(title=title, system_prompt=system_prompt, language_cd = language_cd,
                         description=description)
    session.add(new_prompt)
    session.commit()
    return new_prompt

# Update


def update_prompt(prompt_id: int, **kwargs) -> Prompt:
    prompt = get_prompt_by_id(prompt_id)
    for key, value in kwargs.items():
        setattr(prompt, key, value)
    session.commit()
    return prompt

# Delete


def delete_prompt(prompt_id: int) -> Prompt:
    prompt = get_prompt_by_id(prompt_id)
    session.delete(prompt)
    session.commit()
    return prompt

# Parameters

# Read


def get_parameter_by_id(parameter_id: int) -> Parameter:
    return session.query(Parameter).filter(Parameter.id == parameter_id).first()


def get_all_parameters() -> List[Parameter]:
    return session.query(Parameter).all()


def get_parameters_by_prompt_id(prompt_id: int) -> List[Parameter]:
    return session.query(Parameter).filter(Parameter.prompt_id == prompt_id).all()

# Create


def create_parameter(name: str, type: int, prompt_id: int) -> Parameter:
    new_parameter = Parameter(name=name, type=type, prompt_id=prompt_id)
    session.add(new_parameter)
    session.commit()
    return new_parameter

# Update


def update_parameter(parameter_id: int, **kwargs) -> Parameter:
    parameter = get_parameter_by_id(parameter_id)
    for key, value in kwargs.items():
        setattr(parameter, key, value)
    session.commit()
    return parameter

# Delete


def delete_parameter(parameter_id: int) -> Parameter:
    parameter = get_parameter_by_id(parameter_id)
    session.delete(parameter)
    session.commit()
    return parameter

# Models

# Read


def get_model_by_id(model_id: int) -> Model:
    return session.query(Model).filter(Model.id == model_id).first()


def get_all_models() -> List[Model]:
    return session.query(Model).all()


def get_models_by_provider_id(provider_id: int) -> List[Model]:
    return session.query(Model).filter(Model.provider_id == provider_id).all()

# Create


def create_model(name: str, provider_id: int) -> Model:
    new_model = Model(name=name, provider_id=provider_id)
    session.add(new_model)
    session.commit()
    return new_model

# Update


def update_model(model_id: int, **kwargs) -> Model:
    model = get_model_by_id(model_id)
    for key, value in kwargs.items():
        setattr(model, key, value)
    session.commit
    return model

# Delete


def delete_model(model_id: int) -> Model:
    model = get_model_by_id(model_id)
    session.delete(model)
    session.commit()
    return model

# Provider

# Read


def get_provider_by_id(provider_id: int) -> Provider:
    return session.query(Provider).filter(Provider.id == provider_id).first()


def get_provider_by_name(name: str) -> Provider:
    return session.query(Provider).filter(Provider.name == name).first()


def get_all_providers() -> List[Provider]:
    return session.query(Provider).all()

# Create


def create_provider(name: str) -> Provider:
    new_provider = Provider(name=name)
    session.add(new_provider)
    session.commit()
    return new_provider

# Update


def update_provider(provider_id: int, **kwargs) -> Provider:
    provider = get_provider_by_id(provider_id)
    for key, value in kwargs.items():
        setattr(provider, key, value)
    session.commit()
    return provider

# Delete


def delete_provider(provider_id: int) -> Provider:
    provider = get_provider_by_id(provider_id)
    session.delete(provider)
    session.commit()
    return provider

# Input

# Read

def get_input_by_id(input_id: int) -> Input:
    return session.query(Input).filter(Input.id == input_id).first()

def get_all_inputs() -> List[Input]:
    return session.query(Input).all()

def get_inputs_by_user_id(user_id: int = 0) -> List[Input]:
    if user_id == 0:
        if "user" not in st.session_state:
            st.warning("Missing user information")
            st.stop()
        user_id = st.session_state.user.id
    return session.query(Input).filter(Input.user_id == user_id).order_by(Input.created_at.desc()).all()

def get_last_input_by_user_id(user_id: int) -> Input:
    return session.query(Input).filter(Input.user_id == user_id).order_by(Input.created_at.desc()).first()

# Create    

def create_input(user_id: int, titel: str, text: str) -> Input:
    new_input = Input(user_id=user_id, title=titel, text=text)
    session.add(new_input)
    session.commit()
    return new_input

def create_empty_input(id: int = 0) -> Input:
    if "user" not in st.session_state:
        st.warning("Missing user information")
        st.stop()
    new_input = Input(user_id=st.session_state.user.id, title="New Input-Text", text="New Input-Text")
    session.add(new_input)
    session.commit()
    return new_input

# Update

def update_input(input_id: int, **kwargs) -> Input:
    input = get_input_by_id(input_id)
    for key, value in kwargs.items():
        setattr(input, key, value)
    session.commit()
    return input

# Delete

def delete_input(input_id: int) -> Input:
    input = get_input_by_id(input_id)
    session.delete(input)
    session.commit()
    return input