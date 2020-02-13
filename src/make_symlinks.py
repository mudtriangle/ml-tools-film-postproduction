import os
import json


def get_smart_dirs(media_path, main_class, secondary_class):
    try:
        os.mkdir(media_path + '/smart_dirs')
    except FileExistsError:
        pass

    with open(media_path + '/file_structure.json', 'r') as f:
        structure = json.load(f)

    try:
        os.mkdir(media_path + '/smart_dirs/audio')
    except FileExistsError:
        pass

    for key in structure['audio'].keys():
        dir_path = media_path + '/smart_dirs/audio/' + str(structure['audio'][key][main_class])
        try:
            os.mkdir(dir_path)
        except FileExistsError:
            pass

        os.symlink(key, dir_path + '/symlink-' + key.split('/')[-1])

    try:
        os.mkdir(media_path + '/smart_dirs/video')
    except FileExistsError:
        pass

    for key in structure['video'].keys():
        dir_path = media_path + '/smart_dirs/video/' + str(structure['video'][key][main_class])
        try:
            os.mkdir(dir_path)
        except FileExistsError:
            pass

        os.symlink(key, dir_path + '/symlink-' + key.split('/')[-1])


get_smart_dirs('../test_liene', 'scene', 'shot')
