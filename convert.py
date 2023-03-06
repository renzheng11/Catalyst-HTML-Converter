import pypandoc
import os

# With an input file: it will infer the input format from the filename

for file in os.listdir('.'):
    if str(file).endswith(".docx"):
        output = pypandoc.convert_file(file, 'md', outputfile=file.split(".")[0]+".md")
        assert output == ""
