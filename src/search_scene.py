import numpy as np

from read_pdf import Script
from string_processing import normalize, tokenize, get_ngrams

s = Script('../test_data/TheBigSick.pdf')

string_to_find = "I mean we played cricket, which is just a spicier version of baseball. And we prayed a lot. " +\
                 "Well not a lot, just five times a day."
string_to_find = get_ngrams(tokenize(normalize(string_to_find)), 3)

scores = []
for i in range(len(s.scenes)):
    score = 0
    trigrams = s.scenes[i].get_ngrams(3)

    for ngram in string_to_find:
        if ngram in trigrams:
            score += 1

    scores.append(score)

print(scores)

print('******' * 5)

match = np.argmax(scores)
if scores[match] == 0:
    print('No scene found.')
else:
    print(s.scenes[match])
