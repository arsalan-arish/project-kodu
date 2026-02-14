from core import prompt_response_generator

x: list = prompt_response_generator("birds".split(), 1)
for word in x:
    print(word, end=" ")
