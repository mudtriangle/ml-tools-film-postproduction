from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
import io
import os
from screenplay import Script
from string_processing import normalize, tokenize, get_ngrams
import numpy as np

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '../api_keys/google_cloud.json'

client = speech_v1.SpeechClient()

config = {"language_code": 'en-US',
          "sample_rate_hertz": 48000,
          "encoding": enums.RecognitionConfig.AudioEncoding.LINEAR16,
          "profanity_filter": False,
          "audio_channel_count": 2}

with io.open('../test_data/taxi_driver_003-0.wav', "rb") as f:
    content = f.read()
audio = {"content": content}

response = client.recognize(config, audio)

alternatives = []
for result in response.results:
    alternative = result.alternatives[0]
    alternatives.append(alternative.transcript)

screenplay = Script('../test_data/taxi_driver_script.fdx')

scores = []
for scene in screenplay.scenes:
    curr_score = 0

    for num_ngrams in range(1, 6):
        scene_ngrams = scene.get_dialogue_ngrams(num_ngrams)
        for alt in alternatives:
            dialogue = get_ngrams(tokenize(normalize(alt)), num_ngrams)
            for ngram in dialogue:
                if ngram in scene_ngrams:
                    curr_score += 1

    scores.append(curr_score)

match = np.argmax(scores)
if scores[match] == 0:
    print('No scene found.')
else:
    print(screenplay.scenes[match])
