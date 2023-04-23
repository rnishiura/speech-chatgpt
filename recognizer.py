import speech_recognition

# obsolete: limited usage for free user

def recognize(filepath='output.wav'):
  # filepath = 'speech.wav'
  r = speech_recognition.Recognizer()

  output = speech_recognition.AudioFile(filepath)
  with output as source:
    audio = r.record(source)

  # print(type(audio))

  text = r.recognize_google(audio)
  # text = r.recognize_google(audio, language='ja-JP')
  # print(text)

  return text
  # print(r.recognize_google(audio, show_all=True))

if __name__ == "__main__":
  print(recognize())
  
