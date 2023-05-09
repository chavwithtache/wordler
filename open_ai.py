import openai
import re

openai.api_key = ''


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0.2,  # this is the degree of randomness of the model's output
        )
    except Exception as e:
        return "Having some technical issues. You'll have to do without clues for now!"
    return response.choices[0].message["content"]


def user_question(question: str, word: str):
    prompt = f"""
        The user is trying to guess this word: '{word}'. Their question relating to the word 
        is the following delimited by ```.
        ```{question}```
        The response should be a statement, not a question.
        """

    response = get_completion(prompt)
    response = re.sub(word, '*' * len(word), response, flags=re.IGNORECASE)
    return response
