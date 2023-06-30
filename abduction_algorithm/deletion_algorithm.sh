#!/bin/bash
# give permission to execute the file:
#chmod u+x abduction_algorithm/deletion_algorithm.sh
#execute:
#./abduction_algorithm/deletion_algorithm.sh

######################################################################
# Modifiable parameters

#benchmark name

name_of_benchmark=$1

# the epsilon perturbation
epsilon=$2

# the number of input variables
number_of_variables=$3

# number of input variables minus 1
highest_input_variable_subscript=$(expr $number_of_variables - 1)

#write here your root folder
root_folder=$4

#instance name
instance_name=$5

######################################################################
#folders and files

#properties folders
instances_folder=$root_folder/"abduction_algorithm/instances"/$name_of_benchmark
abduction_properties_folder=$root_folder/"abduction_algorithm/abduction_properties"/$name_of_benchmark
#config file folder
config_file_address=$root_folder/"abduction_algorithm/ymal_config_files/abduction_"$name_of_benchmark".yaml"
#verifier folder
alpha_beta_crown_folder=$root_folder/"alpha-beta-CROWN/complete_verifier"
#python files folder
python_files_folder=$root_folder/"abduction_algorithm/python_scripts"


#results folder
results_folder=$root_folder/"abduction_algorithm/results/deletion_algorithm"


#temporary results text file
explanation_file_address=$root_folder/"abduction_algorithm/explanation.txt"

#temporary verification step file
verification_step_file_address=$root_folder/"abduction_algorithm/verification_step.txt"


######################################################################
# Copy instance file and move it to the abduction properties directory

echo "copying instance ${instance_name} to the abduction_properties folder"
cp "${instances_folder}/${instance_name}" "${abduction_properties_folder}"

#modyfying the config file for the instance
echo "setting the config file for instance ${instance_name}"
python $python_files_folder/modify_config_file.py $config_file_address $abduction_properties_folder/$instance_name


######################################################################
# Deletion algorithm


echo "using epsilon = $epsilon"
echo "applying the deletion algorithm on ${instance_name}"

for ((n=0;n<=$highest_input_variable_subscript;n++))
do
    #delete contraint
    python $python_files_folder/constraint_deletion.py $n $epsilon $instance_name $abduction_properties_folder
    #call verifier to determine if the property is sat or unsat
    python $alpha_beta_crown_folder/abcrown.py --config $config_file_address > $verification_step_file_address
    # checking in the output file
    output=$(tail -2 $verification_step_file_address > >( head -1))
    output=($output) #convert to stringarray
    result=${output[1]}
    echo $result
    #if sat restore constraint
    if [ "$result" = "sat" ]; then
        echo "variable $n is part of the explanation. Restoring constraint..."
        python $python_files_folder/restore_constraint.py $n $instance_name $instances_folder $abduction_properties_folder
        #save the result in a temporal txt file
        echo "1" >> $explanation_file_address
        rm $verification_step_file_address
    #else continue to next iteration
    else 
        echo "variable $n is NOT part of the explanation"
        #save the result in a temporal txt file
        echo "0" >> $explanation_file_address
        rm $verification_step_file_address
    fi
    
    if [ $n -eq $highest_input_variable_subscript ]; then
        python $python_files_folder/add_result_to_csv.py $explanation_file_address $instances_folder/$instance_name $instance_name $epsilon $number_of_variables $results_folder $name_of_benchmark
        rm $explanation_file_address
        echo "finished algorithm execution"
    fi

done





