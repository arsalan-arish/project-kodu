import random
from pathlib import Path
import json
from copy import copy, deepcopy

def data_formatter(p: Path, n: int, readfromCache: bool = False) -> dict:
    """Takes the txt file and the formatting number 'n' (based on n-gram) and returns prediction_dict"""
    if readfromCache:
        p = Path.cwd() / "cache" / f"prediction_dict_{n}_gram"
        prediction_dict = json.loads(p.read_text())
        return prediction_dict

    words_list = list(p.read_text().lower().split())

    pairs_list = list()
    for i in range(len(words_list)):
        pairs_list.append(words_list[i:i+n])

    prediction_dict = dict()
    for pair_list in pairs_list:
        context: list = pair_list[:-1]
        prediction: str = pair_list[-1]
        if not context in prediction_dict:
            prediction_dict[context] = dict()
        if not prediction in prediction_dict[context]:
            prediction_dict[context][prediction] = 0
        prediction_dict[context][prediction] += 1

    for context in prediction_dict:
        totalSum = sum(prediction_dict[context].values())
        for prediction in prediction_dict[context]:
            prediction_dict[context][prediction] /= totalSum

    p = Path.cwd() / "cache" / f"prediction_dict_{n}_gram"
    p.write_text(json.dumps(prediction_dict))

    return prediction_dict


def n_gram_predictor(context : list, prediction_dict : dict, n: int): # n means n-gram
    assert len(context) == n-1
    for i in range(len(context)):
        context[i] = context[i].lower()

    if context in prediction_dict:
        r = random.randint(1,100) / 100
        temp = 0 # Store value for the previous constant in the below loop
        for prediction, constant in prediction_dict[context].items():
            if r > temp and r < constant:
                return prediction
            temp = copy(constant)
    else:
        raise Exception("The context cannot be found in training data (prediction_dict)")
    

def prompt_response_generator(prompt: list) -> list:
    pass

# def prompt_response_generator(prompt: list, w: int, n: int, depth: int = 0):

#     for i in range(len(prompt)):
#         prompt[i] = prompt[i].lower()
    
#     prediction_dict1 = data_formatter(Path("sample-data.txt"),n+1)
#     response = []

#     for i in range(w):
#         ans1 = n_gram_predictor(tuple(prompt), prediction_dict1)
#         if type(ans1) == str:
#             if len(prompt) >= 10 and depth > 0:
#                 prompt.pop(0)
#             prompt.append(ans1)
#             response.append(ans1)
#         elif ans1 == 204 and depth < n: # recursion
#             if len(prompt) >= 1:
#                 if len(prompt) != 1:
#                     prompt.pop(0)
#                 ans2 = prompt_response_generator(prompt, 1, len(prompt),depth+1)
#                 ans3 = ans2[0]
#                 if "\nThe prompt sequences and specifically the last word cannot be found in the training data" not in ans2:
#                     prompt.append(ans3)
#                     response.append(ans3)
#                 if "\nThe prompt sequences and specifically the last word cannot be found in the training data" in ans2 and "\nThe prompt sequences and specifically the last word cannot be found in the training data" not in response:
#                     response.append("\nThe prompt sequences and specifically the last word cannot be found in the training data")
                    
#         else:
#             response.append("\nThe prompt sequences and specifically the last word cannot be found in the training data")
        
#     if "\nThe prompt sequences and specifically the last word cannot be found in the training data" in response:
#         response.remove("\nThe prompt sequences and specifically the last word cannot be found in the training data")
#         response.append("\nThe prompt sequences and specifically the last word cannot be found in the training data")
            
#     return response
