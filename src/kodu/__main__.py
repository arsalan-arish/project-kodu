def main():
    from kodu import prompt_response_generator
    from random import randint
    from sys import argv

    argv.pop(0)
    match len(argv):
        case 0:
            print("Quick Help commands list will be coming soon!")
            exit()
        case 1:
            if argv[0] == "run":
                pass # Lauch shell below
            else:
                print("Please give a vaild command to kodu!")
                exit()

    #* Creating an interactive shell
    print("\n---------+++++++++++-------- WELCOME TO KODU! --------+++++++++++---------\n")
    print("- Give prompt and get responses\n- Enter q to exit\n- Enter r to set constant response length\n- Enter c to set text color\n")
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
        response: str = prompt_response_generator(x, randint(30, 50) if not responseLen else responseLen)
        print(f"\033[3{color}m{response}\033[0m\n")