import numpy as np

from read_pdf import Script
from string_processing import normalize, tokenize, get_ngrams

s = Script('../test_data/TaxiDriver.pdf')

string_to_find = """
                 who wouldn't take it any more, 
                 a man who stood up against the 
                 scum, the cunts, the dogs, the 
                 filth.  Here is
                 """

string_to_find = "new is used to heads you as a man who would not taken any more who would not listen you is used to use a man who would not take it anymore, can you feel the ship here is someone who stood up"

string_to_find = get_ngrams(tokenize(normalize(string_to_find)), 2)
print(string_to_find)

scores = []
for i in range(len(s.scenes)):
    score = 0
    ngrams = s.scenes[i].get_ngrams(2)

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
