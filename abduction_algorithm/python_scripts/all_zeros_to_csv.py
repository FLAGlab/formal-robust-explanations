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



# create a csv file with the following fields
# instance_number name input chosen action epsilon exp 

inputs = op.get_inputs(instance_address, number_of_variables)
action = op.get_action(instance_address)
#the explanation is a list of zeros
explanation = ["0"]*number_of_variables
result_row = [instance_name] + inputs + action + [epsilon] + explanation

with open(csv_file_address, "a") as csvfile:
    print("the explanation is for " + instance_name + "is")
    print(explanation)
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(result_row)

