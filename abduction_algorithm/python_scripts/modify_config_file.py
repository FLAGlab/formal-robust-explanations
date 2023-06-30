import yaml
import sys

#argv[1] config_file_address
#argv[2] property address

config_file_address = sys.argv[1]
property_address = sys.argv[2]

with open(config_file_address,"r") as file:
    config_file = yaml.safe_load(file)
    config_file["specification"]["vnnlib_path"] = property_address

with open(config_file_address,"w") as file:
    yaml.dump(config_file,file,sort_keys=False)

