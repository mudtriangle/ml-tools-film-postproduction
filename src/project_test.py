from get_timecode import get_timecode_audio, get_timecode_video
from screenplay import Screenplay
from get_transcript import get_transcript_audio
from shot_classification import classify_shots
from media_matching import find_audio_match
import json

from datetime import datetime

AUDIO_DIR = '/data/liene_capstone/CAPSTONE/Sound/day 1 card/11-10-19'
VIDEO_DIR = '/data/liene_capstone/CAPSTONE/Day 1'
SCREENPLAY = '/data/liene_capstone/screenplay.fdx'
OUTPUT_DIR = '/data/liene_capstone/file_structure.json'

FRAMES = 25

start_time = datetime.now()
screenplay = Screenplay(SCREENPLAY)
print('Time for loading a screenplay:', datetime.now() - start_time)

file_structure = {'audio': {}, 'video': {}}

start_time = datetime.now()
audio_timecodes = get_timecode_audio(AUDIO_DIR, str(FRAMES), '6')
for audio_file in audio_timecodes.keys():
    file_structure['audio'][audio_file] = {}
    file_structure['audio'][audio_file]['timecode'] = audio_timecodes[audio_file]
print('Time for getting audio timecodes:', datetime.now() - start_time)

with open(OUTPUT_DIR, 'w') as f:
    json.dump(file_structure, f, indent=4)

start_time = datetime.now()
video_timecodes = get_timecode_video(VIDEO_DIR, str(FRAMES), '1')
for video_file in video_timecodes.keys():
    file_structure['video'][video_file] = {}
    file_structure['video'][video_file]['timecode'] = video_timecodes[video_file]
print('Time for getting video timecodes:', datetime.now() - start_time)

with open(OUTPUT_DIR, 'w') as f:
    json.dump(file_structure, f, indent=4)

start_time = datetime.now()
audio_transcripts = get_transcript_audio(AUDIO_DIR)
for audio_file in audio_timecodes.keys():
    file_structure['audio'][audio_file]['transcript'] = audio_transcripts[audio_file]
    file_structure['audio'][audio_file]['scene'] = screenplay.find_scene_from_transcript(audio_transcripts[audio_file])
print('Time for getting audio transcripts:', datetime.now() - start_time)

with open(OUTPUT_DIR, 'w') as f:
    json.dump(file_structure, f, indent=4)

start_time = datetime.now()
shots = classify_shots(VIDEO_DIR)
for video_file in shots.keys():
    file_structure['video'][video_file]['type_of_shot'] = shots[video_file]
print('Time for getting video classifications:', datetime.now() - start_time)

with open(OUTPUT_DIR, 'w') as f:
    json.dump(file_structure, f, indent=4)

start_time = datetime.now()
for video_file in file_structure['video'].keys():
    matches = find_audio_match(file_structure['video'][video_file]['timecode'], file_structure['audio'])
    if len(matches) == 0:
        continue
    file_structure['video'][video_file]['scene'] = file_structure['audio'][matches[0]]['scene']
print('Time for matching video to audio:', datetime.now() - start_time)

with open(OUTPUT_DIR, 'w') as f:
    json.dump(file_structure, f, indent=4)
