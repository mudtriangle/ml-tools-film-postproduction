#
#  Will translate for Google Cloud Speech because of the outstanding performance in comparison.
#


from moviepy.editor import VideoFileClip
from deepspeech import Model
import scipy.io.wavfile as wav
import numpy as np
import speech_recognition as sr
from screenplay import Script
from string_processing import normalize, tokenize, get_ngrams
import json

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

with open('../api_keys/google_cloud.json', 'r') as f:
    api_google_cloud = json.load(f)
api_google_cloud = json.dumps(api_google_cloud)

r = sr.Recognizer()
test = sr.AudioFile('../test_data/taxi_driver_002-0.wav')

noise = sr.AudioFile('../test_data/taxi_driver_002-1.wav')

with noise as ns:
    r.adjust_for_ambient_noise(ns)

with test as source:
    audio = r.record(source)

output = r.recognize_google_cloud(audio, show_all=True, credentials_json=api_google_cloud)
print(output)

screenplay = Script('../test_data/taxi_driver_script.fdx')

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
