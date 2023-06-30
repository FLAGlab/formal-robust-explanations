import sys
import re
import csv
import line_operations as op


explanation_file_address = sys.argv[1]
instance_address = sys.argv[2] 
instance_name = sys.argv[3]
epsilon = sys.argv[4]
number_of_variables = int(sys.argv[5])
csv_file_address = sys.argv[6]+ "/results_"+ sys.argv[7] + "_" + str(epsilon) + ".csv"


def get_explanation(explanation_file_address):
    with open(explanation_file_address,"r") as file:
        lines = file.readlines()
        explanation = []
        for line in lines:
            explanation.append(line[0])
        return explanation

def get_inputs(instance_address, number_of_variables):
    inputs = []
    for i in range(number_of_variables):
         variable = "X_" + str(i)
         _, line, _ = op.find_line_upper_bound(instance_address, variable)
         list_of_numbers = re.findall(r"\-*\d+\.*\d*", line)
         input = list_of_numbers[1]
         inputs.append(input)
    return inputs

def get_action(instance_address):
    _, line, _ = op.find_line_with(instance_address, "; action chosen")
    action = re.findall(r"\d+", line)
    return action

# create a csv file with the following fields
# instance_number name input chosen action epsilon exp 

inputs = get_inputs(instance_address, number_of_variables)
action = get_action(instance_address)
explanation = get_explanation(explanation_file_address)
result_row = [instance_name] + inputs + action + [epsilon] + explanation

with open(csv_file_address, "a") as csvfile:
    print("the explanation is for " + instance_name + "is")
    print(explanation)
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(result_row)

