# ------ Manual Todo (not done by script) ------
* This scripts converts markdown files (.md) to (.html)
    # to convert (.docx) to markdown (.md), use the command:
    # pandoc -s name.docx -o name.md
        # (pandoc can be installed at https://pandoc.org/installing.html)
        # option 2: use a web converter to get (.md) file

    # Manual changes
        # - Change article type before title (ex. special spection, original research, etc.)

    # Checklist for docx
        # - List of keywords should be normal body text (not a heading)
        # - Quotes should be in Heading 7 style
            # - If more than one quote in a row, they both need Heading 7 Style separately
        
        # - Correct spacing in between each item
        # - Empty lines should be normal body text style
        # - Line break between photo and figure

        # - ALT text should not be empty (will throw error)
        # - Do not put quote marks (single or double) in alt-text (need to add manually to html after conversion)

    # Tips for issues
        # - if there are issues with text formatting, go through checklist for docx and reconvert to md then rerun script 
        # - if there are outlying issues with text content, search for it in html to change it