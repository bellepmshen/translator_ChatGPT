# Language Translator

This project is to translate a given PDF file (ex: academic paper) into the language you'd like </br>
by using ChatGPT 3.5 via API call

Here are the files for getting translation:

1. extract_text.py: This is for extracting text from a given PDF file and break the whole document into paragraph level
2. translator.py: This is to make API calls to ask ChatGPT to translate the text into the language we
specify
3. main.ipynb: This is the notebook to execute API calls and obtain the translated text.

## Instruction:

1. Create a new directory and put extract_text.py, translator.py, main.ipynb and the PDF file in this directory.
2. Create a Python file named 'api_key.py' under the same directory and put your API key here
    - Format: api_key =  'your api key from OpenAI'
3. Run main.ipynb
    - Input: 
        - give the language you'd like to ChatGPT to translate
        - give the absolute path of the PDF file (w/ the PDF filename)
        - the script will ask you to put some words in the first and last paragraphs you'd like to start and end translation.
            - This is because we do not need to translate the authors' group or citation information.
    - Output:
        - before directory: This directory will be created once you run main.ipynb and it stores the break-down paragraphs txt files BEFORE translation.
        - after directory: his directory will be created once you run main.ipynb and it stores the break-down paragraphs txt files AFTER translation. The filename 'merge_translation.txt' is the file you'd like to see after translation.

## Notes:

1. The reason why I break down the document into paragraphs is because I found out ChatGPT would perform better once you feed it few paragraphs, not the whole document.
2. If the prompt message is clear, ChatGPT will also perform better, so feel free to revise the prompt message in the 'translate' function in translator.py
3. The sample paper was provided by the first author, S. H. Hsieh from National Synchrotron Radiation Research Center (NSRRC), Hsinchu, Taiwan