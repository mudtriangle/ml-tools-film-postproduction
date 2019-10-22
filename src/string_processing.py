# External libraries
import re
import unicodedata
import numpy as np

from nltk.tokenize import TweetTokenizer
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

# Initialize.
tokenizer = TweetTokenizer()
stemmer = PorterStemmer()
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


# Output the vocabulary from a list of lists of tokens to a given file.
def build_vocab(sentences_tokens, filename):
    vocab = []
    for sentence in sentences_tokens:
        for word in sentence:
            if word not in vocab:
                vocab.append(word)
    vocab.sort()

    # Make a dictionary of words -> indices.
    vocab_dict = {}
    with open('vocabulary.txt', 'w') as f:
        for i in range(len(vocab)):
            f.write('%i,%s\n' % (i + 1, vocab[i]))
            vocab_dict[vocab[i]] = i + 1

    return vocab_dict


# Convert the tokens to numbers from the vocabulary.
def get_numbers(word_tokens, vocab):
    numbers = []
    for word in word_tokens:
        if word not in vocab.keys():
            continue
        numbers.append(vocab[word])

    return numbers


# Add zeros to a list until it reaches the desired length. If it is already longer than the length, truncate.
def padding(target_list, desired_length):
    if len(target_list) < desired_length:
        zeros = list(np.zeros(desired_length - len(target_list), dtype=int))
        fixed_len = zeros + target_list

    else:
        fixed_len = target_list[0:desired_length]

    return fixed_len
