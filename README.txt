
----------------------------------------------------------------------------

## How to run the script
    - Place .docx or .md files in folder named "docx"
    - you can put multiple files in the folder and the script will convert all of them
    - you can make edits in the html file if there are any issues
    - Do not make changes to the file auto.py

## Manual Changes
    - After html is generated, change article type before title
    - (ex. special spection, original research, etc.)

----------------------------------------------------------------------------

## Errors
    - If you run into an error or see a mistake in the html page,
      see the checklist below...

## Checklist for Docx / MD file
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
        - Ensure image hrefs are named correctly for uploading to OJS

    ** LINKS **
        - if a link is not linked, check the md file and include <> around the linked
            - example: <https://doi.org/10.14506/ca33.3.06>

    ** QUOTES **
        - Quotes tags need to be manually added in the html file

    ** BOOK REVIEWS **
        - For book reviews: if the article does not have an abstract, include a empty heading
        in between author(s) and content

    ** MD MARKS **
        - If you see any remaining []{.mark} in the html, remove the []{.mark} symbols from the md

    ** OUTLYING ISSUES **
        - issues with text formatting: go through checklist on md file then rerun script 
        - issues with text content, search for it in html to edit


------
# For converting to an app using py2app:
# py2applet --make-setup auto.py
# rm -rf build dist
# python3 setup.py py2app
# Go to the dist folder, right click on the app and click "Show Package Contents"
# Go to Contents/Resources/
# In the Resources folder paste the word files
# In the terminal run: dist/auto.app/Contents/MacOS/auto