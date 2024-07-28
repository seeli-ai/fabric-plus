from enum import Enum


class Language(Enum):
    EN = 1
    GE = 2


def find_index_of_model_by_short_name(models, short_name):
    for i, model in enumerate(models):
        if model.short_name == short_name:
            return i
    return None

def find_index_of_prompt_by_title(prompts, title):
    for i, model in enumerate(prompts):
        if model.title == title:
            return i
    return None
