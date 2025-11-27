import functions as f

x = f.prompt_response_generator(["the"], 1)
for word in x:
    print(word, end=" ")
