import re

def find_line_with(file_address, regular_expression):
    with open(file_address,"r") as forward_file:
        lines = forward_file.readlines()
        for line in lines:
            if re.findall(regular_expression,line) != []:
                return lines.index(line), line, lines

def find_line_upper_bound(property_address, variable):
    regular_expression = "<=" + " " + variable 
    with open(property_address,"r") as file_object:
        lines = file_object.readlines()
        for line in lines:
            if re.findall(regular_expression,line) != []:
                return lines.index(line), line, lines

def find_line_lower_bound(property_address, variable):
    regular_expression = ">=" + " " + variable 
    with open(property_address,"r") as file_object:
        lines = file_object.readlines()
        for line in lines:
            if re.findall(regular_expression,line) != []:
                return lines.index(line), line, lines 

def erase_lines_after(address, index):
    with open(address,"r") as file:
        lines = file.readlines()
        #truncate the list after index-1
        lines = lines[0:index-1]
        with open(address,"w") as file:
            file.writelines(lines)

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
         _, line, _ = find_line_upper_bound(instance_address, variable)
         list_of_numbers = re.findall(r"\-*\d+\.*\d*", line)
         input = list_of_numbers[1]
         inputs.append(input)
    return inputs

def get_action(instance_address):
    _, line, _ = find_line_with(instance_address, "; action chosen")
    action = re.findall(r"\d+", line)
    return action