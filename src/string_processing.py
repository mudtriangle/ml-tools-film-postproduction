# External libraries
import re
import unicodedata

import nltk
from nltk.tokenize import TweetTokenizer
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

# Initialize.
tokenizer = TweetTokenizer()
stemmer = PorterStemmer()

try:
    stop_words = set(stopwords.words('english'))
except LookupError:
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))


# Takes a string with special characters and returns a string only with English letters.
def strip_accents(original_string):
    return str(unicodedata.normalize('NFD', original_string).encode('ascii', 'ignore').decode("utf-8"))


# Get rid of punctuation and special characters from a string.
def normalize(original_string):
    return strip_accents(re.sub(r'[^\w\s]', ' ', original_string.strip().lower()))


# Takes a normalized string and returns the relevant stemmed tokens for that string.
def tokenize(clean_string):
    words = tokenizer.tokenize(clean_string)
    tokens = []
    for word in words:
        # Ignore stop words.
        if word in stop_words:
            continue

        # Ignore numbers.
        if not word.isalpha():
            continue

        tokens.append(stemmer.stem(word))

    return tokens


def get_ngrams(tokens, n):
    return list(zip(*[tokens[i:] for i in range(n)]))
