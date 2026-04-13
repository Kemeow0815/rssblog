import requests

def markdown(path, locale=True):
    if locale:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        return requests.get(path).text
