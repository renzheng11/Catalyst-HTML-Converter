
# ---------------------------
# Author: Ren Zheng
# renzheng112@gmail.com
# ---------------------------

#import libraries
import re
import os

# Global variables
lastSection = ""
writtenSections = []
topNotes = []

# refactor this !!
# Function: replace markdown styles with html styling tags
def styleText(text):
    # strip all newlines so text is one string
    text = text.replace("\n", "")

    # Replace three --- em dash —
    text = text.replace("---", "&mdash;")

    # Replace two -- em dash –
    text = text.replace("--", "-")

    # Replace \|
    text = text.replace("\|", "|")

    # Replace [.]{.smallcaps}
    text = text.replace(r"[.]{.smallcaps}", "")

    # Replace instances of ellipses \...
    text = text.replace("\...", "...")

    # Replace left and right brackets
    text = text.replace("\[", "[")
    text = text.replace("\]", "]")

    # Replace \"
    # Replace left and right brackets
    text = text.replace('\\"', '"')

    # Replace apostrophes
    text = text.replace("\\'", "'")

    # Replace []{.mark}
    markPattern = r"\[[^{}]*\]{\.mark}"
    searchResult = re.search(markPattern, text)
    if searchResult: #found match
        matchList = re.findall(markPattern, text)
        for item in matchList:
            replacement = item[1:-8]
            text = text.replace(item, replacement)

    # Replace underline link format
    # [[link]{.underline}](link).
    linkPattern = "\[\[.*\]\{\.underline\}\]\([^)\]]*\)"
    searchResult = re.search(linkPattern, text)
    if searchResult:
        matchList = re.findall(linkPattern, text)
        for item in matchList:
            link = item.split("underline}]")[1][:-1][1:]
            text = text.replace(item, f"<a href={link}>{link}</a>")

    # Replace [link]{.underline} or [<link>]{.underline}
    linkPattern = "\[<?.*>?\]\{\.underline\}"
    searchResult = re.search(linkPattern, text)
    if searchResult:
        matchList = re.findall(linkPattern, text)
        
        for item in matchList:
            if item.count("<") == 0:
                link = item[:-13][1:]
                text = text.replace(item, f"<a href={link}>{link}</a>")
                # text = re.sub(linkPattern, , text)
            else:
                link = item[:-14][2:]
                text = text.replace(item, f"<a href={link}>{link}</a>")
                # text = re.sub(linkPattern, , text)
            
    # Replace second link format
    # [link](link).
    linkPattern = "\[.*\]\([^)]*\)"
    searchResult = re.search(linkPattern, text)
    if searchResult:
        matchList = re.findall(linkPattern, text)
        for item in matchList:
            link = item.split("](")[1][:-1]
            text = text.replace(item, f"<a href={link}>{link}</a>")
        
    # Replace "double quote marks" with “quote marks”
    quotePattern = "\"[^\x22]+\""
    searchResult = re.search(quotePattern, text)
    if searchResult: #found match
        matchList = re.findall(quotePattern, text)

        for item in matchList:
            replacement = "“" + item.strip("\"") + "”"
            text = text.replace(item, replacement)

    # # Replace 'single quote marks' with “quote marks”
    # quotePattern = "'([^']*)'[^s]"
    # # '(?!(s ))(?!(re ))(?!(d ))(?!(ll ))(?!(ve ))(?!(t )).*'(?!s)(?!r)(?!d)(?!ll)(?!ve)(?!t)
    # searchResult = re.search(quotePattern, text)
    # if searchResult: #found match
    #     matchList = re.findall(quotePattern, text)

    #     for item in matchList:
    #         if (item[:2] == "s "):
    #             continue
    #         else:
                # itemPattern = '\'' + item.strip("\'") + '\''
                # replacement = "&lsquo;" + item.strip("\'") + "&lsquo;"
                # text = re.sub(itemPattern, replacement, text)

    # Replace instances of ^superscripts^ (not notes)
    superPattern = "\^[^\d]{2}\^"
    searchResult = re.search(superPattern, text)
    if searchResult: #found match
        matchList = re.findall(superPattern, text)
        for item in matchList:
            replacement = "<sup>" + item.strip("\^") + "</sup>"
            text = text.replace(item, replacement)

    # Replace instances of **bold** text
    boldPattern = "\*\*[^*]*\*\*"
    searchResult = re.search(boldPattern, text)
    if searchResult: #found match
        matchList = re.findall(boldPattern, text)

        for item in matchList:
            replacement = "<strong>" + item.strip("**") + "</strong>"
            text = text.replace(item, replacement)

    # Replace instances of ~~strike~~ text
    strikePattern = "~~[^~]*~~"
    searchResult = re.search(strikePattern, text)
    if searchResult: #found match
        matchList = re.findall(strikePattern, text)

        for item in matchList:
            replacement = "<del>" + item.strip("~~") + "</del>"
            text = text.replace(item, replacement)

    # Replace instances of ~subscript~
    superPattern = "[^~]~.+~[^~]"
    searchResult = re.search(superPattern, text)
    if searchResult: #found match
        matchList = re.findall(superPattern, text)
        for item in matchList:
            replacement = "<sub>" + item.replace("~", "") + "</sub>"
            text = text.replace(item, replacement)

    # Replace instances of *italic* text
    italicPattern = "\*(?!\s)[\s\S]*?\*(?<!\s\*)"
    searchResult = re.search(italicPattern, text)
    if searchResult: #found match
        matchList = re.findall(italicPattern, text)

        for item in matchList:
            replacement = "<i>" + item.strip("*") + "</i>"
            text = text.replace(item, replacement)

    # last pass - remove blackslash
    text = text.replace("\\", "")

    return text

