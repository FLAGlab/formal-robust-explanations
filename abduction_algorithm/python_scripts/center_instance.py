import sys
import re
import line_operations as op
import sys

#sys.arg[1] instance address
#sys.argv[2] total number of variables

instance_address = sys.argv[1]
number_of_variables = int(sys.argv[2])


def center_constraint(instance_address, variable):
    #find bound assertion and line index
    upper_bound_index, upper_bound, _ = op.find_line_upper_bound(instance_address, variable)
    #extract all integers or decimals from a string
    numbers_upper_bound = re.findall(r"\-*\d+\.*\d*", upper_bound)
    #the first substring is the variable subscript
    variable_num = numbers_upper_bound[0]
    #the second extracted substring is the bound
    upper_bound_num = numbers_upper_bound[1]
    #convert string to float
    upper_bound_num  = float(upper_bound_num)

    #find bound assertion and line index
    lower_bound_index, lower_bound, properties = op.find_line_lower_bound(instance_address, variable)
    #extract all integers or decimals from a string
    numbers_lower_bound = re.findall(r"\-*\d+\.*\d*", lower_bound)
    #the second substring is the bound
    lower_bound_num =  numbers_lower_bound[1] 
    #convert string to float 
    lower_bound_num = float(lower_bound_num)
    #compute the interval center
    interval_center = (lower_bound_num + upper_bound_num)/2
    #convert to string and supress scientific notation
    #round to 20 decimals
    interval_center = f"{interval_center: .20f}"
    
    #create the new assertions 
    new_assertion_upper_bound = "(assert (<= X_" + variable_num + " " + interval_center +"))" + "\n"
    new_assertion_lower_bound = "(assert (>= X_" + variable_num + " " + interval_center +"))" + "\n"

    with open(instance_address,"w") as property_file:
        properties[lower_bound_index] = new_assertion_upper_bound
        properties[upper_bound_index] = new_assertion_lower_bound
        property_file.writelines(properties)
        

def center_all_constraints(number_of_variables,instance_address):
    print("centering inputs for intance: " + instance_address)
    for i in range(number_of_variables):
        variable = "X_" + str(i)
        center_constraint(instance_address, variable)

center_all_constraints(number_of_variables,instance_address)