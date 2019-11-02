import numpy as np

from screenplay import Script
from string_processing import normalize, tokenize, get_ngrams

s = Script('../test_data/i_spy.fdx')

string_to_find = """Where are you going? Come on! Let's keep playing!"""

string_to_find = get_ngrams(tokenize(normalize(string_to_find)), 3)

scores = []
for i in range(len(s.scenes)):
    score = 0
    ngrams = s.scenes[i].get_dialogue_ngrams(3)

    for ngram in string_to_find:
        if ngram in ngrams:
            print(ngram)
            score += 1

    scores.append(score)

print(scores)

match = np.argmax(scores)
if scores[match] == 0:
    print('No scene found.')
else:
    print(s.scenes[match])
