import perturbation as p
import line_operations as op
import re
import sys

# sys.argv[1] explanation_file_address
# sys.argv[2] epsilon
# sys.argv[3] weight parameter for epsilon
# sys.argv[4] property_address
# sys.argv[5] number of input variables


explanation_file_address = sys.argv[1]
epsilon = float(sys.argv[2])
weight_parameter = float(sys.argv[3])
property_address = sys.argv[4]
number_of_variables = int(sys.argv[5])

#compute the weighted epsilon

epsilon = epsilon/weight_parameter


def delete_constraint(property_address, variable, epsilon):
    upper_bound_index, upper_bound, properties =op.find_line_upper_bound(property_address, variable)
    new_upper_bound = p.perturbation_upper_bound(upper_bound, epsilon)
    lower_bound_index, lower_bound, properties = op.find_line_lower_bound(property_address, variable)
    new_lower_bound = p.perturbation_lower_bound(lower_bound, epsilon)
    with open(property_address,"w") as file_object:
        properties[upper_bound_index] = new_upper_bound + "\n"
        properties[lower_bound_index] = new_lower_bound + "\n"
        file_object.writelines(properties)


#delete constraints selectively

def multiple_deletion(explanation_file_address, epsilon, property_address, number_of_variables):
    
    #read from the explanation.txt file
    with open(explanation_file_address, "r") as file:
        explanation_lines = file.readlines()
        
        #delete constraints selectively
        for variable_number in range(number_of_variables):
            #get the number associated to the variable from the explanation file. 
            list_of_numbers = re.findall(r"\d", explanation_lines[variable_number])
            constraint_explanation_number = list_of_numbers[0]
            if (constraint_explanation_number == "0"):
                #delete constraint
                variable = "X_" + str(variable_number)
                print("deleting constraint associated to variable: " + variable)
                delete_constraint(property_address, variable, epsilon)
            elif (constraint_explanation_number == "1"):
                #do nothing. don't delete
                pass
            else:
                print("error reading the explanation.txt file !!!!!!!!!!!!!!!!!!!!")
        
        
#execute function

print("deleting constraints with weighted epsilon: " + str(epsilon))
multiple_deletion(explanation_file_address, epsilon, property_address, number_of_variables)







