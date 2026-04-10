def main():
    from kodu import prompt_response_generator
    from random import randint

    #* Creating an interactive shell
    print("\n---------+++++++++++-------- WELCOME TO KODU! --------+++++++++++---------\n")
    print("- Give prompt and get responses\n- Enter q to exit\n- Enter r to set constant response length\nEnter c to set text color\n")
    responseLen = 0
    colors = {
        "red": 1,
        "green": 2,
        "yellow": 3,
        "blue": 4,
        "magenta": 5,
        "cyan": 6
    }
    color = colors.get("yellow")
    while True:
        x = input("-=-=-=> ")

        if x == "":
            continue

        elif x == "q":
            exit()

        elif x == "r":
            y = input("-=-=-=> Enter response length -> ")
            try:
                responseLen = int(y)
            except Exception:
                while True:
                    y = input("-=-=-=> Enter a valid int -> ")
                    try: responseLen = int(y)
                    except Exception: continue
            continue

        elif x == "c":
            y = input(f"{colors}\n\nEnter the color number you want -> ")
            try:
                color = int(y)
            except Exception:
                while True:
                    y = input("-=-=-=> Enter a valid int -> ")
                    try: color = int(y)
                    except Exception: continue
            continue

        print()
        res: str = prompt_response_generator(x, randint(16, 30) if not responseLen else responseLen)
        print(f"\033[3{color}m{res}\033[0m\n")
        