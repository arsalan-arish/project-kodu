# Variables Declaration
n = 2 
data = 0
lines = {}
tokenized_line = []
pair_list = []
pairs_list = []
# pair_list_context = []
# pair_list_prediction = []
prediction_dict = {}



# Put the txt document into a dictionary "lines" which contains each line index and its content

with open("sample-data.txt","r") as f:
    data = f.read().lower().split("\n")
    lines = {}
    for i, line in enumerate(data):
        lines[f"line{i}"] = line

# Divide the lines dictionary into pairs_list containing all pair_list(s) of all words throughout the document

pairs_list = []
for j in range(len(lines)):
    if len(tokenized_line := lines[f"line{j}"].split(" ")) >= n:
        templist = []
        for k in range(len(tokenized_line)):
            if k < len(tokenized_line) - 1:
                templist.append([tokenized_line[k], tokenized_line[k+1]])
        for pair_list in templist:
            pairs_list.append(pair_list)

# Sort all the pair_list(s) based on unique string at index 0 of each pair_list. Store in a dictionary

for l in range(len(pairs_list)):
    if pairs_list[l][0] not in prediction_dict:
        prediction_dict[pairs_list[l][0]] = {f"{pairs_list[l][1]}" : 1}
    elif pairs_list[l][0] in prediction_dict:
        if pairs_list[l][1] in prediction_dict[pairs_list[l][0]]:
            prediction_dict[pairs_list[l][0]][pairs_list[l][1]] += 1
        elif pairs_list[l][1] not in prediction_dict[pairs_list[l][0]]:
            prediction_dict[pairs_list[l][0]][pairs_list[l][1]] = 1


# Assign probability constants instead of number of repetition

for key1 in prediction_dict:
    temp = prediction_dict[key1]
    sum = 0
    for key2 in temp:
        sum += temp[key2]
    for key2 in temp:
        temp[key2] = temp[key2]/sum
    

# The final format of data is a dictionary prediction_dict where every key is a unique context sequence and 
# every value isa dictionary of possible predictions for that context sequence along 
# with their probability constants