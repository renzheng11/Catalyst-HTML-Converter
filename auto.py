
# ---------------------------
# Author: Ren Zheng
# rzheng11@gatech.edu
# ---------------------------

#import libraries
import re
import os

# import pandoc

# ------ Manual Todo (not done by script) ------

    # temporary: 
        # This scripts converts markdown files (.md) to (.html)
        # to convert (.docx) to markdown (.md), use the command:
        # pandoc -s name.docx -o name.md
            # (pandoc can be installed at https://pandoc.org/installing.html)
            # option 2: use a web converter to get (.md) file

    # change article type before title (not including in docx)

    # if there are issues with text formatting, make sure the styling headings in docx are correct and rerun
    # if there are issues with text content, search for it in html to change it

# Global variables
lastSection = ""
writtenSections = []
topNotes = []

# refactor this !!
# Function: replace markdown styles with html styling tags 
def styleText(text, lastSection):
    # strip all newlines so text is one string
    text = re.sub("\n", "", text)

    # Replace three --- em dash —
    dashPattern = "---"
    searchResult = re.search(dashPattern, text)
    if searchResult: #found match
        matchList = re.findall(dashPattern, text)

        for item in matchList:
            itemPattern = "---"
            replacement = "—"
            text = re.sub(itemPattern, replacement, text)

    # Replace two -- em dash –
    dashPattern = "--"
    searchResult = re.search(dashPattern, text)
    if searchResult: #found match
        matchList = re.findall(dashPattern, text)

        for item in matchList:
            itemPattern = "--"
            replacement = "–"
            text = re.sub(itemPattern, replacement, text)

    # Replace instances of Apostrophes \'
    aposPattern = "\\\'"
    searchResult = re.search(aposPattern, text)
    if searchResult: #found match
        matchList = re.findall(aposPattern, text)

        for item in matchList:
            itemPattern = '\\\'' + item.strip("\'")
            replacement = "'"
            text = re.sub(itemPattern, replacement, text)

    # Replace "quote marks" with “quote marks”
    # quotePattern = "\"[^\x22]+\""
    # searchResult = re.search(quotePattern, text)
    # if searchResult: #found match
    #     matchList = re.findall(quotePattern, text)

    #     for item in matchList:
    #         itemPattern = '\"' + item.strip("\"") + '\"'
    #         replacement = "“" + item.strip("\"") + "”"
    #         text = re.sub(itemPattern, replacement, text)

    # Replace instances of ^superscripts^ (not notes)
    superPattern = "\^[^\d]{2}\^"
    searchResult = re.search(superPattern, text)
    if searchResult: #found match
        matchList = re.findall(superPattern, text)
        for item in matchList:
            itemPattern = '\^' + item.strip("\^") + '\^'
            replacement = "<sup>" + item.strip("\^") + "</sup>"
            text = re.sub(itemPattern, replacement, text)
    
    # Replace instances of ellipses \...
    ellipsePattern = "\\\.\.\."
    searchResult = re.search(ellipsePattern, text)
    if searchResult: #found match
        matchList = re.findall(ellipsePattern, text)

        for item in matchList:
            itemPattern = "\\\.\.\." + item.strip("\...")
            replacement = "..."
            text = re.sub(itemPattern, replacement, text)

    # Replace instances of **bold** text
    # boldPattern = "\*\*.*\*\*"
    # searchResult = re.search(boldPattern, text)
    # if searchResult: #found match
    #     matchList = re.findall(boldPattern, text)

    #     for item in matchList:
    #         itemPattern = '\*\*' + item.strip("**") + '\*\*'
    #         replacement = "<strong>" + item.strip("**") + "</strong>"
    #         text = re.sub(itemPattern, replacement, text)

    # Replace instances of *italic* text
    italicPattern = "\*(?!\s)[\s\S]*?\*(?<!\s\*)"
    searchResult = re.search(italicPattern, text)
    if searchResult: #found match
        matchList = re.findall(italicPattern, text)

        for item in matchList:
            itemPattern = '\*' + item.strip("*") + '\*'

            ### fix this !!!
            # refPattern = "### Notes\s*"
            # if re.match(refPattern, lastSection):
            #     print("match ref")
            #     replacement = "<i>" + item.strip("*") + "</i>"
            #     print(replacement)
            # else:
            # replacement = "<em>" + item.strip("*") + "</em>"
            replacement = "<i>" + item.strip("*") + "</i>"
            text = re.sub(itemPattern, replacement, text)

    # Left bracket
    bracketPattern = "\\\\\["
    
    searchResult = re.search(bracketPattern, text)
    if searchResult: #found match
        matchList = re.findall(bracketPattern, text)

        for item in matchList:
            
            itemPattern = "\\\\\["
            replacement = "["
            text = re.sub(itemPattern, replacement, text)

    # Right bracket
    bracketPattern = "\\\\\]"
    
    searchResult = re.search(bracketPattern, text)
    if searchResult: #found match
        matchList = re.findall(bracketPattern, text)

        for item in matchList:
            
            itemPattern = "\\\\\]"
            replacement = "]"
            text = re.sub(itemPattern, replacement, text)

    # last pass - remove blackslash
    slashPattern = "\\\\"
    
    searchResult = re.search(slashPattern, text)
    if searchResult: #found match
        matchList = re.findall(slashPattern, text)

        for item in matchList:
            
            itemPattern = "\\\\"
            replacement = ""
            text = re.sub(itemPattern, replacement, text)

    return text

