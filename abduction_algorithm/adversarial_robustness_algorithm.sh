#!/bin/bash
# give permission to execute the file:
#chmod u+x abduction_algorithm/adversarial_robustness_algorithm.sh
#execute:
#./abduction_algorithm/adversarial_robustness_algorithm.sh

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

# results folder address
results_folder=$6


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


#temporary results explanation files
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
# this first step is the equivalent to a very sparse attack
# the perturbation is made only for one input at a time

echo "using epsilon = $epsilon"
echo "applying the algorithm on ${instance_name}"

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
    
    #if sat add constraint to explanation and restore constraint
    if [ "$result" = "sat" ]; then
        echo "variable $n is part of the explanation. Restoring constraint..."
        python $python_files_folder/restore_constraint.py $n $instance_name $instances_folder $abduction_properties_folder
        #save the result in a temporal txt file
        echo "1" >> $explanation_file_address
        rm $verification_step_file_address
    #else DO NOT add constraint to explanation and restore constraint
    else 
        echo "variable $n is NOT part of the explanation. Restoring constraint..."
        python $python_files_folder/restore_constraint.py $n $instance_name $instances_folder $abduction_properties_folder
        #save the result in a temporal txt file
        echo "0" >> $explanation_file_address
        rm $verification_step_file_address
    fi
    
done



######################################################################
#Robustness test on explanation
#check the invariability of the explanation to epsilon weighted perturbations

#get the explanation size
explanation_size=0

while read line; do
    if [ $line = "1" ]; then
        explanation_size=$(( explanation_size +  1 ))        
    fi
done < $explanation_file_address

#determine a weight parameter

weight_parameter=$(( number_of_variables - explanation_size ))

#create a flag for saving the results of robustness tests
robustness_flag=0

# first, determine if the explanation is not empty
if [ $weight_parameter -eq $number_of_variables ] || [ $weight_parameter -eq 0 ]
then
    echo "The initial sparse perturbation might be too weak or is a trivial explanation."
else
    echo "The explanation is not empty. Proceding to robustness test with a weighted/smaller epsilon."
    
    #delete all contraints that produced UNSAT before. That is, the ones corresponding to zeros in the explanation file. 
    echo "inverse weight for epsilon is: "$weight_parameter
    python $python_files_folder/multiple_constraint_w_deletion.py $explanation_file_address $epsilon $weight_parameter $abduction_properties_folder/$instance_name $number_of_variables
    
    #call verifier to determine if the new property is sat or unsat
    python $alpha_beta_crown_folder/abcrown.py --config $config_file_address > $verification_step_file_address
    
    #checking in the verifier's output file
    output=$(tail -2 $verification_step_file_address > >( head -1))
    output=($output) #convert to stringarray
    result=${output[1]}
    echo $result
    
    if [ "$result" = "sat" ] || [ "$result" = "timeout" ]; then
    robustness_flag=0
    echo "it is NOT a robust explanation "$result
    rm $verification_step_file_address
    else
    robustness_flag=1
    echo "it is a robust explanation "$result
    rm $verification_step_file_address
    fi
    
fi

echo "the robust explanation is:"
cat $explanation_file_address


######################################################################
# storing results

if [ $robustness_flag -eq 0 ]; then
    # No robust explanation was found. store an empty explanation in csv file
    python $python_files_folder/all_zeros_to_csv.py $explanation_file_address $instances_folder/$instance_name $instance_name $epsilon $number_of_variables $results_folder $name_of_benchmark
else
    echo "Robust, explanation found!"
    python $python_files_folder/add_result_to_csv.py $explanation_file_address $instances_folder/$instance_name $instance_name $epsilon $number_of_variables $results_folder $name_of_benchmark  
    
fi

rm $explanation_file_address


######################################################################
# end
