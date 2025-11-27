import random

def n_gram_predictor(context : tuple, prediction_dict : dict):
    # always give lower case input no higher case
    n = len(context)+1
     
    if context in prediction_dict:
        r = random.randint(1,100)
        tempdict = prediction_dict[context]
        tempvar = 0
        for prediction ,constant in tempdict.items():
            constant *= 100
            if r < constant + tempvar and r > tempvar:
                return prediction # str
            else:
                tempvar += constant 

    else:
        return 204 # Error
    

def data_formatter(training_data_txt, n):

    # Put the txt document into a dictionary "lines" which contains each line index and its content
    # Training_data_txt should be formatted as proper spaces between words and a line space after each sentence only.
    lines = {}
    with open(training_data_txt,"r") as f:
        data : list = f.read().lower().split("\n")
        for i, line in enumerate(data):
            lines[f"line{i}"] = line

    # Divide the lines dictionary into pairs_list containing all pair_list(s) of all words throughout the document

    tokenized_line = []
    pairs_list = []

    for j in range(len(lines)):
        tokenized_line = lines[f"line{j}"].split()
        if len(tokenized_line) >= n:
            templist = []
            for k in range(len(tokenized_line)):
                if k < len(tokenized_line) - (n-1):
                    templist.append(tokenized_line[k:(k+n)])
            for pair_list in templist:
                pairs_list.append(pair_list)

    # Sort all the pair_list(s) based on unique context. Store in a dictionary prediction_dict

    prediction_dict = {}
    for l in range(len(pairs_list)):
        current_pair_list_in_loop = pairs_list[l]
        context : tuple = tuple(current_pair_list_in_loop[:n-1])
        prediction : str = str(current_pair_list_in_loop[n-1])
        if context not in prediction_dict:
            prediction_dict[context] = {prediction : 1}
        elif context in prediction_dict:
            if prediction in prediction_dict[context]:
                prediction_dict[context][prediction] += 1
            elif prediction not in prediction_dict[context]:
                prediction_dict[context][prediction] = 1


    # Assign probability constants instead of number of repetition

    for context in prediction_dict:
        tempdict = prediction_dict[context]
        sum = 0
        for prediction in tempdict:
            sum += tempdict[prediction]
        for prediction in tempdict:
            tempdict[prediction] /= sum

    # The final format of data is a dictionary prediction_dict where every key is a unique context sequence and 
    # every value is a dictionary of possible predictions for that context sequence along 
    # with their probability constants
    return prediction_dict


def prompt_response_generator(prompt : list, w : int):
    for i in range(len(prompt)):
        prompt[i] = prompt[i].lower()
    n = len(prompt)
    prediction_dict1 = data_formatter("sample-data.txt", n+1)
    response = []

    for i in range(w):
        ans1 = n_gram_predictor(tuple(prompt), prediction_dict1) # str (prediction) OR int (204)
        if type(ans1) == str:
            response.append(ans1)
            prompt.pop(0)
            prompt.append(ans1)
        elif type(ans1) == int: # 204 Error
            # We will remove one word from 0th index of prompt and then feed the prompt again to this function with
            # w = 1. This will return a one string list but we want extract the string from the list and then append the string to the
            # response list. We will the append the string to the prompt as well
            if len(prompt) > 1:
                prompt.pop(0)
                ans2 : list = prompt_response_generator(prompt, 1)
                ans3 : str  = ans2[0]
                response.append(ans3)
                prompt.append(ans3)
            else:
                response.append("\nThe prompt and specifically the last word cannot be found in the training data")
                break

    return response # list