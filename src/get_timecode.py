import subprocess
import os
from moviepy import editor


def get_timecode_audio_file(audio_path, frames, channel):
    fnull = open(os.devnull, 'w')
    res = subprocess.run(['ltcdump', audio_path, '-f', frames, '-c', channel], stdout=subprocess.PIPE, stderr=fnull)
    try:
        output = [x.split()[1] for x in res.stdout.decode('utf-8').split('\n')[2:-1]]
        return output[0] + ' ' + output[-1]
    except IndexError:
        return '-'


def get_timecode_video_file(video_path, frames, channel):
    vid = editor.VideoFileClip(video_path)
    audio = vid.audio

    output_path = video_path.split('.')[:-1]
    output_path.append('wav')
    output_path = '.'.join(output_path)

    audio.write_audiofile(output_path, verbose=False)

    tc = get_timecode_audio_file(output_path, frames, channel)

    os.remove(output_path)
    return tc


def get_timecode_audio(path, frames, channel):
    if os.path.isdir(path):
        timecodes = {}
        audio_files = [path + '/' + x for x in os.listdir(path)]
        for file in audio_files:
            timecodes[file] = get_timecode_audio_file(file, frames, channel)

        return timecodes

    else:
        return get_timecode_audio_file(path, frames, channel)


def get_timecode_video(path, frames, channel):
    if os.path.isdir(path):
        timecodes = {}
        video_files = [path + '/' + x for x in os.listdir(path)]
        for file in video_files:
            timecodes[file] = get_timecode_video_file(file, frames, channel)

        return timecodes

    else:
        return get_timecode_video_file(path, frames, channel)
