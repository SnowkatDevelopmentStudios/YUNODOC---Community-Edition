# Creates a documentation table based off the DOC comment style
# Copyright (C) 2017  Snowkat Development Studios
# Developed by: Ian Cronkright 2017
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License,
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import getopt
import re


def main():
    print("yunodoc  Copyright (C) 2017 Snowkat Development Studios - Developed by: Ian Cronkright")
    print("This program comes with ABSOLUTELY NO WARRANTY.  This is free")
    print("software, and you are welcome to redistribute it under certain")
    print("conditions contained in the license.")
    print("")

    try:
        opts, args = getopt.getopt(sys.argv[1:], "isf:", ["ian", "r3s", "file="])
    except getopt.GetoptError:
        sys.exit(2)

    flag_ian = False
    flag_steven = False
    flag_file = ""

    for opt, arg in opts:
        if opt in ('-s', '--steven'):
            flag_ian = False
            flag_steven = True
        elif opt in ('-i', '--ian'):
            flag_ian = True
            flag_steven = False
        elif opt in ('-f', '--file'):
            flag_file = arg
        else:
            print("-i, --ian    -s, --steven    -f, --file <input>")
            sys.exit(2)

    m_doc_line_object = re.compile(r"(#|\/\/ DOC .*)", re.IGNORECASE)
    m_var_to_typ_object = re.compile(r"VAR (.*?) TYP", re.IGNORECASE)
    m_typ_to_pur_object = re.compile(r"TYP (.*?) PUR", re.IGNORECASE)
    m_pur_and_after_object = re.compile(r"PUR (.*)", re.IGNORECASE)

    doc_var_list = []
    doc_typ_list = []
    doc_pur_list = []

    if flag_file is not "":
        with open(flag_file) as file:
            for line in file:

                if re.match(m_doc_line_object, line):

                    if re.search(m_var_to_typ_object, line):
                        doc_var = re.search(m_var_to_typ_object, line)
                        doc_var_list.append(str(doc_var.group()))

                    if re.search(m_typ_to_pur_object, line):
                        doc_typ = re.search(m_typ_to_pur_object, line)
                        doc_typ_list.append(str(doc_typ.group()))

                    if re.search(m_pur_and_after_object, line):
                        doc_pur = re.search(m_pur_and_after_object, line)
                        doc_pur_list.append(str(doc_pur.group()))
    else:
        print("You must provide an input")
        print("-i, --ian    -s, --steven    -f, --file <input>")
        sys.exit(2)

    if not len(doc_var_list) == 0 or not len(doc_typ_list) == 0 or not len(doc_pur_list) == 0:
        longest_doc_var = max(len(s) for s in doc_var_list)
        longest_doc_typ = max(len(s) for s in doc_typ_list)
        longest_doc_pur = max(len(s) for s in doc_pur_list)

        if longest_doc_var < 11:
            longest_doc_var = 11

        if longest_doc_typ < 6:
            longest_doc_typ = 6

        if longest_doc_pur < 9:
            longest_doc_pur = 9

        table_separator_doc_var = ""
        for i in range(0, longest_doc_var):
            table_separator_doc_var += "-"

        table_separator_doc_typ = ""
        for i in range(0, longest_doc_typ):
            table_separator_doc_typ += "-"

        table_separator_doc_pur = ""
        for i in range(0, longest_doc_pur):
            table_separator_doc_pur += "-"

        output_table = ""

        if flag_ian:
            table_separator = "# ----{0}---- # ----{1}---- # ----{2}---- #".format(
                table_separator_doc_var,
                table_separator_doc_typ,
                table_separator_doc_pur
            )

            table_heading = "#     {0:{1}}     #     {2:{3}}     #     {4:{5}}     #".format(
                "~Variables~", longest_doc_var,
                "~Type~", longest_doc_typ,
                "~Purpose~", longest_doc_pur
            )

            output_table += (table_separator + "\n")
            output_table += (table_heading + "\n")
            output_table += (table_separator + "\n")

            for i, val in enumerate(doc_var_list):
                output_table += "#     {0:{1}}     #     {2:{3}}     #     {4:{5}}     #\n".format(
                    doc_var_list[i], longest_doc_var,
                    doc_typ_list[i], longest_doc_typ,
                    doc_pur_list[i], longest_doc_pur
                )

            output_table += (table_separator + "\n")

        elif flag_steven:
            table_separator = "#-{0}-|-{1}-|-{2}-|".format(
                table_separator_doc_var,
                table_separator_doc_typ,
                table_separator_doc_pur
            )

            table_heading = "# {0:^{1}} | {2:^{3}} | {4:^{5}} |".format(
                "~Variables~", longest_doc_var,
                "~Type~", longest_doc_typ,
                "~Purpose~", longest_doc_pur
            )

            output_table += (table_separator + "\n")
            output_table += (table_heading + "\n")
            output_table += (table_separator + "\n")

            for i, val in enumerate(doc_var_list):
                output_table += "# {0:^{1}} | {2:^{3}} | {4:^{5}} |\n".format(
                    doc_var_list[i], longest_doc_var,
                    doc_typ_list[i], longest_doc_typ,
                    doc_pur_list[i], longest_doc_pur
                )

            output_table += (table_separator + "\n")

        else:
            print("You must provide a style flag")
            print("-i, --ian    -s, --steven")
            sys.exit(2)

        print(output_table)

    else:
        print("Found no doc comments")


if __name__ == '__main__':
    main()
