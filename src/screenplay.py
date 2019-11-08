from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

from bs4 import BeautifulSoup

import io
import os

from string_processing import normalize, tokenize, get_ngrams
from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
import numpy as np

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '../api_keys/google_cloud.json'
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

    def find_scene_from_audio(self, path_to_audio):
        client = speech_v1.SpeechClient()

        config = {"language_code": 'en-US',
                  "sample_rate_hertz": 48000,
                  "encoding": enums.RecognitionConfig.AudioEncoding.LINEAR16,
                  "profanity_filter": False,
                  "audio_channel_count": 2}

        with io.open(path_to_audio, 'rb') as f:
            content = f.read()
        audio = {"content": content}

        response = client.recognize(config, audio)

        alternatives = []
        max_n = None
        for result in response.results:
            alternative = result.alternatives[0]
            tokens = tokenize(normalize(alternative.transcript))

            if max_n is None:
                max_n = len(tokens)
            if max_n > len(tokens):
                max_n = len(tokens)

            alternatives.append(tokens)

        scores = []
        for scene in self.scenes:
            curr_score = 0

            for num_ngrams in range(1, min([6, max_n])):
                scene_ngrams = scene.get_ngrams(num_ngrams)
                for alt in alternatives:
                    dialogue = get_ngrams(alt, num_ngrams)
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

    def get_ngrams(self, n):
        full_text = ''
        for dia in self.dialogues:
            full_text += dia[1] + ' '

        return get_ngrams(tokenize(normalize(full_text)), n)
