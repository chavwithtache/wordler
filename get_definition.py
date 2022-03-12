import urllib.request
import json
# https://dictionaryapi.dev/
DICTIONARY_API = 'https://api.dictionaryapi.dev/api/v2/entries/en/'

def get_word_definition(word):
    result = json.loads(urllib.request.urlopen(f'{DICTIONARY_API}{word}').read())
    meanings = result[0].get('meanings', [])
    for part_of_speech in ['interjection','noun','verb','adjective','adverb']:
        meaning = _get_meaning(meanings, part_of_speech)
        if meaning is not None:
            break
    if meaning is None:
        return [f'Not sure what "{word}" means!']
    else:
        definition = meaning['definitions'][0]
        result_phrase=[f'{word.upper()}: {definition["definition"]}']
        if 'example' in definition:
            result_phrase+=[f'For example: "{definition["example"]}"']
        return result_phrase

def _get_meaning(meanings:list, part_of_speech:str):
    results = [m for m in meanings if m['partOfSpeech'] == part_of_speech]
    if len(results) > 0:
        return results[0]
