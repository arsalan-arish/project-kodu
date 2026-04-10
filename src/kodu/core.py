from random import randint
from pathlib import Path
import json

CACHE_PATH = Path() / "cache"

def data_formatter(dataFile: Path, n: int, readFromCache: bool = False) -> dict:
    """
    Takes the txt file containing data, and the formatting number 'n' (based on n-gram) 
    and returns prediction_dict.
    """
    cachePath = CACHE_PATH / f"prediction_dict_{n}_gram.json"
    if readFromCache:
        prediction_dict = json.loads(cachePath.read_text())
        return prediction_dict

    words_list = dataFile.read_text().lower().split()

    pairs_list = []
    for i in range(len(words_list)):
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


def n_gram_predictor(context : str, prediction_dict : dict, n: int) -> str: # type: ignore pylance
    context = context.lower()
    if context not in prediction_dict:
        raise Exception("The context cannot be found in training data (prediction_dict)")
    
    r = randint(1, 100) / 100
    range_start = 0
    range_end = 0
    for prediction, weight in prediction_dict[context].items():
        range_end += weight
        if r > range_start and r < range_end:
            return prediction
        range_start += weight
        
    

def prompt_response_generator(prompt: str, responseLen: int) -> str:
    n = len(prompt.split()) + 1
    prediction_dict = data_formatter(Path('tests/sample_data.txt'), n, True)
    response = []

    #! Fix this SECTION
    for _ in range(responseLen):
        word = n_gram_predictor(prompt, prediction_dict, n)
        response.append(word)

    return " ".join(response)