import json
from screenplay import Screenplay

with open('../test_liene/file_structure.json', 'r') as f:
    files = json.load(f)

screenplay = Screenplay('../test_liene/screenplay.fdx')

for file in files.keys():
    transcript = ''
    for time in files[file]['transcript'].keys():
        for alternative in files[file]['transcript'][time]:
            transcript += ' ' + alternative

    files[file]['scene'] = int(screenplay.find_scene_from_transcript(transcript))

with open('../test_liene/file_structure.json', 'w') as f:
    json.dump(files, f)
