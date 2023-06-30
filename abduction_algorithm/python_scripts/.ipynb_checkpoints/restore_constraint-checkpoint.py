import perturbation as p
import line_operations as op
import re
import sys

variable_number = sys.argv[1]
instance_name = sys.argv[2]
instance_folder = sys.argv[3]
abduction_properties_folder=sys.argv[4]

instance_address = instance_folder +"/"+ instance_name
property_address = abduction_properties_folder +"/"+ instance_name
variable = "X_" + variable_number

def restore_constraint(property_address, instance_address, variable):
    upper_bound_index, upper_bound, _ = op.find_line_upper_bound(instance_address, variable)
    lower_bound_index, lower_bound, _ = op.find_line_lower_bound(instance_address, variable)
    _, _, properties = op.find_line_upper_bound(property_address, variable)
    with open(property_address,"w") as property_file:
        properties[upper_bound_index] = upper_bound 
        properties[lower_bound_index] = lower_bound
        property_file.writelines(properties)

        
#restore property
restore_constraint(property_address, instance_address, variable)


