#import libraries
import re
# import pandoc

#pandoc command: pandoc -s test.docx -o test.md

# file1 = open("Auto/lil.md", "r")

# with file1 as md:
#     for i in range(30):
#         line = md.readline()
#         print(line)
#         if re.search("\n", line):
#             print("new line")

# file1.close()

print("""
___
___
___

""")

#START
file1 = open("Auto/test.md", "r")
file2 = open("Auto/test.html", "w")

writtenSections = []
topNotes = []

# note in body: <sup><a href="#note1b" id="note1t">1</a></sup>
# note in note links: 
   

notePattern = "\^\d+\^"
onBottom = False
def testForNote(line):
    if re.search(notePattern, line):
        
        match = re.search(notePattern, line).group()
        noteNum = match.strip("^")
        topNotes.append(noteNum)

        # print(f"Match - Note {noteNum}: " + line)
        # print("topNotes: " + str(topNotes))

        if (topNotes.count("1") == 2): # reached bottom Notes section
            lastNote = noteNum
            writeNotes(line, lastNote)

        noteLink = f'<sup><a href="#note{noteNum}b" id="note{noteNum}t">{noteNum}</a></sup>'
        line = line.replace(match, noteLink)
    
    return (line)

def writeNotes(line, lastNote):
    print("starting writeNotes on: " + line)
    # match = re.search(notePattern, line).group()
    noteNum = 1
    noteContent = ""
    #strip line of ^#^
    line = re.sub("\^\d*\^\s+", "", line)
    # add first line of note 1
    noteContent += line

    for l in md:
        if l == "### References\n":
            # reached end of notes, REPLACE !!!
            break
        #until next note

        print("On [LINE]: " + l)
        # print(re.search(notePattern, l))
        
        if (re.search(notePattern, l)):
            # hit next note
            print(l[0:10] + "... matches, [STOP], move onto next note")
            # add complete previous note to html
            
            html.write(
                f"""
                <div id="note{noteNum}b">
                    <p class="notes">
                        <sup><a href="#note{noteNum}t">{noteNum}</a></sup> {noteContent}
                    </p>
                </div>
                """
            )

            



            # reset noteContent
            print("resetting contents")
            #reset note contents
            noteContent = ""

            # add first line of note to contents
            l = re.sub("\^\d*\^\s+", "", l)
            noteContent += l
            noteNum += 1

        else: #note still going
            #add to contents
            noteContent += l
            print("noteContent = " + noteContent)

    print("return writeNotes()")
    return


#function: read all text until next section
lastSection = ""
def readContents(last):
    contents = ""
    active = True
    while active:
        line = md.readline() #read next line
        #if it is not empty and has text
        if (line == "\n"):
            contents += "<br><br>"
        # elif (line.replace("#", "")).replace(" ", "") != "": 
        #if the line is a section title
        anySectionTitle = "^###.+"
        if re.match(anySectionTitle, line):
            # md.readline() #skip newline after section title
            # line is a section title

            #add section name to writtenSections list
            strippedSection = line.replace("#", "").strip()
            writtenSections.append(strippedSection)
            
            return (contents, line)

        # otherwise it is body text
        else:
            line = testForNote(line)
            
            #add line to contents
            contents += line 

        

