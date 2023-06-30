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
def find_model_prediction(forward_pass_address, instance_address):
    regular_expression = "Model prediction is:"
    line_index, prediction_line, lines = op.find_line_with(forward_pass_address, regular_expression)
    tensor_numbers_list_1 = re.findall(r"\-*\d+\.*\d*", prediction_line)
    tensor_numbers_list_2 = re.findall(r"\-*\d+\.*\d*", lines[line_index+1])
    print(prediction_line)
    print(lines[line_index+1])
    print(tensor_numbers_list_1)
    print(tensor_numbers_list_2)
    
    if (len(tensor_numbers_list_1) == 5) and (len(tensor_numbers_list_2) == 3):
    
        #convert strings to numbers
        tensor_numbers_first_actuator = np.array([float(tensor_numbers_list_1[0]),float(tensor_numbers_list_1[1]),float(tensor_numbers_list_1[2]),float(tensor_numbers_list_1[3])])
        tensor_numbers_second_actuator = np.array([float(tensor_numbers_list_1[4]),float(tensor_numbers_list_2[0]),float(tensor_numbers_list_2[1]),float(tensor_numbers_list_2[2])])
    
    else:
        print(instance_address)
        print("first_line:" + str(tensor_numbers_list_1))
        print("second_line:" + str(tensor_numbers_list_2))
        with open(forward_pass_address,"r") as file:
            print(file.read())
        print("ERROR IN PREDICTION TENSOR SHAPE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        sys.exit()
        
    chosen_action_first_actuator = np.argmax(tensor_numbers_first_actuator)
    #the action of the second actuator starts from 4 to match the output variables coding
    chosen_action_second_actuator = np.argmax(tensor_numbers_second_actuator)
    chosen_action_second_actuator = chosen_action_second_actuator + 4
    return tensor_numbers_first_actuator, tensor_numbers_second_actuator, chosen_action_first_actuator, chosen_action_second_actuator



# insert appropriate output constraint
def insert_output_constraint(instance_address, forward_pass_address):
    
    #erase old constraints
    erase_output_constraints(instance_address)

    #get the model prediction
    tensor_numbers_first_actuator, tensor_numbers_second_actuator, first_actuator, second_actuator = find_model_prediction(forward_pass_address, instance_address)
    #get the file lines
    with open(instance_address,"r") as instance_file:
        lines = instance_file.readlines()     
        with open(instance_address, "w") as instance_file:
            #insert new constraints to define counterexample properties
            if (first_actuator == 0) and (second_actuator == 4):
                
                lines.append("\n")
                lines.append("; model prediction:"+ str(tensor_numbers_first_actuator) + str(tensor_numbers_second_actuator) + "\n") 
                lines.append("; action chosen was " + str(first_actuator) + " (first actuator) " + str(second_actuator) + " (second actuator)" + "\n")
                lines.append("; output constraints for counterexample" + "\n")
                lines.append("(assert (or" + "\n")
                
                #inequalities for the first actuator
                lines.append("(and (>= Y_1 Y_0))" + "\n")
                lines.append("(and (>= Y_2 Y_0))" + "\n")
                lines.append("(and (>= Y_3 Y_0))" + "\n")
                
                #inequalities for the second actuator
                lines.append("(and (>= Y_5 Y_4))" + "\n")
                lines.append("(and (>= Y_6 Y_4))" + "\n")
                lines.append("(and (>= Y_7 Y_4))" + "\n")
                
                lines.append("))" + "\n")
                print("adding output constraints for instance" + instance_address)
                instance_file.writelines(lines)
                
            elif (first_actuator == 1) and (second_actuator == 4):
                
                lines.append("\n")
                lines.append("; model prediction:"+ str(tensor_numbers_first_actuator) + str(tensor_numbers_second_actuator) + "\n") 
                lines.append("; action chosen was " + str(first_actuator) + " (first actuator) " + str(second_actuator) + " (second actuator)" + "\n")
                lines.append("; output constraints for counterexample" + "\n")
                lines.append("(assert (or" + "\n")
                
                #inequalities for the first actuator
                lines.append("(and (>= Y_0 Y_1))" + "\n")
                lines.append("(and (>= Y_2 Y_1))" + "\n")
                lines.append("(and (>= Y_3 Y_1))" + "\n")
                
                #inequalities for the second actuator
                lines.append("(and (>= Y_5 Y_4))" + "\n")
                lines.append("(and (>= Y_6 Y_4))" + "\n")
                lines.append("(and (>= Y_7 Y_4))" + "\n")
                
                lines.append("))" + "\n")
                print("adding output constraints for instance" + instance_address)
                instance_file.writelines(lines)
                
            elif (first_actuator == 2) and (second_actuator == 4):
                
                lines.append("\n")
                lines.append("; model prediction:"+ str(tensor_numbers_first_actuator) + str(tensor_numbers_second_actuator) + "\n") 
                lines.append("; action chosen was " + str(first_actuator) + " (first actuator) " + str(second_actuator) + " (second actuator)" + "\n")
                lines.append("; output constraints for counterexample" + "\n")
                lines.append("(assert (or" + "\n")
                
                #inequalities for the first actuator
                lines.append("(and (>= Y_0 Y_2))" + "\n")
                lines.append("(and (>= Y_1 Y_2))" + "\n")
                lines.append("(and (>= Y_3 Y_2))" + "\n")
                
                #inequalities for the second actuator
                lines.append("(and (>= Y_5 Y_4))" + "\n")
                lines.append("(and (>= Y_6 Y_4))" + "\n")
                lines.append("(and (>= Y_7 Y_4))" + "\n")
                
                lines.append("))" + "\n")
                print("adding output constraints for instance" + instance_address)
                instance_file.writelines(lines)
                
            elif (first_actuator == 3) and (second_actuator == 4):
                
                lines.append("\n")
                lines.append("; model prediction:"+ str(tensor_numbers_first_actuator) + str(tensor_numbers_second_actuator) + "\n") 
                lines.append("; action chosen was " + str(first_actuator) + " (first actuator) " + str(second_actuator) + " (second actuator)" + "\n")
                lines.append("; output constraints for counterexample" + "\n")
                lines.append("(assert (or" + "\n")
                
                #inequalities for the first actuator
                lines.append("(and (>= Y_0 Y_3))" + "\n")
                lines.append("(and (>= Y_1 Y_3))" + "\n")
                lines.append("(and (>= Y_2 Y_3))" + "\n")
                
                #inequalities for the second actuator
                lines.append("(and (>= Y_5 Y_4))" + "\n")
                lines.append("(and (>= Y_6 Y_4))" + "\n")
                lines.append("(and (>= Y_7 Y_4))" + "\n")
                
                lines.append("))" + "\n")
                print("adding output constraints for instance" + instance_address)
                instance_file.writelines(lines)
                
            elif (first_actuator == 0) and (second_actuator == 5):
                
                lines.append("\n")
                lines.append("; model prediction:"+ str(tensor_numbers_first_actuator) + str(tensor_numbers_second_actuator) + "\n") 
                lines.append("; action chosen was " + str(first_actuator) + " (first actuator) " + str(second_actuator) + " (second actuator)" + "\n")
                lines.append("; output constraints for counterexample" + "\n")
                lines.append("(assert (or" + "\n")
                
                #inequalities for the first actuator
                lines.append("(and (>= Y_1 Y_0))" + "\n")
                lines.append("(and (>= Y_2 Y_0))" + "\n")
                lines.append("(and (>= Y_3 Y_0))" + "\n")
                
                #inequalities for the second actuator
                lines.append("(and (>= Y_4 Y_5))" + "\n")
                lines.append("(and (>= Y_6 Y_5))" + "\n")
                lines.append("(and (>= Y_7 Y_5))" + "\n")
                
                lines.append("))" + "\n")
                print("adding output constraints for instance" + instance_address)
                instance_file.writelines(lines)
                
            elif (first_actuator == 1) and (second_actuator == 5):
                
                lines.append("\n")
                lines.append("; model prediction:"+ str(tensor_numbers_first_actuator) + str(tensor_numbers_second_actuator) + "\n") 
                lines.append("; action chosen was " + str(first_actuator) + " (first actuator) " + str(second_actuator) + " (second actuator)" + "\n")
                lines.append("; output constraints for counterexample" + "\n")
                lines.append("(assert (or" + "\n")
                
                #inequalities for the first actuator
                lines.append("(and (>= Y_0 Y_1))" + "\n")
                lines.append("(and (>= Y_2 Y_1))" + "\n")
                lines.append("(and (>= Y_3 Y_1))" + "\n")
                
                #inequalities for the second actuator
                lines.append("(and (>= Y_4 Y_5))" + "\n")
                lines.append("(and (>= Y_6 Y_5))" + "\n")
                lines.append("(and (>= Y_7 Y_5))" + "\n")
                
                lines.append("))" + "\n")
                print("adding output constraints for instance" + instance_address)
                instance_file.writelines(lines)
                
            elif (first_actuator == 2) and (second_actuator == 5):
                lines.append("\n")
                lines.append("; model prediction:"+ str(tensor_numbers_first_actuator) + str(tensor_numbers_second_actuator) + "\n") 
                lines.append("; action chosen was " + str(first_actuator) + " (first actuator) " + str(second_actuator) + " (second actuator)" + "\n")
                lines.append("; output constraints for counterexample" + "\n")
                lines.append("(assert (or" + "\n")
                
                #inequalities for the first actuator
                lines.append("(and (>= Y_0 Y_2))" + "\n")
                lines.append("(and (>= Y_1 Y_2))" + "\n")
                lines.append("(and (>= Y_3 Y_2))" + "\n")
                
                #inequalities for the second actuator
                lines.append("(and (>= Y_4 Y_5))" + "\n")
                lines.append("(and (>= Y_6 Y_5))" + "\n")
                lines.append("(and (>= Y_7 Y_5))" + "\n")
                
                lines.append("))" + "\n")
                print("adding output constraints for instance" + instance_address)
                instance_file.writelines(lines)
                
            elif (first_actuator == 3) and (second_actuator == 5):
                
                lines.append("\n")
                lines.append("; model prediction:"+ str(tensor_numbers_first_actuator) + str(tensor_numbers_second_actuator) + "\n") 
                lines.append("; action chosen was " + str(first_actuator) + " (first actuator) " + str(second_actuator) + " (second actuator)" + "\n")
                lines.append("; output constraints for counterexample" + "\n")
                lines.append("(assert (or" + "\n")
                
                #inequalities for the first actuator
                lines.append("(and (>= Y_0 Y_3))" + "\n")
                lines.append("(and (>= Y_1 Y_3))" + "\n")
                lines.append("(and (>= Y_2 Y_3))" + "\n")
                
                #inequalities for the second actuator
                lines.append("(and (>= Y_4 Y_5))" + "\n")
                lines.append("(and (>= Y_6 Y_5))" + "\n")
                lines.append("(and (>= Y_7 Y_5))" + "\n")
                
                lines.append("))" + "\n")
                print("adding output constraints for instance" + instance_address)
                instance_file.writelines(lines)
                
            elif (first_actuator == 0) and (second_actuator == 6):
                
                lines.append("\n")
                lines.append("; model prediction:"+ str(tensor_numbers_first_actuator) + str(tensor_numbers_second_actuator) + "\n") 
                lines.append("; action chosen was " + str(first_actuator) + " (first actuator) " + str(second_actuator) + " (second actuator)" + "\n")
                lines.append("; output constraints for counterexample" + "\n")
                lines.append("(assert (or" + "\n")
                
                #inequalities for the first actuator
                lines.append("(and (>= Y_1 Y_0))" + "\n")
                lines.append("(and (>= Y_2 Y_0))" + "\n")
                lines.append("(and (>= Y_3 Y_0))" + "\n")
                
                #inequalities for the second actuator
                lines.append("(and (>= Y_4 Y_6))" + "\n")
                lines.append("(and (>= Y_5 Y_6))" + "\n")
                lines.append("(and (>= Y_7 Y_6))" + "\n")
                
                lines.append("))" + "\n")
                print("adding output constraints for instance" + instance_address)
                instance_file.writelines(lines)
                
            elif (first_actuator == 1) and (second_actuator == 6):
                
                lines.append("\n")
                lines.append("; model prediction:"+ str(tensor_numbers_first_actuator) + str(tensor_numbers_second_actuator) + "\n") 
                lines.append("; action chosen was " + str(first_actuator) + " (first actuator) " + str(second_actuator) + " (second actuator)" + "\n")
                lines.append("; output constraints for counterexample" + "\n")
                lines.append("(assert (or" + "\n")
                
                #inequalities for the first actuator
                lines.append("(and (>= Y_0 Y_1))" + "\n")
                lines.append("(and (>= Y_2 Y_1))" + "\n")
                lines.append("(and (>= Y_3 Y_1))" + "\n")
                
                #inequalities for the second actuator
                lines.append("(and (>= Y_4 Y_6))" + "\n")
                lines.append("(and (>= Y_5 Y_6))" + "\n")
                lines.append("(and (>= Y_7 Y_6))" + "\n")
                
                lines.append("))" + "\n")
                print("adding output constraints for instance" + instance_address)
                instance_file.writelines(lines)
                
            elif (first_actuator == 2) and (second_actuator == 6):
                lines.append("\n")
                lines.append("; model prediction:"+ str(tensor_numbers_first_actuator) + str(tensor_numbers_second_actuator) + "\n") 
                lines.append("; action chosen was " + str(first_actuator) + " (first actuator) " + str(second_actuator) + " (second actuator)" + "\n")
                lines.append("; output constraints for counterexample" + "\n")
                lines.append("(assert (or" + "\n")
                
                #inequalities for the first actuator
                lines.append("(and (>= Y_0 Y_2))" + "\n")
                lines.append("(and (>= Y_1 Y_2))" + "\n")
                lines.append("(and (>= Y_3 Y_2))" + "\n")
                
                #inequalities for the second actuator
                lines.append("(and (>= Y_4 Y_6))" + "\n")
                lines.append("(and (>= Y_5 Y_6))" + "\n")
                lines.append("(and (>= Y_7 Y_6))" + "\n")
                
                lines.append("))" + "\n")
                print("adding output constraints for instance" + instance_address)
                instance_file.writelines(lines)
                
            elif (first_actuator == 3) and (second_actuator == 6):
                
                lines.append("\n")
                lines.append("; model prediction:"+ str(tensor_numbers_first_actuator) + str(tensor_numbers_second_actuator) + "\n") 
                lines.append("; action chosen was " + str(first_actuator) + " (first actuator) " + str(second_actuator) + " (second actuator)" + "\n")
                lines.append("; output constraints for counterexample" + "\n")
                lines.append("(assert (or" + "\n")
                
                #inequalities for the first actuator
                lines.append("(and (>= Y_0 Y_3))" + "\n")
                lines.append("(and (>= Y_1 Y_3))" + "\n")
                lines.append("(and (>= Y_2 Y_3))" + "\n")
                
                #inequalities for the second actuator
                lines.append("(and (>= Y_4 Y_6))" + "\n")
                lines.append("(and (>= Y_5 Y_6))" + "\n")
                lines.append("(and (>= Y_7 Y_6))" + "\n")
                
                lines.append("))" + "\n")
                print("adding output constraints for instance" + instance_address)
                instance_file.writelines(lines)
                
            elif (first_actuator == 0) and (second_actuator == 7):
                
                lines.append("\n")
                lines.append("; model prediction:"+ str(tensor_numbers_first_actuator) + str(tensor_numbers_second_actuator) + "\n") 
                lines.append("; action chosen was " + str(first_actuator) + " (first actuator) " + str(second_actuator) + " (second actuator)" + "\n")
                lines.append("; output constraints for counterexample" + "\n")
                lines.append("(assert (or" + "\n")
                
                #inequalities for the first actuator
                lines.append("(and (>= Y_1 Y_0))" + "\n")
                lines.append("(and (>= Y_2 Y_0))" + "\n")
                lines.append("(and (>= Y_3 Y_0))" + "\n")
                
                #inequalities for the second actuator
                lines.append("(and (>= Y_4 Y_7))" + "\n")
                lines.append("(and (>= Y_5 Y_7))" + "\n")
                lines.append("(and (>= Y_6 Y_7))" + "\n")
                
                lines.append("))" + "\n")
                print("adding output constraints for instance" + instance_address)
                instance_file.writelines(lines)
                
            elif (first_actuator == 1) and (second_actuator == 7):
                
                lines.append("\n")
                lines.append("; model prediction:"+ str(tensor_numbers_first_actuator) + str(tensor_numbers_second_actuator) + "\n") 
                lines.append("; action chosen was " + str(first_actuator) + " (first actuator) " + str(second_actuator) + " (second actuator)" + "\n")
                lines.append("; output constraints for counterexample" + "\n")
                lines.append("(assert (or" + "\n")
                
                #inequalities for the first actuator
                lines.append("(and (>= Y_0 Y_1))" + "\n")
                lines.append("(and (>= Y_2 Y_1))" + "\n")
                lines.append("(and (>= Y_3 Y_1))" + "\n")
                
                #inequalities for the second actuator
                lines.append("(and (>= Y_4 Y_7))" + "\n")
                lines.append("(and (>= Y_5 Y_7))" + "\n")
                lines.append("(and (>= Y_6 Y_7))" + "\n")
                
                lines.append("))" + "\n")
                print("adding output constraints for instance" + instance_address)
                instance_file.writelines(lines)
                
            elif (first_actuator == 2) and (second_actuator == 7):
                
                lines.append("\n")
                lines.append("; model prediction:"+ str(tensor_numbers_first_actuator) + str(tensor_numbers_second_actuator) + "\n") 
                lines.append("; action chosen was " + str(first_actuator) + " (first actuator) " + str(second_actuator) + " (second actuator)" + "\n")
                lines.append("; output constraints for counterexample" + "\n")
                lines.append("(assert (or" + "\n")
                
                #inequalities for the first actuator
                lines.append("(and (>= Y_0 Y_2))" + "\n")
                lines.append("(and (>= Y_1 Y_2))" + "\n")
                lines.append("(and (>= Y_3 Y_2))" + "\n")
                
                #inequalities for the second actuator
                lines.append("(and (>= Y_4 Y_7))" + "\n")
                lines.append("(and (>= Y_5 Y_7))" + "\n")
                lines.append("(and (>= Y_6 Y_7))" + "\n")
                
                lines.append("))" + "\n")
                print("adding output constraints for instance" + instance_address)
                instance_file.writelines(lines)
                
            elif (first_actuator == 3) and (second_actuator == 7):
                
                lines.append("\n")
                lines.append("; model prediction:"+ str(tensor_numbers_first_actuator) + str(tensor_numbers_second_actuator) + "\n") 
                lines.append("; action chosen was " + str(first_actuator) + " (first actuator) " + str(second_actuator) + " (second actuator)" + "\n")
                lines.append("; output constraints for counterexample" + "\n")
                lines.append("(assert (or" + "\n")
                
                #inequalities for the first actuator
                lines.append("(and (>= Y_0 Y_3))" + "\n")
                lines.append("(and (>= Y_1 Y_3))" + "\n")
                lines.append("(and (>= Y_2 Y_3))" + "\n")
                
                #inequalities for the second actuator
                lines.append("(and (>= Y_4 Y_7))" + "\n")
                lines.append("(and (>= Y_5 Y_7))" + "\n")
                lines.append("(and (>= Y_6 Y_7))" + "\n")
                
                lines.append("))" + "\n")
                print("adding output constraints for instance" + instance_address)
                instance_file.writelines(lines)
                
            else:
                print("error: the chosen action does not match on of the sixteen possibilities.")

#execute function to create the new output constraints
insert_output_constraint(instance_address, forward_pass_address)