# Function: read all body text until next section
def readContents(last, md, html, authors):
    contents = ""

    if last == "Notes":
        line = writeNotes(md, html)
        return (contents, line)

    active = True
    inList = False
    listNum = 0
    itemtext = ""
    nextLine = ""

    while active:
        #read next line
        # if itemtext:
        #     line = itemtext
        # else:
        line = md.readline() 

        #if empty line
        if (line == "\n"):
            contents += "<br><br>"

        # LISTS
        listPattern = r"-   \w*"

        if re.search(listPattern, line):
            print("on line: " + line)
            line = line.strip("-").strip()
            # starting list
            inList = True
            listNum += 1
            print("listNum" + str(listNum))
            
            # # on first item of list
            if listNum == 1:
                print("adding <ul>")
                contents += "<ul>"

            print("adding <li>")
            contents += "<li>"

        if inList and (line == "\n"):
            # end of item
            print("adding </li>")
            contents += "</li>"

            nextLine = md.readline()
            # itemtext = nextLine
            print("nextline: " + nextLine)

        if inList and nextLine.count("-") >= 1:
            print("another dash")
            # itemtext = nextLine
        elif inList and nextLine.count("-") == 0:
            print("adding </ul>")
            contents += "</ul>"
            inList = False
            print("end of list")
            return (contents, line)

        # NOT FINISHED !! images + figures 
        # Figure html
        figurePattern = r"\(?Figure \d\)?"
        
        searchResult = re.search(figurePattern, line)
        if searchResult: #found match
            # get first author last name
            figAuthor = authors[0][0].split(" ")[-1].lower()

            matchList = re.findall(figurePattern, line)

            for item in matchList:
                if item.count("(") == 1:
                    continue
                # get figure #
                figNum = re.findall("\d", item)[0]
                # print("figNum: " + figNum)

                # text = re.sub(itemPattern, replacement, text)

                # print(line)
                figContent = "replace with figContent"

                # until new line
                nextline = md.readline()
                # print("[nextline]: " + nextline)

                # add to figContents

                # print(f"""
                #     <img src="{figAuthor}figure{figNum}.jpg"
                #     alt="Replace image alt"
                #     style="height: Auto; max-width: 100%;;position: relative;">
                #     <p class="imagetext">Figure {figNum}. {figContent}</p>
                # """)

            # contents += f"""
            #         <img src="{figAuthor}figure{figNum}.jpg"
            #         alt="Replace image alt"
            #         style="height: Auto; max-width: 100%;;position: relative;">
            #         <p class="imagetext">Figure {figNum}. {figContent}</p>
            # """

        #if the line is a section title
        anySectionTitle = "^###.+"
        if re.match(anySectionTitle, line):
            #add section name to writtenSections list
            strippedSection = line.replace("#", "").strip()
            writtenSections.append(strippedSection)
            contents = styleText(contents, lastSection)

            contents = testForNote(contents, line)
            
            return (contents, line)

        # otherwise it is body text
        else:
            contents += " " + line 

# Function: test if line has a note
def testForNote(text, line):
    notePattern = "\^\d+\^"

    if re.search(notePattern, text):
        matchList = re.findall(notePattern, text)

        for item in matchList:
            noteNum = item.strip("^")
            topNotes.append(noteNum)

            # if doc reaches bottom Notes section
            if (topNotes.count("1") == 2):
                return line

            noteLink = f'<sup><a href="#note{noteNum}b" id="note{noteNum}t">{noteNum}</a></sup>'
            noteFullPattern = "\^" + noteNum + "\^"
            text = re.sub(noteFullPattern, noteLink, text)
    
    return text

# Function: Write each note in Notes section and link to top notes
def writeNotes(md, html):
    line = md.readline()
    noteNum = 1
    noteContent = ""

    # strip line of ^#^
    line = re.sub("\^\d*\^\s+", "", line)
    # add first line of note 1
    noteContent += line

    for l in md:
        sectionTitle = "^#{3}\s.*$" 
        if re.match(sectionTitle, l):
            # reached end of notes (hit References)
            # write last note:
            noteContent = styleText(noteContent, lastSection)
            html.write(
                f"""
                <div id="note{noteNum}b">
                    <p class="notes">
                        <sup><a href="#note{noteNum}t">{noteNum}</a></sup> {noteContent}
                    </p>
                </div>
                <p class="notes">&nbsp;</p>
                """
            )

            line = l
            break
        
        notePattern = "\^\d+\^"

        # if next note is hit
        if (re.search(notePattern, l)): 
            # add complete previous note to html
            noteContent = styleText(noteContent, lastSection)
            html.write(
                f"""
                <div id="note{noteNum}b">
                    <p class="notes">
                        <sup><a href="#note{noteNum}t">{noteNum}</a></sup> {noteContent}
                    </p>
                </div>
                <p class="notes">&nbsp;</p>
                """
            )

            #reset note contents
            noteContent = ""

            # add first line of note to contents
            l = re.sub("\^\d*\^\s+", "", l)
            noteContent += l

            noteNum += 1

        # if note still going
        else: 
            #add the line to contents
            noteContent += " " + l
    
    # when all notes are read
    return line

