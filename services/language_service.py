import json
from pathlib import Path
from locales import MESSAGES

language_file = Path(__file__).resolve().parent.parent / "languages.json"
default_language = "en"

def get_user_language(user_id:str) -> str:
    try:
        with open(language_file, 'r', encoding='utf-8') as file:
            content = json.load(file)
    except (FileNotFoundError,json.decoder.JSONDecodeError):
        return default_language

    return content.get(user_id, default_language)

def set_user_language(user_id:str, language:str) -> None:
    data = {}
    try:
        with open(language_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except (FileNotFoundError,json.decoder.JSONDecodeError):
        data = {}

    data[str(user_id)] = language

    with open(language_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def get_message(key:str, user_id:str, **kwargs) -> str:
    language = get_user_language(user_id)
    template = MESSAGES[key][language]
    return template.format(**kwargs)

if __name__ == "__main__":
    set_user_language('test_id', 'fa')
    print(get_user_language('test_id'))