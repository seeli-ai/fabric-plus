# -*- coding: utf-8 -*-
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Text
from datetime import datetime, date
from typing import Any, List


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column('id', primary_key=True, autoincrement=True)
    userid: Mapped[str]
    name: Mapped[str] = mapped_column(nullable=True)
    password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    inputs: Mapped[List['Input']] = relationship(
        'Input', back_populates='user', foreign_keys='Input.user_id')

    def __repr__(self):
        return f'<User(name={self.userid}, fullname={self.name}, password={self.password})>'


class Prompt(Base):
    __tablename__ = 'prompts'

    id: Mapped[int] = mapped_column('id', primary_key=True, autoincrement=True)
    title: Mapped[str]
    system_prompt: Mapped[str] = mapped_column(Text)
    user_prompt: Mapped[str] = mapped_column(Text, nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    language_cd: Mapped[int] = mapped_column(default=1)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    parameters: Mapped[List['Parameter']] = relationship(
        'Parameter', back_populates='prompt', foreign_keys='Parameter.prompt_id')

    def __repr__(self):
        return f'<Prompt(prompt={self.title}, created_at={self.created_at})>'
    
    def __str__(self) -> str:
        if self.language_cd == 2:
           return self.title + " (DE)"
        return self.title + " (EN)"


class Parameter(Base):
    __tablename__ = 'parameters'

    id: Mapped[int] = mapped_column('id', primary_key=True, autoincrement=True)
    name: Mapped[str]
    type: Mapped[int]
    prompt_id: Mapped[int] = mapped_column(
        'prompt_id', ForeignKey('prompts.id'))
    prompt: Mapped[Prompt] = relationship(
        'Prompt', back_populates='parameters')

    def __repr__(self):
        return f'<Parameter(name={self.name}, value={self.value})>'


class Model(Base):
    __tablename__ = 'models'

    id: Mapped[int] = mapped_column('id', primary_key=True, autoincrement=True)
    short_name: Mapped[str]
    name: Mapped[str]
    provider_id: Mapped[int] = mapped_column(ForeignKey('providers.id'))
    provider: Mapped['Provider'] = relationship(
        'Provider', back_populates='models')

    def __repr__(self):
        return f'{self.short_name}'


class Provider(Base):
    __tablename__ = 'providers'

    id: Mapped[int] = mapped_column('id', primary_key=True, autoincrement=True)
    name: Mapped[str]
    models: Mapped[List['Model']] = relationship(
        'Model', back_populates='provider', foreign_keys='Model.provider_id')

    def __repr__(self):
        return f'<Provider(name={self.name})>'
    

class Input(Base):
    __tablename__ = 'inputs'

    id: Mapped[int] = mapped_column('id', primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=True)
    text: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship(
        'User', back_populates='inputs')

    def __repr__(self):
        return f'{self.title}'
    
    def __str__(self):
        return f'{self.title} --- {self.created_at.strftime("%d.%m.%Y %H:%M:%S")}'
