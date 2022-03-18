import urllib.request
import json
import random
# https://dictionaryapi.dev/
DICTIONARY_API = 'https://api.dictionaryapi.dev/api/v2/entries/en/'

def get_word_definition(word):
    try:
        result = json.loads(urllib.request.urlopen(f'{DICTIONARY_API}{word}').read())
        meanings = result[0].get('meanings', [])
        definition=random.choice(_get_definitions_with_example(meanings))
        result_phrase=[f'{word.upper()}: {definition["definition"]}']
        if 'example' in definition:
            result_phrase+=[f'For example: "{definition["example"]}"']
        return result_phrase
    except Exception:
        return [f'Not sure what "{word}" means!']

def _get_definitions_with_example(meanings:list):
    defs_with_example=[]
    defs_without_example = []
    for m in meanings:
        for d in m.get('definitions',[]):
            if 'example' in d:
                defs_with_example.append(d)
            else:
                defs_without_example.append(d)
    if len(defs_with_example)>0:
        return defs_with_example
    else:
        return defs_without_example

#print(get_word_definition('diced'))
