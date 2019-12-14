"""Author: Bar Perlman.
This PrinterFactory class is based on the principles of the Factory Design Pattern"""
import re


yellow = "\x1b[1;33;1m{}\x1b[0m"  # color to highlight a matching text


class PrinterFactory:
    def create_printer(self, output_type):
        if output_type == "-u":
            return UnderscorePrinter()
        if output_type == "-m":
            return MachinePrinter()
        if output_type == "-c":
            return ColorPrinter()
        else:  # Output style is not inserted
            return RegularPrinter()


class Printer:
    def print_output(self, files_dictionary, regex):
        pass


"""Responsible for printing in a default manner """


class RegularPrinter(Printer):
    def print_output(self, files_dictionary, regex):
        for file in files_dictionary:
            if len(files_dictionary[file]) > 0:
                print("___________________________________________________________________________")
                print("File name: %s" % file)
            for match in files_dictionary[file]:
                print("Line number: %d | The Line: %s" % (match[0], match[1]))


"""Return all indices of matches in line of the reveived regex"""


def find_start_pos(line, regex):
    iter = re.finditer(regex, line)
    start_positions = [match_pos.start(0) for match_pos in iter]
    return start_positions


def mark_sign_under_match(sign, start_iter, start_pos, line, regex):
    for i in range(start_iter, len(line) + len("The Line: ") - 1):
        if i == start_pos:
            while i < start_pos + len(regex):
                print(sign, end='', flush=True)
                i = i + 1
            return
        else:
            print(" ", end='', flush=True)


"""This class generate machine readable output format"""


class MachinePrinter(Printer):
    def print_output(self, files_dictionary, regex):
        for file in files_dictionary:
            if len(files_dictionary[file]) > 0:
                print("___________________________________________________________________________")
            for match in files_dictionary[file]:
                line = match[1]
                no_line = match[0]
                start_poses = find_start_pos(line, regex)  # Start pos inside line
                for pos in start_poses:
                    # For each match in line print in the readable output
                    # format: file_name:no_line:start_pos:matched_text
                    print("%s:%d:%d:%s" % (file, no_line, pos, regex))


"""This class responsible to print the output in underscore manner"""


class UnderscorePrinter(Printer):
    def print_output(self, files_dictionary, regex):
        for file in files_dictionary:
            if len(files_dictionary[file]) > 0:
                print("___________________________________________________________________________")
                print("File name: %s" % file)
            for match in files_dictionary[file]:
                line = match[1]
                line_num = match[0]
                print("Line number: %d" % line_num)
                print("The Line: %s" % line, end='', flush=True)
                # Print ^ under the matching text
                start_poses = find_start_pos(line, regex)  # Start pos inside line
                start_iter = 0  # index where we last print the ^ + 1
                for pos in start_poses:
                    pos = pos + len("The Line: ")
                    mark_sign_under_match("^", start_iter, pos, line, regex)
                    start_iter = pos + len(regex)
                print("")


"""Class which responsible for output the matches in highlight manner"""


class ColorPrinter(Printer):
    def print_output(self, files_dictionary, regex):
        colored_regex = '\x1b[1;33;1m{}\x1b[0m'.format(regex)  # Colorize regex in bold yellow
        for file in files_dictionary:
            if len(files_dictionary[file]) > 0:
                print("___________________________________________________________________________")
                print("File name: %s" % file)
            for match in files_dictionary[file]:
                line = match[1]
                line_no = match[0]
                colored_line = re.sub(regex, colored_regex, line)
                print("Line number: %d | The Line: %s" % (line_no, colored_line))