#---------start regex filtering and html writing--------
with file1 as md, file2 as html:
    topItems = []
    #reads top of doc in order (not accurately matched)
    for line in md:
        #if line matches abstract
        if re.match("### Abstract(\s+)?", line):
            break
        else:
            #strip line of #'s
            stripHash = line.strip("#")
            #if line is whitespace
            if stripHash.strip() == "":
                continue #to next line
            else:
                #add all lines to topItems
                topItems.append(line)

    #-------Store authors-------
    authors = {}
    # format: "{0: [author, affil, contact], 1: [author, affil, contact]}"
    logo = topItems[0]
    title = topItems[1].strip("#").strip()

    #delete logo and title from topItems
    del topItems[0:2]

    #store author names for metadata
    topIndex = 0
    keyIndex = 0
    topLength = len(topItems)
    
    while topLength != 0:
        author = topItems[topIndex].strip()
        affil = topItems[topIndex + 1].strip()
        contact = topItems[topIndex + 2].strip()

        authors[keyIndex] = [author, affil, contact]

        topLength -= 3
        topIndex += 3
        keyIndex += 1

    authorNames = ""
    for i in range(len(authors)):
        authorNames += (authors[i][0])
        if i < (len(authors) - 1):
            authorNames += ", "

    # ABSTRACT AND KEYWORDS
    md.readline()
    abstract, lastSection = readContents(lastSection)
    keywords, lastSection = readContents(lastSection)

    #write html head with metadata + styling
    html.write(f"""
        <html>

        <head>
            <link href="https://fonts.googleapis.com/css?family=Catamaran&display=swap" rel="stylesheet">
            <meta content="text/html; charset=UTF-8" http-equiv="content-type">
            <meta charset="UTF-8">`
            <meta name="description" content="{title}">
            <meta name="keywords"
                content="{keywords}">
            <meta name="author" content="{authorNames}">

        <!--PAGE STYLING-->

        <!--INCLUDE ALL CSS CLASSES HERE-->

        <style type="text/css">
            /* For all hyperlinks */
            a \u007b
                color: #000099;
            \u007d

            /* CSS class for authorBio*/
            .authorBio \u007b
                margin: 0;
                color: #000000;
                font-size: 12pt !important;
                font-family: 'Catamaran', sans-serif !important;
            \u007d

            /* CSS class for authorBio*/
            .authorName \u007b
                color: #000099;
                font-size: 13pt;
                font-family: 'Catamaran', sans-serif;
            \u007d

            /* For all normal text */
            .c1 \u007b
                color: #000000;
                font-weight: 400;
                text-decoration: none;
                vertical-align: baseline;
                font-size: 12pt;
                line-height: 1.6;
                font-family: 'Catamaran', sans-serif;
                font-style: normal;
            \u007d

            /* For the whole <body> shape */
            .c5 \u007b
                background-color: #ffffff;
                max-width: 600pt;
                padding: 72pt 72pt 72pt 150pt;
            \u007d

            /* For when your quote itself has another quote/dialog */
            .doubleIndent \u007b
                font-size: 12pt;
                position: relative;
                margin-left: 50px;
                width: 545px;
            \u007d

            .figure \u007b
                height: Auto;
                max-width: 100%;
                position: relative;
            \u007d

            /* For image captions */
            .imagetext \u007b
                position: relative;
                padding-top: 10pt;
                color: dimgray;
                font-weight: 700;
                text-decoration: none;
                vertical-align: baseline;
                font-size: 10pt;
                font-family: 'Catamaran', sans-serif;
                font-style: normal;
            \u007d

            /* For list formatting */
            ol \u007b
                margin: 0;
                padding: 0;
            \u007d

            /* For list item formatting */
            li \u007b
                color: #000000;
                font-size: 11.5pt;
                font-family: 'Catamaran', sans-serif;
            \u007d

            /*Only used for gap between Catalyst Logo and paper title/type*/
            .logoGap \u007b

                padding-top: 18pt;
                color: #666666;
                font-size: 24pt;
                padding-bottom: 4pt;
                font-family: 'Catamaran', sans-serif;
                line-height: 1.8909090215509587;
                page-break-after: avoid;
                font-style: italic;
                text-align: left;
            \u007d

            .notes \u007b
                font-size: 12pt;
                line-height: 1.2;
            \u007d

            /*Baseline paragraph formatting*/
            p \u007b
                margin: 0;
                color: #000000;
                font-size: 12pt;
                font-family: 'Catamaran', sans-serif;
            \u007d

            .paperTitle \u007b
                font-family: 'Catamaran', sans-serif;
                font-size: 18pt;
                color: #000099;
            \u007d

            /* CSS class for poem */
            .poem \u007b
                font-style: italic;
                font-size: 11.5pt;
                font-family: 'Catamaran', sans-serif;
            \u007d

            .quotes \u007b
                font-size: 11.5pt;
                font-family: 'Catamaran', sans-serif;
                position: relative;
                margin-left: 50px;
                width: 645px;
                line-height: 1.35;
            \u007d

            /*CSS class for references*/
            .reference \u007b
                margin: 0;
                color: #000000;
                font-size: 11.5pt !important;
                font-family: 'Catamaran', sans-serif !important;
                line-height: 1.35 !important;
                margin-bottom: 11pt;
            \u007d

            .sectionTitle \u007b
                font-size: 17pt;
            \u007d

            .subsectionTitle \u007b
                font-size: 14pt;
                /* font-weight: bold; */
            \u007d

            .sub_subsectionTitle \u007b
                font-size: 12pt;
                font-weight: bold;
            \u007d

            table td,
            table th \u007b
                padding: 0;
            \u007d

            /*Making the webpage responsive*/
            @media only screen and (max-device-width: 480px) \u007b
                body \u007b
                    width: 112% !important;
                    margin-left: 4px;

                \u007d

                .logo \u007b
                    position: relative;
                    right: 27%;
                    width: 451px;
                    height: 164px
                \u007d

                .c5 \u007b
                    max-width: 100%;
                \u007d

                .type \u007b
                    font-size: 33px;
                \u007d
            \u007d
        </style>

        <!--PAGE STYLING ENDS-->
        </head>
    """)

    #write logo + title
    html.write(f"""
        <body class="c5">
        <img class="logo" style="width: 377px; height: 105px; position: relative; right:1%; top: 5%; display: block;"
            alt="Catalyst logo" src="https://drive.google.com/uc?export=view&id=1Y40wZQ6cQZFlrMDNx9n9jECr6xG-gbMK"
            align="right">
        <p class="logoGap">&nbsp;</p>
        <p class="logoGap">&nbsp;</p>
        <div class="c1"></div>
        <p class="c1 type">Article Type</p>
        <p class="paperTitle">
            {title}
        </p>
        <p class="c1">&nbsp;</p>
        <p class="c1">&nbsp;</p>
    """)

    # write authors
    for i in range(len(authors)):
        if i < (len(authors)):
            html.write(f"""
                <p class="authorName">
                {authors[i][0]}
                </p>
                <p class="c1">
                    {authors[i][1]}
                    <br>
                    {authors[i][2]}
                </p>

                <p class="c1">&nbsp;</p>
                <p class="c1">&nbsp;</p>
            """
            )

    # write abstract + keywords
    html.write(f"""
        <!--Main Body-->
        <p class="c1 sectionTitle">Abstract</p>
        <p class="c1">{abstract}</p>

        <p class="c1 sectionTitle">
        Keywords
        </p>
        <p class="c1">
            {keywords}
        </p>
    """)

    #-------Read sections-------
    sectionTitle = "^#{3}\s.*$"
    subsectionTitle = "^#{4}\s.*$"
    subsubsectionTitle = "^^#{5}\s.*$"

    for line in md:
        #if lastSection matches sectionTitle
        if re.match(sectionTitle, lastSection):
            lastSection = lastSection.strip("#").strip()
            html.write(f"""<p class="c1 sectionTitle">{lastSection}</p>""")

        #if lastSection matches subsectionTitle
        elif re.match(subsectionTitle, lastSection):
            lastSection = lastSection.strip("#").strip()
            html.write(f"""<p class="c1 subsectionTitle">{lastSection}</p>""")

        #if lastSection matches subsubsectionTitle
        elif re.match(subsubsectionTitle, lastSection):
            lastSection = lastSection.strip("#").strip()
            html.write(f"""<p class="c1 subsectionTitle">{lastSection}</p>""")

        # write body text under section title
        bodyText, lastSection = readContents(lastSection)

        html.write(f"""<p class="c1">{bodyText}</p>""")
        # html.write("""<p class="c1">&nbsp;</p>""")

        bioPattern = "### Author Bio\s+"
        if re.match(bioPattern, lastSection):
            break

    html.write(f"""<p class="c1 sectionTitle">Author Bio</p>""")
    authorBio = ""
    for line in md:
        authorBio += line
    html.write(f"""<p class="c1">{authorBio}</p>""")



print("close files")
#close files
md.close()
html.close()

#fix EM dash !!!