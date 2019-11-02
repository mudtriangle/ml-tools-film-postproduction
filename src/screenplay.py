from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

from bs4 import BeautifulSoup

from io import StringIO

from string_processing import normalize, tokenize, get_ngrams

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
        ftype = path.split('.')[-1]
        self.scenes = []

        if ftype == 'pdf':
            text = string_from_pdf(path)

            text = text.split('\n')
            scene_text = ''
            for line in text:
                is_heading = False
                for heading in SCENE_HEADINGS:
                    if heading in line:
                        is_heading = True
                        break

                if is_heading:
                    self.scenes.append(Scene(text=scene_text))
                    scene_text = line + '\n'

                else:
                    scene_text += line + '\n'
            self.scenes.append(Scene(text=scene_text))

        elif ftype == 'fdx':
            with open(path, 'r') as f:
                soup = BeautifulSoup(f, 'lxml')
            res = soup.find_all('paragraph')

            elements = []
            for elm in res:
                try:
                    elements.append((elm['type'], elm.text.strip()))
                except KeyError:
                    pass

            curr_scene = []
            for pair in elements:
                if pair[0] == 'Scene Heading':
                    self.scenes.append(Scene(lines=curr_scene))
                    curr_scene = []

                curr_scene.append(pair)
            self.scenes.append(Scene(lines=curr_scene))

    def __str__(self):
        to_print = ''
        for scene in self.scenes:
            to_print += str(scene) + '\n'
        return to_print


class Scene:
    def __init__(self, text='', lines=[]):
        if text != '':
            text = text.split('\n')
            self.header = text[0]
            self.body = '\n'.join(text[1:])
            self.tokens = tokenize(normalize(self.body))

        elif len(lines) != 0:
            if lines[0][0] == 'Scene Heading':
                self.header = lines[0][1]
            else:
                self.header = 'No header'

            self.body = ''
            self.characters = []
            self.actions = []
            self.dialogues = []
            for i in range(1, len(lines)):
                self.body += lines[i][1] + '\n'

                if lines[i][0] == 'Character':
                    if lines[i][1] not in self.characters:
                        self.characters.append(lines[i][1])
                elif lines[i][0] == 'Action':
                    self.actions.append(lines[i][1])
                elif lines[i][0] == 'Dialogue':
                    self.dialogues.append((lines[i - 1][1], lines[i][1]))

    def __str__(self):
        return self.header + '\n' + self.body

    def get_dialogue_ngrams(self, n):
        full_text = ''
        for dia in self.dialogues:
            full_text += dia[1] + ' '

        return get_ngrams(tokenize(normalize(full_text)), n)
