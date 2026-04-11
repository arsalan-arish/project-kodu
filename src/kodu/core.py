from random import randint, choice
from pathlib import Path
import json
import traceback


def data_formatter(dataFile: Path, n: int, preferCache: bool = True) -> dict:
    """
    Takes the txt file containing data, and the formatting number 'n' (based on n-gram) 
    and returns prediction_dict.
    """
    cachePath = Path() / f"cache" / dataFile.name / f"prediction_dict_{n}_gram.json"
    if preferCache:
        try:
            prediction_dict = json.loads(cachePath.read_text())
            return prediction_dict
        except FileNotFoundError as e:
            pass

    words_list = dataFile.read_text().lower().split()

    pairs_list = []
    for i in range(len(words_list) - n - 1):
        pairs_list.append(words_list[i:i+n])

    prediction_dict = {}
    for pair_list in pairs_list:
        context: str = " ".join(pair_list[:-1])
        prediction: str = pair_list[-1]
        if context not in prediction_dict:
            prediction_dict[context] = {}
        if prediction not in prediction_dict[context]:
            prediction_dict[context][prediction] = 0
        prediction_dict[context][prediction] += 1

    for context in prediction_dict:
        totalSum = sum(prediction_dict[context].values())
        for prediction in prediction_dict[context]:
            prediction_dict[context][prediction] /= totalSum

    # Save the prediction_dict to cache (to instantly load next time if needed)
    cachePath.write_text(json.dumps(prediction_dict, sort_keys=True, indent=4))

    return prediction_dict


def n_gram_predictor(context: str, useFallBackAlgorithm: bool = True) -> str:
    context = context.lower()
    n = len(context.split()) + 1
    prediction_dict = data_formatter(Path('tests/sample_data.txt'), n)


    if context not in prediction_dict:
        if not useFallBackAlgorithm:
            raise Exception(f"\033[31mThe context\033[0m \033[36m'{context}'\033[0m \033[31mcannot be found in training data (prediction_dict)\nAnd useFallBackAlgorithm was set to False\033[0m")
        temp_context = context.split()
        if len(temp_context) == 1:
            raise Exception(f"\033[31mThe context\033[0m \033[36m'{context}'\033[0m \033[31mcannot be found in training data (prediction_dict)\033[0m")
        temp_context.pop(0)
        context = " ".join(temp_context)
        word = n_gram_predictor(context)
        return word 
    
    # First check if all the weights are exactly equal. If they are, then return a flat random choice
    weights: list = list(prediction_dict[context].values())
    firstWeight: float = weights[0]
    for weight in weights:
        if weight != firstWeight:
            return choice(list(prediction_dict[context].keys()))

    r = randint(1, 100) / 100
    range_start = 0
    range_end = 0
    for prediction, weight in prediction_dict[context].items():
        range_end += weight
        if r >= range_start and r <= range_end:
            return prediction
        range_start += weight


    raise Exception("\033[31mTHERE IS A SUBTLE BUG IN CORE PREDICTION ALGORITHM! lOOK\033[0m")
    

def prompt_response_generator(prompt: str, responseLen: int, contextCapacity: int = 5) -> str:
    if contextCapacity < 0 or contextCapacity > 10:
        #* INFO: A capacity of 10 has the range to create 2 - 11 grams prediction_dicts
        raise Exception("\033[31mPlease give a valid context capacity, preferred to be btw 1-10.\nElse too much memory and compute will be taken\nMore capacity leads to better precision though\033[0m")

    response = []
    for _ in range(responseLen):
        try:
            word = n_gram_predictor(prompt)
        except Exception as e:
            traceback.print_exc()
            print()
            print("\033[31mCOULD NOT GENERATE FULL RESPONSE\033[0m")
            break

        response.append(word)
        temp_prompt = prompt.split()
        temp_prompt.append(word)
        if len(temp_prompt) > contextCapacity:
            temp_prompt.pop(0)
        prompt = " ".join(temp_prompt)

    return " ".join(response)