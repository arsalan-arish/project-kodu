import random

def n_gram_predictor(context : tuple, prediction_dict : dict):
    # always give lower case input no higher case
     
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

    pairs_list = []
    with open(training_data_txt,"r") as f:
        data : list = f.read().lower().split()
        for i in range(len(data)):
            templist = []
            templist.append(data[i:i+(n)])
            for element in templist:
                pairs_list.append(element)     

    # Sort all the pair_list(s) based on unique context. Store in a dictionary prediction_dict

    prediction_dict = {}
    for l in range(len(pairs_list)):
        current_pair_list_in_loop = pairs_list[l]
        context : tuple = tuple(current_pair_list_in_loop[:n-1])
        try:
            prediction : str = str(current_pair_list_in_loop[n-1])
        except Exception:
            pass
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


def prompt_response_generator(prompt:list, w:int, n:int, depth:int = 0):

    for i in range(len(prompt)):
        prompt[i] = prompt[i].lower()
    
    prediction_dict1 = data_formatter("sample-data.txt",n+1)
    response = []

    for i in range(w):
        ans1 = n_gram_predictor(tuple(prompt), prediction_dict1)
        if type(ans1) == str:
            if len(prompt) >= 10 and depth > 0:
                prompt.pop(0)
            prompt.append(ans1)
            response.append(ans1)
        elif ans1 == 204 and depth < n: # recursion
            if len(prompt) >= 1:
                if len(prompt) != 1:
                    prompt.pop(0)
                ans2 = prompt_response_generator(prompt, 1, len(prompt),depth+1)
                ans3 = ans2[0]
                if "\nThe prompt sequences and specifically the last word cannot be found in the training data" not in ans2:
                    prompt.append(ans3)
                    response.append(ans3)
                if "\nThe prompt sequences and specifically the last word cannot be found in the training data" in ans2 and "\nThe prompt sequences and specifically the last word cannot be found in the training data" not in response:
                    response.append("\nThe prompt sequences and specifically the last word cannot be found in the training data")
                    
        else:
            response.append("\nThe prompt sequences and specifically the last word cannot be found in the training data")
        
    if "\nThe prompt sequences and specifically the last word cannot be found in the training data" in response:
        response.remove("\nThe prompt sequences and specifically the last word cannot be found in the training data")
        response.append("\nThe prompt sequences and specifically the last word cannot be found in the training data")
            
    return response
