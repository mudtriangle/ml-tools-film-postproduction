from moviepy.editor import VideoFileClip
import speech_recognition as sr

vid = VideoFileClip('../test_data/my_cousin_vinny_1.mp4')
audio = vid.audio
audio.write_audiofile('../test_data/my_cousin_vinny_1.wav')

r = sr.Recognizer()
with sr.AudioFile('../test_data/my_cousin_vinny_1.wav') as source:
    # r.adjust_for_ambient_noise(source, duration=1)
    audio = r.record(source)

text = r.recognize_google(audio, show_all=True)
print(text)
