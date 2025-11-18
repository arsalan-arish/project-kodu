# Variables Declaration


n = 5  # Diff constant
data = 0
lines = {}
tokenized_line = []
pair_list = []
pairs_list = []
prediction_dict = {}
txtfile="sample-data.txt"


# Put the txt document into a dictionary "lines" which contains each line index and its content

with open(txtfile,"r") as f:
    data = f.read().lower().split("\n")
    lines = {}
    for i, line in enumerate(data):
        lines[f"line{i}"] = line

# Divide the lines dictionary into pairs_list containing all pair_list(s) of all words throughout the document

pairs_list = []
for j in range(len(lines)):
    tokenized_line = lines[f"line{j}"].split(" ")
    if len(tokenized_line) >= n:
        templist = []
        for k in range(len(tokenized_line)):
            if k < len(tokenized_line) - n-1:
                templist.append(tokenized_line[k:k+n]) 
        for pair_list in templist:
            pairs_list.append(pair_list)

# Sort all the pair_list(s) based on unique context. Store in a dictionary

for l in range(len(pairs_list)):
    context : tuple = tuple(pairs_list[l][:n-1])
    prediction : str = pairs_list[l][n-1]
    if context not in prediction_dict:
        prediction_dict[context] = {prediction : 1}
    elif context in prediction_dict:
        if prediction in prediction_dict[context]:
            prediction_dict[context][prediction] += 1
        elif prediction not in prediction_dict[context]:
            prediction_dict[context][prediction] = 1


# Assign probability constants instead of number of repetition

for context in prediction_dict:
    temp = prediction_dict[context]
    sum = 0
    for prediction in prediction_dict[context]:
        sum += prediction_dict[context][prediction]
    for prediction in prediction_dict[context]:
        prediction_dict[context][prediction] /= sum

# The final format of data is a dictionary prediction_dict where every key is a unique context sequence and 
# every value is a dictionary of possible predictions for that context sequence along 
# with their probability constants