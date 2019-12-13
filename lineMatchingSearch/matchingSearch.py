"""Author: Bar Perlman.
The following script searches for lines matching regular expression in file/s"""

import sys
import re


"""The following function check the inserted command line arguments are in the valid format"""
def check_params_validity(arguments_list):
    minimum_params = 3  # amount of minimum params the program expects to receive
    is_params_valid = True
    params_set = set(arguments_list)
    if "-r" not in params_set and "--regex" not in params_set:
        is_params_valid = False
    if len(arguments_list) < minimum_params:
        is_params_valid = False
    return is_params_valid


arguments_list = sys.argv  # Holds the command line parameters as list
# Check the validity of the inserted parameters for the program
is_valid_args = check_params_validity(arguments_list)
if is_valid_args:
    print("there is r")
# index_of_regex = arguments_list.index("-r")




