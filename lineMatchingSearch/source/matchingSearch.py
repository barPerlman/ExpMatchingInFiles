"""Author: Bar Perlman.
The following script searches for lines matching regular
expression in file/s"""

import sys
import re


"""Returns a range for files to look at in argv list.
In there are no such files in list, returns None"""


def get_range_of_files(arguments_list):
    params_set = set(arguments_list)
    not_valid_index = -1
    first_index = not_valid_index
    last_index = not_valid_index
    if "-f" in params_set:
        first_index = arguments_list.index("-f") + 1
    elif "--files" in params_set:
        first_index = arguments_list.index("--files") + 1
    if first_index > -1:  # Found index for the first file
        last_index = first_index
        # Find the last index of a file in arguments list
        while last_index < len(arguments_list) - 1 \
                and not arguments_list[last_index].startswith("-"):
            last_index = last_index + 1
    files_list = [first_index, last_index]
    if first_index == not_valid_index or last_index == not_valid_index:
        return None
    return files_list


"""Get the reg format or None if not exist"""


def get_reg_format(arguments_list):
    params_set = set(arguments_list)
    if "-r" in params_set:
        return "-r"
    if "--regex" in params_set:
        return "--regex"
    return None


"""The following function check the inserted command line arguments are 
in the valid format"""


def check_params_validity(arguments_list):
    minimum_params = 4  # amount of min. params the program expects to receive
    is_params_valid = True
    params_set = set(arguments_list)
    if get_reg_format(arguments_list) is None:  #check if reg option is exist
        is_params_valid = False
    if len(arguments_list) < minimum_params:
        is_params_valid = False
    return is_params_valid


arguments_list = sys.argv  # Holds the command line parameters as list

# Check the validity of the inserted parameters for the program
is_valid_args = check_params_validity(arguments_list)
if not is_valid_args:
    raise SystemExit("Wrong command line arguments format!")

# Get the regex and the files names from the arguments
regex_str_index = arguments_list.index(get_reg_format(arguments_list)) + 1
# regex holds the string to find in files
regex = arguments_list[regex_str_index]
# get the range to get the files names from in the arguments list
files_range_in_argv = get_range_of_files(arguments_list)
print(files_range_in_argv)

#files_list = get_files_list(arguments_list)