# Function: read all body text until next section
def readContents(last, md, html, authors, extraLine, secLine):
    # brute fix for roundtable articles ?
    contents = extraLine + " " + secLine
    # previous: contents = ""

    if last == "Notes" or last == "Note":
        line = writeNotes(md, html)
        return (contents, line)

    itemtext = ""
    global inList
    onFig = 1

    while True:
        #read next line
        if itemtext:
            line = itemtext
        else:
            line = md.readline() 

        #if empty line
        if (line == "\n"):
            contents += "<br><br>"

        # LISTS
        listPattern = r"-   \w*"

        if re.search(listPattern, line):
            contents = contents.strip().strip("<br><br>") 
            contents += """</p><p class="c1 quotes"><ul><li>""" + line.strip("-").strip()

            inList = True
            nextstartline = ""

            while inList:
                if nextstartline:
                    line = nextstartline
                    nextstartline = ""
                else:
                    line = md.readline()

                if (line == "\n"): # end of item
                    contents += "</li>"

                    nextline = md.readline()
                    if nextline.count("-") >= 1: # next item
                        contents += "<li>" + line
                        nextstartline = nextline

                    if nextline.count("-") == 0: # end of list
                        contents += '</ul></p><p class=c1>&nbsp;</p><p class=c1>' + nextline
                        break
                line = line.strip("-").strip()
                contents += line + " "

        # QUOTES
        if line.count("#######"):
            line = line.strip("####### ")
            contents += f'<p class=quotes>{line}'
            while True:
                line = md.readline()
                if line.strip() == "":
                    break
                contents += line + " "

            contents += '<br><br></p><p class="c1">'
            
        # IMAGES + FIGURES
        fileName = authors[0][0].split(" ")[-1].lower()
        noAlt = False
        if line.count("![") == 1:
            onFig += 1
            contents += f"""</p><img src="{fileName}{onFig}.jpg" class="figure" alt='"""

            if line.count("![]") == 1:
                contents += "'" + '>'
                noAlt = True
                # print(f"[{fileName[0].upper() + fileName[1:]}] Figure {onFig} is missing alt text.")
            else:
                contents +=  line.strip("![")

            # start reading
            inAlt = True

            if not noAlt:
                while inAlt:
                    line = md.readline()
                    if line.count("]") == 1: # end of alt text
                        if (line.count("width=") != 0):
                            line = line.split("]")[0]
                            contents += line +  "'" + '>'
                        break
                    else:
                        contents += line + " "
                        contents = styleText(contents)

            # clear end of alt text from line
            line = ""

            next = md.readline() # empty line
            if next != "\n":
                md.readline()

            figure = ""

            lineNotEmpty = True
            while lineNotEmpty:
                next = md.readline()
                figure += next + " "
                if next == "\n":
                    break

            figNum = figure[7]
            figContent = figure[10:]
            figContent = styleText(figContent)

            contents += f"""
                <p class=imageText>Figure {figNum}. {figContent}</p>
                <br><br>
                <p class=c1>
            """

        #if the line is a section title
        anySectionTitle = "^###.+"
        if re.match(anySectionTitle, line):
            #add section name to writtenSections list
            strippedSection = line.replace("#", "").strip()
            writtenSections.append(strippedSection)
            contents = styleText(contents)

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

            noteLink = f'<sup><a href=#note{noteNum}b id=note{noteNum}t>{noteNum}</a></sup>'
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
        if l.count("###") == 1:
            # reached end of notes (hit References)
            # write last note:

            noteContent = styleText(noteContent)
            html.write(
                f"""
                <div id="note{noteNum}b">
                    <p class="notes">
                        <sup><a href=#note{noteNum}t>{noteNum}</a></sup> {noteContent}
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
            noteContent = styleText(noteContent)
            html.write(
                f"""
                <div id="note{noteNum}b">
                    <p class="notes">
                        <sup><a href=#note{noteNum}t>{noteNum}</a></sup> {noteContent}
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
        unformattedLink = False
        if l == "\n": 
            link = ""
            linkPattern = "<.*>\.*"
            searchResult = re.search(linkPattern, refContent)

            if searchResult: #found a link
                match = re.search(linkPattern, refContent).group()
                link = match.strip("<").strip(">.")
            refContent = re.sub(linkPattern, "", refContent)

            # convert markdown styles
            refContent = styleText(refContent) 

            # add complete previous reference to html
            if link != "": #reference has a link
                html.write(
                    f"""
                    <p class="reference"> {refContent} <a href={link}>{link}</a>.</p>
                    """
                )
            else: #reference does not have a link (in format)
                refSplit = refContent.split()
                for item in refSplit:
                    if item.count("http") == 1:
                        unformattedLink = True
                        link = item[:-1]
                        refContent = refContent[:-1]
                        refContent = refContent.replace(link, "")

                if unformattedLink:
                    html.write(
                    f"""
                    <p class="reference"> {refContent} <a href={link}>{link}</a>.</p>
                    """
                )
                else:
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
    bookReview = False

    fileName = str(file).replace(".md", "")

    mdfile = open(file, "r")
    htmlfile = open(f"{fileName}.html", "w")

    with mdfile as md, htmlfile as html:
        topItems = []
        #reads top of doc in order
        # get title until blank line

        # get rest of top
        for line in md:
            if line.count("###") == 1:
                # hit abstract or ###
                if (topItems[1].count("Book Review") == 1):
                    # title = topItems[1]
                    keywords = "Book Review"
                    bookReview = True
                if bookReview:
                    break
                else:
                    if line.count("Abstract") == 1:
                        break
            # if re.match("### Abstract(\s+)?", line):
            #     break
            else:
                # if title is in second line
                secondTitle = ""
                if line.count("##") == 1:
                    secondTitle = line
                stripHash = line.strip("#")

                # if line is whitespace
                if stripHash.strip() == "":
                    continue #to next line
                else:
                    #add all lines to topItems
                    # if second line of title, replace first line
                    if secondTitle and len(topItems) > 1:
                        topItems[1] = secondTitle
                    else:
                        topItems.append(line)

        #-------Store authors-------
        # authors: "{0: [author, affil, contact], 1: [author, affil, contact]}"
        authors = {}
        
        title = topItems[1].strip("#").strip()
        title = styleText(title)

        # delete logo and title from topItems
        del topItems[0:2]

        #store author names for metadata
        topIndex = 0
        keyIndex = 0
        topLength = len(topItems)
        
        while topLength != 0:
            #author
            author = topItems[topIndex].strip()

            #affil
            if not topItems[topIndex + 2].count("@") == 1:
                topItems[topIndex + 1] = topItems[topIndex + 1] + topItems[topIndex + 2]
                del(topItems[topIndex + 2])
                topLength = topLength - 1

            affil = topItems[topIndex + 1].strip()
            affil = styleText(affil)
            contact = topItems[topIndex + 2].strip()
            contact = styleText(contact)

            authors[keyIndex] = [author, affil, contact]

            topLength -= 3
            topIndex += 3
            keyIndex += 1

        authorNames = ""
        for i in range(len(authors)):
            authorNames += (authors[i][0])
            if i < (len(authors) - 1):
                authorNames += ", "

        authorNames = styleText(authorNames)

        fileName = authors[0][0].split(" ")[-1].lower()

        extraLine = ""

        if not bookReview:
            # ABSTRACT AND KEYWORDS
            # Keywords read manually (a lot of cases of keywords accidentally marked as heading 3)
            emptyLine = md.readline() # empty line
            
            abstract, lastSection = readContents(lastSection, md, html, authors, "", "")
            keywords = ""
            line = md.readline() # probably empty line
            
            if line != "": # if not empty line
                if line.count("#") >= 1:
                    line = line.strip("# ")
                keywords += line # add the line to keywords

            # GET KEYWORDS
            while True:
                line = md.readline()
                if line.count("#") >= 1:
                    line = line.strip("# ")
                keywords += line
                if line.strip() == "": # hit empty line after keywords
                    break
            
            startedContent = False

            # get next section heading
            nextLine = md.readline()
            if nextLine.count("##") >= 1:
                lastSection = nextLine # introduction if it does not go straight into content
                
            else: # goes straight into content
                lastSection = "startedContent"
                extraLine = nextLine

            # OLD VERSION: Read keywords as body section
            # keywords, lastSection = readContents(lastSection, md, html, authors)
            # keywords = keywords.strip("<br><br>")

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
            """)
        else: #book review
            html.write(f"""
                <html>

                <head>
                    <link href="https://fonts.googleapis.com/css?family=Catamaran&display=swap" rel="stylesheet">
                    <meta content="text/html; charset=UTF-8" http-equiv="content-type">
                    <meta charset="UTF-8">
                    <meta name="description" content="{title}">
                    <meta name="author" content="{authorNames}">
            """)

        # STYLING
        html.write(f"""

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

        # write keywords & abstract in meta data
        if not bookReview:
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
                lastSection = styleText(lastSection)
                html.write(f"""<p class="c1 sectionTitle">{lastSection}</p>""")

            #if lastSection matches subsectionTitle
            elif re.match(subsectionTitle, lastSection):
                lastSection = lastSection.strip("#").strip()
                lastSection = styleText(lastSection)
                html.write(f"""<p class="c1 subsectionTitle">{lastSection}</p>""")

            #if lastSection matches subsubsectionTitle
            elif re.match(subsubsectionTitle, lastSection):
                lastSection = lastSection.strip("#").strip()
                lastSection = styleText(lastSection)
                html.write(f"""<p class="c1 sub_subsectionTitle">{lastSection}</p>""")

            bodyText, lastSection = readContents(lastSection, md, html, authors, extraLine, line)
            extraLine = ""

            refPattern = "### References\s*"
            if re.match(refPattern, lastSection):
                html.write(f"""<p class="c1">{bodyText}</p>""")
                writeRefs(md, html)
                break

            html.write(f"""<p class="c1">{bodyText}</p>""")

            bioPattern = "### Author Bio[s]?\s*"
            if re.match(bioPattern, lastSection):
                #reached Author Bios - last section
                break

        # AUTHOR BIOS

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
        authorBio = styleText(authorBio)
        authorBio.strip("<br><br>")
        html.write(f"""<p class="c1">{authorBio}</p>""")

    #close files
    md.close()
    html.close()
    # print(f"\nFinished converting {fileName[0].upper() + fileName[1:]}!\n")

# Convert each md file in folder to html
for file in os.listdir():
    # reset global vars
    writtenSections = []
    topNotes = []

    # if str(file).endswith(".docx"):
    #     # convert to .md

    if str(file).endswith(".md"):
        convertToHTML(file, lastSection)

    