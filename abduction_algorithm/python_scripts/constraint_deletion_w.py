import perturbation as p
import line_operations as op
import re
import sys

# sys.argv[1] variable number
# sys.argv[2] epsilon
# sys.argv[3] instance_name
# sys.argv[4] abduction_properties_folder



variable_number = sys.argv[1]
epsilon = float(sys.argv[2])
weight_parameter = float(sys.argv[3])
instance_name = sys.argv[4]
abduction_properties_folder= sys.argv[5]

epsilon = epsilon/weight_parameter


#instance_address = instance_folder +"/"+ instance_name
property_address = abduction_properties_folder +"/"+ instance_name
variable = "X_" + variable_number


def delete_constraint(property_address, variable, epsilon):
    upper_bound_index, upper_bound, properties = op.find_line_upper_bound(property_address, variable)
    new_upper_bound = p.perturbation_upper_bound(upper_bound, epsilon)
    lower_bound_index, lower_bound, properties = op.find_line_lower_bound(property_address, variable)
    new_lower_bound = p.perturbation_lower_bound(lower_bound, epsilon)
    with open(property_address,"w") as file_object:
        properties[upper_bound_index] = new_upper_bound + "\n"
        properties[lower_bound_index] = new_lower_bound + "\n"
        file_object.writelines(properties)


delete_constraint(property_address, variable, epsilon)
print("perturbing constraint " + str(variable_number) + " with weighted epsilon: " + str(epsilon))





