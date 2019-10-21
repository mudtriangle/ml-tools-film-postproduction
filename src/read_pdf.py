from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

from io import StringIO
import os


DIR = '../test_data'

SCENE_HEADINGS = ['INT ', 'EXT ', 'INT.', 'EXT.' 'CREDIT', 'DAY', 'NIGHT']


def string_from_pdf(path):
    """
    Function that takes the path to a PDF file and returns a string with the text contents from the PDF.
    Uses PDFMiner and StringIO.

    To test: - What happens when a PDF with no text is inputted?
             - Does all of the formatting remain the same?

    Also: how does it generally work? Need to do more research on the nature of PDF files. (!!!)
    """
    # Binary read file.
    f = open(path, 'rb')

    # Initialize ResourceManager, output StringIO, and LAParams.
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()

    # Create TextConverter and PageInterpreter.
    device = TextConverter(rsrcmgr, retstr, codec='utf-8', laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # Initialize set to store page numbers.
    pagenos = set()

    # Loop through every page in the PDF and process it with the interpreter.
    for page in PDFPage.get_pages(f, pagenos, maxpages=0, password='', caching=True, check_extractable=True):
        interpreter.process_page(page)

    # Extract the text from the StringIO.
    text = retstr.getvalue()

    # Close all resources used.
    f.close()
    device.close()
    retstr.close()

    return text


"""
# Call the get_string() function for all of the test cases in test_data.
scripts = os.listdir(DIR)
for script in scripts:
    input_file_path = DIR + '/' + script
    output_file_path = '../test_outputs/' + script[:-4] + '.txt'
    with open(output_file_path, 'w') as output_file:
        output_file.write(string_from_pdf(input_file_path))
"""


class Script:
    def __init__(self, path):
        text = string_from_pdf(path)
        self.scenes = []

        text = text.split('\n')
        scene_text = ''
        for line in text:
            is_heading = False
            for heading in SCENE_HEADINGS:
                if heading in line:
                    is_heading = True
                    break

            if is_heading:
                self.scenes.append(scene_text)
                scene_text = line + '\n'

            else:
                scene_text += line + '\n'

        self.scenes.append(Scene(scene_text))

    def __str__(self):
        to_print = ''
        for scene in self.scenes:
            to_print += str(scene) + '\n'
        return to_print


class Scene:
    def __init__(self, text):
        text = text.split('\n')
        self.header = text[0]
        self.body = '\n'.join(text[1:])

    def __str__(self):
        return self.header + '\n' + self.body


script = Script(DIR + '/ToyStory3.pdf')
print(script.scenes[-1])
