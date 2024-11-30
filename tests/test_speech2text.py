from speech2text.speech2text import Speech2Text

speech2text = Speech2Text('tests/video.mp4', 'tests/audio.wav')
print(speech2text.extract_transcript())