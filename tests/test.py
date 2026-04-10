from kodu import prompt_response_generator
from random import randint

#* Creating an interactive shell
print("\n---------+++++++++++-------- WELCOME TO KODU! --------+++++++++++---------\n")
print("- Give prompt and get responses\n- Enter q to exit\n- Enter r to set constant response length\n")
responseLen = 0
while True:
    x = input("-=-=-=> ")

    if x == "q":
        exit()

    elif x == "r":
        y = input("-=-=-=> Enter response length -> ")
        try:
            responseLen = int(y)
        except Exception:
            y = input("-=-=-=> Enter a valid int -> ")
        continue

    print()
    res: str = prompt_response_generator(x, randint(10, 50) if not responseLen else responseLen)
    print(res, "\n")
    # Print this in color (better)