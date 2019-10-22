from moviepy.editor import VideoFileClip
import speech_recognition as sr

vid = VideoFileClip('../test_data/taxi_driver_1.mov')
audio = vid.audio
audio.write_audiofile('../test_data/taxi_driver_1.wav')

r = sr.Recognizer()
with sr.AudioFile('../test_data/taxi_driver_1.wav') as source:
    audio = r.record(source)

text = r.recognize_google(audio)
print(text)
