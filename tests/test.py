from ..src.core import prompt_response_generator

x = prompt_response_generator("workshop taught a warm-up for help".split(), 1, 10)
for word in x:
    print(word, end=" ")



# print("\n\n            Hi welcome to kodu!             ")
# n = int(input("Set context length (recommended is 10) --> "))
# w = int(input("Enter the number of words of output response you want --> "))

# while True:
#     prompt = input("\n\nEnter your prompt (words separated by space properly)-->").split()
#     while len(prompt) >= 10:
#         prompt = input("Please enter a prompt under 10 words --> ").split()

#     response = prompt_response_generator(prompt, w, n)
#     print("\n\n\n")
#     for word in response:
#         print(word, end=" ")