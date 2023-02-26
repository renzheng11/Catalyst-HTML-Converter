# HTML AUTOMATION GUIDE

Author: Ren Zheng
renzheng112@gmail.com

## How to run the script
    - This scripts converts markdown files (.md) to (.html)
    - To convert (.docx) to markdown (.md)...
        - type this command into the terminal:

        pandoc -s name.docx -o name.md

        - (pandoc can be installed at https://pandoc.org/installing.html)
        - (option 2: use a web converter to get (.md) file)

    - The .md file should be in the same folder as the auto.py script

    - You can make edits in the md file and html file
    - Do not make changes to the file auto.py

## Manual Changes
    - After html is generated, change article type before title
    - (ex. special spection, original research, etc.)

## Errors
    - If you run into an error or see a mistake in the html page, consult the checklist below...

## Checklist for Docx / MD file
    - (you can check either one, I find MD easier to look for mistakes)

    ** SECTIONS & TEXT **
        - List of keywords should be normal body text (not a heading)
        - Ensure author bio heading is not missing
        - Ensure no body sections are empty (including keywords, abstract, author bio content)

    ** LINE BREAKS **
        - Correct spacing in between each item
        - Empty lines should be normal body text style (no empty headings except for book reviews)

    ** IMAGES / FIGURES / ALT-TEXT **
        - Important! Do not put quote marks (single or double) in alt-text (need to add manually to html after conversion)
        - Line break between photo and figure
        - Each image needs to be followed by: Figure. N (where N = number)
        - If there are multiple images next to each other with only one Figure caption, 
            - remove the images from the md file except the first one
            - need to change image file names

    ** LINKS **
        - if a link is not linked, check the md file and include <> around the linked
            - example: <https://doi.org/10.14506/ca33.3.06>

    ** QUOTES **
        - Quotes should be in Heading 7 style
        - If more than one quote in a row, they both need Heading 7 Style separately

    ** BOOK REVIEWS **
        - For book reviews: if the article does not have an abstract, include a empty heading
        in between author(s) and content

    ** OUTLYING ISSUES **
        - issues with text formatting: go through checklist on md file then rerun script 
        - issues with text content, search for it in html to edit