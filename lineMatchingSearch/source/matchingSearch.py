"""Author: Bar Perlman.
The following script searches for lines matching regular
expression in file/s"""

import sys
import re

from source.PrinterFactory import PrinterFactory


def is_matched(files_dictionary):
    for file in files_dictionary:
        if len(files_dictionary[file]) > 0:
            return True
    return False



"""returns true if in case the list optional parameters exist as arguments 
implies they are mutually exclusive"""


# Be aware: you should update this in case of extension of list optional params
def is_output_format_exclusive(params_set):
    parallel_amount_of_flags = 0
    if "-u" in params_set or "--underscore" in params_set:
        parallel_amount_of_flags = parallel_amount_of_flags + 1
    if "-c" in params_set or "--color" in params_set:
        parallel_amount_of_flags = parallel_amount_of_flags + 1
    if "-m" in params_set or "--machine" in params_set:
        parallel_amount_of_flags = parallel_amount_of_flags + 1
    if parallel_amount_of_flags > 1:
        return False
    return True


"""The following responsible to return the requested output format
or None in case there is no preferred one"""


def get_print_type(args_list):
    args_set = set(args_list)
    # The following will check for each optional parameters of output format
    if "-u" in args_set or "--underscore" in args_set:
        return "-u"
    if "-c" in args_set or "--color" in args_set:
        return "-c"
    if "-m" in args_set or "--machine" in args_set:
        return "-m"
    else:
        return None


def check_file_existence(files_dictionary):

    for file in files_dictionary:
        try:
            open(file, "r")
        except IOError:
            return False
    return True




"""Updates the files dictionary with matches lines and their numbers"""


def search_matches(files_dictionary):
    for file_path in files_dictionary:
        with open(file_path, "r") as file:
            line_no = 1
            current_line = file.readline()
            while current_line:
                if re.search(regex, current_line):
                    files_dictionary[file_path].append((line_no, current_line))
                line_no = line_no + 1
                current_line = file.readline()


""" Create and returns a dictionary includes the files names to search at
 as a key. Return None if there are no files in args_list"""


def create_files_dictionary(args_list):
    # get the range from in the arguments list where the files are located
    files_range_in_argv = get_range_of_files(args_list)
    files_dictionary = {}
    if files_range_in_argv is not None:
        for file in args_list[files_range_in_argv[0]:files_range_in_argv[1] + 1:]:
            files_dictionary.setdefault(file, [])
        return files_dictionary
    return None


"""Returns a range for files to look at in argv list.
If there are no such files in list, returns None"""


def get_range_of_files(args_list):
    params_set = set(args_list)
    not_valid_index = -1
    first_index = not_valid_index
    last_index = not_valid_index
    if "-f" in params_set:
        first_index = args_list.index("-f") + 1
    elif "--files" in params_set:
        first_index = args_list.index("--files") + 1
    if first_index > -1:  # Found index for the first file
        last_index = first_index
        # Find the last index of a file in arguments list
        while last_index < len(args_list) - 1 \
                and not args_list[last_index].startswith("-"):
            last_index = last_index + 1
    files_list = [first_index, last_index-1]
    if first_index == not_valid_index or last_index == not_valid_index:
        return None
    return files_list


"""Get the reg format or None if not exist"""


def get_reg_format(args_list):
    params_set = set(args_list)
    if "-r" in params_set:
        return "-r"
    if "--regex" in params_set:
        return "--regex"
    return None


"""The following function check the inserted command line arguments are 
in the valid format"""


def check_params_validity(args_list):
    minimum_params = 4  # amount of min. params the program expects to receive
    is_params_valid = True
    params_set = set(args_list)
    if get_reg_format(args_list) is None:  # Check if reg option is exist
        is_params_valid = False
    if len(args_list) < minimum_params:
        is_params_valid = False
    # Check that optional parameters are mutually exclusive
    if not is_output_format_exclusive(params_set):
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


# Construct a dictionary of files
files_dict = create_files_dictionary(arguments_list)
# In case there are no files in the arguments, ask for files from STDIN
if files_dict is None:
    ask_for_files = True
    is_file_exist = False
    while ask_for_files:
        print("Couldn't find any file in the command.\n"
              "Please insert the prefix '-f' and then the file(s) name(s)"
              "with spaces between them or 'x' to Exit.")
        received_input = sys.stdin.readline()
        if received_input.endswith("\n"):
            received_input = received_input[:-1]
        input_as_list = received_input.split(" ")
        if received_input == "x" or received_input == "X":
            sys.exit("Exited.")
        files_dict = create_files_dictionary(input_as_list)

        if files_dict is not None:
            is_files_exist = check_file_existence(files_dict)
            if is_files_exist:
                ask_for_files = False


# Search for expressions matches in files and updates the dictionary with lines
# and their numbers
searched_successfully = search_matches(files_dict)
# No matches were found
if not is_matched(files_dict):
    sys.exit("Sorry, but no matches were found in the file(s) for the inserted expression.\n"
             "Exited.")
print_type = get_print_type(arguments_list)  # Get printing format

printer_factory = PrinterFactory()  # Get the Printers factory
# Concrete printer by the inserted output type
printer = printer_factory.create_printer(print_type)
printer.print_output(files_dict, regex)

