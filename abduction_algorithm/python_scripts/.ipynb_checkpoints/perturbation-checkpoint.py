import re

def perturbation_upper_bound(upper_bound_assertion, epsilon):
    #extract all integers or decimals from a string
    list_of_numbers = re.findall(r"\-*\d+\.*\d*", upper_bound_assertion)
    #The first extracted substring is the variable subscript
    variable_num = list_of_numbers[0]
    #the second extracted substring is the bound
    bound =  list_of_numbers[1] 
    #convert string to float and perturb it
    bound = float(bound) + epsilon
    #convert float to string
    #round to 20 decimal positions
    bound = f"{bound: .20f}"
    #create the new assertion 
    new_assertion = "(assert (<= X_" + variable_num + " " + bound +"))"
    return new_assertion


def perturbation_lower_bound(lower_bound_assertion, epsilon):
    #extract all integers or decimal from a string
    list_of_numbers = re.findall(r"\-*\d+\.*\d*", lower_bound_assertion)
    #the first extracted substring is the variable subscript
    variable_num = list_of_numbers[0]
    #the second extracted substring is the bound
    bound = list_of_numbers[1]
    #convert the bound string to float and perturb it
    bound = float(bound) - epsilon
    #convert float to string
    #round to 20 decimal positions
    bound = f"{bound: .20f}"
    #create the new assertion
    new_assertion = "(assert (>= X_" + variable_num + " " + bound +"))"
    return new_assertion



