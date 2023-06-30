import re
import line_operations as op
import numpy as np
import sys

#argv[1] instance's address
#argv[2] forward pass folder
instance_address = sys.argv[1]
forward_pass_address = sys.argv[2]+"/"+"forward_pass.txt"

#erase old output constrains
def erase_output_constraints(instance_address):
    regular_expression = "; unsafe if"
    index, line, lines = op.find_line_with(instance_address, regular_expression)
    op.erase_lines_after(instance_address, index)        

# get the model prediction from output textfile
def find_model_prediction(forward_pass_address):
    regular_expression = "Model prediction is:"
    line_index, prediction_line, _ = op.find_line_with(forward_pass_address, regular_expression)
    tensor_numbers_list = re.findall(r"\-*\d+\.*\d*", prediction_line)
    #convert strings to numbers
    tensor_numbers_array = np.array([float(tensor_numbers_list[0]),float(tensor_numbers_list[1]),float(tensor_numbers_list[2]),float(tensor_numbers_list[3])])
    chosen_action = np.argmax(tensor_numbers_array)
    return tensor_numbers_array, chosen_action

# insert appropriate output constraint
def insert_output_constraint(instance_address, forward_pass_address):
    #get the model prediction
    tensor_numbers_array, chosen_action = find_model_prediction(forward_pass_address)
    #erase old constraints
    erase_output_constraints(instance_address)
    #get the file lines
    with open(instance_address,"r") as instance_file:
        lines = instance_file.readlines()     
        with open(instance_address, "w") as instance_file:
            #insert new constraints
            if chosen_action == 0:
                lines.append("\n")
                lines.append("; model prediction:"+ str(tensor_numbers_array) + "\n") 
                lines.append("; action chosen was " + str(chosen_action) + " (argmax)" + "\n")
                lines.append("; output constraints for counterexample" + "\n")
                lines.append("(assert (or" + "\n")
                lines.append("(and (>= Y_1 Y_0))" + "\n")
                lines.append("(and (>= Y_2 Y_0))" + "\n")
                lines.append("(and (>= Y_3 Y_0))" + "\n")
                lines.append("))" + "\n")
                print("adding output constraints for instance" + instance_address)
                instance_file.writelines(lines)
            elif chosen_action == 1:
                lines.append("\n")
                lines.append("; model prediction:"+ str(tensor_numbers_array) + "\n") 
                lines.append("; action chosen was " + str(chosen_action) + " (argmax)" + "\n")
                lines.append("; output constraints for counterexample" + "\n")                
                lines.append("(assert (or" + "\n")
                lines.append("(and (>= Y_0 Y_1))" + "\n")
                lines.append("(and (>= Y_2 Y_1))" + "\n")
                lines.append("(and (>= Y_3 Y_1))" + "\n")
                lines.append("))" + "\n")
                print("adding output constraints for instance" + instance_address)
                instance_file.writelines(lines)
            elif chosen_action == 2:
                lines.append("\n")
                lines.append("; model prediction:"+ str(tensor_numbers_array) + "\n") 
                lines.append("; action chosen was " + str(chosen_action) + " (argmax)" + "\n")
                lines.append("; output constraints for counterexample" + "\n")
                lines.append("(assert (or" + "\n")
                lines.append("(and (>= Y_0 Y_2))" + "\n")
                lines.append("(and (>= Y_1 Y_2))" + "\n")
                lines.append("(and (>= Y_3 Y_2))" + "\n")
                lines.append("))" + "\n") 
                print("adding output constraints for instance" + instance_address)
                instance_file.writelines(lines)              
            elif chosen_action == 3:
                lines.append("\n")
                lines.append("; model prediction:"+ str(tensor_numbers_array) + "\n") 
                lines.append("; action chosen was " + str(chosen_action) + " (argmax)" + "\n")
                lines.append("; output constraints for counterexample" + "\n")                
                lines.append("(assert (or" + "\n")
                lines.append("(and (>= Y_0 Y_3))" + "\n")
                lines.append("(and (>= Y_1 Y_3))" + "\n")
                lines.append("(and (>= Y_2 Y_3))" + "\n")
                lines.append("))" + "\n")
                print("adding output constraints for instance" + instance_address)
                instance_file.writelines(lines)
            else:
                print("error: the chosen action does not match the possibilities [0,1,2,3].")

#execute function to create the new output constraints
insert_output_constraint(instance_address, forward_pass_address)

