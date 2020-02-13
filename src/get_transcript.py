import pydub
from pydub.utils import mediainfo
import os
import io
from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
from moviepy import editor

SIZE = 10000

client = speech_v1.SpeechClient.from_service_account_json('../api_keys/google_cloud.json')


def get_transcript_audio_file(audio_path):
    parent_dir = '/'.join(audio_path.split('/')[:-1])
    temp_dir = parent_dir + '/temp'
    fname = audio_path.split('/')[-1]
    try:
        os.mkdir(temp_dir)
    except FileExistsError:
        pass

    full_audio = pydub.AudioSegment.from_wav(audio_path)
    transcript = {}
    for t in range(0, len(full_audio), SIZE):
        try:
            chunk = full_audio[t:t+SIZE]
        except IndexError:
            chunk = full_audio[t:]

        chunk = chunk.set_sample_width(2)
        chunk.export(temp_dir + '/' + str(int(t / SIZE)) + '_' + fname, format='wav', bitrate='16k')
        chunk_info = mediainfo(temp_dir + '/' + str(int(t / SIZE)) + '_' + fname)

        config = {"language_code": 'en-US',
                  "sample_rate_hertz": int(chunk_info['sample_rate']),
                  "encoding": enums.RecognitionConfig.AudioEncoding.LINEAR16,
                  "profanity_filter": False,
                  "audio_channel_count": int(chunk_info['channels'])}

        with io.open(temp_dir + '/' + str(int(t / SIZE)) + '_' + fname, 'rb') as f:
            content = f.read()
        audio = {"content": content}

        response = client.recognize(config, audio)

        for result in response.results:
            if int(t / 1000) not in transcript.keys():
                transcript[int(t / 1000)] = []

            alternative = result.alternatives[0]
            transcript[int(t / 1000)].append(alternative.transcript)

        os.remove(temp_dir + '/' + str(int(t / SIZE)) + '_' + fname)

    os.rmdir(temp_dir)

    return transcript


def get_transcript_video_file(video_path):
    vid = editor.VideoFileClip(video_path)
    audio = vid.audio

    output_path = video_path.split('.')[:-1]
    output_path.append('wav')
    output_path = '.'.join(output_path)

    audio.write_audiofile(output_path)

    transcript = get_transcript_audio_file(output_path)

    os.remove(output_path)

    return transcript


def get_transcript_audio(path):
    if os.path.isdir(path):
        transcripts = {}
        audio_files = [path + '/' + x for x in os.listdir(path)]
        for file in audio_files:
            transcripts[file] = get_transcript_audio_file(file)

        return transcripts

    else:
        return get_transcript_audio_file(path)


def get_transcript_video(path):
    if os.path.isdir(path):
        transcripts = {}
        video_files = [path + '/' + x for x in os.listdir(path)]
        for file in video_files:
            transcripts[file] = get_transcript_video_file(file)

        return transcripts

    else:
        return get_transcript_video_file(path)
