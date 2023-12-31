#!/bin/bash
# give permission to execute the file:
#chmod u+x abduction_algorithm/create_instances_dubinsrejoin.sh
#execute:
#./abduction_algorithm/create_instances_dubinsrejoin.sh

######################################################################
# Modifiable parameters

#benchmark name
benchmark_name="dubinsrejoin"

#number of input variables
number_of_variables="8"

#root folder address
root_folder="/root"

######################################################################
#folders and files

config_file_address=$root_folder/"abduction_algorithm/ymal_config_files/abduction_"$benchmark_name".yaml"
alpha_beta_crown_folder=$root_folder/"alpha-beta-CROWN/complete_verifier"
forward_pass_folder=$root_folder/"abduction_algorithm"
python_scripts_folder=$root_folder/"abduction_algorithm/python_scripts"

# Move property files from the VNN COMP folder
cp $root_folder/vnncomp2022_benchmarks/benchmarks/rl_benchmarks/vnnlib/$benchmark_name* $root_folder/abduction_algorithm/instances/$benchmark_name

# change directory and unzip all files
cd $root_folder/abduction_algorithm/instances/$benchmark_name
gunzip *.gz

# go back to the root folder
cd $root_folder

# change input constraints to the interval center
for f in $(ls /root/abduction_algorithm/instances/$benchmark_name/*)
do
    python $python_scripts_folder/center_instance.py $f $number_of_variables
done

# create new output constraints
for f in $(ls /root/abduction_algorithm/instances/$benchmark_name/*)
do
    #update ymal config file for the current instance
    python $python_scripts_folder/modify_config_file.py $config_file_address $f
    #compute forward pass by running the verifier. this is slow, but it's done for practical purposes.
    python $alpha_beta_crown_folder/abcrown.py --config $config_file_address > $forward_pass_folder/forward_pass.txt
    #modify output constraints
    python $python_scripts_folder/output_constraints_$benchmark_name.py $f $forward_pass_folder
    #remove forward pass file
    rm $forward_pass_folder/forward_pass.txt
    #remove output file generated by the verifier
    rm $root_folder/out.txt
done
