import subprocess
import os
import json

DIR = '../test_liene/audio'
FRAMES = '25'
CHANNEL = '6'

with open('../test_liene/file_structure.json', 'r') as f:
    f_structure = json.load(f)

audio_files = os.listdir(DIR)

for file in audio_files:
    fname = DIR + '/' + file
    res = subprocess.run(['ltcdump', fname, '-f', FRAMES, '-c', CHANNEL], stdout=subprocess.PIPE)
    try:
        output = [x.split()[1] for x in res.stdout.decode('utf-8').split('\n')[2:-1]]
        f_structure[fname]['timecode'] = output[0] + ' ' + output[-1]
    except IndexError:
        f_structure[fname]['timecode'] = '-'

with open('../test_liene/file_structure.json', 'w') as f:
    json.dump(f_structure, f, indent=4)
