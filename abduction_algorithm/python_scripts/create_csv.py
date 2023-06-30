import sys
import csv

number_of_variables = sys.argv[1]
benchmark_name = sys.argv[2]
results_folder = sys.argv[3]
epsilon = sys.argv[4]


csv_file_address = results_folder + "/results_" + benchmark_name + "_" + str(epsilon) + ".csv"

def get_input_variables(number_of_variables):
    list_of_variables = []
    for i in range(int(number_of_variables)):
        list_of_variables.append("X_"+str(i))
    return list_of_variables

if (benchmark_name == "dubinsrejoin"):
    print("creating csv for " + benchmark_name + " benchmark.")
    list_of_fields = ["instance_name"] + get_input_variables(number_of_variables) + ["action_1","action_2", "epsilon"]
    list_of_fields = list_of_fields + get_input_variables(number_of_variables)   
else:
    list_of_fields = ["instance_name"] + get_input_variables(number_of_variables) + ["action", "epsilon"]
    list_of_fields = list_of_fields + get_input_variables(number_of_variables) 


with open(csv_file_address, "w") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(list_of_fields)
    
    


