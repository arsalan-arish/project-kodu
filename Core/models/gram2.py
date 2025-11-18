# This file will recieve prompt fetch data and from 2gram-data and use it to return predictions
from Core.labelled_data.gram2_data import prediction_dict
import random 

def predict(prompt : tuple):
    if prompt in prediction_dict:
        r = random.randint(1,100)
        tempdict = prediction_dict[prompt] 
        tempvar = 0
        for prediction ,constant in tempdict.items():
            constant *= 100
            if r < constant + tempvar and r > tempvar:
                return prediction 
            else:
                tempvar += constant 

    else:
        return "Prompt Undefined Error"


# always give lower case input no higher case
