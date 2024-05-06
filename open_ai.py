import openai
import re

# DON'T CHECK THIS IN!!
openai.api_key = '***'


def define_word(word):
    result = get_completion(f'Define the word "{word}" in less than 30 words', source="definitions")
    return result


def get_completion(prompt, model="gpt-3.5-turbo", source="clues"):
    messages = [{"role": "user", "content": prompt}]
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0.2,  # this is the degree of randomness of the model's output
        )
    except Exception:
        return f"Having some technical issues. You'll have to do without {source} for now!"
    return response.choices[0].message["content"]


def user_question(question: str, word: str):
    prompt = f"""
        The user is trying to guess this word: '{word}'. Their question relating to the word
        is the following delimited by ```.
        ```{question}```
        The response should be a statement not a question.
        """
    response = get_completion(prompt)
    response = re.sub(word, '*' * len(word), response, flags=re.IGNORECASE)
    return response
