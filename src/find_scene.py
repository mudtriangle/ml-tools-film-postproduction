from moviepy.editor import VideoFileClip
from deepspeech import Model
import scipy.io.wavfile as wav
import numpy as np
import speech_recognition as sr
from screenplay import Script
from string_processing import normalize, tokenize, get_ngrams

'''
vid = VideoFileClip('../test_data/BMPCC_1_2017-12-02_2143_C0027_2.mp4')
audio = vid.audio
audio.write_audiofile('../test_data/sample_audio.wav')
'''

'''
ds = Model('../deepspeech_model/output_graph.pbmm', 26, 9, '../deepspeech_model/alphabet.txt', 500)
fs, audio = wav.read('../test_data/test.wav')

if len(audio.shape) > 1:
    audio = audio.mean(axis=1, dtype=np.int16)

processed_data = ds.stt(audio, fs)
print(processed_data)
'''

r = sr.Recognizer()
test = sr.AudioFile('../test_data/sample_dialogue.wav')

noise = sr.AudioFile('../test_data/sample_noise.wav')

with noise as ns:
    r.adjust_for_ambient_noise(ns)

with test as source:
    audio = r.record(source)

output = r.recognize_google(audio, show_all=True)


screenplay = Script('../test_data/taxi_driver.fdx')

scores = []
for scene in screenplay.scenes:
    curr_score = 0
    scene_ngrams = scene.get_dialogue_ngrams(2)
    for alt in output['alternative']:
        dialogue = get_ngrams(tokenize(normalize(alt['transcript'])), 2)
        for ngram in dialogue:
            if ngram in scene_ngrams:
                curr_score += 1

    scores.append(curr_score)

match = np.argmax(scores)
if scores[match] == 0:
    print('No scene found.')
else:
    print(screenplay.scenes[match])

