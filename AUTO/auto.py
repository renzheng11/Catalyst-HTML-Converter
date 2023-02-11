#import libraries
import re
# import pandoc

#PATTERNS
patternAbstract = "### Abstract"
sectionTitle = "^###\s.*$"
subsectionTitle = "^####\s.*$"
subsubsectionTitle = "^#####\s.*$"



#START
f = open("demo.html", "w")
f.write("""

<html>

<head>
    <link href="https://fonts.googleapis.com/css?family=Catamaran&display=swap" rel="stylesheet">
    <meta content="text/html; charset=UTF-8" http-equiv="content-type">
    <meta charset="UTF-8">
    <meta name="description" content="Data Surrogates as Hosts: Politics of Environmental Governance">
    <meta name="keywords"
        content="keywords">
    <meta name="author" content="Author Name">

    <!--PAGE STYLING-->
""")

f.close()

f = open('demo.md', "r")

next = f.readline() #logo
next = f.readline() #space
next = f.readline() #space
next = f.readline() #space

title = f.readline() #title
print("title: " + title)

next = f.readline() #space
author = f.readline() #author
print("author: " + author)
next = f.readline() #space
affil = f.readline() #affil
print("affil: " + affil) 
next = f.readline() #space
contact = f.readline() #contact
print("contact: " + contact)

#-----------start regex filtering----------
print("*** starting regex ***")


with f as file:
    for line in file:
        stripHashtag = line.strip("#")
        if stripHashtag.strip() == "":
            print("empty line: " + line) 
        else:
            if re.match(sectionTitle, line):
                print("Section: " + line)
            if re.match(subsectionTitle, line):
                print("Subsection: " + line)
            if re.match(subsubsectionTitle, line):
                print("Subsubsection: " + line)



f.close()

print("stripping #")
print("beg" + "### ".strip("#") + "end")