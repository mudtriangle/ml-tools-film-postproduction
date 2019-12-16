# Standard libraries
import io
import os

# Local files
from string_processing import normalize, tokenize, get_ngrams

# External libraries
from bs4 import BeautifulSoup

import numpy as np

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

# Constants
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '../api_keys/google_cloud.json'
DIR = '../test_data'
SCENE_HEADINGS = ['INT ', 'EXT ', 'INT.', 'EXT.' 'CREDIT', 'DAY', 'NIGHT']


# Still requires work.
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
    retstr = io.StringIO()
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


class Screenplay:
    """
    Class that holds a screenplay parsed from a PDF file (still in progress) or a Final Draft FDX file (currently
    functioning). Allows for identification of characters, actions, dialogue, and locations. Currently supports finding
    scenes through transcripts.
    """
    def __init__(self, path):
        # Identify the type of file in the path.
        ftype = path.split('.')[-1]

        # List that carries objects of class Scene identified in the file.
        self.scenes = []

        # Processing for PDF files is still in progress.
        if ftype == 'pdf':
            # Convert a PDF file to plain text.
            text = string_from_pdf(path)
            text = text.split('\n')

            # Identify each scene through separating by scene headings.
            scene_text = ''
            for line in text:
                is_heading = False
                for heading in SCENE_HEADINGS:
                    if heading in line:
                        is_heading = True
                        break

                # Each time a heading is found, make a scene out of the previous lines.
                if is_heading:
                    self.scenes.append(Scene(text=scene_text))
                    scene_text = line + '\n'

                else:
                    scene_text += line + '\n'

            # The remaining lines of the text are the final scene.
            self.scenes.append(Scene(text=scene_text))

        # Processing for FDX files currently working.
        elif ftype == 'fdx':
            # Parse FDX file as an XML.
            with open(path, 'r') as f:
                soup = BeautifulSoup(f, 'lxml')
            # Ignore formatting and metadata.
            res = soup.find_all('paragraph')

            # Build a list of elements from the XML file.
            elements = []
            for elm in res:
                try:
                    elements.append((elm['type'], elm.text.strip()))
                except KeyError:
                    pass

            # Create a list of scenes from the headings, dialogues, actions, and characters.
            curr_scene = []
            for pair in elements:
                # Each time a heading is found, make a scene out of the previous elements.
                if pair[0] == 'Scene Heading' and curr_scene != []:
                    self.scenes.append(Scene(lines=curr_scene))
                    curr_scene = []

                curr_scene.append(pair)

            # The remaining elements are the final scene.
            self.scenes.append(Scene(lines=curr_scene))

    def find_scene_from_transcript(self, transcript):
        transcript_text = ''
        for t in transcript.keys():
            for alternative in transcript[t]:
                transcript_text += ' ' + alternative

        tokens = tokenize(normalize(transcript_text))
        scores = []
        for scene in self.scenes:
            curr_score = 0

            for num_ngrams in range(1, 6):
                scene_ngrams = scene.get_ngrams(num_ngrams)
                dialogue = get_ngrams(tokens, num_ngrams)
                for ngram in dialogue:
                    if ngram in scene_ngrams:
                        curr_score += 1

            scores.append(curr_score)

        match = np.argmax(scores)
        if scores[match] == 0:
            return None
        else:
            return match

    def __str__(self):
        # When called to print, print the text in every scene separated by a return character.
        to_print = ''
        for scene in self.scenes:
            to_print += str(scene) + '\n'
        return to_print


class Scene:
    """
    Class that holds the text and key data for a scene within a screenplay. Only meant to be called within the
    screenplay class. Can either receive raw text or a list of tuples of the form (type of element, content).
    """
    def __init__(self, text='', lines=[]):
        # If text is not empty, use text to build scene.
        if text != '':
            text = text.split('\n')

            # Header is the first line.
            self.header = text[0]

            # Body is the rest of the text.
            self.body = '\n'.join(text[1:])
            self.tokens = tokenize(normalize(self.body))

        # Otherwise, if lines is not empty, use it instead. Preferable and more thorough.
        elif len(lines) != 0:
            # Identify the header of the scene.
            if lines[0][0] == 'Scene Heading':
                self.header = lines[0][1]
            else:
                self.header = 'No header'

            # Identify the main pieces of a scene.
            self.body = ''
            self.characters = []
            self.actions = []
            self.dialogues = []
            last_character = ''
            for i in range(1, len(lines)):
                self.body += lines[i][1] + '\n'

                # If the element is character, add it if it's not already in the list of characters.
                if lines[i][0] == 'Character':
                    character = lines[i][1]

                    # Gets rid of (V.O.), (CONT'D), etc.
                    if character.find(' (') != -1:
                        character = character[0:character.find(' (')]

                    last_character = character
                    if character not in self.characters:
                        self.characters.append(character)

                # If the element is an action, add it to the list of actions.
                elif lines[i][0] == 'Action':
                    self.actions.append(lines[i][1])

                # If the element is dialogue, add it to the list of dialogues in a tuple of the form
                # (name of the character, dialogue).
                elif lines[i][0] == 'Dialogue':
                    self.dialogues.append((last_character, lines[i][1]))

    def __str__(self):
        # When called to print, print the header and the body separated by a return character.
        return self.header + '\n' + self.body

    def get_ngrams(self, n):
        # Generate ngrams from the dialogues for searching purposes.
        full_text = ''
        for dia in self.dialogues:
            full_text += dia[1] + ' '

        return get_ngrams(tokenize(normalize(full_text)), n)
