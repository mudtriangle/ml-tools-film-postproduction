import pydub
from pydub.utils import mediainfo
import os
import io
from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
import json
from screenplay import Screenplay

SIZE = 10000

audio_files = os.listdir('../test_liene/audio')
client = speech_v1.SpeechClient.from_service_account_json('../api_keys/google_cloud.json')
screenplay = Screenplay('../test_liene/screenplay.fdx')

files_dict = {}

for file in audio_files:
    os.mkdir('../test_liene/audio/temp')

    full_audio = pydub.AudioSegment.from_wav('../test_liene/audio/' + file)
    audio_info = {'transcript': {}}
    transcript = ''
    for t in range(0, len(full_audio), SIZE):
        try:
            chunk = full_audio[t:t+SIZE]
        except IndexError:
            chunk = full_audio[t:]

        chunk = chunk.set_sample_width(2)
        chunk.export('../test_liene/audio/temp/' + str(int(t/SIZE)) + '_' + file, format='wav', bitrate='16k')
        chunk_info = mediainfo('../test_liene/audio/temp/' + str(int(t/SIZE)) + '_' + file)

        config = {"language_code": 'en-US',
                  "sample_rate_hertz": int(chunk_info['sample_rate']),
                  "encoding": enums.RecognitionConfig.AudioEncoding.LINEAR16,
                  "profanity_filter": False,
                  "audio_channel_count": int(chunk_info['channels'])}

        with io.open('../test_liene/audio/temp/' + str(int(t/SIZE)) + '_' + file, 'rb') as f:
            content = f.read()
        audio = {"content": content}

        response = client.recognize(config, audio)

        alternatives = []
        for result in response.results:
            if int(t/1000) not in audio_info['transcript'].keys():
                audio_info['transcript'][int(t/1000)] = []

            alternative = result.alternatives[0]
            audio_info['transcript'][int(t/1000)].append(alternative.transcript)
            transcript += ' ' + alternative.transcript

    audio_info['scene'] = int(screenplay.find_scene_from_transcript(transcript))

    temp_files = os.listdir('../test_liene/audio/temp')
    for i in range(len(temp_files)):
        temp_files[i] = '../test_liene/audio/temp/' + temp_files[i]
    for temp_file in temp_files:
        os.remove(temp_file)
    os.rmdir('../test_liene/audio/temp')

    files_dict['../test_liene/audio/' + file] = audio_info

with open('../test_liene/file_structure.json', 'w') as f:
    json.dump(files_dict, f, indent=4)
