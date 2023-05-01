import openai

openai.api_key  = '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'


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.2,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


def user_question(question: str, word: str):
    prompt = f"""
        The user is trying to guess this word: '{word}'. Their question relating to the word 
        is the following delimited by ```.
        ```{question}```
        The response should be a statement, not a question. The response should NOT include the word '{word}'.
        """
    response = get_completion(prompt)
    return response