# Read references
def writeRefs(md, html):
    # write References sectionTitle
    html.write(
        f"""
        <p class="c1 sectionTitle">References</p>
        """
    )

    refContent = ""

    for l in md:
        sectionTitle = "^#{3}\s.*$" 
        if re.match(sectionTitle, l):
            # reached end of references (hit Author Bios reference)
            break 
        
        # if blank space is hit
        if l == "\n": 
            link = ""
            linkPattern = "<.*>\.*"
            searchResult = re.search(linkPattern, refContent)

            
            if searchResult: #found a link
                match = re.search(linkPattern, refContent).group()
                link = match.strip("<").strip(">.")
            refContent = re.sub(linkPattern, "", refContent)

            # convert markdown styles
            refContent = styleText(refContent, lastSection) 

            # add complete previous reference to html
            if link != "": #reference has a link
                html.write(
                    f"""
                    <p class="reference"> {refContent} <a href="{link}">{link}</a>.</p>
                    """
                )
            else: #reference does not have a link
                html.write(
                    f"""
                    <p class="reference"> {refContent}</p>
                    """
                )

            #reset note contents
            refContent = ""
            link = ""

        # if references still going
        else: 
            #add the line to contents
            refContent += " " + l
    return

def convertToHTML(file, lastSection):
    #---------start regex filtering and html writing--------

    fileName = str(file).strip(".md")
    # fileName = str(file).strip(".docx").strip(".m")

    mdfile = open(file, "r")
    htmlfile = open(f"{fileName}.html", "w")

    with mdfile as md, htmlfile as html:
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
        # authors: "{0: [author, affil, contact], 1: [author, affil, contact]}"
        authors = {}
        
        title = topItems[1].strip("#").strip()

        # delete logo and title from topItems
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
        abstract, lastSection = readContents(lastSection, md, html, authors)
        keywords, lastSection = readContents(lastSection, md, html, authors)
        keywords = keywords.strip("<br><br>")

        #write html head with metadata + styling
        html.write(f"""
            <html>

            <head>
                <link href="https://fonts.googleapis.com/css?family=Catamaran&display=swap" rel="stylesheet">
                <meta content="text/html; charset=UTF-8" http-equiv="content-type">
                <meta charset="UTF-8">
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
                """
                )
            if i == len(authors) - 1:
                html.write(f"""
                <p class="c1">&nbsp;</p>
                """)


        # write abstract + keywords
        html.write(f"""
            <!--Main Body-->
            <p class="c1 sectionTitle">Abstract</p>
            <p class="c1">{abstract}</p>

            <p class="c1">&nbsp;</p>

            <p class="c1 sectionTitle">
            Keywords
            </p>
            <p class="c1">
                {keywords}
            </p>
            <p class="c1">&nbsp;</p>
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
            bodyText, lastSection = readContents(lastSection, md, html, authors)

            refPattern = "### References\s*"
            if re.match(refPattern, lastSection):
                writeRefs(md, html)
                break

            html.write(f"""<p class="c1">{bodyText}</p>""")

            bioPattern = "### Author Bio[s]?\s*"
            if re.match(bioPattern, lastSection):
                #reached Author Bios - last section
                break

        if len(authors) == 1:
            html.write(f"""<p class="c1">&nbsp;</p><p class="c1">&nbsp;</p>
            <p class="c1 sectionTitle">Author Bio</p>""")
        else:
            html.write(f"""<p class="c1">&nbsp;</p><p class="c1">&nbsp;</p>
            <p class="c1 sectionTitle">Author Bios</p>""")
        authorBio = ""
        lineNum = 0
        for line in md:
            # until end of file
            lineNum += 1
            if line == "\n" and lineNum > 2:
                authorBio += "<br><br>"
            authorBio += line + " "
        authorBio = styleText(authorBio, lastSection)
        authorBio.strip("<br><br>")
        html.write(f"""<p class="c1">{authorBio}</p>""")

    #close files
    md.close()
    html.close()

# Convert each md file in folder to html
for file in os.listdir():
    # if str(file).endswith(".docx"):
    #     # convert to .md
    if str(file).endswith(".md"):
        convertToHTML(file, lastSection)

