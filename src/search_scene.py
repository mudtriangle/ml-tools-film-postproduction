import numpy as np

from read_pdf import Script
from string_processing import normalize, tokenize, get_ngrams

s = Script('../test_data/MyCousinVinny.pdf')
print(s)

exit(0)

string_to_find = """
what is used to have you as a man who would not take it anymore would not listen you f***** is used to use a man who would not take it anymore come with front side also feel the ship here is someone who stood up
                 """

# string_to_find = "new is used to heads you as a man who would not taken any more who would not listen you is used to use a man who would not take it anymore, can you feel the ship here is someone who stood up"

string_to_find = get_ngrams(tokenize(normalize(string_to_find)), 3)
print(string_to_find)

scores = []
for i in range(len(s.scenes)):
    score = 0
    ngrams = s.scenes[i].get_ngrams(3)

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
