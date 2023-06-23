## Intro

This script converts the docx files of Catalyst articles (in Stage 2) and generates a HTML file based on its contents. 
The script relies on the docx file being in the correct format (following the [Style Guide](https://docs.google.com/document/d/1KhPUAjPnpE2R6YC5VAZp8plm3v8bGDySnvoFNvnZumE/edit)). It will still run if the format is wrong but the wrong format may reflect in the html file.

The info on this doc is also covered in this [video tutorial](https://www.dropbox.com/s/876t685ms2jocei/Tutorial%20for%20Catalyst%20HTML%20article%20converter_1.mp4?dl=0). 

Note: Do not make any changes to "auto.py" file.

<p>&nbsp;</p>

## Set Up

- Download VS Code
- Download script folder from this GitHub page
<p>&nbsp;</p>

## Steps for Conversion

0. **Ensure docx file is in correct formatting.**
    Important checks:
    - Correct spacing / line breaks in between each item
    - Empty lines should be normal body text style
    - List of keywords should be normal body text (not a heading)
    - Author bio headings are not missing
    - No body sections are empty (including keywords, abstract, author bio content)
    - BOOK REVIEWS: make sure there is an empty Heading 3 in between author(s) and review content.
    <p>&nbsp;</p>

1. **Move docx files into folder called 'docx'**
    - Before starting, store copy of the Stage 2 docx files.
    - You can put multiple files in the docx folder and the script will convert all of them.
    - If there are any errors, it may be easier to only put one docx file in the folder at a time and run it.
    - Then put finished html files a separate folder you have created.
    - It will be helpful to only use the folders in this package for conversion and not for storage purposes.
    <p>&nbsp;</p>

2. **Click the auto.py file, hit run button on the top right corner**
    - To open and preview the generated HTML file: double click on file in the folder that it's in.
    <p>&nbsp;</p>

3. **Check / fix errors**
    - If you see any textual or formatting mistakes on the page, you can open and make edits to the .html file.
    - These mistakes might also point out fixes you can make to the .docx file.
    - For help with resolving issues or if there is a problem while running the script, refer to the section below on resolving errors.
    <p>&nbsp;</p>

4. **Make manual changes**
    - Article type
        - After the html is generated, change the article type before the title (i.e. special section, original research, etc.)

    - Images & Alt Text
        - Name image hrefs in the html to their respective file names that will be uploaded to OJS.
        - Add alt text for each image in html file.

    - Quotes
        - Quotes tags need to be manually added in html file (using quotes class).


    - Subscripts
        - The script does not convert subscripts (ex. H<sub>2</sub>O). Subscript tags need to be added manually.

        <p>&nbsp;</p>

5. **Final checks**
    - Check metadata is correct
    - Check all reference links work
    - Check that all the note links work 

    <p>&nbsp;</p>

6. **Organizing Files / Resetting Folders**
    - Store all finished and reviewed html files in their designated folder.
    - Delete all the remaining files in the "docx" folder.

## Resolving Errors

Three ways to fix errors - you can make direct changes to any of the file formats (docx, md, html) and save the files. Note: rerunning the script will use the docx file and overwrite both the resulting md and html files. 

- Make edits to html
    - You can make changes to the html file, save, and store it in a folder designated for finished and reviewed html files.  

- Updating the DOCX file 
    - Often an issue in the html page will reflect a formatting oversight in the docx file. Changes can be made to the docx file and once it has replaced the old version, the script can be run again and a new html file will overwrite the last one. 

- Updating the MD file
    - The script first converts the docx file to markdown (.md) and uses the md file as the source to generate the html file.
    - The md file is only used during conversion and you do not need to worry about its contents after conversion. But it is helpful for seeing where formatting errors are and using it to rerun the script to get an updated html file. 
    - If you make edits to the md and want it to reflect in the resulting html, you should remove the docx file from the folder first (or else it converts the docx to the md each you click the run button and any changes you have made to the md file will be overwritten).

### Potential Errors
(Most of these errors are rare. Don't need to check this every time, only if you see an issue on the html page or if there is a problem when running the script.)

- Heading 
    - Multiple titles might mess up the conversion
        - Temporarily condense it to one title. Make changes to html after. 
    - Check that there are line breaks after abstract / keyword.
    - Check that the article title is H2.
    - Check that nothing in the authors section is a header.
    - If abstract is more than two paragraphs, make it one.

- Book Reviews
    - Make sure there is an empty Heading 3 in between author(s) and review content.

- Images
    - Check that there is a line break between each photo and figure.
    - If there are multiple images next to each other with only one Figure caption, remove the images from the md file except for the first one.
    - Can also remove image file from MD then manually add later.

- Links
    - If a link is not linked, check the md file and include <> around the link
        - example: <https://doi.org/10.14506/ca33.3.06>

- MD MARKS
    -  If you see any remaining []{.mark} (or any other extra markdown inserts) in the html, remove the []{.mark} symbols from the md.

- If the program does not finish (the terminal does not give give an output within a minute or so)
    - To stop the program, press: (mac) ctrl + z / (windows) ctrl + c
    - Remove any non-text content from md and try running away.
    - If this happens, only convert one docx file at a time to see which one is causing the issue.
    - If it keeps happening, that file may need to be converted manually. 

- Generally:
    - If there is a part of the article causing an issue that is hard to fix, remove the part from the md file, convert, then add the part pack manually in html.

<p>&nbsp;</p>