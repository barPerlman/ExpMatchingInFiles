"""Author: Bar Perlman.
This PrinterFactory class is based on the principles of the Factory Design Pattern"""
import re


class PrinterFactory:
    def create_printer(self, output_type):
        if output_type is None:
            return RegularPrinter()
        if output_type == "-u":
            return UnderscorePrinter()


class Printer:
    def print_output(self, files_dictionary, regex):
        pass


class RegularPrinter(Printer):
    def print_output(self, files_dictionary, regex):
        for file in files_dictionary:
            print("___________________________________________________________________________")
            print("File name: %s" % file)
            for match in files_dictionary[file]:
                print("Line number: %d | The Line: %s" % (match[0], match[1]))


def find_start_pos(line, regex):
    return re.search(regex, line).start()


class UnderscorePrinter(Printer):
    def print_output(self, files_dictionary, regex):
        for file in files_dictionary:
            print("___________________________________________________________________________")
            print("File name: %s" % file)
            for match in files_dictionary[file]:
                line = match[1]
                line_num = match[0]
                print("Line number: %d" % line_num)
                print("The Line: %s" % line, end='', flush=True)
                # Print ^ under the matching text
                start_pos = find_start_pos(line, regex)  # Start pos inside line
                # Update the start pos with the prefix output line:
                start_pos = start_pos + len("The Line: ")
                for i in range(0, len(line) + len("The Line: ") - 1):
                    if i == start_pos:
                        while i < start_pos + len(regex):
                            print("^", end='', flush=True)
                            i = i + 1
                    else:
                        print(" ", end='', flush=True)
                print("")
