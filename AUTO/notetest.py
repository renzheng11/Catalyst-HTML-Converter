import re

file1 = open("test.md", "r")
file2 = open("test.html", "w")

with file1 as md, file2 as html:

    note = "\^\d+\^"

    for line in md:
        #if any part of line has a note superscript number
        if re.match(note, line):
            print("match!!! at " + line)