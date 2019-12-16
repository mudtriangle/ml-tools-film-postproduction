import subprocess
import os
from moviepy import editor


def get_audio_timecode_file(audio_path, frames, channel):
    res = subprocess.run(['ltcdump', audio_path, '-f', frames, '-c', channel], stdout=subprocess.PIPE)
    try:
        output = [x.split()[1] for x in res.stdout.decode('utf-8').split('\n')[2:-1]]
        return output[0] + ' ' + output[-1]
    except IndexError:
        return '-'


def get_video_timecode_file(video_path, frames, channel):
    vid = editor.VideoFileClip(video_path)
    audio = vid.audio

    output_path = video_path.split('.')[:-1]
    output_path.append('wav')
    output_path = '.'.join(output_path)

    audio.write_audiofile(output_path)

    tc = get_audio_timecode_file(output_path, frames, channel)

    os.remove(output_path)
    return tc


def get_audio_timecode(path, frames, channel):
    if os.path.isdir(path):
        timecodes = {}
        audio_files = [path + '/' + x for x in os.listdir(path)]
        for file in audio_files:
            timecodes[file] = get_audio_timecode_file(file, frames, channel)

        return timecodes

    else:
        return get_audio_timecode_file(path, frames, channel)


def get_video_timecode(path, frames, channel):
    if os.path.isdir(path):
        timecodes = {}
        video_files = [path + '/' + x for x in os.listdir(path)]
        for file in video_files:
            timecodes[file] = get_video_timecode(file, frames, channel)

        return timecodes

    else:
        return get_video_timecode_file(path, frames, channel)
